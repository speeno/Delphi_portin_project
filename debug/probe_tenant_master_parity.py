#!/usr/bin/env python3
"""테넌트 마스터 패리티 진단 (DSN-DEC-12 / ACC-DATA-03) — 계정 무관.

[`migration/contracts/tenant_master_parity_manifest.yaml`](../migration/contracts/tenant_master_parity_manifest.yaml)
를 단일 원천으로, 각 케이스(A1~A5, B1~B6)가 **올바른 DB + 테넌트** 로 라우팅되는지를
두 층으로 검증한다.

Layer 1 — 라우팅/소유성 (오프라인, 자격증명 0건)
  - 기대 좌표(remote_id, db_name)에 seed_tenant_id 가 실제 존재하는가 (드리프트 가드).
  - 올바른 tenantId 를 명시하면 resolve_unique_tenant 가 unique 로 그 테넌트를 고르는가.
  - tenantId 없이(hcode 미주입) 공유 DB 는 ambiguous(=격리 키 부재 시 fail-closed),
    단독 DB 는 unique 인가 (DSN-DEC-12 기대).
  - resolve_login_route(tenant_id=...) 가 기대 remote_id/db_name/account_family 와 일치하는가.

Layer 2 — 마스터 건수·키 diff (full_parity 케이스만, 라이브 API 필요)
  - 운영자가 --api-base + 환경변수 자격증명을 주면 로그인 → JWT →
    /api/v1/masters/customer·/book 전 페이지 수집 → baseline(JSON) 과 건수·키 diff.
  - 자격증명/baseline 이 없으면 해당 케이스 Layer 2 는 skip.

비밀 정책
---------
- 자격증명은 환경변수로만 주입: BLS_PARITY_<CASE>_USER / _PASSWORD / _TENANT_ID.
  (예: BLS_PARITY_B4_USER, BLS_PARITY_B4_PASSWORD). 본 스크립트는 저장/기록하지 않는다.

사용
----
    # 오프라인 라우팅만 (자격증명 0건) — 항상 실행 가능
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/probe_tenant_master_parity.py --all-shared-db

    # 특정 케이스 + 라이브 마스터 diff
    BLS_PARITY_B4_USER=... BLS_PARITY_B4_PASSWORD=... BLS_PARITY_B4_TENANT_ID=... \
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/probe_tenant_master_parity.py --case B4 --api-base http://localhost:8000
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

MANIFEST = ROOT / "migration" / "contracts" / "tenant_master_parity_manifest.yaml"


def _load_manifest(path: Path) -> dict[str, Any]:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────
# Layer 1 — 오프라인 라우팅/소유성
# ─────────────────────────────────────────────────────────────────
def _probe_routing(case: dict[str, Any]) -> dict[str, Any]:
    from app.services import tenants_directory_service as tds

    exp = case.get("expected") or {}
    remote_id = exp.get("remote_id")
    db_name = exp.get("db_name")
    seed_tid = (case.get("seed_tenant_id") or "").strip()
    shared = bool(case.get("shared_db"))

    out: dict[str, Any] = {"checks": [], "mismatches": []}

    owners = tds.find_owning_tenants(remote_id, db_name)
    owner_ids = [o.get("tenant_id") for o in owners]
    out["coordinate_owner_count"] = len(owners)
    out["is_shared_db_runtime"] = tds.is_shared_db(remote_id, db_name)

    # (1) seed_tenant_id 가 기대 좌표에 존재 (드리프트 가드)
    if seed_tid and seed_tid not in owner_ids:
        out["mismatches"].append(
            {
                "check": "seed_tenant_at_coordinate",
                "expected_tenant_id": seed_tid,
                "actual_owner_tenant_ids": owner_ids,
            }
        )

    # (2) shared_db 플래그 정합
    if shared != out["is_shared_db_runtime"]:
        out["mismatches"].append(
            {
                "check": "shared_db_flag",
                "manifest": shared,
                "runtime": out["is_shared_db_runtime"],
            }
        )

    # (3) 올바른 tenantId 명시 → unique 해당 테넌트
    if seed_tid:
        status, owner, _ = tds.resolve_unique_tenant(
            remote_id, db_name, tenant_id_hint=seed_tid
        )
        got = (owner or {}).get("tenant_id")
        if status != "unique" or got != seed_tid:
            out["mismatches"].append(
                {
                    "check": "explicit_tenant_unique",
                    "expected": {"status": "unique", "tenant_id": seed_tid},
                    "actual": {"status": status, "tenant_id": got},
                }
            )

    # (4) tenantId 없이(hcode 미주입) ownership — DSN-DEC-12 기대
    status0, _o0, cands0 = tds.resolve_unique_tenant(remote_id, db_name)
    out["ownership_without_hint"] = {
        "status": status0,
        "candidate_count": len(cands0),
    }
    expected_status = "ambiguous" if shared else "unique"
    if status0 != expected_status:
        # 공유 DB 가 ambiguous 가 아니면(=unique) 격리 키가 이미 채워진 것으로 간주(정상).
        # 단독 DB 가 unique 가 아니면 라우팅 결함.
        if not (shared and status0 == "unique"):
            out["mismatches"].append(
                {
                    "check": "ownership_without_hint",
                    "expected": expected_status,
                    "actual": status0,
                    "note": "shared_db 는 격리 키 부재 시 ambiguous(fail-closed) 가 정상",
                }
            )

    # (5) resolve_login_route(tenant_id=seed) → 기대 좌표
    if seed_tid:
        route = tds.resolve_login_route(user_id="", tenant_id=seed_tid)
        if route is None:
            out["mismatches"].append(
                {"check": "login_route", "error": "resolve_login_route returned None"}
            )
        else:
            for key in ("remote_id", "db_name", "account_family"):
                if exp.get(key) and route.get(key) != exp.get(key):
                    out["mismatches"].append(
                        {
                            "check": f"login_route.{key}",
                            "expected": exp.get(key),
                            "actual": route.get(key),
                        }
                    )
    out["passed"] = not out["mismatches"]
    return out


# ─────────────────────────────────────────────────────────────────
# Layer 2 — 라이브 마스터 diff (full_parity)
# ─────────────────────────────────────────────────────────────────
def _creds_for(case_id: str) -> dict[str, str] | None:
    pref = f"BLS_PARITY_{case_id.upper()}_"
    user = os.environ.get(pref + "USER")
    pw = os.environ.get(pref + "PASSWORD")
    if not user or not pw:
        return None
    return {
        "user": user,
        "password": pw,
        "tenant_id": os.environ.get(pref + "TENANT_ID", ""),
    }


def _http_json(method: str, url: str, *, headers=None, body=None) -> tuple[int, Any]:
    import urllib.request

    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return getattr(e, "code", 0) or 0, {"error": f"{type(e).__name__}: {e}"}


def _norm_gcode(v: Any) -> str:
    """gcode 비교 정규화 — 선행 0 제거(레거시 zero-pad '00001' ↔ 엑셀 '1' 정합).

    레거시 DB/API 는 Gcode 를 zero-pad 문자열('00001')로, 엑셀 baseline 은 정수형
    ('1')로 보관하는 표기 차이가 있다. 같은 레코드인데 키셋 diff 로 오탐되므로
    양측을 동일 규칙(strip + 선행 0 제거)으로 정규화한다. 숫자가 아니면 원본 strip.
    """
    s = str(v).strip()
    if not s:
        return ""
    stripped = s.lstrip("0")
    return stripped if stripped else "0"


def _collect_master(api_base, token, server_id, path) -> tuple[int, set[str]]:
    """전 페이지 수집 → (total, 정규화 gcode 키 집합)."""
    headers = {"Authorization": f"Bearer {token}"}
    keys: set[str] = set()
    offset, total, limit = 0, None, 500
    while True:
        url = f"{api_base}{path}?serverId={server_id}&limit={limit}&offset={offset}"
        st, doc = _http_json("GET", url, headers=headers)
        if st != 200:
            return -1, keys
        items = doc.get("items") or []
        page = doc.get("page") or {}
        total = page.get("total", total)
        for it in items:
            gc = it.get("gcode") or it.get("hcode")
            if gc is not None:
                keys.add(_norm_gcode(gc))
        if not page.get("has_more"):
            break
        offset += limit
    return (total if total is not None else len(keys)), keys


def _probe_master_diff(case, api_base, baseline_dir) -> dict[str, Any]:
    creds = _creds_for(case["case"])
    if not creds:
        return {"skipped": True, "reason": "credentials not provided (env)"}
    if not api_base:
        return {"skipped": True, "reason": "--api-base not provided"}

    body = {"userId": creds["user"], "password": creds["password"]}
    if creds.get("tenant_id"):
        body["tenantId"] = creds["tenant_id"]
    st, doc = _http_json("POST", f"{api_base}/api/v1/auth/login", body=body)
    if st != 200:
        return {"skipped": False, "login_status": st, "error": doc.get("error") or doc}
    token = doc.get("access_token")
    user = doc.get("user") or {}
    server_id = user.get("server_id")
    out: dict[str, Any] = {
        "skipped": False,
        "jwt": {
            "server_id": server_id,
            "tenant_id": user.get("tenant_id"),
            "account_family": user.get("account_family"),
            "hcode": user.get("hcode"),
        },
        "diffs": {},
    }
    bl = case.get("baseline") or {}
    exp_counts = bl.get("expected_counts") or {}
    for kind, path in (("customers", "/api/v1/masters/customer"),
                       ("books", "/api/v1/masters/book")):
        bfile = bl.get(kind)
        if not bfile:
            continue
        baseline = json.loads((Path(baseline_dir) / bfile).read_text(encoding="utf-8"))
        b_keys = {_norm_gcode(k) for k in baseline.get("by_gcode_name", {}).keys()}
        total, w_keys = _collect_master(api_base, token, server_id, path)
        out["diffs"][kind] = {
            "expected_count": exp_counts.get(kind, baseline.get("count")),
            "web_total": total,
            "baseline_count": baseline.get("count"),
            "only_in_web": len(w_keys - b_keys),
            "only_in_baseline": len(b_keys - w_keys),
            "match": total == baseline.get("count") and not (b_keys - w_keys),
        }
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    p.add_argument("--manifest", default=str(MANIFEST))
    p.add_argument("--case", help="단일 케이스 (예: B4)")
    p.add_argument("--all-shared-db", action="store_true", help="shared_db 케이스만")
    p.add_argument("--api-base", help="라이브 마스터 diff 용 백엔드 base URL")
    p.add_argument("--out", default="/tmp/tenant_master_parity.json")
    p.add_argument("--strict", action="store_true", help="라우팅 mismatch 1건이라도 있으면 exit 2")
    args = p.parse_args(argv)

    man = _load_manifest(Path(args.manifest))
    baseline_dir = ROOT / man.get("baseline_dir", "debug/baselines")
    cases = man.get("cases") or []
    if args.case:
        cases = [c for c in cases if c.get("case") == args.case]
    elif args.all_shared_db:
        cases = [c for c in cases if c.get("shared_db")]

    results = []
    for c in cases:
        r = {"case": c.get("case"), "label": c.get("label"), "mode": c.get("mode")}
        r["routing"] = _probe_routing(c)
        if c.get("mode") == "full_parity":
            r["master_diff"] = _probe_master_diff(c, args.api_base, baseline_dir)
        results.append(r)

    summary = {
        "total": len(results),
        "routing_passed": sum(1 for r in results if r["routing"].get("passed")),
        "routing_failed": sum(1 for r in results if not r["routing"].get("passed")),
    }
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "results": results,
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {args.out}")
    print(f"  routing passed={summary['routing_passed']}/{summary['total']}")
    for r in results:
        rt = r["routing"]
        flag = "OK " if rt.get("passed") else "FAIL"
        print(f"  [{flag}] {r['case']} {r['label']} — owners={rt.get('coordinate_owner_count')} "
              f"ownership_no_hint={rt.get('ownership_without_hint', {}).get('status')}")
        for m in rt.get("mismatches", []):
            print(f"          ! {m}")

    if args.strict and summary["routing_failed"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
