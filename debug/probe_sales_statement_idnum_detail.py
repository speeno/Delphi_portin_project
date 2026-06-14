#!/usr/bin/env python3
"""Sobo21 Idnum + 상세 라인 진단 — 교문서-경리부(00405) 시나리오.

DEC-064 §Idnum 정합 회귀: LIST ``order_key.idnum`` surface 와 detail 라인 수를
레거시(전표번호 00001, 4 book lines) 와 대조한다.

사용:
  PYTHONPATH=도서물류관리프로그램/backend \\
    python3 debug/probe_sales_statement_idnum_detail.py \\
      --server remote_153 --hcode 5019
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

_DEFAULT_GDATE = "2026-06-04"
_DEFAULT_GCODE = "00405"
_DEFAULT_GUBUN = "출고"
_DEFAULT_HCODE = "5019"


def _row_keys_sample(row: dict[str, Any]) -> dict[str, Any]:
    """Idnum/stmt_gcode 관련 키만 추출."""
    out: dict[str, Any] = {}
    for k, v in row.items():
        kl = str(k).lower()
        if kl in ("idnum", "stmt_gcode", "gcode", "jubun", "hcode", "gdate", "gubun"):
            out[str(k)] = v
    return out


async def _raw_grouped_row(
    server_id: str,
    *,
    gdate: str,
    gcode: str,
    gubun: str,
    hcode: str | None,
) -> dict[str, Any]:
    from app.core.db import execute_query
    from app.services.transactions_service import (
        _build_sales_statement_list_where,
        _group_by_stmt_keys,
        _select_stmt_group_keys,
    )

    where_sql, params = await _build_sales_statement_list_where(
        server_id=server_id,
        date_from=gdate,
        date_to=gdate,
        hcode=hcode,
        gcode=gcode,
        gubun=gubun,
    )
    group_by = await _group_by_stmt_keys(server_id)
    select_keys = await _select_stmt_group_keys(server_id)
    sql = (
        f"SELECT {select_keys}, COUNT(*) AS row_count "
        f"FROM S1_Ssub WHERE {where_sql} "
        f"GROUP BY {group_by} "
        "ORDER BY Gdate DESC LIMIT 3"
    )
    rows = await execute_query(server_id, sql, tuple(params))
    return {
        "sql": sql,
        "params": list(params),
        "row_count": len(rows),
        "rows": [_row_keys_sample(dict(r)) for r in rows],
        "first_row_all_keys": list(rows[0].keys()) if rows else [],
    }


async def run_probe(
    *,
    server_id: str,
    gdate: str,
    gcode: str,
    gubun: str,
    hcode: str | None,
    idnum: int | None,
) -> dict[str, Any]:
    from app.services import transactions_service as svc

    out: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "server_id": server_id,
        "input": {
            "gdate": gdate,
            "gcode": gcode,
            "gubun": gubun,
            "hcode": hcode,
            "idnum_filter": idnum,
        },
    }

    try:
        items, total = await svc.list_sales_statements(
            server_id=server_id,
            hcode=hcode,
            date_from=gdate,
            date_to=gdate,
            gcode=gcode,
            gubun=gubun,
            idnum=idnum,
            limit=5,
            offset=0,
        )
        out["list"] = {
            "total": total,
            "items": [
                {
                    "order_key": it.get("order_key"),
                    "row_count": it.get("row_count"),
                    "customer_name": it.get("customer_name"),
                }
                for it in items
            ],
        }
    except Exception as exc:
        out["list_error"] = f"{type(exc).__name__}: {exc}"

    try:
        out["raw_grouped"] = await _raw_grouped_row(
            server_id,
            gdate=gdate,
            gcode=gcode,
            gubun=gubun,
            hcode=hcode,
        )
    except Exception as exc:
        out["raw_grouped_error"] = f"{type(exc).__name__}: {exc}"

    items = out.get("list", {}).get("items") or []
    if items:
        ok = items[0].get("order_key") or {}
        try:
            detail = await svc.get_sales_statement_detail(
                server_id=server_id,
                gdate=str(ok.get("gdate", "")),
                hcode=str(ok.get("hcode", "")),
                jubun=str(ok.get("jubun", "")),
                gjisa=str(ok.get("gjisa", "")),
                idnum=ok.get("idnum") or None,
                gubun=str(ok.get("gubun", "")) or None,
                gcode=str(ok.get("gcode", "")) or None,
            )
            if detail:
                out["detail"] = {
                    "slip_no": detail.get("slip_no"),
                    "order_key": detail.get("order_key"),
                    "line_count": len(detail.get("lines") or []),
                    "bcodes": [ln.get("bcode") for ln in (detail.get("lines") or [])],
                }
            else:
                out["detail"] = None
        except Exception as exc:
            out["detail_error"] = f"{type(exc).__name__}: {exc}"

    if idnum is None:
        try:
            items_id, total_id = await svc.list_sales_statements(
                server_id=server_id,
                hcode=hcode,
                date_from=gdate,
                date_to=gdate,
                idnum=1,
                limit=5,
                offset=0,
            )
            out["list_idnum_1"] = {
                "total": total_id,
                "items": [it.get("order_key") for it in items_id],
            }
        except Exception as exc:
            out["list_idnum_1_error"] = f"{type(exc).__name__}: {exc}"

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Sobo21 Idnum/detail probe")
    parser.add_argument("--server", default="remote_153")
    parser.add_argument("--gdate", default=_DEFAULT_GDATE)
    parser.add_argument("--gcode", default=_DEFAULT_GCODE)
    parser.add_argument("--gubun", default=_DEFAULT_GUBUN)
    parser.add_argument("--hcode", default=_DEFAULT_HCODE)
    parser.add_argument("--idnum", type=int, default=None)
    args = parser.parse_args()
    hcode = (args.hcode or "").strip() or None
    result = asyncio.run(
        run_probe(
            server_id=args.server,
            gdate=args.gdate,
            gcode=args.gcode,
            gubun=args.gubun,
            hcode=hcode,
            idnum=args.idnum,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
