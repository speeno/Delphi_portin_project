"""
Sobo14 신규 도서 스캔 — ISBN 중복검사(`masters_service.find_book_by_isbn`) 회귀 가드.

대상(2026-07-24 사용자: 스캔 ISBN 이 이미 등록된 도서면 기존정보 불러오기):
- 저장 Gisbn 의 하이픈/공백 유무와 무관하게 **숫자만 정규화**해 비교(REPLACE 사용).
- hcode 스코프가 WHERE 에 합성되어 다른 테넌트 도서가 새지 않는다.
- 존재 시 gcode/gname/gisbn, 없으면 None. 빈 ISBN 은 쿼리 없이 None.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import masters_service  # noqa: E402


class _Stub:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def __call__(self, server_id: str, sql: str, params=None):  # noqa: ARG002
        self.calls.append((sql, tuple(params or ())))
        return self.rows


def _run(isbn: str, rows: list[dict[str, Any]], scope_hcode: str | None = None):
    stub = _Stub(rows)
    with patch.object(masters_service, "execute_query", new=stub):
        result = asyncio.run(
            masters_service.find_book_by_isbn(
                server_id="remote_1", isbn=isbn, scope_hcode=scope_hcode
            )
        )
    return result, stub


class FindBookByIsbnTests(TestCase):
    def test_found_returns_book(self) -> None:
        rows = [{"gcode": "B00001", "gname": "테스트도서", "gisbn": "9788912345670"}]
        result, stub = _run("9788912345670", rows)
        self.assertEqual(result, {"gcode": "B00001", "gname": "테스트도서", "gisbn": "9788912345670"})
        sql, params = stub.calls[0]
        self.assertIn("G4_Book", sql)
        self.assertIn("REPLACE", sql)
        self.assertEqual(params[0], "9788912345670")

    def test_not_found_returns_none(self) -> None:
        result, stub = _run("9788912345670", [])
        self.assertIsNone(result)
        self.assertEqual(len(stub.calls), 1)

    def test_hyphens_and_spaces_normalized(self) -> None:
        result, stub = _run("978-89 1234-567-0", [])
        self.assertIsNone(result)
        _, params = stub.calls[0]
        self.assertEqual(params[0], "9788912345670")

    def test_empty_isbn_skips_query(self) -> None:
        result, stub = _run("   ", [])
        self.assertIsNone(result)
        self.assertEqual(stub.calls, [])

    def test_hcode_scope_in_params(self) -> None:
        result, stub = _run("9788912345670", [], scope_hcode="5019")
        self.assertIsNone(result)
        _, params = stub.calls[0]
        self.assertIn("5019", params)


if __name__ == "__main__":
    main()
