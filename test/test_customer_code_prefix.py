"""거래처 구분별 코드 자동발급 회귀 — 접두문자(A~K, I제외) + 6자리 시퀀스.

사용자 스킴(2026-07-05): 거래처구분 선택 시 구내서점→A … 기타거래처→K 접두로 코드 채번.
코드 = <접두><6자리>, 같은 접두 코드 중 MAX+1. mysql3 호환(CAST 없음, 문자 MAX=숫자 MAX).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import masters_service as ms  # noqa: E402


class PrefixMapTests(TestCase):
    def test_all_ten_types_map(self) -> None:
        expected = {
            "구내서점": "A", "인터넷서점": "B", "일반서점": "C", "총판": "D",
            "현매거래처": "E", "eBook거래처": "F", "교과서": "G",
            "본보기도서": "H", "납품거래처": "J", "기타거래처": "K",
        }
        for name, letter in expected.items():
            self.assertEqual(ms.customer_type_prefix(name), letter)

    def test_skips_letter_i(self) -> None:
        # H 다음은 I 가 아니라 J 여야 한다.
        self.assertEqual(ms.customer_type_prefix("본보기도서"), "H")
        self.assertEqual(ms.customer_type_prefix("납품거래처"), "J")
        self.assertNotIn("I", set(
            ms.customer_type_prefix(n) for n in
            ["구내서점", "인터넷서점", "일반서점", "총판", "현매거래처",
             "eBook거래처", "교과서", "본보기도서", "납품거래처", "기타거래처"]
        ))

    def test_space_and_case_insensitive(self) -> None:
        self.assertEqual(ms.customer_type_prefix("eBook 거래처"), "F")
        self.assertEqual(ms.customer_type_prefix("  EBOOK거래처 "), "F")

    def test_unknown_returns_none(self) -> None:
        self.assertIsNone(ms.customer_type_prefix("존재하지않는구분"))
        self.assertIsNone(ms.customer_type_prefix(""))
        self.assertIsNone(ms.customer_type_prefix(None))


class NextCodeByPrefixTests(IsolatedAsyncioTestCase):
    async def _run(self, prefix, max_row):
        captured = {}

        async def fake_exec(_sid, sql, params=()):
            captured["sql"] = sql
            captured["params"] = params
            return [{"mx": max_row}]

        with patch.object(ms, "execute_query", side_effect=fake_exec):
            code = await ms.next_customer_code_by_prefix(server_id="remote_1", prefix=prefix)
        return code, captured

    async def test_first_code_when_none(self) -> None:
        code, cap = await self._run("A", "")
        self.assertEqual(code, "A000001")
        # 접두-6자리만 집계: LIKE 'A%' + LENGTH=7
        self.assertIn("LIKE %s", cap["sql"])
        self.assertIn("LENGTH(Gcode)=7", cap["sql"])
        self.assertEqual(cap["params"][0], "A%")

    async def test_increments_max(self) -> None:
        code, _ = await self._run("A", "A000123")
        self.assertEqual(code, "A000124")

    async def test_prefix_b_independent_sequence(self) -> None:
        code, cap = await self._run("B", "B000009")
        self.assertEqual(code, "B000010")
        self.assertEqual(cap["params"][0], "B%")

    async def test_non_numeric_suffix_falls_back_to_one(self) -> None:
        code, _ = await self._run("A", "ABCDEFG")
        self.assertEqual(code, "A000001")

    async def test_j_prefix(self) -> None:
        code, _ = await self._run("J", "J000041")
        self.assertEqual(code, "J000042")

    async def test_invalid_prefix_raises(self) -> None:
        with self.assertRaises(ValueError):
            await ms.next_customer_code_by_prefix(server_id="remote_1", prefix="1")


class ResolveGubunAutoRegisterTests(IsolatedAsyncioTestCase):
    """미등록 접두 스킴 구분명 → 카테고리 자동 등록(코드=접두문자)."""

    async def _resolve(self, *, name, lookup_rows, dup=False):
        created = {}

        async def fake_meta(_sid):
            cols = {"gcode", "gname", "hcode"}
            return cols, {c: c.capitalize() for c in cols}

        async def fake_exec(_sid, _sql, _params=()):
            return lookup_rows

        async def fake_create(*, server_id, payload, scope_hcode=None):  # noqa: ARG001
            created.update(payload)
            if dup:
                raise ValueError("MASTER_DUPLICATE")
            return {"gcode": payload["gcode"]}

        with patch.object(ms, "g1_gbun_column_meta", new=fake_meta), \
                patch.object(ms, "execute_query", side_effect=fake_exec), \
                patch.object(ms, "create_customer_category", side_effect=fake_create):
            code = await ms._resolve_gubun_code(
                server_id="remote_1", payload={"gbun_name": name, "gubun": ""}
            )
        return code, created

    async def test_unregistered_prefix_type_auto_registers(self) -> None:
        code, created = await self._resolve(name="구내서점", lookup_rows=[])
        self.assertEqual(code, "A")  # 카테고리 코드 = 접두문자
        self.assertEqual(created.get("gcode"), "A")
        self.assertEqual(created.get("gname"), "구내서점")

    async def test_ebook_with_space_registers_prefix_f(self) -> None:
        code, created = await self._resolve(name="eBook 거래처", lookup_rows=[])
        self.assertEqual(code, "F")
        self.assertEqual(created.get("gcode"), "F")

    async def test_already_registered_returns_existing_code(self) -> None:
        code, created = await self._resolve(name="구내서점", lookup_rows=[{"gcode": "07"}])
        self.assertEqual(code, "07")  # 이름 조회 적중 → 자동 등록 안 함
        self.assertEqual(created, {})

    async def test_non_prefix_name_no_autoregister(self) -> None:
        code, created = await self._resolve(name="아무거나상점", lookup_rows=[])
        self.assertEqual(code, "")
        self.assertEqual(created, {})

    async def test_duplicate_on_create_still_returns_prefix(self) -> None:
        # 동시 생성 등으로 카테고리가 이미 있으면 접두 코드 그대로 사용.
        code, _ = await self._resolve(name="총판", lookup_rows=[], dup=True)
        self.assertEqual(code, "D")


if __name__ == "__main__":
    main()
