"""DEC-149 — 거래처관리 목록 = 세부내역 컬럼 전면 + Gpper 오라벨 교정 회귀 가드.

2026-08-13 사용자: "거래처 관리 화면의 모든 정보가 기본적으로 표에 추가되도록"
+ 기본 순서 확정(구분→지역→코드→명→사업자번호→대표자→주소→업태→종목→전화→팩스→
이메일→담당자1→담당자2→비고1) + 거래처구분2 계열 삭제.

핵심 교정 — 레거시 Subu11.pas 정본(전 빌드 동일):
  Gpper=담당자(Edit110, 텍스트) · Gssum=한도액(Edit131) · Gphon=핸드폰번호(Edit132).
종전 웹은 gpper 를 "한도액" 숫자로 취급 — '인터넷, 총판' 같은 실데이터가 0 으로
소실되고 한도액·핸드폰번호는 아예 미노출이었다.

라이브 대사(교문사 5019, 00004 영풍문고): 담당자1 '인터넷, 총판' · 핸드폰번호
'02-399-6412' · 한도액 20,000,000 = 레거시 화면 일치.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import g1_ggeo_adapt as g1_adapt  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

_G1_COLS = [
    "Hcode", "Gubun", "Jubun", "Gcode", "Ocode", "Gname", "Gposa", "Gnumb",
    "Guper", "Gjomo", "Gpost", "Gadd1", "Gadd2", "Gtel1", "Gtel2", "Gfax1",
    "Gfax2", "Grat1", "Grat2", "Grat3", "Grat4", "Grat5", "Grat6", "Grat7",
    "Grat9", "Gqut1", "Yesno", "Name1", "Name2", "Gpper", "Gbigo", "Gphon",
    "Email", "Pubun", "Gnum1", "Gssum",
]


class CustomerListDetailFieldsTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        g1_adapt.clear_g1_column_cache_for_tests()
        self.addCleanup(g1_adapt.clear_g1_column_cache_for_tests)

    async def test_list_returns_detail_fields_with_canonical_semantics(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS" in sql:
                return [{"Field": c} for c in _G1_COLS]
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            if "G1_Gbun" in sql:
                return [{"code": "10004", "name": "인터넷서점"}]
            return [{
                "gcode": "00004", "gname": "(주)영풍문고", "gubun_code": "10004",
                "gpper": "인터넷, 총판", "gphon": "02-399-6412",
                "gssum": 20000000, "name2": "", "yesno": "False",
                "gfax2": "399-6415", "grat7": 0, "gqut1": 0, "grat9": 0,
            }]

        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g1_adapt, "execute_query", fake_exec):
            res = await ms.list_customer_master(server_id="remote_1", q="00004")
        it = res["items"][0]
        self.assertEqual(it["gpper"], "인터넷, 총판", "Gpper=담당자1 텍스트 정본")
        self.assertEqual(it["gphon"], "02-399-6412", "Gphon=핸드폰번호")
        self.assertEqual(it["gssum"], 20000000.0, "Gssum=한도액")
        self.assertEqual(it["sname"], "인터넷서점")
        for k in ("gfax2", "name1", "name2", "yesno", "grat7", "gqut1", "grat9"):
            self.assertIn(k, it)

    async def test_detail_select_treats_gpper_as_text(self) -> None:
        cols = {c.lower() for c in _G1_COLS}
        exact = {c.lower(): c for c in _G1_COLS}
        sql = g1_adapt.customer_detail_select_sql(cols, exact, alias="g")
        self.assertIn("COALESCE(g.Gpper,'') AS gpper", sql, "텍스트 표현식(''), 숫자(0) 금지")
        self.assertIn("COALESCE(g.Gphon,'') AS gphon", sql)
        self.assertIn("COALESCE(g.Gssum,0) AS gssum", sql)


class ModelAndCatalogGuard(TestCase):
    def test_customer_models_gpper_text_and_new_fields(self) -> None:
        from app.models.master import (
            CustomerDetail,
            CustomerListItem,
            CustomerUpdateRequest,
        )

        li = CustomerListItem(gcode="1", gname="t")
        self.assertEqual(li.gpper, "", "목록 gpper 텍스트 기본값")
        for k in ("gphon", "gssum", "gfax2", "name1", "name2", "yesno",
                  "grat7", "gqut1", "grat9"):
            self.assertIn(k, CustomerListItem.model_fields)
        d = CustomerDetail(gcode="1", gname="t")
        self.assertEqual(d.gpper, "")
        self.assertIn("gphon", CustomerDetail.model_fields)
        self.assertIn("gssum", CustomerDetail.model_fields)
        u = CustomerUpdateRequest(serverId="s", gpper="담당", gssum=100)
        self.assertEqual((u.gpper, u.gssum), ("담당", 100.0))

    def test_excel_catalog_canonical_labels(self) -> None:
        from app.services.masters_excel import (
            CUSTOMER_FULL_COLUMNS,
            CUSTOMER_IMPORT_MAP,
            CUSTOMER_NUMERIC_KEYS,
        )

        cols = dict((k, h) for h, k in CUSTOMER_FULL_COLUMNS)
        self.assertEqual(cols["gpper"], "담당자1", '구 "한도액"=gpper 오매핑 정정')
        self.assertEqual(cols["gssum"], "한도액")
        self.assertEqual(cols["gphon"], "핸드폰번호")
        self.assertEqual(CUSTOMER_IMPORT_MAP["담당자1"], "gpper")
        self.assertNotIn("gpper", CUSTOMER_NUMERIC_KEYS, "담당자1 텍스트 — 숫자 파싱 금지")
        self.assertIn("gssum", CUSTOMER_NUMERIC_KEYS)


class ScreenGuard(TestCase):
    PAGE = (FRONTEND / "app" / "(app)" / "master" / "customer" / "page.tsx")
    FORM = (FRONTEND / "components" / "master" / "customer-detail-form.tsx")

    def test_list_columns_order_and_coverage(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        # 사용자 확정 선두 순서 (2026-08-13).
        order = ["거래처구분", "거래처지역", "거래처코드", "거래처명", "사업자등록번호",
                 "대표자", "사업자주소", "업태", "종목", "전화번호", "팩스번호",
                 "이메일", "담당자1", "담당자2", "비고1"]
        pos = [src.index(f'label: "{lbl}"') for lbl in order]
        self.assertEqual(pos, sorted(pos), "컬럼 정의 순서 = 확정 순서")
        for lbl in ("비고2", "핸드폰번호", "한도액", "위탁", "한도", "신간수량",
                    "계산서구분", "발행유무", "출고정지"):
            self.assertIn(f'label: "{lbl}"', src)
        self.assertNotIn('key: "ocode"', src, "거래처코드2(ocode) 목록 제외(삭제 요청)")

    def test_detail_form_canonical_labels(self) -> None:
        # DEC-230 (2026-08-27) — 사용자 지정 명칭: 담당관리자1 / 휴대전화 / 한도 (컬럼 의미는 DEC-149 그대로)
        src = self.FORM.read_text(encoding="utf-8")
        self.assertIn('label="담당관리자1"', src)
        self.assertIn('label="휴대전화"', src)
        self.assertIn('label="한도"', src)
        # 한도액은 gssum 에만 — gpper 숫자 강제 재발 금지.
        self.assertNotIn('label="한도" value={String(data.gpper', src)
        self.assertIn('onChange("gpper", v)', src, "담당자1 텍스트 그대로 저장")


if __name__ == "__main__":
    main()
