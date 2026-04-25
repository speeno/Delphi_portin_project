#!/usr/bin/env python3
"""
rbac_menu_matrix.yaml 의 Fxx 라이선스 키가 default_id_logn_permissions.yaml 에서
해당 account_type 에 대해 차단(X)이 아닌지 점검한다 (느슨한 정합 가드).

실행: repo 루트에서 ``python3 tools/check_default_id_logn_permissions.py``
종료 코드: 불일치 시 1.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RBAC = ROOT / "migration" / "contracts" / "rbac_menu_matrix.yaml"
DEFAULT = ROOT / "migration" / "contracts" / "default_id_logn_permissions.yaml"

# 관리·감사 F 키는 메뉴 매트릭스에 등장해도 신규 사용자 기본 템플릿에서 별도 정책(DEC-007 등).
_SKIP_FKEYS = frozenset({"F18", "F18r", "F90", "F91", "F92"})


def main() -> int:
    rbac = yaml.safe_load(RBAC.read_text(encoding="utf-8"))
    dflt = yaml.safe_load(DEFAULT.read_text(encoding="utf-8"))
    bases = dflt.get("base_templates") or {}
    errors: list[str] = []
    for menu in rbac.get("menus") or []:
        if not isinstance(menu, dict):
            continue
        mid = menu.get("id")
        fxx_keys = [
            k
            for k in (menu.get("license_keys") or [])
            if isinstance(k, str) and k.startswith("F") and k not in _SKIP_FKEYS
        ]
        if not fxx_keys:
            continue
        for at in menu.get("account_types") or []:
            tpl = bases.get(at)
            if not isinstance(tpl, dict):
                continue
            mdef = tpl.get("fxx_defaults") or {}
            for fk in fxx_keys:
                val = str(mdef.get(fk, "X")).strip().upper()
                if val == "X":
                    errors.append(f"{mid}: account_type={at} requires {fk} via license_keys but default is X")
    if errors:
        print("\n".join(errors[:50]))
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more")
        return 1
    print("OK — rbac Fxx license_keys vs default_id_logn_permissions base_templates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
