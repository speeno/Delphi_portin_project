"""DEC-172 — 입고처관리(Sobo12) = 거래처관리(Sobo11)와 동일하게 + 기타거래처(Sobo15) 정본 라벨.

2026-08-13 영업팀(PDF): "[입고처 관리] 거래처관리와 동일하게 작업 요청" — DEC-149(거래처)가
한 것을 입고처관리에 그대로 적용: 목록 = 세부내역 전면(확정 컬럼 순서), 상세 폼 정본 라벨,
XLSX export/import 카탈로그(전 필드 + 필드 선택).

핵심 교정 — 레거시 Subu12.pas / Subu15.pas 정본(전 빌드 동일, G1_Ggeo 와 동일 스키마):
  Gpper=담당자(Edit110, 텍스트) · Gssum=한도액(Edit131) · Gphon=핸드폰번호(Edit132) ·
  Grat7=한도(율, Edit130) · Name1=비고2(Edit126) · Name2=계산서 거래처명(Edit127) ·
  Email=정지사유(Edit129) · Yesno=발행유무(CheckBox1) · Grat9=정지유무(CheckBox2).
종전 웹은 gpper 를 "한도액/한도" 숫자로 취급(담당자 실데이터 0 소실), 담당자=name1·
핸드폰=gjomo1(실컬럼 아님)·정지사유=name2·비고2=email·계산서=pubun 으로 어긋나 있었다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import g2_ggwo_adapt as g2_adapt  # noqa: E402
from app.services import g5_ggeo_adapt as g5_adapt  # noqa: E402
from app.services import masters_service as ms  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"

# 실 스키마(G1_Ggeo/G2_Ggwo/G5_Ggeo 동일) — SHOW COLUMNS 모의.
_G2_COLS = [
    "Hcode", "Gubun", "Jubun", "Gcode", "Ocode", "Gname", "Gposa", "Gnumb",
    "Guper", "Gjomo", "Gpost", "Gadd1", "Gadd2", "Gtel1", "Gtel2", "Gfax1",
    "Gfax2", "Grat1", "Grat2", "Grat3", "Grat4", "Grat5", "Grat6", "Grat7",
    "Grat8", "Grat9", "Gqut1", "Yesno", "Name1", "Name2", "Gpper", "Gbigo",
    "Gphon", "Email", "Pubun", "Gnum1", "Gssum",
]
_GBUN_COLS = ["Hcode", "Gcode", "Gname"]


def _meta(cols: list[str]) -> tuple[set[str], dict[str, str]]:
    return {c.lower() for c in cols}, {c.lower(): c for c in cols}


class InboundVendorListFullTests(IsolatedAsyncioTestCase):
    """목록 행 = 세부내역 전면 — gpper 텍스트 + gssum/gphon/grat7, 구분명은 G2_Gbun 맵."""

    def setUp(self) -> None:
        g2_adapt.clear_g2_column_cache_for_tests()
        self.addCleanup(g2_adapt.clear_g2_column_cache_for_tests)

    async def test_list_returns_detail_fields_with_canonical_semantics(self) -> None:
        captured: dict[str, str] = {}

        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS FROM G2_Ggwo" in sql:
                return [{"Field": c} for c in _G2_COLS]
            if "SHOW COLUMNS FROM G2_Gbun" in sql:
                return [{"Field": c} for c in _GBUN_COLS]
            if "COUNT(*)" in sql:
                return [{"row_count": 1}]
            if "FROM G2_Gbun" in sql:
                captured["gbun_sql"] = sql
                return [{"code": "01", "name": "출판사"}]
            captured["select_sql"] = sql
            return [{
                "gcode": "00012", "gname": "테스트출판", "gubun": "01",
                "gpper": "김담당, 총판", "gphon": "010-1234-5678", "gssum": 3000000,
                "grat7": 65, "name1": "비고둘", "name2": "계산서명", "email": "정지사유X",
                "yesno": "True", "grat9": 1, "gadd1": "서울", "gadd2": "마포",
            }]

        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g2_adapt, "execute_query", fake_exec):
            res = await ms.list_inbound_vendors(server_id="remote_1", q="00012", scope_hcode="5019")

        it = res["items"][0]
        self.assertEqual(it["gpper"], "김담당, 총판", "Gpper=담당자 텍스트 정본(숫자 강제 금지)")
        self.assertEqual(it["gphon"], "010-1234-5678", "Gphon=핸드폰번호")
        self.assertEqual(it["gssum"], 3000000.0, "Gssum=한도액")
        self.assertEqual(it["grat7"], 65.0, "Grat7=한도(율)")
        self.assertEqual(it["gbun_name"], "출판사", "구분명 = G2_Gbun 맵 해석")
        self.assertEqual(it["gjuso"], "서울 마포")
        for k in ("name1", "name2", "email", "yesno", "grat9", "gposa", "gnumb", "gjomo",
                  "gfax1", "gfax2", "gbigo", "gqut1"):
            self.assertIn(k, it)
        # 목록 SELECT: JOIN/서브쿼리 0, 텍스트 gpper 표현식.
        sql = captured["select_sql"]
        self.assertNotIn("JOIN", sql)
        self.assertNotIn("(SELECT", sql)
        self.assertIn("COALESCE(g.Gpper,'') AS gpper", sql)
        self.assertNotIn("COALESCE(g.Gpper,0)", sql)
        self.assertNotIn("gjomo1", sql, "Gjomo1 은 실컬럼이 아님 — 어댑터 오선택 제거")
        # 구분 맵은 hcode 스코프로 조회.
        self.assertIn("Hcode=%s", captured["gbun_sql"])

    async def test_get_detail_maps_gpper_text_and_new_fields(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS FROM G2_Ggwo" in sql:
                return [{"Field": c} for c in _G2_COLS]
            if "SHOW COLUMNS FROM G2_Gbun" in sql:
                return [{"Field": c} for c in _GBUN_COLS]
            return [{"gcode": "00012", "gname": "테스트출판", "gpper": "김담당",
                     "gphon": "010-0", "gssum": 100, "grat7": 60, "gbun_name": "출판사"}]

        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g2_adapt, "execute_query", fake_exec):
            item = await ms.get_inbound_vendor(server_id="remote_1", gcode="00012", scope_hcode="5019")
        assert item is not None
        self.assertEqual(item["gpper"], "김담당")
        self.assertEqual(item["gphon"], "010-0")
        self.assertEqual(item["gssum"], 100.0)
        self.assertEqual(item["grat7"], 60.0)
        self.assertNotIn("gjomo1", item)

    async def test_update_puts_gpper_in_text_params_and_gssum_numeric(self) -> None:
        captured: dict[str, object] = {}

        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS FROM G2_Ggwo" in sql:
                return [{"Field": c} for c in _G2_COLS]
            if "SHOW COLUMNS FROM G2_Gbun" in sql:
                return [{"Field": c} for c in _GBUN_COLS]
            return [{"Gcode": "00012"}]

        async def fake_tx(server_id, statements):
            captured["sql"], captured["params"] = statements[0]
            return [1]

        payload = {"gpper": "김담당, 총판", "gphon": "010-1", "gssum": "2500000",
                   "grat7": 65, "name2": "계산서명", "email": "정지사유"}
        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g2_adapt, "execute_query", fake_exec), \
                patch.object(ms, "execute_in_transaction", fake_tx):
            res = await ms.update_inbound_vendor(
                server_id="remote_1", gcode="00012", payload=payload, scope_hcode="5019"
            )
        assert res is not None
        sql = str(captured["sql"])
        params = list(captured["params"])  # type: ignore[arg-type]
        self.assertIn("Gpper=%s", sql)
        self.assertIn("Gphon=%s", sql)
        self.assertIn("Gssum=%s", sql)
        self.assertIn("Grat7=%s", sql)
        sets = [c.strip() for c in sql.split("SET", 1)[1].split("WHERE", 1)[0].split(",")]
        idx = {c.split("=")[0]: i for i, c in enumerate(sets)}
        self.assertEqual(params[idx["Gpper"]], "김담당, 총판", "담당자 텍스트 그대로 저장(0 소실 금지)")
        self.assertEqual(params[idx["Gphon"]], "010-1")
        self.assertEqual(params[idx["Gssum"]], 2500000.0)
        self.assertEqual(params[idx["Grat7"]], 65.0)
        self.assertEqual(params[idx["Name2"]], "계산서명")
        self.assertEqual(params[idx["Email"]], "정지사유")
        self.assertIn("gpper", res["updated_fields"])
        self.assertIn("gssum", res["updated_fields"])
        # hcode 격리 유지.
        self.assertIn("Hcode=%s", sql.split("WHERE", 1)[1])
        self.assertEqual(params[-1], "5019")

    async def test_create_inserts_gpper_text(self) -> None:
        captured: dict[str, object] = {}

        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS FROM G2_Ggwo" in sql:
                return [{"Field": c} for c in _G2_COLS]
            if "SHOW COLUMNS FROM G2_Gbun" in sql:
                return [{"Field": c} for c in _GBUN_COLS]
            return []  # 중복 없음

        async def fake_tx(server_id, statements):
            captured["sql"], captured["params"] = statements[0]
            return [1]

        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g2_adapt, "execute_query", fake_exec), \
                patch.object(ms, "execute_in_transaction", fake_tx):
            await ms.create_inbound_vendor(
                server_id="remote_1",
                payload={"gcode": "00099", "gname": "신규", "gpper": "담당텍스트", "gssum": 10},
                scope_hcode="5019",
            )
        sql = str(captured["sql"])
        cols = [c.strip() for c in sql.split("(", 1)[1].split(")", 1)[0].split(",")]
        params = list(captured["params"])  # type: ignore[arg-type]
        self.assertEqual(params[cols.index("Gpper")], "담당텍스트")
        self.assertEqual(params[cols.index("Gssum")], 10.0)
        self.assertNotIn("Gjomo1", cols)


class EtcCustomerCanonicalTests(IsolatedAsyncioTestCase):
    """Sobo15 — Gpper 텍스트 + Gphon/Gssum/Pubun/Email/Grat9 배선."""

    def setUp(self) -> None:
        g5_adapt.clear_g5_column_cache_for_tests()
        self.addCleanup(g5_adapt.clear_g5_column_cache_for_tests)

    async def test_update_gpper_text_and_new_fields(self) -> None:
        captured: dict[str, object] = {}

        async def fake_exec(server_id, sql, params=()):
            if "SHOW COLUMNS FROM G5_Ggeo" in sql:
                return [{"Field": c} for c in _G2_COLS]
            if "SHOW COLUMNS FROM G5_Gbun" in sql:
                return [{"Field": c} for c in _GBUN_COLS]
            return [{"Gcode": "K0001"}]

        async def fake_tx(server_id, statements):
            captured["sql"], captured["params"] = statements[0]
            return [1]

        payload = {"gpper": "기타담당", "gphon": "010-9", "gssum": 7, "pubun": "1",
                   "email": "사유", "grat9": 1, "yesno": "1"}
        with patch.object(ms, "execute_query", fake_exec), \
                patch.object(g5_adapt, "execute_query", fake_exec), \
                patch.object(ms, "execute_in_transaction", fake_tx):
            res = await ms.update_etc_customer(
                server_id="remote_1", gcode="K0001", payload=payload, scope_hcode="5019"
            )
        assert res is not None
        sql = str(captured["sql"])
        params = list(captured["params"])  # type: ignore[arg-type]
        sets = [c.strip() for c in sql.split("SET", 1)[1].split("WHERE", 1)[0].split(",")]
        idx = {c.split("=")[0]: i for i, c in enumerate(sets)}
        self.assertEqual(params[idx["Gpper"]], "기타담당")
        self.assertEqual(params[idx["Gphon"]], "010-9")
        self.assertEqual(params[idx["Gssum"]], 7.0)
        self.assertEqual(params[idx["Pubun"]], "1")
        self.assertEqual(params[idx["Email"]], "사유")
        self.assertEqual(params[idx["Grat9"]], 1)
        self.assertEqual(params[idx["Yesno"]], "True", "발행유무 레거시 'True'/'False' 저장 관례")

    def test_g5_detail_select_gpper_text(self) -> None:
        cols, exact = _meta(_G2_COLS)
        sql = g5_adapt.etc_customer_detail_select_sql(cols, exact, alias="g")
        self.assertIn("COALESCE(g.Gpper,'') AS gpper", sql)
        for k in ("gphon", "pubun", "email"):
            self.assertIn(f"AS {k}", sql)
        self.assertIn("COALESCE(g.Gssum,0) AS gssum", sql)
        self.assertIn("COALESCE(g.Grat9,0) AS grat9", sql)


class ModelAndCatalogGuard(TestCase):
    def test_inbound_vendor_models(self) -> None:
        from app.models.master import (
            InboundVendorCreateRequest,
            InboundVendorDetail,
            InboundVendorListItem,
            InboundVendorUpdateRequest,
        )

        li = InboundVendorListItem(gcode="1", gname="t")
        self.assertEqual(li.gpper, "", "목록 gpper 텍스트 기본값")
        for k in ("gposa", "gnumb", "gjomo", "gfax1", "gfax2", "gpper", "gphon", "gssum",
                  "grat1", "grat6", "grat7", "gqut1", "grat9", "gbigo", "name1", "name2",
                  "yesno", "email"):
            self.assertIn(k, InboundVendorListItem.model_fields)
        d = InboundVendorDetail(gcode="1", gname="t")
        self.assertEqual(d.gpper, "")
        for k in ("gphon", "gssum", "grat7"):
            self.assertIn(k, InboundVendorDetail.model_fields)
        self.assertNotIn("gjomo1", InboundVendorDetail.model_fields)
        u = InboundVendorUpdateRequest(serverId="s", gpper="담당", gssum=100, grat7=60)
        self.assertEqual((u.gpper, u.gssum, u.grat7), ("담당", 100.0, 60.0))
        c = InboundVendorCreateRequest(serverId="s", gcode="1", gname="n", gpper="담당")
        self.assertEqual(c.gpper, "담당")

    def test_etc_customer_models(self) -> None:
        from app.models.master import EtcCustomerDetail, EtcCustomerUpdateRequest

        d = EtcCustomerDetail(gcode="1")
        self.assertEqual(d.gpper, "")
        for k in ("gphon", "gssum", "pubun", "email", "grat9"):
            self.assertIn(k, EtcCustomerDetail.model_fields)
        u = EtcCustomerUpdateRequest(serverId="s", gpper="담당", gssum=1, grat9=1)
        self.assertEqual((u.gpper, u.gssum, u.grat9), ("담당", 1.0, 1))

    def test_excel_catalog_order_keys_and_import_maps(self) -> None:
        from app.services.masters_excel import (
            INBOUND_VENDOR_COLUMNS,
            INBOUND_VENDOR_FULL_COLUMNS,
            INBOUND_VENDOR_IMPORT_MAP,
            INBOUND_VENDOR_IMPORT_PK,
            INBOUND_VENDOR_NUMERIC_KEYS,
            inbound_vendor_field_catalog,
            select_inbound_vendor_columns,
        )

        from app.services.masters_excel import key_of

        keys = [key_of(k) for _h, k in INBOUND_VENDOR_FULL_COLUMNS]
        labels = dict((key_of(k), h) for h, k in INBOUND_VENDOR_FULL_COLUMNS)
        # 확정 표시 순서. DEC-234 — 전화/팩스는 합본 가상 키(gtel/gfax), import 시 expand_phone_fields 로 1/2 분리.
        expected = [
            "gbun_name", "jubun", "gcode", "ocode", "gname", "gnumb", "gposa", "gadd1", "gadd2",
            "guper", "gjomo", "gtel", "gfax", "gpper", "gbigo", "name1",
            "gphon", "gpost", "gssum", "grat1", "grat2", "grat3", "grat4", "grat5", "grat7",
            "grat6", "gqut1", "name2", "yesno", "grat9", "email",
        ]
        self.assertEqual(keys, expected)
        self.assertEqual(labels["gpper"], "담당자", '구 "한도액"=gpper 오매핑 정정')
        self.assertEqual(labels["gssum"], "한도액")
        self.assertEqual(labels["gphon"], "핸드폰번호")
        self.assertEqual(labels["grat7"], "한도")
        self.assertEqual(labels["name1"], "비고2")
        self.assertEqual(labels["name2"], "계산서 거래처명")
        self.assertEqual(labels["email"], "정지사유")
        self.assertNotIn("pubun", labels, "Sobo12 폼에 계산서구분(Pubun) 없음 — 카탈로그 제외")
        self.assertNotIn("gnum1", labels)
        # 하위호환 별칭·카탈로그·부분선택.
        self.assertIs(INBOUND_VENDOR_COLUMNS, INBOUND_VENDOR_FULL_COLUMNS)
        self.assertEqual([f["key"] for f in inbound_vendor_field_catalog()], expected)
        self.assertEqual(
            [k for _h, k in select_inbound_vendor_columns(["gpper", "gname"])],
            ["gcode", "gname", "gpper"],
            "PK 항상 포함 + 카탈로그 순서",
        )
        self.assertEqual(select_inbound_vendor_columns(None), INBOUND_VENDOR_FULL_COLUMNS)
        # import — PK 헤더 = 입고처코드, 맵 = 카탈로그(PK 제외), 숫자키에 gpper 없음.
        self.assertEqual(INBOUND_VENDOR_IMPORT_PK, ("입고처코드", "gcode"))
        self.assertEqual(INBOUND_VENDOR_IMPORT_MAP["담당자"], "gpper")
        self.assertEqual(INBOUND_VENDOR_IMPORT_MAP["한도액"], "gssum")
        self.assertEqual(INBOUND_VENDOR_IMPORT_MAP["입고처구분"], "gbun_name")
        self.assertNotIn("입고처코드", INBOUND_VENDOR_IMPORT_MAP)
        self.assertNotIn("gpper", INBOUND_VENDOR_NUMERIC_KEYS, "담당자 텍스트 — 숫자 파싱 금지")
        self.assertEqual(
            INBOUND_VENDOR_NUMERIC_KEYS,
            frozenset({"gssum", "grat1", "grat2", "grat3", "grat4", "grat5", "grat6",
                       "grat7", "gqut1", "grat9"}),
        )

    def test_import_parse_keeps_gpper_text(self) -> None:
        """다운로드 서식 역반영 — 담당자는 텍스트 그대로, 한도액은 숫자."""
        from io import BytesIO

        from openpyxl import Workbook

        from app.services import masters_excel as mx

        wb = Workbook()
        ws = wb.active
        ws.append([h for h, _k in mx.INBOUND_VENDOR_FULL_COLUMNS])
        row = {k: "" for _h, k in mx.INBOUND_VENDOR_FULL_COLUMNS}
        row.update({"gcode": "00012", "gname": "테스트", "gpper": "김담당, 총판", "gssum": "1,000",
                    "grat7": 65, "gbun_name": "출판사"})
        ws.append([row[k] for _h, k in mx.INBOUND_VENDOR_FULL_COLUMNS])
        buf = BytesIO()
        wb.save(buf)
        parsed = mx.parse_master_xlsx(
            buf.getvalue(),
            pk=mx.INBOUND_VENDOR_IMPORT_PK,
            field_map=mx.INBOUND_VENDOR_IMPORT_MAP,
            numeric_keys=mx.INBOUND_VENDOR_NUMERIC_KEYS,
        )
        self.assertTrue(parsed["header_ok"])
        payload = parsed["rows"][0]["payload"]
        self.assertEqual(parsed["rows"][0]["gcode"], "00012")
        self.assertEqual(payload["gpper"], "김담당, 총판")
        self.assertEqual(payload["gssum"], 1000)
        self.assertEqual(payload["grat7"], 65)
        self.assertEqual(payload["gbun_name"], "출판사")


class ScreenGuard(TestCase):
    PAGE = FRONTEND / "app" / "(app)" / "master" / "inbound-vendor" / "page.tsx"
    FORM = FRONTEND / "components" / "master" / "inbound-vendor-detail-form.tsx"
    ETC_FORM = FRONTEND / "components" / "master" / "etc-customer-detail-form.tsx"
    API = FRONTEND / "lib" / "master-api.ts"

    def test_list_columns_order_and_coverage(self) -> None:
        src = self.PAGE.read_text(encoding="utf-8")
        order = ["입고처구분", "입고처지역", "입고처코드", "입고처명", "사업자등록번호", "대표자",
                 "사업자주소", "업태", "종목", "전화번호", "팩스번호", "담당자", "비고1", "비고2",
                 "핸드폰번호", "우편번호", "한도액", "위탁", "현매", "매절", "납품", "특별", "한도",
                 "기타", "신간수량", "계산서 거래처명", "발행유무", "출고정지", "정지사유"]
        pos = [src.index(f'label: "{lbl}"') for lbl in order]
        self.assertEqual(pos, sorted(pos), "컬럼 정의 순서 = 확정 순서")
        self.assertIn('key: "gpper", label: "담당자"', src)
        self.assertIn('key: "gssum", label: "한도액"', src)
        self.assertIn('key: "grat7", label: "한도"', src)
        self.assertNotIn('key: "ocode"', src, "입고처코드2(ocode) 목록 제외(거래처 동형)")
        # 엑셀 필드 선택 UI(거래처 동형).
        self.assertIn("inboundVendorApi\n      .exportFields()", src.replace("\r", ""))
        self.assertIn("저장할 필드 선택", src)

    def test_detail_form_canonical_labels(self) -> None:
        src = self.FORM.read_text(encoding="utf-8")
        pairs = {
            'label="담당자" value={data.gpper': "Sobo12.Edit110",
            'label="핸드폰번호" value={data.gphon': "Sobo12.Edit132",
            'label="한도액" value={String(data.gssum': "Sobo12.Edit131",
            'label="한도" value={data.grat7': "Sobo12.Edit130",
            'label="기타" value={data.grat6': "Sobo12.Edit123",
            'label="비고1" value={data.gbigo': "Sobo12.Edit125",
            'label="비고2" value={data.name1': "Sobo12.Edit126",
            'label="계산서 거래처명" value={data.name2': "Sobo12.Edit127",
            'label="발행유무" value={data.yesno': "Sobo12.CheckBox1",
            'label="정지유무" value={String(data.grat9': "Sobo12.CheckBox2",
            'label="정지사유" value={data.email': "Sobo12.Edit129",
        }
        for snippet, legacy_id in pairs.items():
            self.assertIn(snippet, src, snippet)
            line = next(l for l in src.splitlines() if snippet in l)
            self.assertIn(legacy_id, line, f"{snippet} ↔ {legacy_id}")
        self.assertNotIn("gjomo1", src.split("*/", 1)[1], "gjomo1 바인딩 제거(주석 제외)")
        self.assertNotIn('label="한도액" value={String(data.gpper', src)
        self.assertNotIn('label="계산서" value={data.pubun', src, "Sobo12 에 계산서구분 없음")
        self.assertIn('onChange("gpper", v)', src, "담당자 텍스트 그대로 저장")

    def test_etc_form_canonical_labels(self) -> None:
        src = self.ETC_FORM.read_text(encoding="utf-8")
        pairs = {
            'label="담당자" value={data.gpper': "Sobo15.Edit110",
            'label="핸드폰번호" value={data.gphon': "Sobo15.Edit132",
            'label="한도액" value={String(data.gssum': "Sobo15.Edit131",
            'label="비고2" value={data.name1': "Sobo15.Edit126",
            'label="계산서 거래처명" value={data.name2': "Sobo15.Edit127",
            'label="계산서구분" value={data.pubun': "Sobo15.Edit128",
            'label="정지사유" value={data.email': "Sobo15.Edit129",
            'label="정지유무" value={String(data.grat9': "Sobo15.CheckBox2",
        }
        for snippet, legacy_id in pairs.items():
            self.assertIn(snippet, src, snippet)
            line = next(l for l in src.splitlines() if snippet in l)
            self.assertIn(legacy_id, line, f"{snippet} ↔ {legacy_id}")
        self.assertNotIn('label="한도액" value={String(data.gpper', src)
        self.assertNotIn('label="계산서 거래처명" value={data.name1', src)
        self.assertNotIn('label="정지사유" value={data.name2', src)

    def test_api_types(self) -> None:
        src = self.API.read_text(encoding="utf-8")
        self.assertNotIn("gjomo1", src)
        self.assertIn("exports/inbound-vendor-fields", src)
        # InboundVendorDetail: gpper 텍스트 + gphon/gssum/grat7.
        seg = src.split("export interface InboundVendorDetail", 1)[1].split("}", 1)[0]
        self.assertIn("gpper: string;", seg)
        for k in ("gphon: string;", "gssum: number;", "grat7: number;"):
            self.assertIn(k, seg)
        seg = src.split("export interface EtcCustomerDetail", 1)[1].split("}", 1)[0]
        self.assertIn("gpper: string;", seg)
        for k in ("gphon: string;", "gssum: number;", "pubun: string;", "email: string;", "grat9: number;"):
            self.assertIn(k, seg)


if __name__ == "__main__":
    main()
