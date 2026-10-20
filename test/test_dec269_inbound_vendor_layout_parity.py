"""DEC-269 — 신규 입고처 등록 화면을 거래처(Sobo11)와 «같은 배열»로 (2026-09-09 사용자).

「신규입고처 등록시 입력 컴포넌트 위치 및 배열을 첨부한 거래처 기본정보 및 청구정보 배열과
동일하게 맞춰주세요.」

거래처에 있고 입고처에 없던 칸(상세주소1/2·주소2 우편번호·연락처2 세트·담당관리자2/연락처2·메모)은
``G1_Ggeo_Ext``(DEC-230)·``G4_Book_Ebook``(DEC-068) 선례대로 **레거시 무변경 사이드 테이블**
``G2_Ggwo_Ext`` 에 담는다. DEC-172 의 라벨↔실컬럼 바인딩(담당자=Gpper·정지사유=Email·
계산서 거래처명=Name2·한도(율)=Grat7·비고2=Name1)은 **그대로**다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import inbound_vendor_ext_service as ext  # noqa: E402

FORM = (FRONT / "components" / "master" / "inbound-vendor-detail-form.tsx").read_text(encoding="utf-8")
CUST = (FRONT / "components" / "master" / "customer-detail-form.tsx").read_text(encoding="utf-8")


class ExtService(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ext._ensured.add("remote_x")

    def test_columns_are_side_table_only(self) -> None:
        self.assertEqual(ext._TABLE, "G2_Ggwo_Ext")
        # 입고처는 정지사유가 레거시 Email 컬럼(DEC-172)이라 StopReason 이 없다.
        self.assertNotIn("stop_reason", ext.FIELDS)
        self.assertEqual(
            set(ext.FIELDS),
            {"zip2", "add1_detail", "add2_detail", "tel2", "fax2", "phon2", "email2", "manager2", "contact2", "memo"},
        )
        self.assertIn("CREATE TABLE IF NOT EXISTS G2_Ggwo_Ext", ext._CREATE_SQL)
        self.assertIn("PRIMARY KEY (Hcode, Gcode)", ext._CREATE_SQL)

    async def test_upsert_merges_and_scopes_by_hcode(self) -> None:
        calls: list = []

        async def fake(server_id, sql, params=()):
            calls.append((sql, params))
            if sql.startswith("SELECT"):
                return [{k: ("3층" if k == "add1_detail" else "") for k in ext.FIELDS}]
            return []

        with patch.object(ext, "execute_query", fake):
            changed = await ext.upsert_ext(
                server_id="remote_x", gcode="00001", scope_hcode="5019", values={"zip2": "03187", "memo": None}
            )
        self.assertEqual(changed, ["zip2"])
        rep = [c for c in calls if c[0].startswith("REPLACE INTO")][0]
        self.assertIn("G2_Ggwo_Ext (Hcode, Gcode, Zip2, Add1Detail", rep[0])
        self.assertEqual(rep[1][:4], ("5019", "00001", "03187", "3층"), "기존 값 보존 + 제공 값 반영")
        sel = [c for c in calls if c[0].startswith("SELECT")][0]
        self.assertIn("WHERE Hcode=%s AND Gcode=%s", sel[0])  # hcode 격리

    async def test_all_empty_deletes_row(self) -> None:
        calls: list = []

        async def fake(server_id, sql, params=()):
            calls.append((sql, params))
            if sql.startswith("SELECT"):
                return [{k: ("x" if k == "memo" else "") for k in ext.FIELDS}]
            return []

        with patch.object(ext, "execute_query", fake):
            changed = await ext.upsert_ext(server_id="remote_x", gcode="00001", scope_hcode="5019", values={"memo": ""})
        self.assertEqual(changed, ["memo"])
        self.assertTrue(any(c[0].startswith("DELETE FROM G2_Ggwo_Ext") for c in calls))


class RouterWiring(TestCase):
    SRC = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers" / "masters.py").read_text(encoding="utf-8")

    def test_detail_merges_ext(self) -> None:
        self.assertIn("await inbound_vendor_ext_service.get_ext(", self.SRC)

    def test_create_and_patch_split_ext_keys(self) -> None:
        self.assertEqual(self.SRC.count("in inbound_vendor_ext_service.FIELDS"), 2)  # create + patch
        self.assertIn("await inbound_vendor_ext_service.upsert_ext(", self.SRC)

    def test_delete_removes_ext_row(self) -> None:
        self.assertIn("await inbound_vendor_ext_service.delete_ext(", self.SRC)

    def test_model_exposes_ext_fields(self) -> None:
        models = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "models" / "master.py").read_text(encoding="utf-8")
        i = models.index("class InboundVendorDetail(BaseModel)")
        block = models[i : models.index("class InboundVendorDetailResponse", i)]
        for f in ("zip2", "add1_detail", "add2_detail", "tel2", "fax2", "phon2", "email2", "manager2", "contact2", "memo"):
            self.assertIn(f"{f}: str", block, f)


class FormLayoutParity(TestCase):
    """DEC-412: 프론트 재설계(M-DEC-6/8) 운영 반영 — 거래처와 «같은 배열» 대신 입고처 피그마(1:4594) 배열.

    두 화면은 이제 각자의 피그마를 따른다(거래처 = 기본·거래 조건·계산서 3단, 입고처 = 4열 기본정보 + 비고).
    대신 지킨다: 공용 4열 칸(FORM_GRID)·공용 AddressGroup, 그리고 DEC-269 확장 칸(G2_Ggwo_Ext)이
    피그마 밖이어도 숨김 블록에서 값·레거시 id 를 유지해 저장 시 그대로 왕복하는 것.
    """

    @staticmethod
    def _split() -> tuple[str, str]:
        visible, hidden = FORM.split('<div hidden data-hidden-fields="figma-inbound-vendor">', 1)
        return visible, hidden.split("<ReadOnlyBanner", 1)[0]

    def test_basic_info_rows_match_customer(self) -> None:
        # DEC-293 — 공용 4열 균등 칸(FORM_GRID) + 공용 AddressGroup(form-grid.tsx).
        for src in (CUST, FORM):
            self.assertIn('from "@/components/master/form-grid";', src)
            self.assertNotIn("function AddressGroup", src, "주소 그룹은 공용 컴포넌트")
        visible, hidden = self._split()
        self.assertEqual(visible.count('<div className={FORM_GRID} data-form-grid="">'), 1, "기본정보 4열 한 판")
        # 피그마 순서: 구분 · 코드 · 입고처명 · 지역 / 사업자번호 · 대표자 · 업태 · 종목 / 담당자 · 휴대전화 · 전화 · 팩스 / 주소 · 이메일
        order = ['label="입고처 구분"', 'label="입고처 코드"', 'label="입고처명"', 'label="입고처 지역"',
                 'label="사업자번호"', 'label="대표자"', 'label="업태"', 'label="종목"',
                 'label="담당자"', 'label="휴대전화"', 'label="전화번호"', 'label="팩스번호"',
                 'label="주소"', 'label="이메일"']
        pos = [visible.index(lbl) for lbl in order]
        self.assertEqual(pos, sorted(pos), "피그마 칸 순서")
        # 주소1 = 우편번호+검색+주소+상세주소 그룹(보임), 주소2 그룹은 숨김 블록(DEC-269 확장 칸 보존).
        self.assertEqual(visible.count("<AddressGroup"), 1)
        self.assertIn("detail={data.add1_detail", visible)
        self.assertEqual(hidden.count("<AddressGroup"), 1)
        self.assertIn("detail={data.add2_detail", hidden)
        # 이메일 = 확장 email2 (G2_Ggwo.Email 은 정지사유 정본)
        self.assertIn("Sobo12.Ext.Email2", visible)
        for lid in ("Sobo12.Ext.Tel2", "Sobo12.Ext.Fax2", "Sobo12.Ext.Phon2"):
            self.assertIn(lid, hidden, lid)

    def test_billing_rows_match_customer(self) -> None:
        # 보이는 칸: 담당자(Gpper) + 비고(Gbigo). 담당관리자2·연락처·비고2·메모·계산서·발행유무는 숨김 블록.
        visible, hidden = self._split()
        self.assertIn("<Label>비고</Label>", visible)
        for label in ('label="담당관리자2"', 'label="연락처"', 'label="비고2"', "<Label>메모</Label>",
                      'label="계산서 거래처명"', 'label="발행유무"'):
            self.assertIn(label, hidden, label)
        self.assertIn('data-legacy-id="Sobo12.Ext.Memo"', hidden)
        self.assertIn('legacyId="Sobo12.Ext.Manager2"', hidden)
        self.assertIn('legacyId="Sobo12.Ext.Contact2"', hidden)

    def test_dec172_bindings_unchanged(self) -> None:
        """배열만 바꾼다 — 라벨↔실컬럼 바인딩(DEC-172)은 그대로."""
        for legacy_id, field in (
            ("Sobo12.Edit110", "data.gpper"),    # 담당자 = Gpper
            ("Sobo12.Edit128", "data.gnum1"),    # 연락처
            ("Sobo12.Edit125", "data.gbigo"),    # 비고1
            ("Sobo12.Edit126", "data.name1"),    # 비고2
            ("Sobo12.Edit127", "data.name2"),    # 계산서 거래처명
            ("Sobo12.Edit129", "data.email"),    # 정지사유
            ("Sobo12.Edit130", "data.grat7"),    # 한도(율)
            ("Sobo12.Edit131", "data.gssum"),    # 한도액
            ("Sobo12.Edit132", "data.gphon"),    # 핸드폰번호
            ("Sobo12.Edit104", "data.ocode"),    # 입고처코드2
        ):
            i = FORM.index(legacy_id)
            around = FORM[max(0, i - 400) : i + 80]
            self.assertIn(field, around, f"{legacy_id} ↔ {field}")

    def test_save_round_trips_hidden_fields(self) -> None:
        """숨김 칸은 화면에서 편집하지 않아도 상세 저장(PATCH)에 원값 그대로 실린다 — 값 소실 없음."""
        detail = (FRONT / "app" / "(app)" / "master" / "inbound-vendor" / "[gcode]" / "page.tsx").read_text(encoding="utf-8")
        body = detail[detail.index("inboundVendorApi.update("): detail.index("snapshotRef.current = { ...data };", detail.index("inboundVendorApi.update("))]
        for k in ("ocode", "gssum", "grat1", "grat2", "grat3", "grat4", "grat5", "grat6", "grat7", "grat9",
                  "gqut1", "name1", "name2", "email", "yesno", "gnum1", "zip2", "add2_detail", "tel2", "fax2",
                  "phon2", "manager2", "contact2", "memo"):
            self.assertIn(f"{k}: data.{k},", body, k)


if __name__ == "__main__":
    main()
