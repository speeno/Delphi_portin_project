#!/usr/bin/env python3
"""
로그인 라우팅 진단 — DSN-DEC-08 / DSN-DEC-09 (read-only).

용도
----
"미래가치" 같은 특정 계정이 로그인되지 않을 때, 실제로 라우팅이 어디서 막히는지
운영자가 즉시 확인할 수 있도록 백엔드 서비스 함수를 직접 호출해 다음을 출력한다.

    1. login_id_index 조회 상태 (single / ambiguous / miss)
    2. 인덱스에 박혀 있는 모든 (remote_id, db_name, hcode) 후보
    3. ``resolve_login_route_candidates`` 가 실제로 만들어내는 후보 목록과 출처
       (account_family / hcode / index_single / index_ambiguous / logical_db_peer /
        directory_sweep / fallback_auth_server)
    4. 현재 라우터 정책에서 차단/허용 여부 (DSN-DEC-09 ambiguous 정책)
    5. 라우팅에 영향을 주는 환경 변수 요약
    6. (옵션) ``--password`` 가 주어지면 각 후보에 대해 ``authenticate_user`` 를
       시도해 어느 후보에서 비밀번호가 일치하는지(=narrow 가능한지)까지 기록.

실행 (저장소 루트 기준)
----------------------
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/diagnose_login_routing.py 미래가치
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/diagnose_login_routing.py 미래가치 --hcode 1001
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/diagnose_login_routing.py 미래가치 \
            --password '...' --probe

비밀 정책
---------
- ``--probe`` 는 운영 DB 에 실제 ``Id_Logn`` 쿼리를 보내므로 read-only 자격 환경
  에서만 사용한다.
- 비밀번호는 stdout 에 인쇄되지 않는다 (출력은 후보별 match 여부만 표시).
- ``--write-json`` 으로 결과를 파일로 떨어뜨릴 수 있고, 비밀번호는 포함되지 않는다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


# 라우팅 결정에 영향을 주는 환경 변수 화이트리스트 (감사 추적 + 진단 표시용).
_ROUTING_ENV_KEYS: tuple[str, ...] = (
    "BLS_AUTH_SERVER_ID",
    "BLS_ADMIN_USER_IDS",
    "BLS_LOGIN_MAX_CANDIDATES",
    "BLS_LOGIN_DIRECTORY_SWEEP",
    "BLS_LOGIN_SWEEP_MAX",
    "BLS_LOGIN_AMBIGUOUS_PROBE",
    "BLS_LOGIN_INDEX_REFRESH_MIN_INTERVAL_SECS",
    "BLS_LOGIN_ID_INDEX_PATH",
    "BLS_TENANTS_DIRECTORY_PATH",
    "BLS_TENANTS_DIRECTORY_OVERLAY_PATH",
    "BLS_DEFAULT_ROLE",
)


def _env_summary() -> dict[str, str]:
    return {k: os.environ.get(k, "") for k in _ROUTING_ENV_KEYS}


def _index_lookup(login_id: str, hcode: str | None) -> dict[str, Any]:
    from app.services import login_id_index_service  # 지연 임포트 — 백엔드 sys.path 설정 후

    raw = login_id_index_service._load().get("by_login_id", {}).get(login_id)
    return {
        "raw_entries": list(raw or []),
        "lookup": login_id_index_service.lookup(login_id, hcode=hcode or None),
        "stats": login_id_index_service.get_stats(),
    }


def _route_candidates(
    login_id: str, *, hcode: str | None, tenant_id: str | None
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    from app.services import tenants_directory_service  # 지연 임포트

    cands = tenants_directory_service.resolve_login_route_candidates(
        user_id=login_id, tenant_id=tenant_id, hcode=hcode
    )
    single = tenants_directory_service.resolve_login_route(
        user_id=login_id, tenant_id=tenant_id, hcode=hcode
    )
    return cands, single


def _policy_simulation(
    login_id: str,
    candidates: list[dict[str, Any]],
    *,
    hcode: str | None,
    tenant_id: str | None,
) -> dict[str, Any]:
    """현재 ``auth.py`` 의 ambiguous 차단 / 시도 순회 정책을 비밀 없이 재현."""
    from app.services.auth_service import should_bypass_login_id_index_ambiguity

    has_ambiguous = any((c.get("candidate_via") or "") == "index_ambiguous" for c in candidates)
    has_real_db = any(
        (c.get("remote_id") or "").strip() and (c.get("db_name") or "").strip()
        for c in candidates
    )
    raw = (os.environ.get("BLS_LOGIN_AMBIGUOUS_PROBE") or "").strip().lower()
    strict_mode = raw in ("block", "strict", "0", "false", "no")
    bypass = should_bypass_login_id_index_ambiguity(login_id)
    blocked = (
        has_ambiguous
        and strict_mode
        and not (hcode or "").strip()
        and not (tenant_id or "").strip()
        and not bypass
    )
    return {
        "has_ambiguous_index_candidate": has_ambiguous,
        "has_real_db_candidate": has_real_db,
        "strict_mode_via_BLS_LOGIN_AMBIGUOUS_PROBE": strict_mode,
        "admin_bypass": bypass,
        "would_block_before_probe": blocked,
        "fallback_auth_server_id": os.environ.get("BLS_AUTH_SERVER_ID") or "remote_138",
        "policy_note": (
            "DSN-DEC-09 v2 (2026-04-27): 기본은 비밀번호로 narrow 한다. "
            "BLS_LOGIN_AMBIGUOUS_PROBE=block 으로 v1 엄격 모드 복원."
        ),
    }


async def _probe_candidates(
    login_id: str, password: str, candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    from app.services.auth_service import authenticate_user  # 지연 임포트

    results: list[dict[str, Any]] = []
    for c in candidates:
        sid = (c.get("remote_id") or "").strip()
        dbn = (c.get("db_name") or "").strip()
        if not sid:
            results.append(
                {
                    "remote_id": "",
                    "db_name": dbn,
                    "candidate_via": c.get("candidate_via") or "",
                    "result": "skipped_no_remote",
                }
            )
            continue
        try:
            u = await authenticate_user(sid, login_id, password, db_name=dbn or None)
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "remote_id": sid,
                    "db_name": dbn,
                    "candidate_via": c.get("candidate_via") or "",
                    "result": "exception",
                    "error": f"{type(exc).__name__}: {str(exc)[:160]}",
                }
            )
            continue
        if u is None:
            results.append(
                {
                    "remote_id": sid,
                    "db_name": dbn,
                    "candidate_via": c.get("candidate_via") or "",
                    "result": "no_match",
                }
            )
        else:
            results.append(
                {
                    "remote_id": sid,
                    "db_name": dbn,
                    "candidate_via": c.get("candidate_via") or "",
                    "result": "password_match",
                    "hcode": (u.get("hcode") or "").strip(),
                    "user_name": (u.get("user_name") or "").strip(),
                    "tenant_id": (u.get("tenant_id") or ""),
                    "account_family": (u.get("account_family") or ""),
                    "resolved_db": (u.get("resolved_db") or "").strip(),
                }
            )
    return results


async def _maybe_lazy_refresh(force: bool) -> dict[str, Any]:
    from app.services import login_id_index_service  # 지연 임포트

    return await login_id_index_service.lazy_refresh(force=force)


def _print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def _print_dict_table(rows: list[dict[str, Any]], cols: list[str]) -> None:
    if not rows:
        print("  (없음)")
        return
    widths = [len(c) for c in cols]
    for r in rows:
        for i, c in enumerate(cols):
            widths[i] = max(widths[i], len(str(r.get(c, ""))))
    header = "  " + "  ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
    print(header)
    print("  " + "  ".join("-" * widths[i] for i in range(len(cols))))
    for r in rows:
        print("  " + "  ".join(str(r.get(c, "")).ljust(widths[i]) for i, c in enumerate(cols)))


async def _amain() -> int:
    parser = argparse.ArgumentParser(
        description="로그인 라우팅 진단 (DSN-DEC-08/09) — 비밀 read-only.",
    )
    parser.add_argument("user_id", help="진단할 login_id (Id_Logn.Gcode)")
    parser.add_argument("--hcode", default=None, help="라우팅 힌트 hcode (선택)")
    parser.add_argument(
        "--tenant-id", dest="tenant_id", default=None, help="라우팅 힌트 tenant_id (선택)"
    )
    parser.add_argument(
        "--password",
        default=None,
        help="후보별 authenticate_user 검증 (선택, --probe 와 같이 사용)",
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        help="라이브 DB 에 후보별 인증 쿼리를 실제로 보낸다 (--password 필요)",
    )
    parser.add_argument(
        "--lazy-refresh",
        action="store_true",
        help="진단 직전에 login_id_index lazy_refresh 1회 호출",
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="cooldown 무시하고 강제 rebuild (운영 영향 — 신중히)",
    )
    parser.add_argument(
        "--write-json",
        default=None,
        help="결과를 JSON 파일로 저장 (비밀번호는 포함되지 않음)",
    )
    args = parser.parse_args()

    login_id = (args.user_id or "").strip()
    hcode = (args.hcode or "").strip() or None
    tenant_id = (args.tenant_id or "").strip() or None

    if args.probe and not args.password:
        print("[ERR] --probe 는 --password 와 함께 사용해야 합니다", file=sys.stderr)
        return 2

    print(f"login_id = {login_id!r}")
    print(f"hcode    = {hcode!r}")
    print(f"tenant_id= {tenant_id!r}")

    refresh_result: dict[str, Any] | None = None
    if args.lazy_refresh or args.force_refresh:
        _print_section("0) lazy_refresh")
        refresh_result = await _maybe_lazy_refresh(force=bool(args.force_refresh))
        print(json.dumps(refresh_result, ensure_ascii=False, indent=2, default=str))

    _print_section("1) login_id_index lookup")
    idx_state = _index_lookup(login_id, hcode)
    print(f"index stats: {json.dumps(idx_state['stats'], ensure_ascii=False)}")
    raw_entries = idx_state["raw_entries"]
    print(f"raw entries for {login_id!r}: {len(raw_entries)}")
    _print_dict_table(
        [
            {
                "hcode": e.get("hcode", ""),
                "remote_id": e.get("remote_id", ""),
                "db_name": e.get("db_name", ""),
                "tenant_id": e.get("tenant_id", ""),
                "account_family": e.get("account_family", ""),
            }
            for e in raw_entries
        ],
        ["hcode", "remote_id", "db_name", "tenant_id", "account_family"],
    )
    lookup = idx_state["lookup"]
    print(f"lookup status: {lookup.get('status')}")
    if lookup.get("status") == "single":
        print(f"  route: {json.dumps(lookup.get('route'), ensure_ascii=False)}")
    elif lookup.get("status") == "ambiguous":
        cands_idx = lookup.get("candidates") or []
        print(f"  ambiguous candidates: {len(cands_idx)}")

    _print_section("2) resolve_login_route_candidates")
    candidates, single_route = _route_candidates(login_id, hcode=hcode, tenant_id=tenant_id)
    print(f"single resolve: {json.dumps(single_route, ensure_ascii=False, default=str)}")
    print(f"candidate_count: {len(candidates)}")
    _print_dict_table(
        [
            {
                "priority": c.get("priority", ""),
                "candidate_via": c.get("candidate_via", ""),
                "confidence": c.get("confidence", ""),
                "remote_id": c.get("remote_id", ""),
                "db_name": c.get("db_name", ""),
                "account_family": c.get("account_family", ""),
                "tenant_id": c.get("tenant_id", ""),
                "via": c.get("via", ""),
                "index_status": c.get("index_status", ""),
            }
            for c in candidates
        ],
        [
            "priority",
            "candidate_via",
            "confidence",
            "remote_id",
            "db_name",
            "account_family",
            "tenant_id",
            "via",
            "index_status",
        ],
    )

    _print_section("3) policy simulation")
    policy = _policy_simulation(
        login_id, candidates, hcode=hcode, tenant_id=tenant_id
    )
    print(json.dumps(policy, ensure_ascii=False, indent=2))

    _print_section("4) routing env vars")
    env = _env_summary()
    for k in _ROUTING_ENV_KEYS:
        v = env.get(k, "")
        print(f"  {k} = {v!r}")

    probe_results: list[dict[str, Any]] | None = None
    if args.probe:
        _print_section("5) authenticate_user probe (각 후보에 대해 비밀번호 검증)")
        probe_results = await _probe_candidates(login_id, args.password or "", candidates)
        _print_dict_table(
            [
                {
                    "remote_id": r.get("remote_id", ""),
                    "db_name": r.get("db_name", ""),
                    "candidate_via": r.get("candidate_via", ""),
                    "result": r.get("result", ""),
                    "hcode": r.get("hcode", ""),
                    "tenant_id": r.get("tenant_id", ""),
                    "account_family": r.get("account_family", ""),
                }
                for r in probe_results
            ],
            [
                "remote_id",
                "db_name",
                "candidate_via",
                "result",
                "hcode",
                "tenant_id",
                "account_family",
            ],
        )
        matches = [r for r in probe_results if r.get("result") == "password_match"]
        print(f"\n  비밀번호 매치 후보 수: {len(matches)}")
        if len(matches) == 1:
            m = matches[0]
            print(
                f"  → 단일 매치 (정상): {m['remote_id']}/{m['db_name']} hcode={m.get('hcode')} "
                f"tenant_id={m.get('tenant_id')}"
            )
        elif len(matches) >= 2:
            print(
                "  → 중복 매치 (충돌). 동일 비밀번호가 여러 DB 에 존재한다는 뜻이다.\n"
                "    별도 hcode/tenantId 힌트 필요."
            )
        else:
            print("  → 매치 없음. 비밀번호 불일치 또는 인덱스에 누락된 신규 계정.")

    if args.write_json:
        out_path = Path(args.write_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(
                {
                    "login_id": login_id,
                    "hcode": hcode,
                    "tenant_id": tenant_id,
                    "refresh_result": refresh_result,
                    "index_lookup": idx_state,
                    "single_route": single_route,
                    "candidates": candidates,
                    "policy_simulation": policy,
                    "env": env,
                    "probe_results": probe_results,
                },
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )
        print(f"\nJSON 결과 저장: {out_path}")

    return 0


def main() -> int:
    try:
        return asyncio.run(_amain())
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
