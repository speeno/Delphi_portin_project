#!/usr/bin/env python3
"""대표 계정 라우팅 일괄 검증 (DSN-DEC-08/09/12).

목적
----
[`docs/welove-login-tenant-audit-samples.md`](../docs/welove-login-tenant-audit-samples.md) §1
의 매트릭스를 JSON 정본 [analysis/welove_login_routing_expectations.json](../analysis/welove_login_routing_expectations.json)
으로 받아, 각 샘플마다 [`debug/diagnose_login_routing.py`](diagnose_login_routing.py)
를 호출해 실제 라우팅 결과를 기대값과 비교한다.

운영 절차
---------
1. SME/운영자가 매트릭스 JSON 의 ``login_id_hint`` / ``hcode_hint`` / ``tenant_id_hint``
   를 실제 ID·hcode 로 채운다 (자격증명 0건 유지 — 비밀번호는 채우지 않는다).
2. read-only 자격 환경에서 본 스크립트를 실행:

       PYTHONPATH=도서물류관리프로그램/backend \
           python3 debug/verify_login_routing_matrix.py \
               --matrix analysis/welove_login_routing_expectations.json \
               --out /tmp/welove_routing_verify.json

3. 출력 JSON 의 ``mismatches`` 가 비어 있어야 통과. 비밀번호 검증 (``--probe``) 은
   본 스크립트에서 직접 실행하지 않으며 운영자가 별도 호출한다 (G3).

비밀 정책
---------
- 본 스크립트는 비밀번호를 다루지 않는다 (입력/저장 금지).
- ``diagnose_login_routing`` 호출 결과의 ``probe_results`` 도 본 검증에는 사용하지 않는다.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


def _load_matrix(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _hint_filled(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    v = value.strip()
    return bool(v) and not (v.startswith("<") and v.endswith(">"))


def _run_one(sample: dict[str, Any]) -> dict[str, Any]:
    """샘플 1건을 진단한다 — 비밀번호/probe 미사용 (read-only)."""
    from app.services.tenants_directory_service import (
        resolve_login_route,
        resolve_unique_tenant,
    )

    login_id = (sample.get("login_id_hint") or "").strip()
    hcode = sample.get("hcode_hint")
    tenant_id = sample.get("tenant_id_hint")
    hcode = hcode.strip() if isinstance(hcode, str) else None
    if hcode and (hcode.startswith("<") and hcode.endswith(">")):
        hcode = None
    tenant_id = tenant_id.strip() if isinstance(tenant_id, str) else None
    if tenant_id and (tenant_id.startswith("<") and tenant_id.endswith(">")):
        tenant_id = None

    result: dict[str, Any] = {
        "case": sample.get("case"),
        "label": sample.get("label"),
        "skipped": not _hint_filled(login_id),
        "actual": {},
        "mismatches": [],
    }
    if result["skipped"]:
        result["skip_reason"] = "login_id_hint not filled by operator"
        return result

    try:
        route = resolve_login_route(
            user_id=login_id,
            hcode=hcode,
            tenant_id=tenant_id,
        )
    except Exception as e:  # noqa: BLE001
        result["error"] = f"{type(e).__name__}: {e}"
        return result

    if route is None:
        result["error"] = "resolve_login_route returned None (no route resolved)"
        return result

    actual = {
        "remote_id": route.get("remote_id"),
        "db_name": route.get("db_name"),
        "account_family": route.get("account_family"),
        "tenant_id": route.get("tenant_id"),
        "via": route.get("via"),
    }

    # DSN-DEC-12 ownership status — hcode 힌트 유무에 따라 분기
    try:
        if actual["remote_id"] and actual["db_name"]:
            status, _t, cands = resolve_unique_tenant(
                actual["remote_id"],
                actual["db_name"],
                hcode=hcode,
                tenant_id_hint=tenant_id,
                account_family_hint=actual.get("account_family"),
            )
            actual["ownership_status"] = status
            actual["ownership_candidate_count"] = len(cands)
    except Exception as e:  # noqa: BLE001
        actual["ownership_error"] = f"{type(e).__name__}: {e}"

    result["actual"] = actual

    expected = sample.get("expected") or {}
    for key in ("remote_id", "db_name", "account_family"):
        exp = expected.get(key)
        if exp is None or (isinstance(exp, str) and exp.startswith("<")):
            continue
        if actual.get(key) != exp:
            result["mismatches"].append(
                {"field": key, "expected": exp, "actual": actual.get(key)}
            )
    # ownership 기대값 (with/without hcode 분기)
    own_exp_key = (
        "ownership_status_with_hcode" if hcode else "ownership_status_without_hcode"
    )
    own_exp = expected.get(own_exp_key) or expected.get("ownership_status")
    if own_exp and actual.get("ownership_status") and own_exp != actual["ownership_status"]:
        result["mismatches"].append(
            {
                "field": "ownership_status",
                "expected": own_exp,
                "actual": actual["ownership_status"],
                "hcode_provided": bool(hcode),
            }
        )
    return result


def _run_all(matrix: dict[str, Any]) -> dict[str, Any]:
    out_samples: list[dict[str, Any]] = []
    for s in matrix.get("samples") or []:
        out_samples.append(_run_one(s))
    summary = {
        "total": len(out_samples),
        "skipped": sum(1 for r in out_samples if r.get("skipped")),
        "errored": sum(1 for r in out_samples if r.get("error")),
        "mismatched": sum(1 for r in out_samples if r.get("mismatches")),
        "passed": sum(
            1
            for r in out_samples
            if not r.get("skipped") and not r.get("error") and not r.get("mismatches")
        ),
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "results": out_samples,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--matrix",
        default=str(ROOT / "analysis" / "welove_login_routing_expectations.json"),
    )
    parser.add_argument("--out", default="/tmp/welove_routing_verify.json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="mismatched > 0 또는 errored > 0 시 exit 2 (CI/스크립트용)",
    )
    args = parser.parse_args(argv)

    matrix_path = Path(args.matrix)
    if not matrix_path.exists():
        print(f"[ERR] matrix not found: {matrix_path}", file=sys.stderr)
        return 2
    matrix = _load_matrix(matrix_path)

    report = _run_all(matrix)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {out_path}")
    print(f"  passed={report['summary']['passed']}/{report['summary']['total']}")
    print(f"  skipped={report['summary']['skipped']}  (login_id_hint 미입력)")
    print(f"  mismatched={report['summary']['mismatched']}  errored={report['summary']['errored']}")

    if args.strict and (report["summary"]["mismatched"] > 0 or report["summary"]["errored"] > 0):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
