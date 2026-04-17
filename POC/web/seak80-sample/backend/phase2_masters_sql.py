"""
Phase-2 read-only POC: single-table master list (D_Select prefix + optional Hcode + LIMIT).

Table/order pairs follow docs/phase1-structure/13-db-sql-references.csv (SubuNN.pas grid SELECT).
"""

from __future__ import annotations

import re
from typing import Any

from sobo67_sql import _escape_literal

# form_id -> (table, ORDER BY fragment; identifiers only)
PHASE2_MASTER_SPECS: dict[str, tuple[str, str]] = {
    "sobo11": ("G1_Ggeo", "Gcode"),
    "sobo15": ("G1_Ggeo", "Gcode"),
    "sobo14": ("G4_Book", "Gcode"),
    "sobo16": ("G6_Ggeo", "Gcode"),
    "sobo17": ("G7_Gbun", "Gcode"),
    "sobo17_1": ("G7_Gbun", "Gcode"),
    "sobo18": ("G7_Ggeo", "Gcode"),
    "sobo48": ("G7_Ggeo", "Gcode"),
    "sobo13_1": ("T0_Gbun", "Gcode"),
}


def phase2_resolve_form(form_id: str) -> tuple[str, str] | None:
    key = (form_id or "").strip().lower()
    return PHASE2_MASTER_SPECS.get(key)


def _assert_sql_identifier(name: str, *, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name):
        raise ValueError(f"invalid {label}: {name!r}")
    return name


def _assert_order_by_clause(ob: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_, ]+", ob):
        raise ValueError(f"invalid order by: {ob!r}")
    return ob.strip()


def build_phase2_simple_select_pymysql(
    *,
    d_select_prefix: str,
    table: str,
    order_by: str,
    hcode: str,
    limit_rows: int,
) -> tuple[str, list[Any]]:
    _assert_sql_identifier(table, label="table")
    ob = _assert_order_by_clause(order_by)
    hc = (hcode or "").strip()
    if hc:
        where_rest = "Hcode = %s"
        params: list[Any] = [hc]
    else:
        where_rest = "1=1"
        params = []
    where_full = f"{d_select_prefix}{where_rest}"
    lim = max(1, min(int(limit_rows), 2000))
    sql = f"SELECT * FROM {table} WHERE {where_full} ORDER BY {ob} LIMIT %s"
    params.append(lim)
    return sql, params


def build_phase2_simple_select_mysql3_sql(
    *,
    d_select_prefix: str,
    table: str,
    order_by: str,
    hcode: str,
    limit_rows: int,
) -> str:
    _assert_sql_identifier(table, label="table")
    ob = _assert_order_by_clause(order_by)
    hc = (hcode or "").strip()
    if hc:
        esc = _escape_literal(hc)
        where_rest = f"Hcode = '{esc}'"
    else:
        where_rest = "1=1"
    where_full = f"{d_select_prefix}{where_rest}"
    lim = max(1, min(int(limit_rows), 2000))
    return f"SELECT * FROM {table} WHERE {where_full} ORDER BY {ob} LIMIT {lim}"
