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
        for k in ext.FIELDS:
            self.assertEqual(models.count(f"    {k}: str | None = None\n"), 2, k)
            self.assertIn(f'    {k}: str = ""\n', models, k)


class FormLayout(TestCase):
    def setUp(self) -> None:
        self.src = (FRONT / "components" / "master" / "customer-detail-form.tsx").read_text(encoding="utf-8")

    def test_sections_and_order(self) -> None:
        s = self.src
        base = s.index('data-legacy-id="Sobo11.Panel101"'); bill = s.index('data-legacy-id="Sobo11.Panel201"')
        self.assertLess(base, bill)
        order = ["Sobo11.Edit101", "거래처지역", "거래처코드", "거래정지", '"사유"',
                 "거래처명", "대표자", "사업자등록번호", '"업태"', '"종목"', '"한도"',
                 'label="주소1"', 'label="유선전화"', 'label="팩스번호"', 'label="휴대전화"', 'label="이메일"',
                 'label="주소2"', "Sobo11.Ext.Tel2", "Sobo11.Ext.Fax2", "Sobo11.Ext.Phon2", "Sobo11.Ext.Email2",
                 "청구정보", '"위탁"', '"현매"', '"매절"', '"납품"', '"특별"', '"기타"', '"신간수량"',
                 "<InvoiceKindRow", "담당관리자1", "Sobo11.Ext.Contact1", "비고1", "담당관리자2", "Sobo11.Edit130", "비고2", "<Label>메모</Label>"]
        pos = -1
        for tok in order:
            i = s.index(tok, pos + 1)
            self.assertGreater(i, pos, tok)
            pos = i

    def test_address_split_and_postcode(self) -> None:
        self.assertIn('import { PostcodeSearchButton } from "@/components/shared/postcode-search";', self.src)
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
