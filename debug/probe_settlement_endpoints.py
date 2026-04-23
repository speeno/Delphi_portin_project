#!/usr/bin/env python3
"""정산 7화면 endpoint 라이브 probe — DEC-058 Wave A 후속 (admin 권한 회복).

목적
----
정산 메뉴의 모든 화면(7개)이 admin 토큰으로 200 OK 인지 확인하고,
실패하는 endpoint 의 정확한 detail (Pydantic / SettlementValidationError /
DB syntax / 컬럼 부재 등) 을 한눈에 식별한다.

호출 방식
---------
서비스 함수를 직접 호출 (FastAPI/JWT 우회). DEC-058 분기 0 적용 *전에는*
admin 토큰 발급에 분기 3 (Id_Logn Fxx) 가 간섭하여 권한 누락 가능성이
있으므로, probe 는 라우터를 거치지 않고 service 함수만 호출한다.

실행 (저장소 루트):

  PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_settlement_endpoints.py
  PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_settlement_endpoints.py --month 202604

옵션:
  --month YYYYMM    : 기준월 (default: 202604)
  --servers a,b,c   : 대상 서버 ID 콤마 구분 (default: servers.yaml 전체)
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import traceback
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.config import get_server_profiles  # noqa: E402
from app.services import (  # noqa: E402
    cash_service,
    settlement_service,
    tax_invoice_service,
)


# 정산 7화면 ↔ service 함수 매핑
ENDPOINTS = [
    "billing",            # GET /api/v1/settlement/billing
    "billing_period",     # GET /api/v1/settlement/billing/period (list_period_summary)
    "cash",               # GET /api/v1/settlement/cash
    "cash_status_hcode",  # GET /api/v1/settlement/cash-status?variant=hcode
    "cash_status_sdate",  # GET /api/v1/settlement/cash-status?variant=sdate
    "outstanding",        # GET /api/v1/settlement/outstanding (compute_outstanding_by_customer)
    "tax_invoice",        # GET /api/v1/settlement/tax-invoice
]


async def _call_one(name: str, server_id: str, month: str) -> dict[str, Any]:
    """단일 endpoint 를 호출하고 결과/에러를 dict 로 반환."""
    out: dict[str, Any] = {
        "name": name, "ok": False, "items": None, "total": None, "error": None,
    }
    try:
        if name == "billing":
            items, total = await settlement_service.list_billing(
                server_id=server_id, month_from=month, month_to=month,
                hcode=None, variant="standard",
                include_cancelled=False, limit=10, offset=0,
            )
            out.update(items=len(items), total=total)
        elif name == "billing_period":
            res = await settlement_service.list_period_summary(
                server_id=server_id, month_from=month, month_to=month,
                hcode=None, limit=10, offset=0,
            )
            out.update(items=len(res.get("items", [])), total=res.get("total"))
        elif name == "cash":
            items, total = await cash_service.list_cash(
                server_id=server_id,
                date_from=f"{month[:4]}.{month[4:6]}.01",
                date_to=f"{month[:4]}.{month[4:6]}.28",
                hcode=None, include_cancelled=False, limit=10, offset=0,
            )
            out.update(items=len(items), total=total)
        elif name == "cash_status_hcode":
            res = await settlement_service.cash_status(
                server_id=server_id, variant="hcode", month=month,
                hcode=None, limit=10, offset=0,
            )
            out.update(items=len(res.get("items", [])), total=res.get("total_count"))
        elif name == "cash_status_sdate":
            res = await settlement_service.cash_status(
                server_id=server_id, variant="sdate", month=month,
                hcode=None, limit=10, offset=0,
            )
            out.update(items=len(res.get("items", [])), total=res.get("total_count"))
        elif name == "outstanding":
            res = await settlement_service.compute_outstanding_by_customer(
                server_id=server_id, month_from=month, month_to=month,
                hcode=None, limit=10, offset=0,
            )
            out.update(items=len(res.get("items", [])), total=res.get("total_count"))
        elif name == "tax_invoice":
            res = await tax_invoice_service.list_tax_invoices(
                server_id=server_id, gdate=month, hcode=None, limit=10, offset=0,
            )
            out.update(items=len(res.get("items", [])), total=res.get("total_count"))
        else:
            out["error"] = f"unknown endpoint: {name}"
            return out
        out["ok"] = True
    except Exception as exc:  # noqa: BLE001
        tb_short = "\n".join(traceback.format_exception_only(type(exc), exc)).strip()
        out["error"] = tb_short
    return out


async def _probe_server(server_id: str, month: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name in ENDPOINTS:
        rows.append(await _call_one(name, server_id, month))
    return rows


def _print_table(server_id: str, rows: list[dict[str, Any]]) -> None:
    print(f"\n=== {server_id} ===")
    print(f"{'endpoint':<22} {'ok':<4} {'items':>6} {'total':>8}  detail")
    print("-" * 100)
    for r in rows:
        ok = "OK" if r["ok"] else "FAIL"
        items = "" if r["items"] is None else str(r["items"])
        total = "" if r["total"] is None else str(r["total"])
        detail = (r["error"] or "")[:80]
        print(f"{r['name']:<22} {ok:<4} {items:>6} {total:>8}  {detail}")


async def _amain(args: argparse.Namespace) -> int:
    if args.servers:
        ids = [s.strip() for s in args.servers.split(",") if s.strip()]
    else:
        profs = get_server_profiles()
        ids = sorted({(p.get("id") or "").strip() for p in profs if p.get("id")})
    print(f"대상 서버 {len(ids)}대: {', '.join(ids)}\n기준월: {args.month}")

    fail_counts: dict[str, int] = {n: 0 for n in ENDPOINTS}
    for sid in ids:
        rows = await _probe_server(sid, args.month)
        _print_table(sid, rows)
        for r in rows:
            if not r["ok"]:
                fail_counts[r["name"]] += 1

    total = len(ids)
    print("\n=== 요약 (FAIL 수 / 전체 서버) ===")
    for n in ENDPOINTS:
        fc = fail_counts[n]
        flag = "" if fc == 0 else "  ← FIX"
        print(f"  {n:<22}  {fc}/{total}{flag}")
    return 0 if all(v == 0 for v in fail_counts.values()) else 1


def main() -> int:
    p = argparse.ArgumentParser(description="정산 7화면 라이브 probe")
    p.add_argument("--month", default="202604", help="기준월 YYYYMM")
    p.add_argument("--servers", default="", help="콤마 구분 서버 ID")
    args = p.parse_args()
    return asyncio.run(_amain(args))


if __name__ == "__main__":
    sys.exit(main())
