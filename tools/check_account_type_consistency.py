#!/usr/bin/env python3
"""계약·RBAC JSON 의 account_type / warehouse_menu_tiers 정본을 점검한다.

실행 (repo 루트)::

    python3 tools/check_account_type_consistency.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_AT = frozenset({"T1", "T2_DIST", "T2_PUB", "T3"})
ALLOWED_TIERS = frozenset({"lite", "full"})


def main() -> int:
    issues: list[str] = []

    td = ROOT / "migration" / "contracts" / "tenants_directory.yaml"
    if td.exists():
        tdoc = yaml.safe_load(td.read_text(encoding="utf-8")) or {}
        for row in tdoc.get("tenants") or []:
            if not isinstance(row, dict):
                continue
            val = str(row.get("default_account_type") or "").strip()
            if not val:
                continue
            if val not in CANONICAL_AT:
                issues.append(
                    f"{td.relative_to(ROOT)}: tenant {row.get('tenant_id')!r} default_account_type={val!r}"
                )

    perm = ROOT / "migration" / "contracts" / "default_id_logn_permissions.yaml"
    if perm.exists():
        doc = yaml.safe_load(perm.read_text(encoding="utf-8")) or {}
        bases = doc.get("base_templates") or {}
        if isinstance(bases, dict):
            for k in bases.keys():
                if str(k) not in CANONICAL_AT:
                    issues.append(f"{perm.relative_to(ROOT)}: base_templates key {k!r} not in 4-way set")

    for rel in (
        "analysis/rbac_menu_matrix.json",
        "도서물류관리프로그램/frontend/src/data/rbac_menu_matrix.json",
    ):
        p = ROOT / rel
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        for m in data.get("menus") or []:
            mid = m.get("id", "?")
            for at in m.get("account_types") or []:
                if at not in CANONICAL_AT:
                    issues.append(f"{rel} menu {mid}: invalid account_type {at!r}")
            for wt in m.get("warehouse_menu_tiers") or []:
                if wt not in ALLOWED_TIERS:
                    issues.append(f"{rel} menu {mid}: invalid warehouse_menu_tier {wt!r}")

    if issues:
        print("WARN — account_type 정합 점검:\n" + "\n".join(issues[:100]))
        return 1
    print("OK — account_type / warehouse_menu_tiers 정합")
    return 0


if __name__ == "__main__":
    sys.exit(main())
