#!/usr/bin/env python3
"""테넌트 업무 화면 패리티 진단 (업무 화면 0건 분류용).

목적
----
기초관리(마스터)는 보이는데 업무 화면(outbound/settlement/stats)에서 0건이 나오는 케이스를
동일 JWT 기준으로 진단한다.

분류 기준
---------
- 401/403: 권한/소유권 이슈
- 200 + total=0: 데이터 없음 또는 스코프/기간 과필터
- 200 + total>0: 연결/권한은 정상, 기본 기간/세션 복원 문제 가능
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "migration" / "contracts" / "tenant_transaction_parity_manifest.yaml"


def _load_manifest(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _http_json(method: str, url: str, *, headers: dict[str, str] | None = None, body: Any = None) -> tuple[int, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return int(resp.status), json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        status = int(getattr(e, "code", 0) or 0)
        try:
            body = json.loads(e.read().decode("utf-8"))  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            body = {"error": f"{type(e).__name__}: {e}"}
        return status, body


def _creds_for(case_id: str, seed_tenant_id: str | None) -> dict[str, str] | None:
    pref = f"BLS_PARITY_{case_id.upper()}_"
    user = os.environ.get(pref + "USER")
    pw = os.environ.get(pref + "PASSWORD")
    if not user or not pw:
        return None
    return {
        "user": user,
        "password": pw,
        "tenant_id": os.environ.get(pref + "TENANT_ID") or (seed_tenant_id or ""),
    }


def _extract_total(doc: Any) -> int | None:
    if not isinstance(doc, dict):
        return None
    page = doc.get("page")
    if isinstance(page, dict) and isinstance(page.get("total"), int):
        return int(page["total"])
    for key in ("total", "total_count"):
        v = doc.get(key)
        if isinstance(v, int):
            return int(v)
    items = doc.get("items")
    if isinstance(items, list):
        return len(items)
    return None


def _extract_items_len(doc: Any) -> int | None:
    if not isinstance(doc, dict):
        return None
    items = doc.get("items")
    if isinstance(items, list):
        return len(items)
    return None


def _extract_error_code(doc: Any) -> str:
    if not isinstance(doc, dict):
        return ""
    detail = doc.get("detail")
    if isinstance(detail, dict):
        code = detail.get("code")
        if isinstance(code, str):
            return code
    code2 = doc.get("code")
    return code2 if isinstance(code2, str) else ""


def _dot(d: date) -> str:
    return d.strftime("%Y.%m.%d")


def _dash(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _build_params(name: str, base: dict[str, Any], day_window: int, today: date) -> dict[str, Any]:
    params = dict(base)
    from_day = today - timedelta(days=day_window)
    if name == "outbound_orders":
        params["dateFrom"] = _dot(from_day)
        params["dateTo"] = _dot(today)
    elif name == "settlement_cash":
        params["dateFrom"] = _dot(from_day)
        params["dateTo"] = _dot(today)
    elif name == "stats_customer_analysis":
        params["dateFrom"] = _dash(from_day)
        params["dateTo"] = _dash(today)
    return params


def _classify(status: int, total: int | None) -> str:
    if status in (401, 403):
        return "permission_or_ownership"
    if status >= 400:
        return "request_failed"
    if total is None:
        return "ok_unknown_total"
    if total == 0:
        return "ok_empty"
    return "ok_nonzero"


def _query_url(base_url: str, path: str, params: dict[str, Any]) -> str:
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    return f"{base_url}{path}?{q}"


def _probe_case(case: dict[str, Any], api_base: str) -> dict[str, Any]:
    case_id = str(case.get("case") or "")
    creds = _creds_for(case_id, case.get("seed_tenant_id"))
    if not creds:
        return {
            "case": case_id,
            "label": case.get("label"),
            "skipped": True,
            "reason": "credentials not provided (env)",
        }

    login_body: dict[str, Any] = {"userId": creds["user"], "password": creds["password"]}
    if creds.get("tenant_id"):
        login_body["tenantId"] = creds["tenant_id"]
    st, login_doc = _http_json("POST", f"{api_base}/api/v1/auth/login", body=login_body)
    if st != 200:
        return {
            "case": case_id,
            "label": case.get("label"),
            "skipped": False,
            "login_status": st,
            "error_code": _extract_error_code(login_doc),
            "error": login_doc,
        }

    token = (login_doc or {}).get("access_token")
    user = (login_doc or {}).get("user") or {}
    headers = {"Authorization": f"Bearer {token}"}
    server_id = str(user.get("server_id") or "")
    endpoints = (case.get("endpoints") or {}) if isinstance(case.get("endpoints"), dict) else {}

    today = date.today()
    windows = case.get("date_windows_days") or [90]
    rows: list[dict[str, Any]] = []

    for window in windows:
        for name, cfg in endpoints.items():
            path = str((cfg or {}).get("path") or "")
            base_params = (cfg or {}).get("params") or {}
            params = _build_params(name, base_params, int(window), today)
            params["serverId"] = server_id
            url = _query_url(api_base, path, params)
            status, doc = _http_json("GET", url, headers=headers)
            total = _extract_total(doc)
            rows.append(
                {
                    "endpoint": name,
                    "path": path,
                    "window_days": int(window),
                    "http_status": status,
                    "total": total,
                    "items_len": _extract_items_len(doc),
                    "classification": _classify(status, total),
                    "error_code": _extract_error_code(doc),
                    "date_range": {
                        "dateFrom": params.get("dateFrom"),
                        "dateTo": params.get("dateTo"),
                    },
                }
            )

    return {
        "case": case_id,
        "label": case.get("label"),
        "skipped": False,
        "jwt": {
            "server_id": server_id,
            "tenant_id": user.get("tenant_id"),
            "hcode": user.get("hcode"),
            "account_type": user.get("account_type"),
            "build_role": user.get("build_role"),
        },
        "expected": case.get("expected") or {},
        "canonical_hq_hcode": case.get("canonical_hq_hcode"),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", default=str(MANIFEST))
    parser.add_argument("--case", default="B4", help="단일 케이스 실행 (예: B4)")
    parser.add_argument("--api-base", default="http://localhost:8000")
    parser.add_argument(
        "--out",
        default="analysis/audit/tenant-transaction-parity-B4.json",
        help="리포트 출력 경로(저장소 루트 상대/절대)",
    )
    args = parser.parse_args(argv)

    manifest = _load_manifest(Path(args.manifest))
    cases = list(manifest.get("cases") or [])
    case = next((c for c in cases if c.get("case") == args.case), None)
    if not case:
        raise SystemExit(f"case not found: {args.case}")

    result = _probe_case(case, args.api_base.rstrip("/"))
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "case": args.case,
        "skipped": bool(result.get("skipped")),
        "rows": len(result.get("rows") or []),
        "classifications": {},
    }
    for row in result.get("rows") or []:
        key = row.get("classification") or "unknown"
        summary["classifications"][key] = int(summary["classifications"].get(key, 0)) + 1

    report = {"summary": summary, "result": result}
    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {out}")
    print(f"  skipped={summary['skipped']} rows={summary['rows']} class={summary['classifications']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

