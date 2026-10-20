"""DEC-230 — 거래처 상세 재배치·확장 필드 사이드 테이블·우편번호 검색 (2026-08-27 사용자 요청)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import customer_ext_service as ext  # noqa: E402


class ExtService(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ext._ensured.add("remote_x")

    async def test_upsert_merges_and_replaces(self) -> None:
        calls: list = []

        async def fake(server_id, sql, params=()):
            calls.append((sql, params))
            if sql.startswith("SELECT"):
                return [{"zip2": "", "add1_detail": "3층", "add2_detail": "", "tel2": "", "fax2": "", "phon2": "", "email2": "", "stop_reason": "", "contact1": "", "memo": ""}]
            return []

        with patch.object(ext, "execute_query", fake):
            changed = await ext.upsert_ext(server_id="remote_x", gcode="00001", scope_hcode="5019", values={"zip2": "03187", "memo": None})
        self.assertEqual(changed, ["zip2"])
        rep = [c for c in calls if c[0].startswith("REPLACE INTO")][0]
        self.assertIn("G1_Ggeo_Ext (Hcode, Gcode, Zip2, Add1Detail", rep[0])
        self.assertEqual(rep[1][:4], ("5019", "00001", "03187", "3층"), "기존 값(상세주소1) 보존 + 제공 값 반영")

    async def test_all_empty_deletes_row(self) -> None:
        calls: list = []

        async def fake(server_id, sql, params=()):
            calls.append(sql)
            if sql.startswith("SELECT"):
                return [{k: ("x" if k == "memo" else "") for k in ext.FIELDS}]
            return []

        with patch.object(ext, "execute_query", fake):
            changed = await ext.upsert_ext(server_id="remote_x", gcode="00001", scope_hcode="5019", values={"memo": ""})
        self.assertEqual(changed, ["memo"])
        self.assertTrue(any(s.startswith("DELETE FROM G1_Ggeo_Ext") for s in calls))

    async def test_get_failure_is_empty(self) -> None:
        async def boom(*a, **k):
            raise RuntimeError("db down")

        with patch.object(ext, "execute_query", boom):
            self.assertEqual(await ext.get_ext(server_id="remote_x", gcode="1", scope_hcode="5019"), ext.empty())


class RouterAndModels(TestCase):
    def test_router_hooks(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        self.assertIn("await customer_ext_service.get_ext(", src)
        self.assertEqual(src.count("ext = {k: body.pop(k) for k in list(body) if k in customer_ext_service.FIELDS}"), 2)
        self.assertIn("await customer_ext_service.delete_ext(", src)
        models = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "models" / "master.py").read_text(encoding="utf-8")
        # 거래처 요청 모델(Create/Update)만 센다 — DEC-269 로 입고처 모델에도 같은 키가 생겼다.
        cust = models[models.index("class CustomerUpdateRequest") : models.index("class CustomerUpdateResponse")]
        for k in ext.FIELDS:
            self.assertEqual(cust.count(f"    {k}: str | None = None\n"), 2, k)
            self.assertIn(f'    {k}: str = ""\n', models, k)


class FormLayout(TestCase):
    def setUp(self) -> None:
        self.src = (FRONT / "components" / "master" / "customer-detail-form.tsx").read_text(encoding="utf-8")

    def test_sections_and_order(self) -> None:
        s = self.src
        base = s.index('data-legacy-id="Sobo11.Panel101"'); bill = s.index('data-legacy-id="Sobo11.Panel201"')
        self.assertLess(base, bill)
        # DEC-412: 프론트 재설계(M-DEC-3 · M-DEC-15) 운영 반영 — Figma 순서: 기본 4행(구분 · 코드 · 거래처명 · 지역 /
        # 사업자번호 · 대표자 · 업태 · 종목 / 담당자 · 휴대전화 · 전화 · 팩스 / 주소1+이메일1 · 주소2+이메일2) →
        # 거래 조건(비율 + 한도액) → 계산서 · 담당 · 출고 여부 · 비고1 → 비고2.
        # DEC-335(거래처명 맨 앞)는 Figma 로 구분 → 코드 → 거래처명 순서가 됐다.
        # DEC-412: 프론트 재설계 M-DEC-3 — 의도적 제거: 유선전화2 · 팩스2 · 휴대전화2 · 정지 사유 · 담당자 연락처 · 메모.
        # 숨김 블록(data-hidden-fields="figma-customer")에 바인딩만 남고, 저장 시 불러온 값을 그대로 다시 보낸다
        # (test_pages_send_ext_fields · test_dec293).
        order = ['data-legacy-id="Sobo11.Panel101"',
                 "Sobo11.Edit101", "Sobo11.Edit103", "Sobo11.Edit105", "Sobo11.Edit102",
                 "Sobo11.Edit107", "Sobo11.Edit106", "Sobo11.Edit108", "Sobo11.Edit109",
                 "Sobo11.Edit110", "Sobo11.Edit132", "Sobo11.Edit112", "Sobo11.Edit114",
                 'label="주소1"', "Sobo11.Edit129", 'label="주소2"', "Sobo11.Ext.Email2",
                 'data-legacy-id="Sobo11.Panel201"', "거래 조건",
                 '"위탁"', '"현매"', '"매절"', '"납품"', '"특별"', '"한도"', '"기타"', '"신간수량"', '"한도액"',
                 '"계산서"', "Sobo11.CheckBox1", '"담당"', "Sobo11.Edit127", '"출고 여부"', "Sobo11.CheckBox2",
                 '"비고1"', "Sobo11.Edit125", "<Label>비고2</Label>", "Sobo11.Edit126"]
        pos = -1
        for tok in order:
            i = s.index(tok, pos + 1)
            self.assertGreater(i, pos, tok)
            pos = i

    def test_address_split_and_postcode(self) -> None:
        # DEC-293 — 주소 그룹(우편번호·검색·주소·상세주소 한 줄)은 입고처와 공용 form-grid.tsx.
        grid = (FRONT / "components" / "master" / "form-grid.tsx").read_text(encoding="utf-8")
        self.assertIn('import { PostcodeSearchButton } from "@/components/shared/postcode-search";', grid)
        self.assertIn('from "@/components/master/form-grid";', self.src)
        self.assertEqual(self.src.count("<AddressGroup"), 2)
        for lid in ("Sobo11.Edit111", "Sobo11.Edit116", "Sobo11.Ext.Add1Detail", "Sobo11.Ext.Zip2", "Sobo11.Edit117", "Sobo11.Ext.Add2Detail"):
            self.assertIn(lid, self.src, lid)
        pc = (FRONT / "components" / "shared" / "postcode-search.tsx").read_text(encoding="utf-8")
        self.assertIn("t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js", pc)
        self.assertIn(".embed(boxRef.current", pc, "팝업 대신 화면 내 embed")

    def test_pages_send_ext_fields(self) -> None:
        for sub in ("[gcode]", "new"):
            src = (FRONT / "app" / "(app)" / "master" / "customer" / sub / "page.tsx").read_text(encoding="utf-8")
            for k in ext.FIELDS:
                self.assertIn(f"{k}: data.{k}", src, f"{sub}: {k}")


if __name__ == "__main__":
    main()
