#!/usr/bin/env python3
"""
servers.yaml 의 모든 서버에 대해:
  1) T5_Ssub 컬럼 목록 (스키마 차이 확인)
  2) cash_service.list_cash / settlement_service.cash_status 스모크 실행

실행 (저장소 루트 또는 본 디렉터리에서):

  PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_settlement_t5_all_servers.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.config import get_server_profiles  # noqa: E402
from app.core.db import execute_query  # noqa: E402
from app.services import cash_service, settlement_service  # noqa: E402
from app.services.t5_ssub_adapt import clear_t5_column_cache_for_tests  # noqa: E402


async def probe_one(sid: str) -> dict:
    row: dict = {
        "id": sid,
        "t5_columns": None,
        "flags": None,
        "list_cash": None,
        "cash_status_hcode": None,
        "cash_status_sdate": None,
        "error": None,
    }
    try:
        desc = await execute_query(sid, "SHOW COLUMNS FROM T5_Ssub", ())
        cols = {str(r.get("Field") or "").lower() for r in desc}
        row["t5_columns"] = sorted(cols)
        row["flags"] = {
            "sdate": "sdate" in cols,
            "jubun": "jubun" in cols,
            "yesno": "yesno" in cols,
            "id_col": "id" in cols,
            "check_col": "check" in cols,
        }
        items, total = await cash_service.list_cash(
            server_id=sid,
            date_from="2026.01.01",
            date_to="2026.12.31",
            hcode=None,
            include_cancelled=False,
            limit=5,
            offset=0,
        )
        row["list_cash"] = {"ok": True, "total": total, "returned": len(items)}
        cs = await settlement_service.cash_status(
            server_id=sid,
            variant="hcode",
            month="202601",
            hcode=None,
            limit=5,
            offset=0,
        )
        row["cash_status_hcode"] = {
            "ok": True,
            "total_count": cs.get("total_count"),
            "returned": len(cs.get("items", [])),
        }
        cs_sd = await settlement_service.cash_status(
            server_id=sid,
            variant="sdate",
            month="202601",
            hcode=None,
            limit=5,
            offset=0,
        )
        row["cash_status_sdate"] = {
            "ok": True,
            "total_count": cs_sd.get("total_count"),
            "returned": len(cs_sd.get("items", [])),
        }
    except Exception as exc:  # noqa: BLE001
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


async def main() -> None:
    clear_t5_column_cache_for_tests()
    profiles = get_server_profiles()
    ids = sorted({(p.get("id") or "").strip() for p in profiles if p.get("id")})
    print(f"대상 서버 {len(ids)}대: {', '.join(ids)}\n")

    results: list[dict] = []
    for sid in ids:
        results.append(await probe_one(sid))

    for r in results:
        sid = r["id"]
        print(f"=== {sid} ===")
        if r["error"]:
            print(f"  실패: {r['error']}")
            continue
        print(f"  T5 플래그: {r['flags']}")
        print(f"  list_cash: {r['list_cash']}")
        print(f"  cash_status[hcode]: {r['cash_status_hcode']}")
        print(f"  cash_status[sdate]: {r['cash_status_sdate']}")
        print(f"  컬럼 수: {len(r['t5_columns'] or [])}")
        print()

    ok = sum(1 for r in results if not r.get("error"))
    print(f"요약: 성공 {ok}/{len(results)}대")


if __name__ == "__main__":
    asyncio.run(main())
