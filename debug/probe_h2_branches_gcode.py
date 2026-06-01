#!/usr/bin/env python3
"""H2_Gbun 지사 — gcode 표기(00001 vs 1)별 branches total 진단.

교보문고 등 G1_Ggeo 는 zero-pad, H2_Gbun 은 선행 0 제거 키로 저장된 테넌트에서
`GET /masters/customer/{gcode}/branches` 가 0건인지 비교한다.

사용:
  PYTHONPATH=도서물류관리프로그램/backend \\
    python3 debug/probe_h2_branches_gcode.py \\
      --server remote_153 --gcodes 00001,1 \\
      --out analysis/audit/h2-branches-gcode.json
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


async def _probe_gcode(server_id: str, gcode: str, scope_hcode: str | None) -> dict[str, Any]:
    from app.services import masters_service
    from app.services.h2_gbun_adapt import gcode_lookup_variants

    info: dict[str, Any] = {
        "server_id": server_id,
        "gcode": gcode,
        "variants": list(gcode_lookup_variants(gcode)),
    }
    try:
        res = await masters_service.list_customer_branches(
            server_id=server_id,
            gcode=gcode,
            limit=5,
            offset=0,
            scope_hcode=scope_hcode,
        )
        total = int((res.get("page") or {}).get("total") or 0)
        items = res.get("items") or []
        info["ok"] = True
        info["total"] = total
        info["sample"] = [
            {"id": it.get("id"), "gjisa_value": it.get("gjisa_value"), "gcode": it.get("gcode")}
            for it in items[:3]
        ]
    except Exception as e:  # noqa: BLE001
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return info


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--server", action="append", dest="servers", default=None)
    p.add_argument("--gcodes", default="00001,1", help="comma-separated gcode candidates")
    p.add_argument("--scope-hcode", default=None, help="JWT publisher hcode for 2nd Hcode fallback")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()

    servers = args.servers or _DEFAULT_SERVERS
    gcodes = [g.strip() for g in args.gcodes.split(",") if g.strip()]
    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gcodes": gcodes,
        "scope_hcode": args.scope_hcode,
        "servers": {},
    }

    for sid in servers:
        report["servers"][sid] = []
        for gc in gcodes:
            report["servers"][sid].append(
                await _probe_gcode(sid, gc, args.scope_hcode)
            )

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)

    mismatches = []
    for sid, rows in report["servers"].items():
        totals = {r["gcode"]: r.get("total") for r in rows if r.get("ok")}
        if len(totals) >= 2 and len(set(totals.values())) > 1:
            mismatches.append((sid, totals))
    if mismatches:
        print("NOTE: same customer different totals across gcode strings:", mismatches, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
