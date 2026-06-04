#!/usr/bin/env python3
"""S1_Ssub 거래명세서 — Gjisa·Jubun·Hcode·Scode LIST COUNT 진단.

교보문고(00001)·영풍문고(00004) 등 고정 조건에서 필터 조합별 행 수를 비교한다.

사용:
  PYTHONPATH=도서물류관리프로그램/backend \\
    python3 debug/probe_sales_statement_list_gjisa.py \\
      --server remote_153 --gcode 00004 --gdate 2026-05-14 --scenario yeongpung
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

_DEFAULT_SERVERS = ["remote_138", "remote_153", "remote_154", "remote_155"]

_GJISA_CANDIDATES_KYOBO = [
    "01|광화문점",
    "광화문점",
    "2|부곡리(매장)",
    "2.부곡리(매장)",
    "부곡리(매장)",
    "부곡리 (매장)",
]

_GJISA_CANDIDATES_YEONGPUNG = [
    "온라인",
    "온라인|온라인",
]


async def _count_where(
    server_id: str,
    *,
    where_sql: str,
    params: tuple[Any, ...],
) -> int:
    from app.core.db import execute_query

    sql = f"SELECT COUNT(*) AS c FROM S1_Ssub WHERE {where_sql}"
    rows = await execute_query(server_id, sql, params)
    return int((rows[0] or {}).get("c") or 0)


async def _count_modern_list(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    gjisa: str,
    hcode: str | None,
) -> dict[str, Any]:
    from app.services.transactions_service import _build_sales_statement_list_where

    where_sql, params = await _build_sales_statement_list_where(
        server_id=server_id,
        date_from=gdate,
        date_to=gdate,
        hcode=hcode,
        gcode=gcode,
        gubun=gubun,
        gjisa=gjisa,
        jubun=jubun,
    )
    return {
        "where": where_sql,
        "params": list(params),
        "count": await _count_where(server_id, where_sql=where_sql, params=tuple(params)),
    }


async def _count_for_gjisa(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    gjisa: str,
    hcode: str | None = None,
    scode_x: bool = False,
) -> dict[str, Any]:
    from app.core.db import execute_query
    from app.services.h2_gbun_adapt import (
        gcode_lookup_variants,
        gjisa_lookup_variants,
        jubun_lookup_variants,
        sales_statement_ocode_sql,
        sql_in_clause,
    )
    from app.services.transactions_service import _normalize_gdate

    g = _normalize_gdate(gdate)
    where = ["Gdate=%s", "Gubun=%s", sales_statement_ocode_sql(server_id)]
    params: list[Any] = [g, gubun]
    j_clause, j_params = sql_in_clause("COALESCE(Jubun,'')", jubun_lookup_variants(jubun))
    where.append(j_clause)
    params.extend(j_params)
    if scode_x:
        where.append("Scode='X'")
    g_clause, g_params = sql_in_clause("Gcode", gcode_lookup_variants(gcode))
    where.append(g_clause)
    params.extend(g_params)
    if hcode is not None:
        where.append("Hcode=%s")
        params.append(hcode)
    if gjisa:
        clause, jp = sql_in_clause("COALESCE(Gjisa,'')", gjisa_lookup_variants(gjisa))
        where.append(clause)
        params.extend(jp)
    sql = f"SELECT COUNT(*) AS c FROM S1_Ssub WHERE {' AND '.join(where)}"
    rows = await execute_query(server_id, sql, tuple(params))
    return {"gjisa_filter": gjisa, "hcode": hcode, "scode_x": scode_x, "count": int((rows[0] or {}).get("c") or 0)}


async def _distinct_gjisa(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    hcode: str | None = None,
) -> list[str]:
    from app.core.db import execute_query
    from app.services.h2_gbun_adapt import (
        gcode_lookup_variants,
        jubun_lookup_variants,
        sales_statement_ocode_sql,
        sql_in_clause,
    )
    from app.services.transactions_service import _normalize_gdate

    g = _normalize_gdate(gdate)
    where = ["Gdate=%s", "Gubun=%s", sales_statement_ocode_sql(server_id), "Scode='X'"]
    params: list[Any] = [g, gubun]
    if hcode:
        where.append("Hcode=%s")
        params.append(hcode)
    j_clause, j_params = sql_in_clause("COALESCE(Jubun,'')", jubun_lookup_variants(jubun))
    where.append(j_clause)
    params.extend(j_params)
    g_clause, g_params = sql_in_clause("Gcode", gcode_lookup_variants(gcode))
    where.append(g_clause)
    params.extend(g_params)
    sql = (
        f"SELECT DISTINCT COALESCE(Gjisa,'') AS gjisa FROM S1_Ssub WHERE {' AND '.join(where)} "
        "ORDER BY gjisa LIMIT 50"
    )
    rows = await execute_query(server_id, sql, tuple(params))
    return [_safe(r.get("gjisa")) for r in rows]


def _safe(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, bytes):
        return v.decode("euc-kr", errors="replace")
    return str(v).strip()


async def _parity_matrix(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    gjisa: str,
    jwt_hcode: str,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    async def add(label: str, **kwargs: Any) -> None:
        ju = kwargs.pop("jubun", jubun)
        row = await _count_for_gjisa(
            server_id, gdate=gdate, gcode=gcode, gubun=gubun, jubun=ju, **kwargs
        )
        row["label"] = label
        rows.append(row)

    await add("legacy_exact_jubun_gjisa", gjisa=gjisa, scode_x=True, hcode="")
    await add("jubun_unpadded_1", gjisa=gjisa, jubun="1", scode_x=True, hcode="")
    await add("jwt_hcode_only", gjisa=gjisa, scode_x=True, hcode=jwt_hcode)
    await add("no_scode", gjisa=gjisa, jubun=jubun, scode_x=False, hcode="")
    modern = await _count_modern_list(
        server_id,
        gdate=gdate,
        gcode=gcode,
        gubun=gubun,
        jubun=jubun,
        gjisa=gjisa,
        hcode=None,
    )
    modern_jwt = await _count_modern_list(
        server_id,
        gdate=gdate,
        gcode=gcode,
        gubun=gubun,
        jubun=jubun,
        gjisa=gjisa,
        hcode=jwt_hcode,
    )
    return {
        "matrix": rows,
        "modern_no_hcode": modern,
        "modern_jwt_hcode": modern_jwt,
    }


async def _probe_server(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    candidates: list[str],
    jwt_hcode: str,
    run_matrix: bool,
) -> dict[str, Any]:
    from app.services.h2_gbun_adapt import gjisa_lookup_variants

    info: dict[str, Any] = {"server_id": server_id, "ok": True}
    try:
        distinct = await _distinct_gjisa(
            server_id,
            gdate=gdate,
            gcode=gcode,
            gubun=gubun,
            jubun=jubun,
            hcode=jwt_hcode or None,
        )
        info["distinct_gjisa"] = distinct
        counts = []
        for cand in candidates:
            expanded = gjisa_lookup_variants(cand)
            row = await _count_for_gjisa(
                server_id,
                gdate=gdate,
                gcode=gcode,
                gubun=gubun,
                jubun=jubun,
                gjisa=cand,
                scode_x=True,
                hcode="",
            )
            row["variants"] = list(expanded)
            counts.append(row)
        info["candidate_counts"] = counts
        if run_matrix:
            info["parity"] = await _parity_matrix(
                server_id,
                gdate=gdate,
                gcode=gcode,
                gubun=gubun,
                jubun=jubun,
                gjisa=candidates[0] if candidates else "",
                jwt_hcode=jwt_hcode,
            )
    except Exception as e:  # noqa: BLE001
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return info


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--server", action="append", dest="servers", default=None)
    p.add_argument("--gcode", default="00004")
    p.add_argument("--gdate", default="2026-05-14")
    p.add_argument("--gubun", default="출고")
    p.add_argument("--jubun", default="00001")
    p.add_argument("--jwt-hcode", default="5019", help="T2_PUB scope hcode for parity matrix")
    p.add_argument("--scenario", choices=["kyobo", "yeongpung", "custom"], default="yeongpung")
    p.add_argument("--candidates", default=None)
    p.add_argument("--matrix", action="store_true", help="Run hcode/jubun/scode parity matrix")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()

    if args.candidates:
        candidates = [c.strip() for c in args.candidates.split(",") if c.strip()]
    elif args.scenario == "kyobo":
        candidates = list(_GJISA_CANDIDATES_KYOBO)
    else:
        candidates = list(_GJISA_CANDIDATES_YEONGPUNG)

    servers = args.servers or _DEFAULT_SERVERS
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gcode": args.gcode,
        "gdate": args.gdate,
        "gubun": args.gubun,
        "jubun": args.jubun,
        "scenario": args.scenario,
        "servers": {},
    }

    for sid in servers:
        report["servers"][sid] = await _probe_server(
            sid,
            gdate=args.gdate,
            gcode=args.gcode,
            gubun=args.gubun,
            jubun=args.jubun,
            candidates=candidates,
            jwt_hcode=args.jwt_hcode,
            run_matrix=args.matrix or args.scenario == "yeongpung",
        )

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
