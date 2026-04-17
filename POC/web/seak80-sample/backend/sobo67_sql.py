"""
Sobo67 / Subu67 SQL: S1_Ssub detail aggregate + Sg_Csum second pass.

Uses table alias `s` on S1_Ssub for JOIN safety. G4_Book join when Hcode is set.
"""

from __future__ import annotations

from typing import Any, Literal

GridKind = Literal["grid1", "grid2"]


def _escape_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "''")


def ocode_like_for_mode(mode: str) -> str:
    """Subu67 Panel102 -> Ocode LIKE (first S1_Ssub pass)."""
    m = (mode or "").strip().lower()
    if m in ("hq", "a", "bonsa"):
        return "%A%"
    return "%B%"


def scode_like_letter_for_mode(mode: str) -> str:
    """Subu67 St2 for Sg_Csum / Scode LIKE (second pass). Same A/B split as Ocode branch."""
    m = (mode or "").strip().lower()
    if m in ("hq", "a", "bonsa"):
        return "A"
    return "B"


def build_sobo67_detail_pymysql(
    *,
    grid: GridKind,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    bcode_from: str,
    bcode_to: str,
    parent_bcode: str,
    t00: int,
    limit_rows: int,
    detail_offset: int = 0,
) -> tuple[str, list[Any]]:
    """Grouped detail rows matching Delphi first Socket SQL (S1_Ssub)."""
    date_lo = f"{date_from.strip()}.00"
    date_hi = f"{date_to.strip()}.99"
    like_pat = ocode_like_for_mode(book_mode)
    params: list[Any] = []
    clauses = ["s.Gdate >= %s", "s.Gdate <= %s", "s.Ocode LIKE %s"]
    params.extend([date_lo, date_hi, like_pat])

    if hcode.strip():
        clauses.append("s.Hcode = %s")
        params.append(hcode.strip())
    if scode_filter:
        clauses.append(
            "((s.Scode='X' AND s.Gcode<>%s) OR s.Scode='Y' OR s.Scode='Z')"
        )
        params.append("00001")

    bf = (bcode_from or "").strip()
    bt = (bcode_to or "").strip()
    if bf:
        clauses.append("s.Bcode >= %s")
        params.append(bf)
    if bt:
        clauses.append("s.Bcode <= %s")
        params.append(bt)

    pb = (parent_bcode or "").strip()
    if grid == "grid2":
        if pb:
            clauses.append("s.Bcode = %s")
            params.append(pb)
        elif t00 != 1:
            # Month grid without parent row: no rows until user selects year row.
            clauses.append("1=0")

    where_inner = " AND ".join(clauses)
    where_full = d_select_prefix + where_inner

    lim = max(1, min(int(limit_rows), 50_000))
    off = max(0, int(detail_offset))

    # Plain equality keeps G4_Book index use; padding/spaces -> batch fill (main.py).
    join_sql = "LEFT JOIN G4_Book b ON b.Hcode = s.Hcode AND b.Gcode = s.Bcode "
    gname_expr = "COALESCE(MAX(TRIM(b.Gname)), '') AS gname"

    sql = (
        "SELECT s.Bcode AS bcode, s.Gdate AS gdate, s.Scode AS scode, "
        "s.Gubun AS gubun, s.Pubun AS pubun, "
        "s.Hcode AS row_hcode, "
        "SUM(s.Gsqut) AS gsqut, SUM(s.Gssum) AS gssum, "
        f"{gname_expr} "
        "FROM S1_Ssub s "
        + join_sql
        + "WHERE "
        + where_full
        + " GROUP BY s.Bcode, s.Gdate, s.Scode, s.Gubun, s.Pubun, s.Hcode "
        "ORDER BY s.Bcode, s.Gdate, s.Scode, s.Gubun, s.Pubun "
    )
    # offset==0: single-arg LIMIT avoids "LIMIT 0,n" / driver rewrites that surface as OFFSET on old servers.
    if off <= 0:
        sql += "LIMIT %s"
        params.append(lim)
    else:
        sql += "LIMIT %s, %s"
        params.extend([off, lim])
    return sql, params


def build_sobo67_sg_csum_pymysql(
    *,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    bcode_from: str,
    bcode_to: str,
    parent_bcode: str,
    t00: int,
    limit_rows: int,
) -> tuple[str, list[Any]]:
    """
    Sg_Csum second pass (Subu67): Select Gcode,Gdate,Sum(Gbsum) From Sg_Csum Where ...
    St1 uses Scode LIKE (not Ocode) and optional Gcode range on c.Gcode.
    """
    date_lo = f"{date_from.strip()}.00"
    date_hi = f"{date_to.strip()}.99"
    letter = scode_like_letter_for_mode(book_mode)
    scode_like = f"%{letter}%"
    params: list[Any] = [date_lo, date_hi, scode_like]
    clauses = ["Gdate >= %s", "Gdate <= %s", "Scode LIKE %s"]

    if hcode.strip():
        clauses.append("Hcode = %s")
        params.append(hcode.strip())

    bf = (bcode_from or "").strip()
    bt = (bcode_to or "").strip()
    pb = (parent_bcode or "").strip()

    if t00 != 1:
        if pb:
            clauses.append("Gcode = %s")
            params.append(pb)
    elif t00 == 1 and bf and bt:
        clauses.append("Gcode >= %s")
        params.append(bf)
        clauses.append("Gcode <= %s")
        params.append(bt)

    where_inner = " AND ".join(clauses)
    where_full = d_select_prefix + where_inner
    lim = max(1, min(int(limit_rows), 50_000))
    sql = (
        "SELECT Gcode AS gcode, Gdate AS gdate, COALESCE(SUM(Gbsum), 0) AS gbsum "
        "FROM Sg_Csum WHERE "
        + where_full
        + " GROUP BY Gcode, Gdate ORDER BY Gcode, Gdate LIMIT %s"
    )
    params.append(lim)
    return sql, params


def build_sobo67_detail_mysql3_sql(
    *,
    grid: GridKind,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    bcode_from: str,
    bcode_to: str,
    parent_bcode: str,
    t00: int,
    limit_rows: int,
    detail_offset: int = 0,
) -> str:
    esc_lo = _escape_literal(f"{date_from.strip()}.00")
    esc_hi = _escape_literal(f"{date_to.strip()}.99")
    like_pat = _escape_literal(ocode_like_for_mode(book_mode))
    parts = [
        f"s.Gdate >= '{esc_lo}'",
        f"s.Gdate <= '{esc_hi}'",
        f"s.Ocode LIKE '{like_pat}'",
    ]
    if hcode.strip():
        parts.append(f"s.Hcode = '{_escape_literal(hcode.strip())}'")
    if scode_filter:
        parts.append(
            "((s.Scode='X' AND s.Gcode<>'00001') OR s.Scode='Y' OR s.Scode='Z')"
        )
    bf = (bcode_from or "").strip()
    bt = (bcode_to or "").strip()
    if bf:
        parts.append(f"s.Bcode >= '{_escape_literal(bf)}'")
    if bt:
        parts.append(f"s.Bcode <= '{_escape_literal(bt)}'")

    pb = (parent_bcode or "").strip()
    if grid == "grid2":
        if pb:
            parts.append(f"s.Bcode = '{_escape_literal(pb)}'")
        elif t00 != 1:
            parts.append("1=0")

    where_inner = " AND ".join(parts)
    where_full = f"{d_select_prefix}{where_inner}"
    lim = max(1, min(int(limit_rows), 50_000))
    off = max(0, int(detail_offset))

    join_sql = "LEFT JOIN G4_Book b ON b.Hcode = s.Hcode AND b.Gcode = s.Bcode "
    gname_expr = "COALESCE(MAX(TRIM(b.Gname)), '') AS gname"

    base = (
        "SELECT s.Bcode AS bcode, s.Gdate AS gdate, s.Scode AS scode, "
        "s.Gubun AS gubun, s.Pubun AS pubun, "
        "s.Hcode AS row_hcode, "
        "SUM(s.Gsqut) AS gsqut, SUM(s.Gssum) AS gssum, "
        f"{gname_expr} "
        "FROM S1_Ssub s "
        + join_sql
        + "WHERE "
        + where_full
        + " GROUP BY s.Bcode, s.Gdate, s.Scode, s.Gubun, s.Pubun, s.Hcode "
        "ORDER BY s.Bcode, s.Gdate, s.Scode, s.Gubun, s.Pubun "
    )
    if off <= 0:
        return base + f"LIMIT {lim}"
    return base + f"LIMIT {off}, {lim}"


def build_sobo67_sg_csum_mysql3_sql(
    *,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    bcode_from: str,
    bcode_to: str,
    parent_bcode: str,
    t00: int,
    limit_rows: int,
) -> str:
    esc_lo = _escape_literal(f"{date_from.strip()}.00")
    esc_hi = _escape_literal(f"{date_to.strip()}.99")
    letter = scode_like_letter_for_mode(book_mode)
    esc_like = _escape_literal(f"%{letter}%")
    parts = [
        f"Gdate >= '{esc_lo}'",
        f"Gdate <= '{esc_hi}'",
        f"Scode LIKE '{esc_like}'",
    ]
    if hcode.strip():
        parts.append(f"Hcode = '{_escape_literal(hcode.strip())}'")

    bf = (bcode_from or "").strip()
    bt = (bcode_to or "").strip()
    pb = (parent_bcode or "").strip()
    if t00 != 1:
        if pb:
            parts.append(f"Gcode = '{_escape_literal(pb)}'")
    elif t00 == 1 and bf and bt:
        parts.append(f"Gcode >= '{_escape_literal(bf)}'")
        parts.append(f"Gcode <= '{_escape_literal(bt)}'")

    where_inner = " AND ".join(parts)
    where_full = f"{d_select_prefix}{where_inner}"
    lim = max(1, min(int(limit_rows), 50_000))
    return (
        "SELECT Gcode AS gcode, Gdate AS gdate, COALESCE(SUM(Gbsum), 0) AS gbsum "
        "FROM Sg_Csum WHERE "
        + where_full
        + f" GROUP BY Gcode, Gdate ORDER BY Gcode, Gdate LIMIT {lim}"
    )


# --- Backward-compatible names for tests (detail shape) ---
def build_sobo67_proto_pymysql(
    *,
    grid: GridKind,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    limit_rows: int,
) -> tuple[str, list[Any]]:
    return build_sobo67_detail_pymysql(
        grid=grid,
        d_select_prefix=d_select_prefix,
        date_from=date_from,
        date_to=date_to,
        hcode=hcode,
        book_mode=book_mode,
        scode_filter=scode_filter,
        bcode_from="",
        bcode_to="",
        parent_bcode="",
        t00=1 if grid == "grid2" else 0,
        limit_rows=limit_rows,
    )


def build_sobo67_proto_mysql3_sql(
    *,
    grid: GridKind,
    d_select_prefix: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    limit_rows: int,
) -> str:
    return build_sobo67_detail_mysql3_sql(
        grid=grid,
        d_select_prefix=d_select_prefix,
        date_from=date_from,
        date_to=date_to,
        hcode=hcode,
        book_mode=book_mode,
        scode_filter=scode_filter,
        bcode_from="",
        bcode_to="",
        parent_bcode="",
        t00=1 if grid == "grid2" else 0,
        limit_rows=limit_rows,
    )
