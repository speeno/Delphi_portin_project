#!/usr/bin/env python3
"""
마스터 6 종 LIST 검색 진단 (DEC-024 직후 회귀).

실행 환경
---------
- 백엔드 서버가 떠 있는 환경에서 실행.
- 로그인 토큰을 환경변수 ``BLS_AUTH_TOKEN`` 으로 넘기거나,
  ``--user/--password`` 로 즉석 로그인.
- 백엔드 측에는 ``BLS_DEBUG_MASTER_SEARCH=1`` 을 주고 띄워두면 service 진입 시
  q raw bytes / pattern bytes / SQL / params / fetched 행 수 가 logger 로 흘러나온다.

사용법
------
    export BLS_AUTH_TOKEN=...
    python3 debug/diagnose_master_search.py \
        --base-url http://127.0.0.1:8000 \
        --server remote_154 \
        --q-ascii A \
        --q-korean 도서

동작
----
- 6 개 list endpoint 를 (q 없음 / ASCII q / 한글 q) × 6 = 18 회 호출.
- HTTP status, 요청 URL (percent-encoding 그대로), 응답 page.total / returned
  를 표 형태로 출력.
- 한 환경에서 ASCII 는 매치되는데 한글만 0 행이 나오면 charset/콜레이션 이슈,
  q 미지정·ASCII 모두 0 행이면 LIMIT/OFFSET 또는 권한 이슈로 1차 판정.

주의
----
- 본 스크립트는 read-only. 어떤 PATCH/INSERT 도 호출하지 않는다.
- 운영 환경에서 돌릴 때는 가능하면 토큰 권한이 read 만 있는 계정 사용.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from typing import Any

import urllib.request

ENDPOINTS: list[tuple[str, str]] = [
    ("customer", "/api/v1/masters/customer"),
    ("book", "/api/v1/masters/book"),
    ("publisher", "/api/v1/masters/publisher"),
    ("book-code", "/api/v1/masters/book-code"),
    ("discount", "/api/v1/masters/discount"),
    ("logistics-cost", "/api/v1/masters/logistics-cost"),
]


def _login(base_url: str, user_id: str, password: str) -> str:
    payload = json.dumps({"user_id": user_id, "password": password}).encode("utf-8")
    req = urllib.request.Request(
        urllib.parse.urljoin(base_url, "/api/v1/auth/login"),
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    token = body.get("access_token") or body.get("token")
    if not token:
        raise SystemExit(f"login failed: {body}")
    return str(token)


def _call(
    base_url: str, path: str, *, server_id: str, q: str | None, token: str
) -> dict[str, Any]:
    params = {"serverId": server_id, "limit": "10"}
    if q is not None and q != "":
        params["q"] = q
    qs = urllib.parse.urlencode(params)
    url = urllib.parse.urljoin(base_url, f"{path}?{qs}")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            status = resp.status
    except urllib.error.HTTPError as e:
        try:
            data = json.loads(e.read().decode("utf-8"))
        except Exception:
            data = {"error": str(e)}
        status = e.code
    page = (data or {}).get("page") or {}
    return {
        "url": url,
        "status": status,
        "total": page.get("total"),
        "returned": len((data or {}).get("items") or []),
        "page": page,
        "error": data.get("detail") if status >= 400 else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=os.environ.get("BLS_BASE_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--server", required=True, help="servers.yaml 의 server id")
    parser.add_argument("--user", default=os.environ.get("BLS_USER"))
    parser.add_argument("--password", default=os.environ.get("BLS_PASSWORD"))
    parser.add_argument("--token", default=os.environ.get("BLS_AUTH_TOKEN"))
    parser.add_argument("--q-ascii", default="A")
    parser.add_argument("--q-korean", default="도서")
    args = parser.parse_args()

    token = args.token
    if not token:
        if not (args.user and args.password):
            print("BLS_AUTH_TOKEN 또는 --user/--password 둘 중 하나가 필요합니다.", file=sys.stderr)
            return 2
        token = _login(args.base_url, args.user, args.password)

    rows: list[dict[str, Any]] = []
    for label, path in ENDPOINTS:
        for q_label, q_val in (("(none)", None), ("ascii", args.q_ascii), ("korean", args.q_korean)):
            r = _call(args.base_url, path, server_id=args.server, q=q_val, token=token)
            rows.append({"endpoint": label, "q_kind": q_label, "q": q_val, **r})

    print(
        "{:<15} {:<8} {:>6} {:>8} {:>8}  url".format(
            "endpoint", "q_kind", "status", "total", "returned"
        )
    )
    for r in rows:
        print(
            "{:<15} {:<8} {:>6} {:>8} {:>8}  {}".format(
                r["endpoint"],
                r["q_kind"],
                r["status"],
                "-" if r["total"] is None else r["total"],
                r["returned"],
                r["url"],
            )
        )

    bad = [r for r in rows if r["status"] >= 400]
    zero_korean = [
        r
        for r in rows
        if r["status"] < 400 and r["q_kind"] == "korean" and (r["total"] or 0) == 0
    ]
    summary: dict[str, Any] = {
        "rows": rows,
        "errors": bad,
        "korean_zero": zero_korean,
    }
    out_path = os.environ.get("BLS_DIAG_OUT")
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\n[saved] {out_path}", file=sys.stderr)

    if bad:
        print(f"\n[FAIL] {len(bad)} endpoint 에서 4xx/5xx", file=sys.stderr)
        return 1
    if zero_korean:
        print(
            f"\n[WARN] 한글 검색 0행 endpoint {len(zero_korean)} — charset/COLLATE 가설 확인",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
