#!/usr/bin/env python3
"""Generate analysis/masters_menu_account_type_inventory.json from rbac_menu_matrix.

계획 항목 inventory-masters-matrix: 기초관리(§3 masters) 행별로
총판/출판/자체물류 축에서 '동일 노출 가능 여부'를 기계 태깅한다.

실행: python3 tools/gen_masters_menu_inventory.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "analysis" / "rbac_menu_matrix.json"
OUT = ROOT / "analysis" / "masters_menu_account_type_inventory.json"


def _tag_row(menu: dict) -> dict:
    at = menu.get("account_types") or []
    br = menu.get("build_roles") or []
    wt = menu.get("warehouse_menu_tiers") or []
    at_set = set(at)

    all_four = at_set >= {"T1", "T2_DIST", "T2_PUB", "T3"}
    has_tier = bool(wt)
    has_br = bool(br)
    dist_only = at_set.issubset({"T1", "T2_DIST", "T3"}) and ("T2_PUB" not in at_set)
    pub_side = "T2_PUB" in at_set and "T2_DIST" not in at_set and not has_tier

    if all_four and not has_tier and not has_br:
        exposure = "all_account_types_nav_item"
        same_ok = True
        note = "4유형 공통·build_role 미제한 — 상위 NAV와 유사"
    elif has_tier or (has_br and "warehouse_publisher" in br):
        exposure = "warehouse_or_build_gated"
        same_ok = False
        note = "자체물류 lite/full 또는 build_role 로 분기 — 총판·출판 동일 노출 아님"
    elif dist_only and "T2_PUB" not in at_set:
        exposure = "distributor_or_warehouse_shell"
        same_ok = False
        note = "T2_PUB 비포함 — 출판사(publisher) 셸과 노출 불일치"
    elif pub_side:
        exposure = "publisher_shell_heavy"
        same_ok = False
        note = "출판 측 위주 — 총판 전용 메뉴와 다름"
    else:
        exposure = "mixed_matrix"
        same_ok = not (has_tier or has_br)
        note = "account_types/build_roles/warehouse_menu_tiers 조합 검토 필요"

    return {
        "menu_id": menu["id"],
        "caption": menu.get("caption"),
        "route": menu.get("route"),
        "license_keys": menu.get("license_keys") or [],
        "account_types": at,
        "build_roles": br,
        "warehouse_menu_tiers": wt,
        "source_builds": menu.get("source_builds") or [],
        "same_exposure_ok_for_all_publishers_and_distributors": same_ok,
        "exposure_class": exposure,
        "notes_ko": note,
    }


def main() -> None:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    masters = [m for m in data["menus"] if m.get("section") == "masters"]
    inv = {
        "schema_version": "1.0.0",
        "source_matrix": str(MATRIX.relative_to(ROOT)),
        "nav_masters_context": "ACC-MENU-NAV-01 기초관리 하위 — section=masters 만 포함",
        "rows": [_tag_row(m) for m in masters],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[gen_masters_menu_inventory] {len(inv['rows'])} rows -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
