#!/usr/bin/env python3
"""저자(Sobo13·G3_Gjeo) "김" 검색 4서버 라이브 정합 점검.

목적
----
- `remote_138/153/154/155` 4서버에서 `masters_service.list_authors(q="김")` 가
  500/SQL(1064/1054) 회귀 없이 동작하고, 레거시 기대(코드 오름차순 정렬·저자명 노출)와
  맞는지 수치로 드러낸다 (multi-db-compat 룰 DoD: L4 매트릭스 GET 성공).
- 검색 결과 1건 이상이면 `get_author` 상세 조회가 성공하고 본 폼 필드가 빈 문자열
  fallback 으로 일관 동작하는지 확인한다.

앱과 동일 경로(`masters_service`)를 직접 호출 → 서버별 풀·MySQL 3.23 어댑터 재사용.
라이브 DB 필요 — CI 자동 실행 X. 운영자가 read-only 자격 환경에서 수동 실행.

사용
----
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/probe_author_kim_search.py \
            --servers remote_138 remote_153 remote_154 remote_155 \
            --q 김 --out analysis/audit/sobo13-author-kim-4server.json
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
# 저자 본 폼(Panel002) 핵심 필드 — 상세 fallback 일관성 확인용.
_DETAIL_FIELDS = (
    "gposa", "gname", "gubun", "gbun_name", "date1", "gjice", "gnumb",
    "gnum1", "gscho", "gnum2", "gtel1", "gtel2", "gfax1", "gfax2",
    "gpost", "opost", "gadd1", "gadd2", "oadd1", "oadd2", "gbigo",
)


def _is_sorted_by_gcode(items: list[dict[str, Any]]) -> bool:
    codes = [str(it.get("gcode") or "") for it in items]
    return codes == sorted(codes)


async def _probe_one(server_id: str, q: str, limit: int) -> dict[str, Any]:
    from app import services  # noqa: F401  (ensure package import)
    from app.services import masters_service

    info: dict[str, Any] = {"server_id": server_id, "q": q}
    try:
        res = await masters_service.list_authors(server_id=server_id, q=q, limit=limit, offset=0)
    except Exception as e:  # noqa: BLE001
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
        return info

    items = res.get("items", [])
    info["ok"] = True
    info["total"] = (res.get("page") or {}).get("total")
    info["returned"] = len(items)
    info["sorted_by_gcode"] = _is_sorted_by_gcode(items)
    info["all_have_gname"] = all(bool(str(it.get("gname") or "").strip()) for it in items) if items else None
    info["sample"] = [
        {"gcode": it.get("gcode"), "gname": it.get("gname"), "hcode": it.get("hcode")}
        for it in items[:5]
    ]

    # 상세 조회 일관성 — 첫 결과 1건.
    if items:
        gcode = str(items[0].get("gcode") or "")
        try:
            detail = await masters_service.get_author(server_id=server_id, gcode=gcode)
            if detail is None:
                info["detail_ok"] = False
                info["detail_note"] = f"get_author({gcode}) returned None"
            else:
                missing = [f for f in _DETAIL_FIELDS if f not in detail]
                info["detail_ok"] = not missing
                info["detail_gcode"] = gcode
                info["detail_missing_fields"] = missing
                info["detail_gposa"] = detail.get("gposa")
                info["detail_gbun_name"] = detail.get("gbun_name")
        except Exception as e:  # noqa: BLE001
            info["detail_ok"] = False
            info["detail_error"] = f"{type(e).__name__}: {e}"
    else:
        info["detail_ok"] = None
        info["detail_note"] = "no items to drill into"
    return info


async def _run(servers: list[str], q: str, limit: int) -> dict[str, Any]:
    out: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "screen": "Sobo13",
        "table": "G3_Gjeo",
        "q": q,
        "servers": {},
    }
    for sid in servers:
        out["servers"][sid] = await _probe_one(sid, q, limit)
    oks = [v for v in out["servers"].values() if v.get("ok")]
    out["summary"] = {
        "server_count": len(servers),
        "list_ok": len(oks),
        "list_failed": len(servers) - len(oks),
        "all_sorted": all(v.get("sorted_by_gcode") for v in oks) if oks else None,
        "detail_ok": sum(1 for v in oks if v.get("detail_ok") is True),
    }
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    p.add_argument("--servers", nargs="+", default=_DEFAULT_SERVERS)
    p.add_argument("--q", default="김", help='검색어 (기본 "김")')
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--out", default="/tmp/sobo13-author-kim-4server.json")
    args = p.parse_args(argv)

    async def _run_and_cleanup():
        try:
            return await _run(args.servers, args.q, args.limit)
        finally:
            try:
                from app.core.db import close_all_pools
                await close_all_pools()
            except Exception:  # noqa: BLE001
                pass

    try:
        report = asyncio.run(_run_and_cleanup())
    except Exception as e:  # noqa: BLE001
        print(f"[ERR] live query failed: {type(e).__name__}: {e}", file=sys.stderr)
        print("  (라이브 DB 접근/자격증명이 필요합니다 — read-only 환경에서 실행)", file=sys.stderr)
        return 2

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {args.out}")
    for sid, info in report["servers"].items():
        if info.get("ok"):
            print(
                f"  {sid}: returned={info.get('returned')} total={info.get('total')} "
                f"sorted={info.get('sorted_by_gcode')} detail_ok={info.get('detail_ok')}"
            )
        else:
            print(f"  {sid}: LIST FAILED — {info.get('error')}")
    s = report["summary"]
    print(f"  summary: list_ok={s['list_ok']}/{s['server_count']} detail_ok={s['detail_ok']} all_sorted={s['all_sorted']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
