"""
Seak04.pas FilterTing on Gg_Post: post/addr LIKE '%term%', ORDER BY post vs addr (Str < '9____').

Delphi omits LIMIT; HTTP API caps rows for safety.
"""

from __future__ import annotations

from typing import Any


def _escape_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "''")


def order_by_seak04(term: str) -> str:
    """Delphi Seak04: if Str < '9____' then Order By Post else Order By Addr."""
    return "post" if term < "9____" else "addr"


def build_seak04_mysql3_sql(term: str, limit: int) -> str:
    """Single string for MySQL 3.x raw protocol (only escaped literals)."""
    esc = _escape_literal(term)
    like = f"'%{esc}%'"
    inner = f"(post LIKE {like} OR addr LIKE {like})"
    ob = order_by_seak04(term)
    lim = int(limit)
    return (
        "SELECT post, addr, dddd, dong, city FROM Gg_Post WHERE "
        + inner
        + f" ORDER BY {ob} LIMIT 0, {lim}"
    )


def build_seak04_pymysql(term: str, limit: int) -> tuple[str, list[Any]]:
    like_val = f"%{term}%"
    inner_sql = "(post LIKE %s OR addr LIKE %s)"
    params: list[Any] = [like_val, like_val]
    ob = order_by_seak04(term)
    lim = int(limit)
    sql = (
        "SELECT post AS post, addr AS addr, dddd AS dddd, dong AS dong, city AS city "
        "FROM Gg_Post WHERE " + inner_sql + f" ORDER BY {ob} LIMIT %s"
    )
    params.append(lim)
    return sql, params
