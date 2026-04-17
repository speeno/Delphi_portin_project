"""
Seek20 / Seek30 SQL builders aligned with Seek02.pas / Seek03.pas (chul_09 FilterTing).

- Prefix LIKE on gcode, gname, gposa when not lower_mode; LOWER() + %%term%% when lower_mode.
- Empty search term: keyword clause is 1=1 (like Seak80 empty q).
- Empty Hcode: omit Hcode filter (all Hcode values); non-empty Hcode adds Hcode = value.
- ORDER BY gcode vs gname when term < '9____' (Delphi string order).
- Optional Limit 0, 200 (checkbox), optional extra LIMIT cap.
- d_select_sql: YAML fragment concatenated immediately after WHERE (legacy D_Select).
"""

from __future__ import annotations

from typing import Any


def _escape_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "''")


def order_by_seek(term: str) -> str:
    """Seek02/03: if Str < '9____' then Order By Gcode else Order By Gname."""
    return "gcode" if term < "9____" else "gname"


def build_seek20_mysql3_sql(
    term: str,
    hcode: str,
    d_select_prefix: str,
    *,
    lower_mode: bool,
    exclude_grat9: bool,
    limit200: bool,
    limit_cap: int | None,
    include_gqut9: bool = True,
) -> str:
    """Single string for MySQL 3.x raw protocol (only escaped literals)."""
    if not term:
        inner = "1=1"
    else:
        esc_t = _escape_literal(term)
        if lower_mode:
            like_val = f"'%{esc_t}%'"
            inner = (
                f"(LOWER(gcode) LIKE LOWER({like_val}) OR "
                f"LOWER(gname) LIKE LOWER({like_val}) OR "
                f"LOWER(gposa) LIKE LOWER({like_val}))"
            )
        else:
            p = f"'{esc_t}%'"
            inner = f"(gcode LIKE {p} OR gname LIKE {p} OR gposa LIKE {p})"

    if exclude_grat9:
        inner = f"((Grat9<>1 OR Grat9 IS NULL) AND ({inner}))"

    if hcode:
        esc_h = _escape_literal(hcode)
        where_rest = f"Hcode = '{esc_h}' AND {inner}"
    else:
        where_rest = inner
    where_full = f"{d_select_prefix}{where_rest}"
    ob = order_by_seek(term)
    cols = (
        "gubun, jubun, gcode, ocode, gname, gposa, gtel1, gtel2, gadd1, gadd2"
        + (", gqut9" if include_gqut9 else "")
    )
    sql = f"SELECT {cols} FROM G2_Ggwo WHERE " + where_full + f" ORDER BY {ob}"
    lim = _effective_limit(limit200, limit_cap)
    if lim is not None:
        sql += f" LIMIT 0, {int(lim)}"
    return sql


def build_seek20_pymysql(
    term: str,
    hcode: str,
    d_select_prefix: str,
    *,
    lower_mode: bool,
    exclude_grat9: bool,
    limit200: bool,
    limit_cap: int | None,
    include_gqut9: bool = True,
) -> tuple[str, list[Any]]:
    params: list[Any] = []
    if not term:
        inner_sql = "1=1"
    elif lower_mode:
        like_val = f"%{term}%"
        inner_sql = (
            "(LOWER(gcode) LIKE LOWER(%s) OR LOWER(gname) LIKE LOWER(%s) OR "
            "LOWER(gposa) LIKE LOWER(%s))"
        )
        params.extend([like_val, like_val, like_val])
    else:
        p = term + "%"
        inner_sql = "(gcode LIKE %s OR gname LIKE %s OR gposa LIKE %s)"
        params.extend([p, p, p])

    if exclude_grat9:
        inner_sql = f"((Grat9<>1 OR Grat9 IS NULL) AND ({inner_sql}))"

    if hcode:
        where_rest = "Hcode = %s AND " + inner_sql
        params.insert(0, hcode)
    else:
        where_rest = inner_sql
    ob = order_by_seek(term)
    gq = ", gqut9 AS gqut9" if include_gqut9 else ""
    sql = (
        "SELECT gubun AS gubun, jubun AS jubun, gcode AS gcode, ocode AS ocode, "
        "gname AS gname, gposa AS gposa, gtel1 AS gtel1, gtel2 AS gtel2, "
        "gadd1 AS gadd1, gadd2 AS gadd2"
        f"{gq} FROM G2_Ggwo WHERE " + d_select_prefix + where_rest + f" ORDER BY {ob}"
    )
    lim = _effective_limit(limit200, limit_cap)
    if lim is not None:
        sql += " LIMIT %s"
        params.append(int(lim))
    return sql, params


def build_seek30_mysql3_sql(
    term: str,
    hcode: str,
    d_select_prefix: str,
    *,
    lower_mode: bool,
    limit200: bool,
    limit_cap: int | None,
) -> str:
    if not term:
        inner = "1=1"
    else:
        esc_t = _escape_literal(term)
        if lower_mode:
            like_val = f"'%{esc_t}%'"
            inner = (
                f"(LOWER(gcode) LIKE LOWER({like_val}) OR "
                f"LOWER(gname) LIKE LOWER({like_val}) OR "
                f"LOWER(gposa) LIKE LOWER({like_val}))"
            )
        else:
            p = f"'{esc_t}%'"
            inner = f"(gcode LIKE {p} OR gname LIKE {p} OR gposa LIKE {p})"

    if hcode:
        esc_h = _escape_literal(hcode)
        where_rest = f"Hcode = '{esc_h}' AND {inner}"
    else:
        where_rest = inner
    where_full = f"{d_select_prefix}{where_rest}"
    ob = order_by_seek(term)
    sql = (
        "SELECT scode, gcode, gposa, gname, gtel1, gtel2 "
        "FROM G3_Gjeo WHERE " + where_full + f" ORDER BY {ob}"
    )
    lim = _effective_limit(limit200, limit_cap)
    if lim is not None:
        sql += f" LIMIT 0, {int(lim)}"
    return sql


def build_seek30_pymysql(
    term: str,
    hcode: str,
    d_select_prefix: str,
    *,
    lower_mode: bool,
    limit200: bool,
    limit_cap: int | None,
) -> tuple[str, list[Any]]:
    params: list[Any] = []
    if not term:
        inner_sql = "1=1"
    elif lower_mode:
        like_val = f"%{term}%"
        inner_sql = (
            "(LOWER(gcode) LIKE LOWER(%s) OR LOWER(gname) LIKE LOWER(%s) OR "
            "LOWER(gposa) LIKE LOWER(%s))"
        )
        params.extend([like_val, like_val, like_val])
    else:
        p = term + "%"
        inner_sql = "(gcode LIKE %s OR gname LIKE %s OR gposa LIKE %s)"
        params.extend([p, p, p])

    if hcode:
        where_rest = "Hcode = %s AND " + inner_sql
        params.insert(0, hcode)
    else:
        where_rest = inner_sql
    ob = order_by_seek(term)
    sql = (
        "SELECT scode AS scode, gcode AS gcode, gposa AS gposa, gname AS gname, "
        "gtel1 AS gtel1, gtel2 AS gtel2 "
        "FROM G3_Gjeo WHERE " + d_select_prefix + where_rest + f" ORDER BY {ob}"
    )
    lim = _effective_limit(limit200, limit_cap)
    if lim is not None:
        sql += " LIMIT %s"
        params.append(int(lim))
    return sql, params


def _effective_limit(limit200: bool, limit_cap: int | None) -> int | None:
    if limit200 and limit_cap is not None:
        return min(200, int(limit_cap))
    if limit200:
        return 200
    if limit_cap is not None:
        return int(limit_cap)
    return None


def enrich_seek20_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """CalcFields-like: append stop-sale tag to display name when gqut9 == '1' (Seek02)."""
    stop_suffix = "<\uCD9C\uACE0\uC815\uC9C0>"  # <???????>
    out: list[dict[str, Any]] = []
    for r in rows:
        row = dict(r)
        gname = row.get("gname")
        gq = row.get("gqut9")
        gq_s = "" if gq is None else str(gq).strip()
        base = "" if gname is None else str(gname)
        if gq_s == "1":
            row["sname"] = base + stop_suffix
        else:
            row["sname"] = base
        out.append(row)
    return out
