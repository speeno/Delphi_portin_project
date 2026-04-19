#!/usr/bin/env python3
"""
백엔드 API — 전 DB 서버 연동 점검 (멀티 DB API 연동 점검 계획)

`servers.yaml` 에 등록된 모든 서버에 대해 4 단계 점검:

  L0  설정     — id / mysql3_protocol / ssh_tunnel / db
  L2  DB 추상화— SELECT 1 (execute_query 단일 진입점)
  L4r 라우터  — TestClient + JWT/dependency 우회로 GET 스모크
  R   리포팅  — 텍스트 + (선택) JSON

실행 (저장소 루트에서):

  PYTHONPATH=도서물류관리프로그램/backend \
    python3 debug/probe_backend_all_servers.py [--layer l2|l4|all] \
                                               [--write-json PATH] \
                                               [--include-cancelled] \
                                               [--month 202604] \
                                               [--date-from 2026.04.01 --date-to 2026.04.30]

성공 기준 (DoD)
---------------
- L2: 모든 서버 SELECT 1 성공.
- L4: 라우터 그룹별 최소 1 GET 이 모든 서버에서 200 (빈 목록 허용) 또는
      알려진 스키마 차이로 인한 500 의 경우 reason 분류.

CI 옵트인
---------
환경 변수 ``RUN_DB_SMOKE=1`` 일 때만 실제 네트워크 검증을 수행.
미설정 시 dry-run 모드 (어떤 라우터/서버를 검증하려 했는지만 인쇄).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from contextlib import suppress
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.config import get_server_profiles  # noqa: E402
from app.core.db import execute_query  # noqa: E402
from app.core.sql_mysql3 import mysql3_protocol  # noqa: E402


# ─────────────────────────────────────────────────────────────────────
# L0 — 설정 요약
# ─────────────────────────────────────────────────────────────────────
def summarize_profile(prof: dict[str, Any]) -> dict[str, Any]:
    """비밀 없이 정렬된 요약."""
    ssh = prof.get("ssh_tunnel") or {}
    return {
        "id": (prof.get("id") or "").strip(),
        "label": (prof.get("label") or "").strip(),
        "host": (prof.get("host") or "").strip(),
        "port": int(prof.get("port") or 0),
        "db": (prof.get("database") or prof.get("db") or "").strip(),
        "mysql3": bool(prof.get("mysql3_protocol")),
        "ssh": bool(ssh),
        "ssh_host": (ssh.get("host") or "").strip() if ssh else "",
    }


# ─────────────────────────────────────────────────────────────────────
# L2 — SELECT 1
# ─────────────────────────────────────────────────────────────────────
async def probe_select_one(server_id: str) -> dict[str, Any]:
    out: dict[str, Any] = {"layer": "L2", "ok": False, "detail": ""}
    try:
        rows = await execute_query(server_id, "SELECT 1 AS one", ())
        out["ok"] = True
        out["detail"] = f"rows={len(rows)} mysql3={mysql3_protocol(server_id)}"
    except Exception as exc:  # noqa: BLE001
        out["detail"] = f"{type(exc).__name__}: {exc}"
    return out


# ─────────────────────────────────────────────────────────────────────
# L4 — 라우터 GET 스모크 (TestClient + 의존성 우회)
# ─────────────────────────────────────────────────────────────────────
def _build_test_client():
    """FastAPI 앱을 import 하고 get_current_user 를 우회한다."""
    # 지연 import: PYTHONPATH 가 들어간 뒤에야 app 모듈을 찾을 수 있음.
    from fastapi.testclient import TestClient  # noqa: PLC0415

    from app.main import app  # noqa: PLC0415
    from app.routers.auth import get_current_user  # noqa: PLC0415

    async def _override() -> dict[str, str]:
        return {"user_id": "smoke", "server_id": "remote_1"}

    app.dependency_overrides[get_current_user] = _override
    return TestClient(app)


# 라우터 그룹별 최소 GET 매트릭스
# (group, path 또는 path_factory(server_id, args), accepted_status_set, expect_keys)
def _routes_for(server_id: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    sid = server_id
    df = args.date_from
    dt = args.date_to
    month = args.month
    return [
        {
            "group": "common.servers",
            "path": "/api/v1/servers",
            "ok_status": {200},
        },
        {
            "group": "common.health",
            "path": "/api/v1/health",
            "ok_status": {200},
        },
        {
            "group": "masters.customer",
            "path": f"/api/v1/masters/customer?serverId={sid}&limit=1",
            "ok_status": {200},
        },
        {
            "group": "masters.book",
            "path": f"/api/v1/masters/book?serverId={sid}&limit=1",
            "ok_status": {200},
        },
        {
            "group": "masters.publisher",
            "path": f"/api/v1/masters/publisher?serverId={sid}&limit=1",
            "ok_status": {200},
        },
        {
            "group": "outbound.orders",
            "path": (
                f"/api/v1/outbound/orders?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1"
            ),
            "ok_status": {200},
        },
        {
            "group": "inbound.receipts",
            "path": (
                f"/api/v1/inbound/receipts?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1"
            ),
            "ok_status": {200},
        },
        {
            "group": "returns.list",
            "path": (
                f"/api/v1/returns?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1"
            ),
            "ok_status": {200},
        },
        {
            "group": "settlement.cash",
            "path": (
                f"/api/v1/settlement/cash?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
        {
            "group": "settlement.cash_status_hcode",
            "path": (
                f"/api/v1/settlement/cash-status?serverId={sid}"
                f"&variant=hcode&month={month}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
        {
            "group": "settlement.cash_status_sdate",
            "path": (
                f"/api/v1/settlement/cash-status?serverId={sid}"
                f"&variant=sdate&month={month}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
        {
            "group": "settlement.billing",
            "path": (
                f"/api/v1/settlement/billing?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
        # ─── C5 Phase 2 (settlement_billing.yaml v1.1.0) ─────────────
        # 빈 결과(200)·서버측 잠재적 권한 거부(401·403) 모두 허용 — 본 매트릭스는 라우팅
        # 등록 여부와 SQL 호환성만 검증. 마감(423) 도 정책 통과로 분류한다.
        {
            "group": "settlement.tax_invoice",
            "path": (
                f"/api/v1/settlement/tax-invoice?serverId={sid}&gdate={month}"
            ),
            "ok_status": {200},
        },
        {
            "group": "settlement.audit_settlement",
            "path": (
                f"/api/v1/audit/settlement?serverId={sid}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
        {
            "group": "transactions.statement",
            "path": (
                f"/api/v1/transactions/sales-statement?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            "ok_status": {200},
        },
    ]


def probe_routes(client, server_id: str, args: argparse.Namespace) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for spec in _routes_for(server_id, args):
        path = spec["path"]
        try:
            res = client.get(path)
            ok = res.status_code in spec["ok_status"]
            detail = f"{res.status_code} bytes={len(res.content)}"
            if not ok:
                # 응답 body 의 머리만 함께 (서버 reason 분석에 도움).
                try:
                    head = res.text[:160].replace("\n", " ")
                except Exception:  # noqa: BLE001
                    head = ""
                detail = f"{detail} body~={head!r}"
            out.append({
                "layer": "L4",
                "group": spec["group"],
                "path": path,
                "ok": ok,
                "status": res.status_code,
                "detail": detail,
            })
        except Exception as exc:  # noqa: BLE001
            out.append({
                "layer": "L4",
                "group": spec["group"],
                "path": path,
                "ok": False,
                "status": 0,
                "detail": f"{type(exc).__name__}: {exc}",
            })
    return out


# ─────────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────────
async def run(args: argparse.Namespace) -> int:
    profiles = get_server_profiles()
    rows = [summarize_profile(p) for p in profiles if p.get("id")]
    rows = [r for r in rows if r["id"]]
    rows.sort(key=lambda r: r["id"])

    print(f"=== L0 설정 요약 ({len(rows)}대) ===")
    for r in rows:
        ssh_marker = "ssh" if r["ssh"] else "direct"
        flag = "mysql3" if r["mysql3"] else "mysql>=4"
        print(
            f"  - {r['id']:14s} db={r['db']:>8s} {ssh_marker} {flag} "
            f"label={r['label']!r}"
        )

    dry_run = os.environ.get("RUN_DB_SMOKE", "").strip() not in {"1", "true", "True"}
    if dry_run:
        print("\n[dry-run] RUN_DB_SMOKE=1 미설정 — 네트워크 검증 생략 (계획만 출력)")
        plan: list[dict[str, Any]] = []
        for r in rows:
            for spec in _routes_for(r["id"], args):
                plan.append({"server": r["id"], "group": spec["group"], "path": spec["path"]})
        for p in plan:
            print(f"  · {p['server']} {p['group']:34s} {p['path']}")
        if args.write_json:
            _write_json(
                args.write_json,
                {
                    "checkedAt": _utc_iso(),
                    "mode": "dry-run",
                    "servers": rows,
                    "planned_calls": plan,
                },
            )
        return 0

    # 실제 검증
    layers = args.layer
    results: dict[str, Any] = {
        "checkedAt": _utc_iso(),
        "mode": "live",
        "layer": layers,
        "servers": rows,
        "l2": {},
        "l4": {},
    }

    if layers in {"l2", "all"}:
        print("\n=== L2 SELECT 1 ===")
        for r in rows:
            res = await probe_select_one(r["id"])
            results["l2"][r["id"]] = res
            mark = "OK" if res["ok"] else "FAIL"
            print(f"  {mark:4s} {r['id']:14s} {res['detail']}")

    if layers in {"l4", "all"}:
        print("\n=== L4 라우터 GET 스모크 ===")
        client = _build_test_client()
        try:
            for r in rows:
                if layers == "l4" or results["l2"].get(r["id"], {}).get("ok", True):
                    rs = probe_routes(client, r["id"], args)
                else:
                    rs = [{
                        "layer": "L4", "group": "skipped",
                        "path": "", "ok": False, "status": 0,
                        "detail": "L2 SELECT 1 실패로 인해 라우터 스모크 생략",
                    }]
                results["l4"][r["id"]] = rs
                ok = sum(1 for x in rs if x["ok"])
                print(f"  {r['id']:14s} {ok}/{len(rs)} OK")
                for x in rs:
                    mark = "OK" if x["ok"] else "FAIL"
                    print(f"    {mark:4s} {x['group']:34s} {x['detail']}")
        finally:
            with suppress(Exception):
                client.close()

    # DoD 요약
    l2_ok = all(v.get("ok") for v in results["l2"].values()) if results["l2"] else True
    l4_total = sum(len(v) for v in results["l4"].values())
    l4_ok = sum(1 for v in results["l4"].values() for x in v if x["ok"])
    print(
        f"\n=== 요약 === L2 모두성공={l2_ok}  "
        f"L4 OK={l4_ok}/{l4_total}"
    )

    if args.write_json:
        _write_json(args.write_json, results)

    failed = (not l2_ok) or (l4_total and l4_ok < l4_total)
    return 1 if failed else 0


def _utc_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: str, payload: dict[str, Any]) -> None:
    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → JSON 저장: {p}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--layer", choices=["l2", "l4", "all"], default="all")
    parser.add_argument("--write-json", default="", help="결과 JSON 저장 경로 (비밀 없음)")
    parser.add_argument("--date-from", default="2026.04.01", help="목록 GET 의 dateFrom (YYYY.MM.DD)")
    parser.add_argument("--date-to", default="2026.04.30", help="목록 GET 의 dateTo (YYYY.MM.DD)")
    parser.add_argument("--month", default="202604", help="cash-status month (YYYYMM)")
    parser.add_argument("--include-cancelled", action="store_true", help="목록 GET 에 includeCancelled=true 추가")
    args = parser.parse_args()
    if args.include_cancelled:
        # 매트릭스에서 직접 사용하지 않고 향후 확장 자리. 현재는 기본 false 로 충분.
        pass
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
