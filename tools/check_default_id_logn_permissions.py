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
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.services.default_id_logn_permissions_service import (  # noqa: E402
    resolve_default_permissions,
)
RBAC = ROOT / "migration" / "contracts" / "rbac_menu_matrix.yaml"

# 관리·감사 F 키는 메뉴 매트릭스에 등장해도 신규 사용자 기본 템플릿에서 별도 정책(DEC-007 등).
_SKIP_FKEYS = frozenset({"F18", "F18r", "F90", "F91", "F92"})


def main() -> int:
    rbac = yaml.safe_load(RBAC.read_text(encoding="utf-8"))
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
        accts = menu.get("account_types") or []
        if not accts:
            # 매트릭스: account_types 비어 있으면 해당 차원 무제한 — Fxx 교차검증 생략
            continue
        roles = menu.get("build_roles") or [None]
        for fk in fxx_keys:
            ok_any = False
            for at in accts:
                if str(at) == "T1":
                    # 계약에 T1 베이스 템플릿이 없음 — 슈퍼/운영 계정은 별 DEC 로 Fxx 부여
                    ok_any = True
                    break
                for role in roles:
                    perms = resolve_default_permissions(
                        account_type=str(at),
                        build_role=str(role) if role else None,
                    )
                    val = str(perms.get(fk, "X")).strip().upper()
                    if val != "X":
                        ok_any = True
                        break
                if ok_any:
                    break
            if not ok_any:
                errors.append(
                    f"{mid}: license_keys require {fk} but no account_type×build_role combo grants it"
                )
    if errors:
        print("\n".join(errors[:50]))
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more")
        return 1
    print("OK — rbac Fxx license_keys vs default_id_logn_permissions base_templates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
