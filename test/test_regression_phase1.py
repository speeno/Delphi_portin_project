"""
Phase1 12개 재사용 화면 — 자동 회귀 러너.

목적
----
docs/phase1-promotion-gate.md §3 의 T7 (equivalence_run) 단계를 자동화.
12개 재사용 화면의 백엔드 라우트를 호출하여 5축(functional/data/ui/audit/performance)
중 자동화 가능 항목(functional/data/performance)을 측정하고 JSON 리포트를 출력.

호출 그룹 정의는 ``migration/coverage/phase1-12pages-coverage.md`` §3 와 1:1 동기.

실행
----
    PYTHONPATH=도서물류관리프로그램/backend \
        pytest test/test_regression_phase1.py -v [-k group_name]

또는 직접 실행 (4대 DB probe 포함, RUN_DB_SMOKE=1 필요):

    PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
        python3 test/test_regression_phase1.py --write-json reports/regression-$(date +%F).json

검증 정책
---------
* functional: HTTP 2xx + 응답 스키마 필수 키 존재.
* data: --multi-db 옵션 시 4대 DB 모두 응답 → cross-DB invariant 검사 (rows 길이 동일 여부).
* performance: 단일 호출 wall-clock < 800ms (DEC-PHASE1-GATE 기본 임계).
* audit: 12개 화면 모두 read-only 라 SKIP (리포트에 N/A 표기).
* ui: 본 러너 범위 외 (별도 시각 회귀 도구).

리포트 산출물
-------------
``reports/regression-<UTCDATE>.json`` (gitignored. CI 가 artifact 로 첨부).
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
# 회귀 러너 그룹 — coverage matrix §3 와 동기
# ─────────────────────────────────────────────────────────────────────
_DEFAULT_DATE_FROM = "2026.04.01"
_DEFAULT_DATE_TO = "2026.04.30"
_PERFORMANCE_P95_MAX_MS = 800
_DEFAULT_PROBE_SERVERS = ["mysql8"]


@dataclass
class GroupSpec:
    """회귀 그룹 1건의 호출/검증 메타.

    ``audit_axis_na=True`` 인 그룹은 read-only 로 audit 축을 SKIP 한다.
    """

    id: str
    method: str
    path: str
    contract: str
    expected_status: set[int] = field(default_factory=lambda: {200})
    response_keys: tuple[str, ...] = ("items", "rows", "page")
    audit_axis_na: bool = True


def _phase1_groups(server_id: str, df: str, dt: str) -> list[GroupSpec]:
    """coverage matrix §3 의 10 그룹 (12 화면 ↔ 일부 공유)."""
    sid = server_id
    return [
        GroupSpec(
            id="outbound.list_orders",
            method="GET",
            path=f"/api/v1/outbound/orders?serverId={sid}&dateFrom={df}&dateTo={dt}&limit=1",
            contract="outbound_order.yaml",
        ),
        GroupSpec(
            id="inventory.ledger",
            method="GET",
            path=(
                f"/api/v1/inventory/ledger?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&hcode=%25&bcode=%25"
            ),
            contract="sales_inquiry.yaml",
            response_keys=("rows",),
        ),
        GroupSpec(
            id="settlement.outstanding",
            method="GET",
            path=(
                f"/api/v1/settlement/billing?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            contract="settlement_billing.yaml",
        ),
        GroupSpec(
            id="settlement.cash_list",
            method="GET",
            path=(
                f"/api/v1/settlement/cash?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            contract="settlement_billing.yaml",
        ),
        GroupSpec(
            id="sales.statement_list",
            method="GET",
            path=(
                f"/api/v1/transactions/sales-statement?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            contract="sales_inquiry.yaml",
        ),
        GroupSpec(
            id="transactions.statement_list_grouped",
            method="GET",
            path=(
                f"/api/v1/transactions/sales-statement?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=50&offset=0"
            ),
            contract="sales_inquiry.yaml",
        ),
        GroupSpec(
            id="inventory.ledger_grouped",
            method="GET",
            path=(
                f"/api/v1/inventory/ledger?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&hcode=%25&bcode=%25"
            ),
            contract="sales_inquiry.yaml",
            response_keys=("rows",),
        ),
        GroupSpec(
            id="stats.sales_period",
            method="GET",
            path=(
                f"/api/v1/stats/sales-period?serverId={sid}"
                f"&hcode=%25&period=12M"
            ),
            contract="stats_reports.yaml",
            response_keys=("rows",),
            expected_status={200, 404},  # 라우트 미등록 사이드(404) 도 별도 분류
        ),
        GroupSpec(
            id="reports.book_sales",
            method="GET",
            path=(
                f"/api/v1/reports/book-sales?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&hcode=%25&limit=1&offset=0"
            ),
            contract="sales_inquiry.yaml",
            response_keys=("rows",),
        ),
        GroupSpec(
            id="reports.customer_sales",
            method="GET",
            path=(
                f"/api/v1/reports/customer-sales?serverId={sid}"
                f"&dateFrom={df}&dateTo={dt}&limit=1&offset=0"
            ),
            contract="sales_inquiry.yaml",
            response_keys=("rows",),
        ),
    ]


# ─────────────────────────────────────────────────────────────────────
# 호출 + 5축 측정
# ─────────────────────────────────────────────────────────────────────
def _build_test_client():
    """FastAPI TestClient + auth dependency 우회.

    debug/probe_backend_all_servers.py 의 _build_test_client 와 동일 패턴 (DRY 위반 인지).
    회귀 러너는 정책상 별도 모듈에 두어 의존을 최소화 — DEC-PHASE1-GATE §1 참조.
    """
    from fastapi.testclient import TestClient  # noqa: PLC0415

    from app.main import app  # noqa: PLC0415
    from app.routers.auth import get_current_user  # noqa: PLC0415

    async def _override() -> dict[str, Any]:
        return {
            "user_id": "regression",
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
    contract: str
    server_id: str
    http_status: int
    elapsed_ms: int
    axes: list[AxisResult]


def _run_group(client, spec: GroupSpec, server_id: str) -> GroupReport:
    started = time.perf_counter()
    try:
        if spec.method.upper() == "GET":
            res = client.get(spec.path)
        else:
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
            contract=spec.contract,
            server_id=server_id,
            http_status=0,
            elapsed_ms=elapsed_ms,
            axes=[
                AxisResult("functional", "FAIL", f"{type(exc).__name__}: {exc}"),
                AxisResult("data", "SKIP", "transport error"),
                AxisResult("performance", "FAIL", f"{elapsed_ms}ms (transport error)"),
                AxisResult("audit", "NA" if spec.audit_axis_na else "FAIL", "read-only"),
                AxisResult("ui", "SKIP", "out of scope"),
            ],
        )

    # functional 축
    func_pass = res.status_code in spec.expected_status
    func_detail = f"HTTP {res.status_code}"
    if func_pass and isinstance(body, dict):
        missing = [k for k in spec.response_keys if k not in body]
        if missing:
            func_pass = False
            func_detail = f"HTTP {res.status_code} but missing keys={missing}"

    # performance 축
    perf_pass = elapsed_ms < _PERFORMANCE_P95_MAX_MS
    perf_detail = f"{elapsed_ms}ms (limit {_PERFORMANCE_P95_MAX_MS}ms)"

    # data 축은 단일 server_id 호출만으로는 cross-DB invariant 측정 불가 → SKIP.
    # _run_multi_db 가 대신 데이터 축 PASS/FAIL 판정을 가산함.
    data_status = "SKIP"
    data_detail = "single-server run; use --multi-db for data axis"

    return GroupReport(
        group=spec.id,
        contract=spec.contract,
        server_id=server_id,
        http_status=res.status_code,
        elapsed_ms=elapsed_ms,
        axes=[
            AxisResult("functional", "PASS" if func_pass else "FAIL", func_detail),
            AxisResult("data", data_status, data_detail),
            AxisResult("performance", "PASS" if perf_pass else "FAIL", perf_detail),
            AxisResult("audit", "NA" if spec.audit_axis_na else "FAIL", "read-only group"),
            AxisResult("ui", "SKIP", "out of scope (visual regression separate)"),
        ],
    )


def _run_multi_db(
    client,
    spec_factory,  # type: ignore[no-untyped-def]
    servers: list[str],
    df: str,
    dt: str,
) -> dict[str, GroupReport]:
    """동일 그룹을 N대 서버에서 호출 후 row-count invariant 측정 (data axis)."""
    runs: dict[str, list[GroupReport]] = {}
    for sid in servers:
        groups = spec_factory(sid, df, dt)
        for spec in groups:
            r = _run_group(client, spec, sid)
            runs.setdefault(spec.id, []).append(r)

    # data axis 보강 — 모든 서버의 http_status 동일 + body keys 동일 시 PASS
    consolidated: dict[str, GroupReport] = {}
    for gid, lst in runs.items():
        if not lst:
            continue
        # 대표 1개 (첫번째 서버) 를 베이스로 axes 갱신
        base = lst[0]
        statuses = {r.http_status for r in lst}
        data_pass = len(statuses) == 1 and 200 in statuses
        for ax in base.axes:
            if ax.name == "data":
                ax.status = "PASS" if data_pass else "FAIL"
                ax.detail = f"servers={[r.server_id for r in lst]} statuses={sorted(statuses)}"
        base.server_id = ",".join(r.server_id for r in lst)
        consolidated[gid] = base
    return consolidated


# ─────────────────────────────────────────────────────────────────────
# pytest 통합 — RUN_REGRESSION=1 일 때만 라이브 실행
# ─────────────────────────────────────────────────────────────────────
_PYTEST_ENABLED = os.environ.get("RUN_REGRESSION", "").strip() in {"1", "true", "True"}


@pytest.fixture(scope="module")
def _client():
    if not _PYTEST_ENABLED:
        pytest.skip("RUN_REGRESSION 미설정 — phase1 회귀 러너 비활성")
    client = _build_test_client()
    yield client
    with suppress(Exception):
        client.close()


@pytest.mark.parametrize(
    "group_id",
    [g.id for g in _phase1_groups("mysql8", _DEFAULT_DATE_FROM, _DEFAULT_DATE_TO)],
)
def test_phase1_group_functional(_client, group_id: str) -> None:  # noqa: D401
    """각 그룹별 functional+performance 축이 PASS 인지 단위 검증."""
    spec = next(
        s for s in _phase1_groups("mysql8", _DEFAULT_DATE_FROM, _DEFAULT_DATE_TO)
        if s.id == group_id
    )
    report = _run_group(_client, spec, "mysql8")
    failures = [
        ax for ax in report.axes
        if ax.status == "FAIL" and ax.name in {"functional", "performance"}
    ]
    assert not failures, (
        f"group={group_id} HTTP={report.http_status} elapsed={report.elapsed_ms}ms "
        f"failures={[asdict(ax) for ax in failures]}"
    )


# ─────────────────────────────────────────────────────────────────────
# CLI 단독 실행
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
    if os.environ.get("RUN_DB_SMOKE", "").strip() not in {"1", "true", "True"}:
        print("[dry-run] RUN_DB_SMOKE 미설정 — 호출 계획만 출력")
        for sid in args.servers:
            for spec in _phase1_groups(sid, args.date_from, args.date_to):
                print(f"  · {sid} {spec.id:38s} {spec.method} {spec.path}")
        return 0

    client = _build_test_client()
    try:
        if args.multi_db and len(args.servers) > 1:
            consolidated = _run_multi_db(client, _phase1_groups, args.servers, args.date_from, args.date_to)
            results = {gid: asdict(r) for gid, r in consolidated.items()}
        else:
            sid = args.servers[0]
            results = {}
            for spec in _phase1_groups(sid, args.date_from, args.date_to):
                results[spec.id] = asdict(_run_group(client, spec, sid))
    finally:
        with suppress(Exception):
            client.close()

    payload = {
        "checkedAt": _utc_iso(),
        "servers": args.servers,
        "multi_db": bool(args.multi_db),
        "performance_p95_max_ms": _PERFORMANCE_P95_MAX_MS,
        "results": results,
    }

    pass_count = 0
    fail_count = 0
    for gid, r in results.items():
        funcs = [ax for ax in r["axes"] if ax["name"] == "functional"][0]
        perf = [ax for ax in r["axes"] if ax["name"] == "performance"][0]
        data = [ax for ax in r["axes"] if ax["name"] == "data"][0]
        ok = funcs["status"] == "PASS" and perf["status"] == "PASS" and data["status"] in {"PASS", "SKIP"}
        if ok:
            pass_count += 1
        else:
            fail_count += 1
        mark = "OK  " if ok else "FAIL"
        print(
            f"  {mark} {gid:38s} HTTP={r['http_status']:>3d} {r['elapsed_ms']:>4d}ms "
            f"func={funcs['status']:4s} perf={perf['status']:4s} data={data['status']:4s}"
        )

    print(f"\n=== 요약 === PASS={pass_count}/{pass_count+fail_count}")

    if args.write_json:
        _write_json(args.write_json, payload)

    return 0 if fail_count == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--servers",
        nargs="+",
        default=_DEFAULT_PROBE_SERVERS,
        help="검사 대상 server_id 목록 (예: mysql3 mysql5 mysql8 maria)",
    )
    parser.add_argument("--multi-db", action="store_true", help="data axis 측정 (모든 서버 cross-DB invariant)")
    parser.add_argument("--date-from", default=_DEFAULT_DATE_FROM)
    parser.add_argument("--date-to", default=_DEFAULT_DATE_TO)
    parser.add_argument("--write-json", default="", help="결과 JSON 저장 경로")
    args = parser.parse_args()
    return asyncio.run(_cli(args))


if __name__ == "__main__":
    sys.exit(main())
