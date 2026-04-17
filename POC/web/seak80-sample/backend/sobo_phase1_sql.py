"""
Phase-1 read-only POC: Sobo13 T1_Gbun, Sobo12 G2_Gbun (Subu13.pas / Subu12.pas).

Uses D_Select prefix from profile (servers.yaml d_select_sql), same as Seek20.
"""

from __future__ import annotations

from typing import Any


def _escape_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "''")


def build_sobo13_t1_gbun_pymysql(
    *,
    d_select_prefix: str,
    hcode: str,
    gcode: str,
    limit_rows: int,
) -> tuple[str, list[Any]]:
    """Empty hcode = all Hcode (same idea as Seek20/Seek30); optional Gcode."""
    hc = (hcode or "").strip()
    gc = (gcode or "").strip()
    clauses: list[str] = []
    params: list[Any] = []
    if hc:
        clauses.append("Hcode = %s")
        params.append(hc)
    if gc:
        clauses.append("Gcode = %s")
        params.append(gc)
    inner = " AND ".join(clauses) if clauses else "1=1"
    where_full = f"{d_select_prefix}{inner}"
    lim = max(1, min(int(limit_rows), 2000))
    sql = (
        "SELECT * FROM T1_Gbun WHERE "
        + where_full
        + " ORDER BY Gcode, Gjisa LIMIT %s"
    )
    params.append(lim)
    return sql, params


def build_sobo13_t1_gbun_mysql3_sql(
    *,
    d_select_prefix: str,
    hcode: str,
    gcode: str,
    limit_rows: int,
) -> str:
    hc = (hcode or "").strip()
    gc = (gcode or "").strip()
    parts: list[str] = []
    if hc:
        parts.append(f"Hcode = '{_escape_literal(hc)}'")
    if gc:
        parts.append(f"Gcode = '{_escape_literal(gc)}'")
    inner = " AND ".join(parts) if parts else "1=1"
    where_full = f"{d_select_prefix}{inner}"
    lim = max(1, min(int(limit_rows), 2000))
    return (
        "SELECT * FROM T1_Gbun WHERE "
        + where_full
        + f" ORDER BY Gcode, Gjisa LIMIT {lim}"
    )


def build_sobo12_g2_gbun_pymysql(
    *,
    d_select_prefix: str,
    hcode: str,
    limit_rows: int,
) -> tuple[str, list[Any]]:
    """Empty hcode = all Hcode (Seek20-style)."""
    hc = (hcode or "").strip()
    if hc:
        where_full = f"{d_select_prefix}Hcode = %s"
        params: list[Any] = [hc]
    else:
        where_full = f"{d_select_prefix}1=1"
        params = []
    lim = max(1, min(int(limit_rows), 2000))
    sql = (
        "SELECT * FROM G2_Gbun WHERE "
        + where_full
        + " ORDER BY Gcode LIMIT %s"
    )
    params.append(lim)
    return sql, params


def build_sobo12_g2_gbun_mysql3_sql(
    *,
    d_select_prefix: str,
    hcode: str,
    limit_rows: int,
) -> str:
    hc = (hcode or "").strip()
    if hc:
        where_full = f"{d_select_prefix}Hcode = '{_escape_literal(hc)}'"
    else:
        where_full = f"{d_select_prefix}1=1"
    lim = max(1, min(int(limit_rows), 2000))
    return "SELECT * FROM G2_Gbun WHERE " + where_full + f" ORDER BY Gcode LIMIT {lim}"
