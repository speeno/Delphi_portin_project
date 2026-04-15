"""sobo_phase1_sql: T1_Gbun / G2_Gbun builders (PyMySQL + mysql3 LIMIT shape)."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from sobo_phase1_sql import (  # noqa: E402
    build_sobo12_g2_gbun_mysql3_sql,
    build_sobo12_g2_gbun_pymysql,
    build_sobo13_t1_gbun_mysql3_sql,
    build_sobo13_t1_gbun_pymysql,
)


def test_sobo13_pymysql_empty_hcode_is_all_hcode():
    sql, params = build_sobo13_t1_gbun_pymysql(
        d_select_prefix="",
        hcode="  ",
        gcode="",
        limit_rows=10,
    )
    assert "1=1" in sql
    assert params == [10]


def test_sobo13_pymysql_gcode_only_no_hcode():
    sql, params = build_sobo13_t1_gbun_pymysql(
        d_select_prefix="",
        hcode="",
        gcode="G1",
        limit_rows=5,
    )
    assert "Gcode = %s" in sql
    assert "Hcode = %s" not in sql
    assert params == ["G1", 5]


def test_sobo13_mysql3_single_limit():
    sql = build_sobo13_t1_gbun_mysql3_sql(
        d_select_prefix="",
        hcode="H0001",
        gcode="",
        limit_rows=100,
    )
    assert "LIMIT 100" in sql
    assert "LIMIT %s" not in sql
    assert "H0001" in sql


def test_sobo13_mysql3_empty_hcode():
    sql = build_sobo13_t1_gbun_mysql3_sql(
        d_select_prefix="",
        hcode="",
        gcode="",
        limit_rows=20,
    )
    assert "1=1" in sql
    assert "LIMIT 20" in sql


def test_sobo13_mysql3_optional_gcode():
    sql = build_sobo13_t1_gbun_mysql3_sql(
        d_select_prefix="",
        hcode="H1",
        gcode="G9",
        limit_rows=50,
    )
    assert "Gcode" in sql
    assert "G9" in sql
    assert "LIMIT 50" in sql


def test_sobo12_pymysql_hcode_and_limit():
    sql, params = build_sobo12_g2_gbun_pymysql(
        d_select_prefix="",
        hcode="H2",
        limit_rows=200,
    )
    assert "G2_Gbun" in sql
    assert params[0] == "H2"
    assert params[1] == 200
    assert "LIMIT %s" in sql


def test_sobo12_mysql3_single_limit():
    sql = build_sobo12_g2_gbun_mysql3_sql(
        d_select_prefix="",
        hcode="HX",
        limit_rows=17,
    )
    assert "LIMIT 17" in sql
    assert "HX" in sql


def test_sobo12_pymysql_empty_hcode():
    sql, params = build_sobo12_g2_gbun_pymysql(
        d_select_prefix="",
        hcode="",
        limit_rows=100,
    )
    assert "1=1" in sql
    assert params == [100]


def test_sobo12_mysql3_empty_hcode():
    sql = build_sobo12_g2_gbun_mysql3_sql(
        d_select_prefix="",
        hcode="",
        limit_rows=9,
    )
    assert "1=1" in sql
    assert "LIMIT 9" in sql
