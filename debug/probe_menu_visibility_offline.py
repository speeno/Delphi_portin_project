"""오프라인 메뉴 가시성 베이스라인 (DB 자격증명 불필요).

라이브 프로브(``debug/probe_login_menu_visibility.py``)는 백엔드 + 로그인이 필요하지만,
본 스크립트는 ``app.core.menu_policy.build_nav_payload`` 규칙을 대표 계정 컨텍스트에
직접 적용해 결정적 스냅샷을 만든다 (MENUVIS-DEC-07 show-first 전/후 회귀 비교용).

사용 예::

    PYTHONPATH=도서물류관리프로그램/backend \
      python3 debug/probe_menu_visibility_offline.py \
      --out analysis/audit/menu-visibility-show-first-baseline.json

산출:
- 대표 컨텍스트별 visible/disabled/hidden menu ID 집계
- 누락 보고된 3 메뉴(ACC-MENU-MASTERS-02/03/06) 의 컨텍스트별 가시성 요약
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
sys.path.insert(0, str(ROOT / "backend"))

from app.core.menu_policy import MenuPolicyContext, build_nav_payload  # noqa: E402

# 누락 보고된 기초관리 3 화면 (입고처/기타거래처/저자)
TARGET_MENUS = ["ACC-MENU-MASTERS-02", "ACC-MENU-MASTERS-03", "ACC-MENU-MASTERS-06"]

# 대표 계정 컨텍스트 (ACTR 산출 결과 모사) — 회귀의 결정적 입력.
SCENARIOS: list[dict[str, Any]] = [
    {"label": "unmapped_empty_account_type", "account_type": None, "build_role": None},
    {"label": "T1_admin_scope", "account_type": "T1", "build_role": "distributor"},
    {"label": "T2_DIST_distributor", "account_type": "T2_DIST", "build_role": "distributor"},
    {"label": "T2_PUB_publisher", "account_type": "T2_PUB", "build_role": "publisher"},
    {"label": "T3_warehouse_publisher_lite", "account_type": "T3",
     "build_role": "warehouse_publisher", "warehouse_menu_tier": "lite"},
    {"label": "T3_warehouse_publisher_full", "account_type": "T3",
     "build_role": "warehouse_publisher", "warehouse_menu_tier": "full"},
    {"label": "department_accounting", "account_type": "T3",
     "build_role": "warehouse_publisher", "warehouse_menu_tier": "lite",
     "login_profile": "department_accounting"},
]


def _eval(scn: dict[str, Any]) -> dict[str, Any]:
    ctx = MenuPolicyContext(
        account_type=scn.get("account_type"),
        build_role=scn.get("build_role"),
        warehouse_menu_tier=scn.get("warehouse_menu_tier"),
        login_profile=scn.get("login_profile"),
        license_keys=frozenset(scn.get("license_keys") or []),
        is_super_user=bool(scn.get("is_super_user")),
        active_build_id=scn.get("active_build_id"),
    )
    nav = build_nav_payload(ctx)
    items = nav.get("items", [])
    visible = [x["id"] for x in items if x.get("visible")]
    disabled = [x["id"] for x in items if x.get("visible") and x.get("disabled")]
    hidden = [x["id"] for x in items if not x.get("visible")]
    target = {
        m: next(
            (
                {"visible": x.get("visible"), "disabled": x.get("disabled"), "reasons": x.get("reasons")}
                for x in items
                if x["id"] == m
            ),
            {"visible": None, "note": "menu_id_not_in_matrix"},
        )
        for m in TARGET_MENUS
    }
    return {
        "label": scn["label"],
        "context": {k: v for k, v in scn.items() if k != "label"},
        "counts": {"visible": len(visible), "disabled": len(disabled), "hidden": len(hidden)},
        "target_menus": target,
        "visible_menu_ids": visible,
        "hidden_menu_ids": hidden,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="offline menu visibility baseline")
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "mode": "offline_menu_policy_eval",
        "decision": "MENUVIS-DEC-07 (show-first) baseline",
        "target_menus": TARGET_MENUS,
        "scenarios": [_eval(s) for s in SCENARIOS],
    }

    out_path = (args.out or "").strip()
    if out_path:
        p = Path(out_path)
        if not p.is_absolute():
            p = ROOT / p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload["saved_to"] = out_path

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
