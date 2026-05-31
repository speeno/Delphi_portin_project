#!/usr/bin/env python3
"""거래처(Sobo11) 거래처구분 표시 정합 — 4서버 라이브 점검.

`get_customer_master` 가 G1_Gbun 조인명을 올바르게 반환하는지 확인한다.
기본 샘플: gcode 00039 (한가람문고), --q 로 이름 검색 후 첫 건 상세.

사용:
  PYTHONPATH=도서물류관리프로그램/backend \\
    python3 debug/probe_customer_gbun_display.py \\
      --gcode 00039 --out analysis/audit/sobo11-gbun-display.json
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


async def _probe_one(
    server_id: str,
    gcode: str | None,
    q: str | None,
) -> dict[str, Any]:
    from app.services import masters_service

    info: dict[str, Any] = {"server_id": server_id}
    try:
        target = gcode
        if not target and q:
            res = await masters_service.list_customer_master(
                server_id=server_id, q=q, limit=5, offset=0
            )
            items = res.get("items") or []
            if items:
                target = str(items[0].get("gcode") or "")
                info["list_sample"] = [
                    {"gcode": it.get("gcode"), "gname": it.get("gname")} for it in items[:3]
                ]
        if not target:
            info["ok"] = False
            info["error"] = "no gcode"
            return info

        detail = await masters_service.get_customer_master(server_id=server_id, gcode=target)
        if detail is None:
            info["ok"] = False
            info["error"] = "not found"
            return info

        cats = await masters_service.list_customer_categories(server_id=server_id, limit=500)
        cat_names = {str(c.get("gname") or "") for c in cats.get("items") or []}

        info["ok"] = True
        info["gcode"] = target
        info["gname"] = detail.get("gname")
        info["gubun"] = detail.get("gubun")
        info["gbun_name"] = detail.get("gbun_name")
        info["gbun_orphan"] = detail.get("gbun_orphan")
        info["gbun_legacy_sname"] = detail.get("gbun_legacy_sname")
        info["gbun_name_in_master"] = detail.get("gbun_name") in cat_names if detail.get("gbun_name") else None
        info["category_count"] = len(cats.get("items") or [])
    except Exception as e:  # noqa: BLE001
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return info


async def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--servers", nargs="*", default=_DEFAULT_SERVERS)
    p.add_argument("--gcode", default="00039")
    p.add_argument("--q", default=None, help="gcode 없을 때 목록 검색어")
    p.add_argument("--out", default="analysis/audit/sobo11-gbun-display.json")
    args = p.parse_args()

    results = []
    for sid in args.servers:
        results.append(await _probe_one(sid, args.gcode or None, args.q))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gcode": args.gcode,
        "q": args.q,
        "servers": results,
    }
    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    failed = [r for r in results if not r.get("ok")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
