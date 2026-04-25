#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
DATA = BACKEND / "data"

TENANTS_CONTRACT = ROOT / "migration" / "contracts" / "tenants_directory.yaml"
WHITELIST_JSON = DATA / "web_publisher_whitelist.json"
TENANTS_SEED_JSON = DATA / "tenants_directory_seed.json"
TENANTS_OVERLAY_JSON = DATA / "tenants_directory_overlay.json"
ACCOUNT_OVERLAY_JSON = DATA / "account_directory_overlay.json"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_tenants_contract_ids() -> set[str]:
    if not TENANTS_CONTRACT.exists():
        return set()
    data = yaml.safe_load(TENANTS_CONTRACT.read_text(encoding="utf-8")) or {}
    tenants = data.get("tenants") or []
    return {str(t.get("tenant_id") or "").strip() for t in tenants if str(t.get("tenant_id") or "").strip()}


def _load_runtime_tenants() -> list[dict[str, Any]]:
    seed = _load_json(TENANTS_SEED_JSON).get("tenants") or []
    overlay = _load_json(TENANTS_OVERLAY_JSON).get("tenants") or []
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for row in seed:
        key = (str(row.get("tenant_id") or "").strip(), str(row.get("account_family") or "").strip())
        out[key] = dict(row)
    for row in overlay:
        key = (str(row.get("tenant_id") or "").strip(), str(row.get("account_family") or "").strip())
        merged = dict(out.get(key, {}))
        merged.update(row)
        out[key] = merged
    return list(out.values())


def main() -> int:
    issues: list[str] = []

    contract_tenant_ids = _load_tenants_contract_ids()
    runtime_tenants = _load_runtime_tenants()
    tenant_by_id = {
        str(t.get("tenant_id") or "").strip(): t
        for t in runtime_tenants
        if str(t.get("tenant_id") or "").strip()
    }

    whitelist_entries = _load_json(WHITELIST_JSON).get("entries") or []
    pub_to_dist: dict[str, set[str]] = {}
    for e in whitelist_entries:
        ph = str(e.get("publisher_hcode") or "").strip()
        dh = str(e.get("dist_hcode") or "").strip()
        dt = str(e.get("dist_tenant_id") or "").strip()
        if not ph:
            continue
        pub_to_dist.setdefault(ph, set())
        if dh:
            pub_to_dist[ph].add(dh)
        if dt and dt not in tenant_by_id and dt not in contract_tenant_ids:
            issues.append(f"WHL_UNKNOWN_DIST_TENANT: publisher_hcode={ph} dist_tenant_id={dt}")
        if dt:
            t = tenant_by_id.get(dt)
            if t and str(t.get("default_account_type") or "").strip() != "T2_DIST":
                issues.append(
                    f"WHL_DIST_TENANT_NOT_T2_DIST: publisher_hcode={ph} dist_tenant_id={dt} "
                    f"default_account_type={t.get('default_account_type')}"
                )

    for ph, dset in pub_to_dist.items():
        if len(dset) > 1:
            issues.append(
                f"WHL_AMBIGUOUS_PUBLISHER_HCODE: publisher_hcode={ph} dist_hcodes={sorted(dset)}"
            )

    for t in runtime_tenants:
        tid = str(t.get("tenant_id") or "").strip()
        ptid = str(t.get("parent_tenant_id") or "").strip()
        if ptid and ptid not in tenant_by_id and ptid not in contract_tenant_ids:
            issues.append(f"TENANT_UNKNOWN_PARENT: tenant_id={tid} parent_tenant_id={ptid}")

    account_overrides = _load_json(ACCOUNT_OVERLAY_JSON).get("overrides") or []
    for o in account_overrides:
        at = str(o.get("account_type") or "").strip()
        dh = str(o.get("dist_hcode") or "").strip()
        gcode = str(o.get("gcode") or "").strip()
        dbn = str(o.get("db_name") or "").strip()
        if at == "T2_PUB" and not dh:
            issues.append(f"OVERLAY_T2_PUB_NO_DIST_HCODE: gcode={gcode} db_name={dbn}")

    print(f"[affiliation-integrity] checked whitelist={len(whitelist_entries)} tenants={len(runtime_tenants)}")
    if not issues:
        print("[affiliation-integrity] OK - no mismatch found")
        return 0
    print("[affiliation-integrity] MISMATCH FOUND")
    for line in issues:
        print(f" - {line}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
