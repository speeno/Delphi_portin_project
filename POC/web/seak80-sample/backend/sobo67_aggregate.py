"""
Subu67 Button101 / Button201 row classification (memory grid) from S1_Ssub detail rows.

Source: Subu67.pas While loops after Socket.MakeGrid ? Scode/Gubun/Pubun branching.
"""

from __future__ import annotations

from typing import Any, TypedDict


class Sobo67DetailRow(TypedDict, total=False):
    bcode: str
    gdate: str
    scode: str
    gubun: str
    pubun: str
    gsqut: float | int
    gssum: float | int
    gname: str


def _f(x: Any) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def grain_key(gdate: str, *, year_only: bool) -> str:
    """Match Subu67: year grid Copy(Gdate,1,4); month grid Copy(Gdate,1,7)."""
    g = (gdate or "").strip()
    if len(g) < 4:
        return ""
    if year_only:
        return g[:4]
    if len(g) >= 7:
        return g[:7]
    return g[:4]


def _empty_bucket(gname: str) -> dict[str, Any]:
    return {
        "gdate": "",
        "gcode": "",
        "gname": gname or "",
        "giqut": 0.0,
        "goqut": 0.0,
        "gjqut": 0.0,
        "gbqut": 0.0,
        "gpqut": 0.0,
        "gosum": 0.0,
        "gbsum": 0.0,
        "gpsum": 0.0,
    }


def apply_delphi_line(bucket: dict[str, Any], scode: str, gubun: str, pubun: str, t01: float, t02: float) -> None:
    """One S1_Ssub grouped line ? Subu67.pas classification (Korean literals)."""
    st5 = (scode or "").strip()
    st3 = (gubun or "").strip()
    st4 = (pubun or "").strip()

    if st5 == "Y":
        if st3 == "\uc785\uace0":
            bucket["giqut"] = _f(bucket["giqut"]) + t01
        elif st3 == "\ubc18\ud488":
            bucket["giqut"] = _f(bucket["giqut"]) - t01
    else:
        if st4 == "\ubc18\ud488":
            bucket["gbqut"] = _f(bucket["gbqut"]) + t01
            bucket["gbsum"] = _f(bucket["gbsum"]) + t02
        elif st4 == "\ud3d0\uae30":
            if st5 == "X":
                bucket["gbqut"] = _f(bucket["gbqut"]) + t01
            if st5 == "Z":
                bucket["gpqut"] = _f(bucket["gpqut"]) + t01
            bucket["gbsum"] = _f(bucket["gbsum"]) + t02
        elif st4 == "\uc99d\uc815":
            bucket["gjqut"] = _f(bucket["gjqut"]) + t01
            bucket["gosum"] = _f(bucket["gosum"]) + t02
        elif st3 == "\ucd9c\uace0":
            bucket["goqut"] = _f(bucket["goqut"]) + t01
            bucket["gosum"] = _f(bucket["gosum"]) + t02


def aggregate_detail_rows(
    rows: list[dict[str, Any]],
    *,
    year_grain: bool,
) -> list[dict[str, Any]]:
    """
    Fold detail rows into (grain_date, bcode) buckets with Subu67 quantity/amount columns.
    """
    buckets: dict[tuple[str, str], dict[str, Any]] = {}

    for raw in rows:
        bc = str(raw.get("bcode") or raw.get("gcode") or "").strip()
        gd = str(raw.get("gdate") or "").strip()
        gk = grain_key(gd, year_only=year_grain)
        if not gk or not bc:
            continue
        key = (gk, bc)
        gn = str(raw.get("gname") or "").strip()
        if key not in buckets:
            b = _empty_bucket(gn)
            b["gdate"] = gk
            b["gcode"] = bc
            buckets[key] = b
        else:
            if gn and not (buckets[key].get("gname") or "").strip():
                buckets[key]["gname"] = gn

        apply_delphi_line(
            buckets[key],
            str(raw.get("scode") or ""),
            str(raw.get("gubun") or ""),
            str(raw.get("pubun") or ""),
            _f(raw.get("gsqut")),
            _f(raw.get("gssum")),
        )

    out = list(buckets.values())
    out.sort(key=lambda r: (r.get("gcode") or "", r.get("gdate") or ""))
    return out


def merge_aggregate_grids(
    left: list[dict[str, Any]],
    right: list[dict[str, Any]],
    *,
    year_grain: bool,
) -> list[dict[str, Any]]:
    """
    Merge two aggregate_detail_rows outputs by (grain gdate, gcode), summing measures.
    Used when S1_Ssub detail is fetched in LIMIT/OFFSET chunks (gpsum merged later via Sg_Csum).
    """
    qty_keys = ("giqut", "goqut", "gjqut", "gbqut", "gpqut", "gosum", "gbsum", "gpsum")
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for r in left + right:
        gk, gc = _grid_row_key(r, year_grain=year_grain)
        if not gk or not gc:
            continue
        key = (gk, gc)
        if key not in index:
            row = _empty_bucket(str(r.get("gname") or "").strip())
            row["gdate"] = gk
            row["gcode"] = gc
            if (r.get("gname") or "").strip():
                row["gname"] = str(r.get("gname") or "").strip()
            for k in qty_keys:
                row[k] = _f(r.get(k))
            index[key] = row
        else:
            t = index[key]
            for k in qty_keys:
                t[k] = _f(t.get(k)) + _f(r.get(k))
            if not (t.get("gname") or "").strip() and (r.get("gname") or "").strip():
                t["gname"] = str(r.get("gname") or "").strip()
    out = list(index.values())
    out.sort(key=lambda r: (r.get("gcode") or "", r.get("gdate") or ""))
    return out


def _grid_row_key(r: dict[str, Any], *, year_grain: bool) -> tuple[str, str]:
    gc = str(r.get("gcode") or "").strip()
    gd = str(r.get("gdate") or "").strip()
    gk = grain_key(gd, year_only=year_grain)
    return (gk, gc)


def merge_sg_csum_gpsum(
    grid_rows: list[dict[str, Any]],
    sg_rows: list[dict[str, Any]],
    *,
    year_grain: bool,
) -> None:
    """
    Second pass: Sg_Csum Sum(Gbsum) -> accumulate into gpsum on matching (grain, gcode).
    Subu67.pas locates nSqry/mSqry by Gdate prefix + Gcode.
    """
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for r in grid_rows:
        gk, gc = _grid_row_key(r, year_grain=year_grain)
        if gk and gc:
            index[(gk, gc)] = r

    for sg in sg_rows:
        gc = str(sg.get("gcode") or "").strip()
        gfull = str(sg.get("gdate") or "").strip()
        gk = grain_key(gfull, year_only=year_grain)
        if not gc or not gk:
            continue
        t01 = _f(sg.get("gbsum"))
        row = index.get((gk, gc))
        if row is None:
            row = _empty_bucket("")
            row["gdate"] = gk
            row["gcode"] = gc
            grid_rows.append(row)
            index[(gk, gc)] = row
        row["gpsum"] = _f(row.get("gpsum")) + t01


def footer_totals(rows: list[dict[str, Any]]) -> dict[str, float]:
    keys = ("giqut", "goqut", "gjqut", "gbqut", "gpqut", "gosum", "gbsum", "gpsum")
    acc: dict[str, float] = {k: 0.0 for k in keys}
    for r in rows:
        for k in keys:
            acc[k] += _f(r.get(k))
    return acc
