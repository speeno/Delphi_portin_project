"""거래처 구분별 코드 자동발급 회귀 — 접두문자(A~K, I제외) + 잔여 자리 시퀀스.

사용자 스킴(2026-07-05): 거래처구분 선택 시 구내서점→A … 기타거래처→K 접두로 코드 채번.
코드 = <접두><나머지 자리>, 같은 접두 코드 중 MAX+1. mysql3 호환(CAST 없음, 문자 MAX=숫자 MAX).

자리수는 ``G1_Ggeo.Gcode`` 실제 컬럼 폭에서 뽑는다(DEC-262). 종전 고정 6자리(=7자)는
레거시 varchar(5) 를 넘겨 조용히 잘려 저장됐고(``J000001``→``J0000``) 등록 직후 상세가
404 였다 — 2026-09-08 사고.
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
    async def _run(self, prefix, max_row, width=5):
        captured = {}

        async def fake_exec(_sid, sql, params=()):
            captured["sql"] = sql
            captured["params"] = params
            return [{"mx": max_row}]

        async def fake_width(_sid, _table, _column="Gcode"):
            return width

        with patch.object(ms, "execute_query", side_effect=fake_exec), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_customer_code_by_prefix(server_id="remote_1", prefix=prefix)
        return code, captured

    async def test_first_code_when_none(self) -> None:
        code, cap = await self._run("A", "")
        self.assertEqual(code, "A0001")
        # 접두-정폭 코드만 집계: LIKE 'A%' + LENGTH=<컬럼 폭>
        self.assertIn("LIKE %s", cap["sql"])
        self.assertIn("LENGTH(Gcode)=%s", cap["sql"])
        self.assertEqual(cap["params"][0], "A%")
        self.assertEqual(cap["params"][1], 5)

    async def test_code_never_exceeds_column_width(self) -> None:
        # DEC-262 — varchar(5) 컬럼에 6자 이상이 나오면 안 된다(조용한 잘림 → 상세 404).
        for prefix, mx in (("A", ""), ("A", "A9998"), ("K", "K0041")):
            code, _ = await self._run(prefix, mx)
            self.assertLessEqual(len(code), 5, code)

    async def test_increments_max(self) -> None:
        code, _ = await self._run("A", "A0123")
        self.assertEqual(code, "A0124")

    async def test_wider_column_uses_more_digits(self) -> None:
        # 폭이 넓은 테넌트(varchar(8))면 자리수도 따라 늘어난다.
        code, cap = await self._run("A", "A0000123", width=8)
        self.assertEqual(code, "A0000124")
        self.assertEqual(cap["params"][1], 8)

    async def test_prefix_b_independent_sequence(self) -> None:
        code, cap = await self._run("B", "B0009")
        self.assertEqual(code, "B0010")
        self.assertEqual(cap["params"][0], "B%")

    async def test_non_numeric_suffix_falls_back_to_one(self) -> None:
        code, _ = await self._run("A", "ABCDE")
        self.assertEqual(code, "A0001")

    async def test_j_prefix(self) -> None:
        code, _ = await self._run("J", "J0041")
        self.assertEqual(code, "J0042")

    async def test_sequence_exhausted_falls_back_to_manual(self) -> None:
        # 자리 소진 시 폭을 넘기지 말고 빈 값(수기 입력)으로 물러난다.
        code, _ = await self._run("A", "A9999")
        self.assertEqual(code, "")

    async def test_width_unknown_falls_back_to_five(self) -> None:
        code, _ = await self._run("A", "", width=None)
        self.assertEqual(code, "A0001")

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
