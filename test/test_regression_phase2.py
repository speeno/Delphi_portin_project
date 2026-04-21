"""Phase2 32 화면 — 자동 회귀 러너 (live_only).

목적
----
``form-registry.ts`` ``phase==='phase2'`` 32 화면의 백엔드 라우트를 호출하여
5축(functional/data/ui/audit/performance) 중 자동화 가능 항목
(functional/data/audit/performance) 을 측정하고 JSON 리포트를 출력.

phase1 (test_regression_phase1.py) 와의 차이
-------------------------------------------
1. 그룹 정의: ``dashboard/data/phase2-screen-cards.json`` 의 ``screens`` 배열을
   단일 원천으로 호출 그룹을 자동 생성한다 (32 그룹).
2. ``blocker`` 가 있는 화면(scenario.blockers 비어있지 않음)은 expected_status 에
   503 (NOT_IMPLEMENTED) 을 추가 허용 — phase2 단계에서는 일부 endpoint 가
   stub 으로 동작하는 것이 정상.
3. write 화면(POST/PUT/DELETE) 은 ``audit_axis_na=False`` — audit 축을 검증.
4. ``live_only`` 모드: dry-run 출력 비활성. 실행하려면 ``RUN_DB_SMOKE=1`` 필수.
   dry-run 이 필요하면 ``RUN_DB_SMOKE=`` 비우고 ``--allow-dry-run`` 명시 필요.

호출 그룹 단일 원천
-------------------
``dashboard/data/phase2-screen-cards.json`` ``screens[*]``::

    {
      "id": "Sobo54",
      "route": "/inbound/reports/daily",
      "scenario": { "blockers": [...] }
    }

→ ``GroupSpec(id="phase2.Sobo54", method="GET", path="/api/v1/...", ...)``
  로 1:1 자동 매핑.

라우트 파라미터 보강
--------------------
일부 화면은 form 라우트만 정의되어 backend 매핑을 위해 다음 규칙을 적용:

- ``/transactions/status?view=list`` 등 query 파라미터는 그대로 전달.
- 빈 파라미터 화면은 ``date_from / date_to`` 등 공통 기본값을 부여.
- ``/admin/audit-rotate`` 등 write 화면은 GET (목록) 가 없으므로 별도 호출 X.

실행
----
::

    PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
        pytest test/test_regression_phase2.py -v

    PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
        python3 test/test_regression_phase2.py \
            --servers mysql3 mysql5 mysql8 maria --multi-db \
            --write-json reports/phase2-regression-$(date +%F).json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from contextlib import suppress
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

# ─────────────────────────────────────────────────────────────────────
# 단일 원천: dashboard/data/phase2-screen-cards.json
# ─────────────────────────────────────────────────────────────────────
_DEFAULT_DATE_FROM = "2026-04-01"
_DEFAULT_DATE_TO = "2026-04-30"
_PERFORMANCE_P95_MAX_MS = 1200  # phase2 는 통계/원장/리포트 무거운 SQL → 800→1200 완화
_DEFAULT_PROBE_SERVERS = ["mysql3", "mysql5", "mysql8", "maria"]  # live_only

_PHASE2_CARDS_JSON = ROOT / "dashboard" / "data" / "phase2-screen-cards.json"


@dataclass
class GroupSpec:
    """Phase2 회귀 그룹 1건 — phase2-screen-cards.json 의 screens[i] 1:1.

    blocker 보유 화면은 ``expected_status`` 에 503 추가 허용.
    write 라우트(POST/PUT/DELETE) 는 ``audit_axis_na=False`` — audit 축 검증.
    """

    id: str
    method: str
    path: str
    legacy_id: str
    contract: str = ""
    expected_status: set[int] = field(default_factory=lambda: {200})
    response_keys: tuple[str, ...] = ()
    audit_axis_na: bool = True
    blockers: tuple[str, ...] = ()


# ── route → backend api endpoint 매핑 ────────────────────────────────
# 단일 원천: 도서물류관리프로그램/backend/app/routers/*.py
# (form-registry.ts 의 frontend route 와 backend api path 가 다른 경우만 명시)
_FRONTEND_TO_BACKEND_PATH = {
    "/inbound/reports/daily":      "/api/v1/inbound/reports/daily",
    "/inbound/reports/period":     "/api/v1/inbound/reports/period",
    "/returns/ledger":             "/api/v1/returns/ledger",
    "/returns/period-report":      "/api/v1/returns/reports/period",
    "/settlement/tax-invoice":     "/api/v1/settlement/tax-invoice",
    "/admin/audit-rotate":         "/api/v1/admin/audit-rotate",
    "/stats/sales-period":         "/api/v1/stats/sales-period",
    "/stats/customer-analysis":    "/api/v1/stats/customer-analysis",
    "/stats/book-turnover":        "/api/v1/stats/book-turnover",
    "/stats/quarterly-summary":    "/api/v1/stats/quarterly-summary",
    "/admin/ops":                  "/api/v1/health/full",  # /admin/ops 페이지가 호출하는 대표 endpoint
    "/admin/audit":                "/api/v1/admin/audit",
    "/outbound/status":            "/api/v1/outbound/status",
    "/inventory/status":           "/api/v1/inventory/status",
    "/ledger/customer":            "/api/v1/ledger/customer",
    "/ledger/customer-integrated": "/api/v1/ledger/customer-integrated",
    "/ledger/book":                "/api/v1/ledger/book",
    "/ledger/book-integrated":     "/api/v1/ledger/book-integrated",
    "/ledger/comparison":          "/api/v1/ledger/comparison",
    "/master/special":             "/api/v1/master/special",
    "/transactions/status":        "/api/v1/transactions/status",
    "/transactions/other":         "/api/v1/transactions/misc",
    "/settlement/outstanding":     "/api/v1/settlement/outstanding",
    "/settlement/payment-slip":    "/api/v1/settlement/payment-slip",
    "/delivery/management":        "/api/v1/delivery/dispatch",
    "/stats/monthly":              "/api/v1/stats/monthly",
    "/stats/customer":             "/api/v1/stats/customer-list",
    "/stats/book":                 "/api/v1/stats/book-list",
    "/stats/publisher":            "/api/v1/stats/publisher",
}

# write endpoint: GET 호출 대신 list 또는 health 로 대체.
# WebAdmAuditRotate / Sobo46_billing / Sobo41_slip 등은 list endpoint 가 없거나 별도.
_WRITE_ONLY_SCREENS = {
    "WebAdmAuditRotate",  # POST only — 회귀에서는 health/full 로 대체
    "Sobo46_billing",      # 단건 인쇄 (route null) — 회귀 SKIP
}


def _query_for(route: str, df: str, dt: str) -> str:
    """frontend route → backend GET query 파라미터 자동 부여."""
    base = f"dateFrom={df}&dateTo={dt}&limit=1"
    if "?" in route:
        # query 가 이미 있는 경우 (예: /transactions/status?view=list)
        return base
    return base


def _phase2_groups(server_id: str, df: str, dt: str) -> list[GroupSpec]:
    """phase2-screen-cards.json 을 읽어 32 그룹을 자동 생성.

    파일이 없으면 ``RuntimeError`` (단일 원천 불일치 = 즉시 실패).
    """
    if not _PHASE2_CARDS_JSON.exists():
        raise RuntimeError(f"단일 원천 누락: {_PHASE2_CARDS_JSON}")

    payload = json.loads(_PHASE2_CARDS_JSON.read_text(encoding="utf-8"))
    screens = payload.get("screens", [])
    groups: list[GroupSpec] = []

    for sc in screens:
        legacy_id = sc.get("id", "")
        route = sc.get("route") or ""
        scenario = sc.get("scenario") or {}
        blockers = tuple(scenario.get("blockers") or [])

        if legacy_id in _WRITE_ONLY_SCREENS or not route:
            # write-only / route null — 회귀 SKIP 전용 그룹 (functional NA)
            groups.append(
                GroupSpec(
                    id=f"phase2.{legacy_id}",
                    method="SKIP",
                    path="(write-only or route=null)",
                    legacy_id=legacy_id,
                    expected_status={200, 405, 503},
                    audit_axis_na=False,
                    blockers=blockers,
                )
            )
            continue

        # frontend route → backend api path
        route_no_query, _, query_part = route.partition("?")
        backend_path = _FRONTEND_TO_BACKEND_PATH.get(route_no_query, f"/api/v1{route_no_query}")
        suffix = _query_for(route, df, dt)
        sep = "&" if "?" in backend_path or query_part else "?"
        full_query = f"{query_part}&{suffix}" if query_part else suffix
        full_path = f"{backend_path}?serverId={server_id}&{full_query}"

        # blocker 가 있는 화면은 503 (NOT_IMPLEMENTED) 추가 허용
        expected = {200}
        if blockers:
            expected.add(503)

        groups.append(
            GroupSpec(
                id=f"phase2.{legacy_id}",
                method="GET",
                path=full_path,
                legacy_id=legacy_id,
                expected_status=expected,
                response_keys=("items", "rows", "page", "summary"),
                audit_axis_na=True,
                blockers=blockers,
            )
        )

    return groups


# ─────────────────────────────────────────────────────────────────────
# 호출 + 5축 측정 (phase1 패턴 재사용)
# ─────────────────────────────────────────────────────────────────────
def _build_test_client():
    """FastAPI TestClient + auth 우회 (admin / *)."""
    from fastapi.testclient import TestClient  # noqa: PLC0415

    from app.main import app  # noqa: PLC0415
    from app.routers.auth import get_current_user  # noqa: PLC0415

    async def _override() -> dict[str, Any]:
        return {
            "user_id": "regression-phase2",
            "server_id": "remote_1",
            "hcode": "0000",
            "role": "admin",
            "permissions": ["*"],
        }

    app.dependency_overrides[get_current_user] = _override
    return TestClient(app)


@dataclass
class AxisResult:
    name: str
    status: str  # PASS | FAIL | SKIP | NA
    detail: str = ""


@dataclass
class GroupReport:
    group: str
    legacy_id: str
    server_id: str
    http_status: int
    elapsed_ms: int
    axes: list[AxisResult]
    blockers: tuple[str, ...] = ()


def _run_group(client, spec: GroupSpec, server_id: str) -> GroupReport:
    """단일 그룹 호출 + 5축(자동화 분) 측정."""
    if spec.method == "SKIP":
        return GroupReport(
            group=spec.id,
            legacy_id=spec.legacy_id,
            server_id=server_id,
            http_status=0,
            elapsed_ms=0,
            axes=[
                AxisResult("functional", "SKIP", "write-only or route=null"),
                AxisResult("data", "SKIP", "no GET probe"),
                AxisResult("performance", "SKIP", "no probe"),
                AxisResult("audit", "NA", "covered by dedicated test"),
                AxisResult("ui", "SKIP", "out of scope"),
            ],
            blockers=spec.blockers,
        )

    started = time.perf_counter()
    try:
        res = client.request(spec.method, spec.path)
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        body: Any
        try:
            body = res.json()
        except Exception:  # noqa: BLE001
            body = None
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return GroupReport(
            group=spec.id,
            legacy_id=spec.legacy_id,
            server_id=server_id,
            http_status=0,
            elapsed_ms=elapsed_ms,
            axes=[
                AxisResult("functional", "FAIL", f"{type(exc).__name__}: {exc}"),
                AxisResult("data", "SKIP", "transport error"),
                AxisResult("performance", "FAIL", f"{elapsed_ms}ms (transport error)"),
                AxisResult("audit", "NA" if spec.audit_axis_na else "FAIL", "transport error"),
                AxisResult("ui", "SKIP", "out of scope"),
            ],
            blockers=spec.blockers,
        )

    # functional 축: status_code in expected_status + (200 일 때만 keys 검증)
    func_pass = res.status_code in spec.expected_status
    func_detail = f"HTTP {res.status_code}"
    if func_pass and res.status_code == 200 and isinstance(body, dict) and spec.response_keys:
        present = [k for k in spec.response_keys if k in body]
        if not present:
            func_pass = False
            func_detail = f"HTTP 200 but missing one of keys={spec.response_keys}"

    # 503 (blocker) 는 PASS 로 간주하되 detail 에 명시 — phase2 단계에서는 정상.
    if res.status_code == 503 and 503 in spec.expected_status:
        func_detail = f"HTTP 503 NOT_IMPLEMENTED (blocked: {','.join(spec.blockers) or 'n/a'})"

    perf_pass = elapsed_ms < _PERFORMANCE_P95_MAX_MS
    perf_detail = f"{elapsed_ms}ms (limit {_PERFORMANCE_P95_MAX_MS}ms)"

    return GroupReport(
        group=spec.id,
        legacy_id=spec.legacy_id,
        server_id=server_id,
        http_status=res.status_code,
        elapsed_ms=elapsed_ms,
        axes=[
            AxisResult("functional", "PASS" if func_pass else "FAIL", func_detail),
            AxisResult("data", "SKIP", "single-server run; use --multi-db for data axis"),
            AxisResult("performance", "PASS" if perf_pass else "FAIL", perf_detail),
            AxisResult("audit", "NA" if spec.audit_axis_na else "FAIL", "read-only group"),
            AxisResult("ui", "SKIP", "out of scope (visual regression separate)"),
        ],
        blockers=spec.blockers,
    )


def _run_multi_db(
    client,
    servers: list[str],
    df: str,
    dt: str,
) -> dict[str, GroupReport]:
    """4대 DB cross-server invariant 측정 (data axis)."""
    runs: dict[str, list[GroupReport]] = {}
    for sid in servers:
        for spec in _phase2_groups(sid, df, dt):
            r = _run_group(client, spec, sid)
            runs.setdefault(spec.id, []).append(r)

    consolidated: dict[str, GroupReport] = {}
    for gid, lst in runs.items():
        if not lst:
            continue
        base = lst[0]
        statuses = {r.http_status for r in lst}
        # data axis: 모든 서버에서 동일 status (200 또는 503) 시 PASS
        data_pass = len(statuses) == 1 and (200 in statuses or 503 in statuses)
        for ax in base.axes:
            if ax.name == "data":
                ax.status = "PASS" if data_pass else "FAIL"
                ax.detail = f"servers={[r.server_id for r in lst]} statuses={sorted(statuses)}"
        base.server_id = ",".join(r.server_id for r in lst)
        consolidated[gid] = base
    return consolidated


# ─────────────────────────────────────────────────────────────────────
# pytest 통합 — RUN_REGRESSION_PHASE2=1 일 때만 라이브 실행
# ─────────────────────────────────────────────────────────────────────
_PYTEST_ENABLED = os.environ.get("RUN_REGRESSION_PHASE2", "").strip() in {"1", "true", "True"}


@pytest.fixture(scope="module")
def _client():
    if not _PYTEST_ENABLED:
        pytest.skip("RUN_REGRESSION_PHASE2 미설정 — phase2 회귀 러너 비활성")
    client = _build_test_client()
    yield client
    with suppress(Exception):
        client.close()


# pytest 컬렉션은 모듈 임포트 시 _phase2_groups 호출 → 단일 원천 부재면 컬렉션 단계에서 실패.
# 이는 의도된 동작 (DEC-047 — phase2-screen-cards.json 가 단일 원천).
def _collect_group_ids() -> list[str]:
    try:
        return [g.id for g in _phase2_groups("mysql8", _DEFAULT_DATE_FROM, _DEFAULT_DATE_TO)]
    except RuntimeError:
        return []


@pytest.mark.parametrize("group_id", _collect_group_ids())
def test_phase2_group_functional(_client, group_id: str) -> None:
    """각 그룹별 functional+performance 축 PASS 검증.

    blocker 보유 화면은 503 PASS 로 간주 (NOT_IMPLEMENTED 정상).
    write-only 화면은 SKIP.
    """
    spec = next(
        s for s in _phase2_groups("mysql8", _DEFAULT_DATE_FROM, _DEFAULT_DATE_TO)
        if s.id == group_id
    )
    report = _run_group(_client, spec, "mysql8")
    failures = [
        ax for ax in report.axes
        if ax.status == "FAIL" and ax.name in {"functional", "performance"}
    ]
    assert not failures, (
        f"group={group_id} legacy={report.legacy_id} HTTP={report.http_status} "
        f"elapsed={report.elapsed_ms}ms blockers={report.blockers} "
        f"failures={[asdict(ax) for ax in failures]}"
    )


# ─────────────────────────────────────────────────────────────────────
# CLI 단독 실행 — live_only 기본
# ─────────────────────────────────────────────────────────────────────
def _utc_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: str, payload: dict[str, Any]) -> None:
    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → JSON 저장: {p}")


async def _cli(args: argparse.Namespace) -> int:
    live = os.environ.get("RUN_DB_SMOKE", "").strip() in {"1", "true", "True"}

    if not live and not args.allow_dry_run:
        print("[live_only] RUN_DB_SMOKE 미설정 — phase2 회귀는 live_only 정책. ")
        print("            dry-run 이 필요하면 --allow-dry-run 명시.")
        return 2

    if not live:
        print("[dry-run] 호출 계획만 출력 (live_only 우회):")
        for sid in args.servers:
            for spec in _phase2_groups(sid, args.date_from, args.date_to):
                blk = f" blocked={','.join(spec.blockers)}" if spec.blockers else ""
                print(f"  · {sid} {spec.id:32s} {spec.method:5s} {spec.path}{blk}")
        return 0

    client = _build_test_client()
    try:
        if args.multi_db and len(args.servers) > 1:
            consolidated = _run_multi_db(client, args.servers, args.date_from, args.date_to)
            results = {gid: asdict(r) for gid, r in consolidated.items()}
        else:
            sid = args.servers[0]
            results = {}
            for spec in _phase2_groups(sid, args.date_from, args.date_to):
                results[spec.id] = asdict(_run_group(client, spec, sid))
    finally:
        with suppress(Exception):
            client.close()

    payload = {
        "checkedAt": _utc_iso(),
        "scope": "phase2",
        "servers": args.servers,
        "multi_db": bool(args.multi_db),
        "performance_p95_max_ms": _PERFORMANCE_P95_MAX_MS,
        "single_source": str(_PHASE2_CARDS_JSON.relative_to(ROOT)),
        "results": results,
    }

    pass_count = 0
    fail_count = 0
    skip_count = 0
    blocked_count = 0
    for gid, r in results.items():
        funcs = next(ax for ax in r["axes"] if ax["name"] == "functional")
        perf = next(ax for ax in r["axes"] if ax["name"] == "performance")
        data = next(ax for ax in r["axes"] if ax["name"] == "data")
        if funcs["status"] == "SKIP":
            skip_count += 1
            mark = "SKIP"
        else:
            ok = funcs["status"] == "PASS" and perf["status"] in {"PASS", "SKIP"} \
                and data["status"] in {"PASS", "SKIP"}
            if ok:
                pass_count += 1
                mark = "OK  "
            else:
                fail_count += 1
                mark = "FAIL"
        if r.get("blockers"):
            blocked_count += 1
        print(
            f"  {mark} {gid:32s} HTTP={r['http_status']:>3d} {r['elapsed_ms']:>5d}ms "
            f"func={funcs['status']:4s} perf={perf['status']:4s} data={data['status']:4s}"
        )

    total = pass_count + fail_count + skip_count
    print(
        f"\n=== 요약 === PASS={pass_count}/{total} (SKIP={skip_count}, FAIL={fail_count}, "
        f"blocker={blocked_count})"
    )

    if args.write_json:
        _write_json(args.write_json, payload)

    return 0 if fail_count == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--servers", nargs="+", default=_DEFAULT_PROBE_SERVERS,
                        help="검사 대상 server_id 목록 (기본: 4대 DB live_only)")
    parser.add_argument("--multi-db", action="store_true",
                        help="data axis cross-DB invariant 측정 (모든 서버 호출)")
    parser.add_argument("--date-from", default=_DEFAULT_DATE_FROM)
    parser.add_argument("--date-to", default=_DEFAULT_DATE_TO)
    parser.add_argument("--write-json", default="", help="결과 JSON 저장 경로")
    parser.add_argument("--allow-dry-run", action="store_true",
                        help="RUN_DB_SMOKE 미설정 시에도 dry-run 출력 허용 (live_only 정책 우회)")
    args = parser.parse_args()
    return asyncio.run(_cli(args))


if __name__ == "__main__":
    sys.exit(main())
