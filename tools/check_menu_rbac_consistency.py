#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RBAC_PATH = ROOT / "migration" / "contracts" / "rbac_menu_matrix.yaml"
FORM_REGISTRY_PATH = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
MATRIX_PATH = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "account-menu-matrix.ts"
PERMS_PATH = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "use-permissions.ts"


def _load_rbac_ids() -> set[str]:
    doc = yaml.safe_load(RBAC_PATH.read_text(encoding="utf-8")) or {}
    ids: set[str] = set()
    for row in doc.get("menus") or []:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            ids.add(row["id"])
    return ids


def _extract_form_menu_ids() -> set[str]:
    text = FORM_REGISTRY_PATH.read_text(encoding="utf-8")
    return set(re.findall(r'menuId:\s*"([A-Z0-9\-]+)"', text))


def main() -> int:
    ok = True
    rbac_ids = _load_rbac_ids()
    form_ids = _extract_form_menu_ids()

    missing = sorted(i for i in form_ids if i not in rbac_ids)
    if missing:
        ok = False
        print("[FAIL] form-registry menuId not found in rbac_menu_matrix.yaml:")
        for x in missing:
            print(" -", x)

    mtxt = MATRIX_PATH.read_text(encoding="utf-8")
    ptxt = PERMS_PATH.read_text(encoding="utf-8")
    runtime_patterns = [
        r"input\.licenseKeys",
        r"licenseKeys\s*\?\?",
        r"perms\.licenseKeys",
        r"licenseKeys\.join\(",
    ]
    combined = mtxt + "\n" + ptxt + "\n" + FORM_REGISTRY_PATH.read_text(encoding="utf-8")
    if any(re.search(p, combined) for p in runtime_patterns):
        ok = False
        print("[FAIL] license key runtime dependency remains in frontend gating logic.")

    if ok:
        print("[OK] menu/rbac consistency passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
