"""hcode 격리가 ``OR`` 로 새 나가지 않는다 (2026-09-09 도서 자동완성 실사고).

SQL 은 ``AND`` 가 ``OR`` 보다 강하게 결합한다. 검색 조건에 ``OR`` 를 둔 채 ``AND Hcode=%s``
를 이어 붙이면::

    WHERE Gcode LIKE %s OR Gname LIKE %s AND Hcode=%s
    →     Gcode LIKE %s OR (Gname LIKE %s AND Hcode=%s)

가 되어 **코드로 검색하면 타사(타 출판사) 도서가 그대로 나온다**. 공용 헬퍼가 구조적으로
막고(괄호 자동 삽입), 호출부도 괄호를 유지하는지 정적으로 확인한다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.hcode_isolation import append_hcode_clause  # noqa: E402
from app.services import masters_service as ms  # noqa: E402


class AppendHcodeClauseOrTests(TestCase):
    def test_top_level_or_is_parenthesized(self) -> None:
        where, params = append_hcode_clause(
            "WHERE Gcode LIKE %s OR Gname LIKE %s", ["%q%", "%q%"], "5019"
        )
        self.assertEqual(where, "WHERE (Gcode LIKE %s OR Gname LIKE %s) AND Hcode=%s")
        self.assertEqual(params, ["%q%", "%q%", "5019"])

    def test_already_parenthesized_is_not_double_wrapped(self) -> None:
        where, _ = append_hcode_clause(
            "WHERE (Gcode LIKE %s OR Gname LIKE %s)", ["%q%", "%q%"], "5019"
        )
        self.assertEqual(where, "WHERE (Gcode LIKE %s OR Gname LIKE %s) AND Hcode=%s")

    def test_and_only_condition_is_untouched(self) -> None:
        where, _ = append_hcode_clause("WHERE Gcode=%s AND Gname=%s", ["a", "b"], "5019")
        self.assertEqual(where, "WHERE Gcode=%s AND Gname=%s AND Hcode=%s")

    def test_or_inside_a_word_is_not_mistaken(self) -> None:
        # 'Order'/'Ocode' 같은 식별자 안의 or 는 연산자가 아니다.
        where, _ = append_hcode_clause("WHERE Ocode=%s", ["A"], "5019")
        self.assertEqual(where, "WHERE Ocode=%s AND Hcode=%s")

    def test_and_fragment_without_where_keeps_scope_bound(self) -> None:
        where, _ = append_hcode_clause("Gcode=%s OR Gname=%s", ["a", "b"], "5019")
        self.assertEqual(where, "(Gcode=%s OR Gname=%s) AND Hcode=%s")


class BookAutocompleteScopeTests(IsolatedAsyncioTestCase):
    async def test_search_products_scopes_both_search_branches(self) -> None:
        captured: dict = {}

        async def fake_exec(_sid, sql, params=()):
            captured["sql"], captured["params"] = sql, params
            return []

        with patch.object(ms, "execute_query", side_effect=fake_exec):
            await ms.search_products(server_id="s", q="341", scope_hcode="5019")
        sql = " ".join(captured["sql"].split())
        self.assertIn("WHERE (Gcode LIKE %s OR Gname LIKE %s) AND Hcode=%s", sql)
        self.assertIn("5019", captured["params"])


class NoUnparenthesizedOrAtCallSitesTests(TestCase):
    """정적 가드 — 호출부가 괄호를 빠뜨리면(헬퍼가 막더라도) 의도를 되살리게 한다."""

    _CALL = re.compile(r"append_hcode_clause\(")
    _OR_FRAGMENT = re.compile(r'"(WHERE [^"]*\bOR\b[^"]*)"', re.IGNORECASE)

    def test_where_fragments_with_or_are_parenthesized(self) -> None:
        offenders: list[str] = []
        for path in sorted((BACKEND / "app").rglob("*.py")):
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for i, line in enumerate(lines):
                if not self._CALL.search(line):
                    continue
                for frag in self._OR_FRAGMENT.findall("\n".join(lines[max(0, i - 12): i + 1])):
                    body = frag[5:].strip()
                    if not (body.startswith("(") and body.endswith(")")):
                        offenders.append(f"{path.relative_to(BACKEND)}:{i + 1}: {frag[:80]}")
        self.assertEqual(offenders, [], "OR 검색 조건에 괄호가 없다 — hcode 격리가 샌다")


if __name__ == "__main__":
    main()
