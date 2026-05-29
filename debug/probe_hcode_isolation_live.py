"""Hcode 격리 라이브 검증 스크립트 — Phase 4 DB verify.

목표
----
T2_PUB / T3 공유 DB 계정으로 hcode 를 **생략**하고 list GET 호출 시:
1. 200 OK 반환 (코드 변경으로 회귀 0건).
2. 결과 row 수가 본인 hcode 로 명시 호출했을 때와 동일.
3. 슈퍼 유저 호출 결과보다 적음(격리 적용 확인).

사용
----
```
export PROBE_BASE=https://api.example.com
export PROBE_T2_PUB_TOKEN=<JWT>            # 본인 hcode=PUB01 인 출판사 계정
export PROBE_SUPER_TOKEN=<JWT>             # 슈퍼유저 (검증용 비교)
export PROBE_SERVER_ID=remote_153
export PROBE_HCODE=PUB01
export PROBE_DATE_FROM=2026-04-01
export PROBE_DATE_TO=2026-04-30
python3 debug/probe_hcode_isolation_live.py
```

라이브 DB 가 필요하므로 CI 에서는 자동 실행 X. 로컬/스테이징에서 운영자 수동 실행.

DoD
----
1. **T2_PUB 빈 hcode == 본인 hcode**: 동일 row 수.
2. **T2_PUB 명시 다른 hcode → 403**.
3. **슈퍼 호출 row 수 > T2_PUB row 수**.

본 스크립트는 [`enforce_hcode_isolation`](../도서물류관리프로그램/backend/app/core/deps.py)
의 라우터-레벨 통합 검증을 실 DB 에서 보강한다 (단위 테스트는
[`test/test_routers_hcode_coalesce.py`](../test/test_routers_hcode_coalesce.py)).
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any

try:
    import requests  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - optional dep
    print("[probe] requests not installed; pip install requests", file=sys.stderr)
    sys.exit(2)

BASE = os.environ.get("PROBE_BASE", "http://localhost:8000").rstrip("/")
T2_TOKEN = os.environ.get("PROBE_T2_PUB_TOKEN", "")
SUPER_TOKEN = os.environ.get("PROBE_SUPER_TOKEN", "")
SERVER_ID = os.environ.get("PROBE_SERVER_ID", "remote_153")
HCODE = os.environ.get("PROBE_HCODE", "PUB01")
DATE_FROM = os.environ.get("PROBE_DATE_FROM", "2026-04-01")
DATE_TO = os.environ.get("PROBE_DATE_TO", "2026-04-30")
TIMEOUT = float(os.environ.get("PROBE_TIMEOUT", "10"))

# DoD 검증할 list/집계 GET 엔드포인트.
ENDPOINTS = [
    {
        "name": "outbound.orders",
        "path": "/api/v1/outbound/orders",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
    },
    {
        "name": "inbound.receipts",
        "path": "/api/v1/inbound/receipts",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
    },
    {
        "name": "returns.list",
        "path": "/api/v1/returns",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
    },
    {
        "name": "transactions.sales-statement",
        "path": "/api/v1/transactions/sales-statement",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
    },
    {
        "name": "settlement.billing",
        "path": "/api/v1/settlement/billing",
        "params": {"serverId": SERVER_ID, "monthFrom": DATE_FROM[:7], "monthTo": DATE_TO[:7], "limit": 50},
        "count_key": "page.total",
    },
    # ── ACC-DATA-03 갭 클로즈 — 식별자/범위/패턴/body hcode tamper 경로 ──
    {
        "name": "ledger.customer (customerCode→Hcode)",
        "path": "/api/v1/ledger/customer",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
        "tamper_param": "customerCode",
        "own_required": True,  # customerCode 는 required — 빈 호출 생략.
    },
    {
        "name": "ledger.customer-integrated (customerPattern)",
        "path": "/api/v1/ledger/customer-integrated",
        "params": {"serverId": SERVER_ID, "dateFrom": DATE_FROM, "dateTo": DATE_TO, "limit": 50},
        "count_key": "page.total",
        "tamper_param": "customerPattern",
    },
    {
        "name": "courier.lines (hcodeFrom)",
        "path": "/api/v1/shipping/courier/lines",
        "params": {"serverId": SERVER_ID, "gdate": DATE_FROM.replace("-", "."), "limit": 50},
        "count_key": "total",
        "tamper_param": "hcodeFrom",
    },
    {
        "name": "scan.match (body hcode)",
        "path": "/api/v1/scan/match",
        "method": "POST",
        "body": {"barcode": "0000000000000", "context": "outbound", "server_id": SERVER_ID},
        "count_key": None,
        "tamper_param": "hcode",
        "tamper_in": "body",
        "own_required": True,
    },
]


def _walk(d: Any, path: str) -> Any:
    cur: Any = d
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur


def _call(
    token: str,
    path: str,
    params: dict[str, Any],
    *,
    method: str = "GET",
    json_body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any]]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    if method.upper() == "POST":
        r = requests.post(
            BASE + path, params=params, json=json_body or {}, headers=headers, timeout=TIMEOUT
        )
    else:
        r = requests.get(BASE + path, params=params, headers=headers, timeout=TIMEOUT)
    body: dict[str, Any]
    try:
        body = r.json()
    except Exception:
        body = {"_raw": r.text[:200]}
    return r.status_code, body


def _apply_tamper(
    ep: dict[str, Any], base_params: dict[str, Any], value: str
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """tamper_param 을 query 또는 body 에 주입한 (params, json_body) 반환."""
    param = ep.get("tamper_param", "hcode")
    where = ep.get("tamper_in", "query")
    body = dict(ep["body"]) if ep.get("body") is not None else None
    params = dict(base_params)
    if where == "body" and body is not None:
        body[param] = value
    else:
        params[param] = value
    return params, body


def _check(ep: dict[str, Any]) -> dict[str, Any]:
    name = ep["name"]
    path = ep["path"]
    base_params = dict(ep["params"])
    count_key = ep["count_key"]
    method = ep.get("method", "GET")
    base_body = dict(ep["body"]) if ep.get("body") is not None else None
    own_required = bool(ep.get("own_required"))

    if not T2_TOKEN:
        return {"endpoint": name, "skipped": "PROBE_T2_PUB_TOKEN missing"}

    # 1) T2_PUB 빈 식별자 (required 식별자면 생략).
    if own_required:
        s1, b1 = None, None
    else:
        s1, b1 = _call(T2_TOKEN, path, base_params, method=method, json_body=base_body)
    # 2) T2_PUB 명시 식별자 = 본인 hcode
    own_params, own_body = _apply_tamper(ep, base_params, HCODE)
    s2, b2 = _call(T2_TOKEN, path, own_params, method=method, json_body=own_body)
    # 3) T2_PUB 명시 타사 식별자 (격리 가드 → 403)
    oth_params, oth_body = _apply_tamper(ep, base_params, "OTHER")
    s3, b3 = _call(T2_TOKEN, path, oth_params, method=method, json_body=oth_body)
    # 4) Super 빈 식별자 (있으면)
    s4 = b4 = None
    if SUPER_TOKEN and not own_required:
        s4, b4 = _call(SUPER_TOKEN, path, base_params, method=method, json_body=base_body)

    n1 = _walk(b1, count_key) if (count_key and s1 == 200) else None
    n2 = _walk(b2, count_key) if (count_key and s2 == 200) else None
    n4 = _walk(b4, count_key) if (count_key and s4 == 200 and b4) else None

    return {
        "endpoint": name,
        "tamper_param": ep.get("tamper_param", "hcode"),
        "t2pub_empty": {"status": s1, "count": n1} if not own_required else "n/a",
        "t2pub_own": {"status": s2, "count": n2},
        "t2pub_other": {"status": s3, "expected": 403},
        "super_empty": {"status": s4, "count": n4} if (SUPER_TOKEN and not own_required) else "n/a",
        "dod_isolation_match": (n1 == n2) if (n1 is not None and n2 is not None) else None,
        "dod_tamper_403": s3 == 403,
        "dod_super_wider": (n4 is not None and n1 is not None and n4 > n1)
        if (SUPER_TOKEN and n1 is not None) else None,
    }


def main() -> int:
    out: list[dict[str, Any]] = []
    for ep in ENDPOINTS:
        out.append(_check(ep))
        time.sleep(0.1)
    print(json.dumps({
        "base": BASE,
        "server_id": SERVER_ID,
        "hcode": HCODE,
        "results": out,
    }, ensure_ascii=False, indent=2))

    failures = [r for r in out if isinstance(r, dict) and (
        r.get("dod_isolation_match") is False
        or r.get("dod_tamper_403") is False
    )]
    if failures:
        print(f"\n[probe] {len(failures)} endpoint(s) violate DoD", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
