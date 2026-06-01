#!/usr/bin/env python3
"""S1_Ssub 거래명세서 — Gjisa 표기별 LIST COUNT 진단.

교보문고(00001)·당일·출고·전표 등 고정 조건에서 ``DISTINCT Gjisa`` 와
``gjisa_lookup_variants`` 후보별 행 수를 비교한다 (광화문점·부곡리 매장).

사용:
  PYTHONPATH=도서물류관리프로그램/backend \\
    python3 debug/probe_sales_statement_list_gjisa.py \\
      --server remote_153 --gcode 00001 --gdate 2026-05-14
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

_GJISA_CANDIDATES = [
    "01|광화문점",
    "광화문점",
    "2|부곡리(매장)",
    "2.부곡리(매장)",
    "부곡리(매장)",
    "부곡리 (매장)",
]


async def _count_for_gjisa(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    gjisa: str,
) -> dict[str, Any]:
    from app.core.db import execute_query
    from app.services.h2_gbun_adapt import gcode_lookup_variants, sql_in_clause
    from app.services.transactions_service import _normalize_gdate

    g = _normalize_gdate(gdate)
    where = ["Gdate=%s", "Gubun=%s", "COALESCE(Jubun,'')=%s", "Ocode='B'"]
    params: list[Any] = [g, gubun, jubun]
    g_clause, g_params = sql_in_clause("Gcode", gcode_lookup_variants(gcode))
    where.append(g_clause)
    params.extend(g_params)
    if gjisa:
        from app.services.h2_gbun_adapt import gjisa_lookup_variants

        clause, jp = sql_in_clause("COALESCE(Gjisa,'')", gjisa_lookup_variants(gjisa))
        where.append(clause)
        params.extend(jp)
    sql = f"SELECT COUNT(*) AS c FROM S1_Ssub WHERE {' AND '.join(where)}"
    rows = await execute_query(server_id, sql, tuple(params))
    return {"gjisa_filter": gjisa, "count": int((rows[0] or {}).get("c") or 0)}


async def _distinct_gjisa(
    server_id: str, *, gdate: str, gcode: str, gubun: str, jubun: str
) -> list[str]:
    from app.core.db import execute_query
    from app.services.h2_gbun_adapt import gcode_lookup_variants, sql_in_clause
    from app.services.transactions_service import _normalize_gdate

    g = _normalize_gdate(gdate)
    where = ["Gdate=%s", "Gubun=%s", "COALESCE(Jubun,'')=%s", "Ocode='B'"]
    params: list[Any] = [g, gubun, jubun]
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


async def _probe_server(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    jubun: str,
    candidates: list[str],
) -> dict[str, Any]:
    from app.services.h2_gbun_adapt import gjisa_lookup_variants

    info: dict[str, Any] = {"server_id": server_id, "ok": True}
    try:
        distinct = await _distinct_gjisa(
            server_id, gdate=gdate, gcode=gcode, gubun=gubun, jubun=jubun
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
            )
            row["variants"] = list(expanded)
            counts.append(row)
        info["candidate_counts"] = counts
    except Exception as e:  # noqa: BLE001
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return info


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--server", action="append", dest="servers", default=None)
    p.add_argument("--gcode", default="00001")
    p.add_argument("--gdate", default="2026-05-14")
    p.add_argument("--gubun", default="출고")
    p.add_argument("--jubun", default="00001")
    p.add_argument("--candidates", default=",".join(_GJISA_CANDIDATES))
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()

    servers = args.servers or _DEFAULT_SERVERS
    candidates = [c.strip() for c in args.candidates.split(",") if c.strip()]
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gcode": args.gcode,
        "gdate": args.gdate,
        "gubun": args.gubun,
        "jubun": args.jubun,
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
