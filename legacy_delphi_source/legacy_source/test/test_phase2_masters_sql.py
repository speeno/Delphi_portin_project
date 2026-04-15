"""phase2_masters_sql: PyMySQL + mysql3 builders (empty hcode, LIMIT)."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

import pytest  # noqa: E402

from phase2_masters_sql import (  # noqa: E402
    build_phase2_simple_select_mysql3_sql,
    build_phase2_simple_select_pymysql,
    phase2_resolve_form,
)


def test_phase2_resolve_unknown():
    assert phase2_resolve_form("sobo99") is None
    assert phase2_resolve_form("SOBO11")[0] == "G1_Ggeo"


def test_phase2_pymysql_empty_hcode():
    sql, params = build_phase2_simple_select_pymysql(
        d_select_prefix="",
        table="G1_Ggeo",
        order_by="Gcode",
        hcode="  ",
        limit_rows=10,
    )
    assert "FROM G1_Ggeo" in sql
    assert "1=1" in sql
    assert "LIMIT %s" in sql
    assert params == [10]


def test_phase2_pymysql_hcode():
    sql, params = build_phase2_simple_select_pymysql(
        d_select_prefix="",
        table="G7_Gbun",
        order_by="Gcode",
        hcode="H01",
        limit_rows=5,
    )
    assert "Hcode = %s" in sql
    assert params == ["H01", 5]


def test_phase2_mysql3_single_limit():
    sql = build_phase2_simple_select_mysql3_sql(
        d_select_prefix="",
        table="G4_Book",
        order_by="Gcode",
        hcode="H9",
        limit_rows=100,
    )
    assert "LIMIT 100" in sql
    assert "LIMIT %s" not in sql
    assert "H9" in sql


def test_phase2_invalid_table_raises():
    with pytest.raises(ValueError):
        build_phase2_simple_select_pymysql(
            d_select_prefix="",
            table="G1_Ggeo;DROP",
            order_by="Gcode",
            hcode="",
            limit_rows=1,
        )


def test_phase2_invalid_order_by_raises():
    with pytest.raises(ValueError):
        build_phase2_simple_select_pymysql(
            d_select_prefix="",
            table="G1_Ggeo",
            order_by="Gcode;DROP",
            hcode="",
            limit_rows=1,
        )
