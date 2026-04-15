"""sobo67_sql prototype WHERE / GROUP BY shape."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from sobo67_sql import build_sobo67_proto_mysql3_sql, build_sobo67_proto_pymysql  # noqa: E402


def test_pymysql_has_s1_ssub_and_group():
    sql, params = build_sobo67_proto_pymysql(
        grid="grid1",
        d_select_prefix="",
        date_from="2024.01",
        date_to="2024.12",
        hcode="H1",
        book_mode="book",
        scode_filter=False,
        limit_rows=100,
    )
    assert "FROM S1_Ssub" in sql
    assert "LEFT JOIN G4_Book" in sql
    assert "GROUP BY" in sql
    assert params[0] == "2024.01.00"
    assert "H1" in params
    assert "LIMIT %s" in sql
    assert params[-1] == 100


def test_pymysql_empty_hcode_no_extra_bind():
    sql, params = build_sobo67_proto_pymysql(
        grid="grid2",
        d_select_prefix="",
        date_from="2024.01",
        date_to="2024.03",
        hcode="",
        book_mode="hq",
        scode_filter=True,
        limit_rows=50,
    )
    assert "Hcode = %s" not in sql
    assert "00001" in params


def test_mysql3_hq_like():
    sql = build_sobo67_proto_mysql3_sql(
        grid="grid1",
        d_select_prefix="",
        date_from="2024.01",
        date_to="2024.12",
        hcode="",
        book_mode="hq",
        scode_filter=False,
        limit_rows=10,
    )
    assert "%A%" in sql
    assert "LIMIT 10" in sql
    assert "LIMIT 0," not in sql
