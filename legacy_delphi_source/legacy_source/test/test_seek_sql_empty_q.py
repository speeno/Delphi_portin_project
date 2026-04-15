"""seek_sql: empty q / empty hcode build correct WHERE clauses and param lists."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from seek_sql import (  # noqa: E402
    build_seek20_mysql3_sql,
    build_seek20_pymysql,
    build_seek30_mysql3_sql,
    build_seek30_pymysql,
)


def test_seek20_pymysql_empty_q_no_like_params():
    sql, params = build_seek20_pymysql(
        "",
        "H0001",
        "",
        lower_mode=False,
        exclude_grat9=False,
        limit200=False,
        limit_cap=None,
    )
    assert "1=1" in sql
    assert params == ["H0001"]


def test_seek20_pymysql_empty_q_exclude_grat9():
    sql, params = build_seek20_pymysql(
        "",
        "H0001",
        "",
        lower_mode=False,
        exclude_grat9=True,
        limit200=False,
        limit_cap=None,
    )
    assert "Grat9" in sql
    assert "1=1" in sql
    assert params == ["H0001"]


def test_seek30_mysql3_empty_q():
    sql = build_seek30_mysql3_sql(
        "",
        "H1",
        "",
        lower_mode=True,
        limit200=False,
        limit_cap=None,
    )
    assert "1=1" in sql
    assert "LIKE" not in sql
    assert "Hcode =" in sql


def test_seek30_mysql3_empty_q_and_empty_hcode():
    sql = build_seek30_mysql3_sql(
        "",
        "",
        "",
        lower_mode=False,
        limit200=False,
        limit_cap=None,
    )
    assert "1=1" in sql
    assert "Hcode =" not in sql


def test_seek20_mysql3_nonempty_still_like():
    sql = build_seek20_mysql3_sql(
        "ab",
        "H1",
        "",
        lower_mode=False,
        exclude_grat9=False,
        limit200=False,
        limit_cap=None,
    )
    assert "gcode LIKE" in sql
    assert "1=1" not in sql


def test_seek30_pymysql_empty_q():
    sql, params = build_seek30_pymysql(
        "",
        "HX",
        "",
        lower_mode=False,
        limit200=False,
        limit_cap=None,
    )
    assert "1=1" in sql
    assert params == ["HX"]


def test_seek20_pymysql_empty_hcode_empty_q():
    sql, params = build_seek20_pymysql(
        "",
        "",
        "",
        lower_mode=False,
        exclude_grat9=False,
        limit200=False,
        limit_cap=None,
    )
    assert "1=1" in sql
    assert "Hcode =" not in sql
    assert params == []


def test_seek20_pymysql_empty_hcode_with_term():
    sql, params = build_seek20_pymysql(
        "ab",
        "",
        "",
        lower_mode=False,
        exclude_grat9=False,
        limit200=False,
        limit_cap=None,
    )
    assert "Hcode =" not in sql
    assert params == ["ab%", "ab%", "ab%"]
