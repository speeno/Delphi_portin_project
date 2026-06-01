#!/usr/bin/env python3
"""거래명세서 Label104 — PrinJing live probe (DEC-064)."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.prinjing_service import compute_warehouse_stock_qty  # noqa: E402


async def main() -> None:
    p = argparse.ArgumentParser(description="PrinJing stock probe")
    p.add_argument("--server", default="remote_153")
    p.add_argument("--hcode", required=True)
    p.add_argument("--bcode", required=True)
    p.add_argument("--ocode", default="B")
    args = p.parse_args()
    qty = await compute_warehouse_stock_qty(
        args.server,
        ocode=args.ocode,
        bcode=args.bcode,
        hcode=args.hcode,
    )
    print(f"server={args.server} hcode={args.hcode} bcode={args.bcode} stock_qty={qty}")


if __name__ == "__main__":
    asyncio.run(main())
