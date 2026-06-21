"""aiomysql DECIMAL/NEWDECIMAL bytes 변환 회귀 (2026-06-21).

풀이 ``use_unicode=False`` 라 소수 컬럼이 bytes 로 오는데, PyMySQL 기본 변환기
``decimal.Decimal(bytes)`` 는 TypeError(_read_row_from_packet) 다. 소수 컬럼이나
그 SUM/AVG(NEWDECIMAL) 를 SELECT 하는 모든 조회(일별/기간 입고내역서 등)가 죽던
근본 결함 → DECIMAL/NEWDECIMAL 변환기를 bytes-tolerant 로 교체한다.
"""

from __future__ import annotations

import decimal
import sys
from pathlib import Path
from unittest import TestCase

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

import app.core.db as db  # noqa: E402
from pymysql.constants import FIELD_TYPE  # noqa: E402
from pymysql.converters import decoders as PYMYSQL_DECODERS  # noqa: E402


class DecimalBytesConverterTest(TestCase):
    def test_handles_bytes_str_none_and_bad(self) -> None:
        f = db._decimal_bytes_tolerant
        self.assertEqual(f(b"1000.5"), decimal.Decimal("1000.5"))   # bytes (핵심)
        self.assertEqual(f(b"80"), decimal.Decimal("80"))
        self.assertEqual(f("3.14"), decimal.Decimal("3.14"))         # str
        self.assertIsNone(f(None))                                   # NULL
        self.assertEqual(f(b"\xff\xfe"), decimal.Decimal(0))         # 불량 → 0 (500 금지)

    def test_default_decimal_converter_raises_on_bytes(self) -> None:
        # 회귀 근거: 기본 변환기는 bytes 에서 TypeError → 우리가 교체해야 하는 이유.
        with self.assertRaises(TypeError):
            decimal.Decimal(b"1.5")

    def test_conv_overrides_only_decimal_preserving_rest(self) -> None:
        conv = db._AIOMYSQL_CONV
        # DECIMAL(0)·NEWDECIMAL(246) 만 교체
        self.assertIs(conv[FIELD_TYPE.DECIMAL], db._decimal_bytes_tolerant)
        self.assertIs(conv[FIELD_TYPE.NEWDECIMAL], db._decimal_bytes_tolerant)
        # 문자열·정수·실수 변환기는 보존(기존 동작 무변경)
        self.assertIs(conv[FIELD_TYPE.VAR_STRING], PYMYSQL_DECODERS[FIELD_TYPE.VAR_STRING])
        self.assertIs(conv[FIELD_TYPE.LONG], PYMYSQL_DECODERS[FIELD_TYPE.LONG])
        self.assertIs(conv[FIELD_TYPE.FLOAT], PYMYSQL_DECODERS[FIELD_TYPE.FLOAT])
        self.assertEqual(len(conv), len(PYMYSQL_DECODERS))


if __name__ == "__main__":
    from unittest import main

    main(verbosity=2)
