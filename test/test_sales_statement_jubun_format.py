"""formatIdnumInput / formatJubunInput / formatIdnumDisplay — TS 로직 미러.

DEC-064 §Idnum 정합 (2026-06-05) — 전표번호=Idnum 5자리 zero-pad,
Jubun=거래구분 차수(2자리) 분리.
"""

from __future__ import annotations

import re
from unittest import TestCase


def format_jubun_input(raw: str) -> str:
    """Mirror of frontend/src/lib/sales-statement-jubun.ts ``formatJubunInput`` — 동기 유지."""
    digits = re.sub(r"\D", "", raw or "")
    if not digits:
        return ""
    if len(digits) <= 2:
        return digits
    core = digits[-5:] if len(digits) > 5 else digits
    return core.zfill(5)


def format_idnum_input(raw: str) -> str:
    """Mirror of frontend/src/lib/sales-statement-jubun.ts ``formatIdnumInput`` — 동기 유지.

    Subu21 Edit109 — 항상 5자리 zero-pad. 6자리 이상은 끝 5자리만 (`Format('%05s', St2)`).
    """
    digits = re.sub(r"\D", "", raw or "")
    if not digits:
        return ""
    core = digits[-5:] if len(digits) > 5 else digits
    return core.zfill(5)


def format_idnum_display(idnum):
    """Mirror of ``formatIdnumDisplay`` — 0/None/비유효 → 빈 문자열."""
    if idnum is None:
        return ""
    try:
        n = int(idnum) if not isinstance(idnum, int) else idnum
    except (TypeError, ValueError):
        return ""
    if n <= 0:
        return ""
    return f"{n:05d}"


def gdate_to_date_input(gdate: str) -> str:
    g = (gdate or "").strip()
    if not g:
        return g
    if "." in g and "-" not in g:
        return g.replace(".", "-")
    return g


def resolve_sales_statement_ocode(account_family):
    if (account_family or "").strip().lower() == "chul_09":
        return "A"
    return "B"


class JubunFormatTest(TestCase):
    """기존 jubun(=거래차수) backward-compat 회귀 — 2자리 패딩 금지."""

    def test_two_digit_not_padded_to_five(self) -> None:
        self.assertEqual(format_jubun_input("11"), "11")
        self.assertEqual(format_jubun_input("1"), "1")

    def test_three_plus_digits_padded(self) -> None:
        self.assertEqual(format_jubun_input("123"), "00123")

    def test_long_input_truncates_to_five(self) -> None:
        self.assertEqual(format_jubun_input("123456"), "23456")

    def test_gdate_to_date_input(self) -> None:
        self.assertEqual(gdate_to_date_input("2026.05.14"), "2026-05-14")

    def test_resolve_ocode_chul09(self) -> None:
        self.assertEqual(resolve_sales_statement_ocode("chul_09"), "A")
        self.assertEqual(resolve_sales_statement_ocode("chul_05"), "B")


class IdnumFormatTest(TestCase):
    """DEC-064 §Idnum — Edit109 5자리 zero-pad 정합."""

    def test_short_input_padded_to_five(self) -> None:
        self.assertEqual(format_idnum_input("1"), "00001")
        self.assertEqual(format_idnum_input("12"), "00012")
        self.assertEqual(format_idnum_input("12345"), "12345")

    def test_long_input_keeps_last_five(self) -> None:
        self.assertEqual(format_idnum_input("123456"), "23456")

    def test_blank_returns_empty(self) -> None:
        self.assertEqual(format_idnum_input(""), "")
        self.assertEqual(format_idnum_input("abc"), "")

    def test_display_zero_pad(self) -> None:
        self.assertEqual(format_idnum_display(1), "00001")
        self.assertEqual(format_idnum_display("12345"), "12345")

    def test_display_invalid(self) -> None:
        self.assertEqual(format_idnum_display(0), "")
        self.assertEqual(format_idnum_display(None), "")
        self.assertEqual(format_idnum_display(-1), "")
        self.assertEqual(format_idnum_display("abc"), "")


if __name__ == "__main__":
    from unittest import main

    main()
