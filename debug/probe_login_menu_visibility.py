"""로그인 계정별 메뉴 가시성 프로브 (경리부/서브계정 패턴 진단).

사용 예:

    export PROBE_BASE=http://localhost:8000
    export PROBE_USER_ID=경리부
    export PROBE_PASSWORD=pw
    export PROBE_TENANT_ID=fa6758ea-a7e5-5d27-bf87-ccee0a90e72c
    python3 debug/probe_login_menu_visibility.py

비교 모드 예:

    python3 debug/probe_login_menu_visibility.py \
      --user-id "교문사" \
      --password "pw" \
      --tenant-id "fa6758ea-a7e5-5d27-bf87-ccee0a90e72c" \
      --compare-user-id "경리부" \
      --compare-password "pw" \
      --out "analysis/audit/login-menu-visibility-probe-20260525.json"

산출:
- 로그인 응답 user/JWT 핵심 클레임
- menu_policy 기준 visible/disabled menu IDs
- 비교 모드 시 계정 간 visible/disabled diff
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import requests  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    print("[probe] requests 패키지가 필요합니다: pip install requests", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.core.menu_policy import MenuPolicyContext, build_nav_payload  # noqa: E402


def _decode_jwt_payload(token: str) -> dict[str, Any]:
    try:
        chunks = token.split(".")
        if len(chunks) < 2:
            return {}
        payload = chunks[1]
        padding = "=" * ((4 - len(payload) % 4) % 4)
        raw = base64.urlsafe_b64decode(payload + padding)
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


def _env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="login menu visibility probe")
    parser.add_argument("--base", default=_env("PROBE_BASE", "http://localhost:8000"))
    parser.add_argument("--user-id", default=_env("PROBE_USER_ID"))
    parser.add_argument("--password", default=_env("PROBE_PASSWORD"))
    parser.add_argument("--tenant-id", default=_env("PROBE_TENANT_ID"))
    parser.add_argument("--hcode", default=_env("PROBE_HCODE"))
    parser.add_argument("--compare-user-id", default=_env("PROBE_COMPARE_USER_ID"))
    parser.add_argument("--compare-password", default=_env("PROBE_COMPARE_PASSWORD"))
    parser.add_argument("--compare-tenant-id", default=_env("PROBE_COMPARE_TENANT_ID"))
    parser.add_argument("--compare-hcode", default=_env("PROBE_COMPARE_HCODE"))
    parser.add_argument("--out", default=_env("PROBE_OUT"))
    return parser


def _probe_login(
    *,
    base: str,
    user_id: str,
    password: str,
    tenant_id: str = "",
    hcode: str = "",
) -> tuple[int, dict[str, Any]]:
    payload: dict[str, Any] = {"userId": user_id, "password": password}
    if tenant_id:
        payload["tenantId"] = tenant_id
    if hcode:
        payload["hcode"] = hcode

    res = requests.post(f"{base.rstrip('/')}/api/v1/auth/login", json=payload, timeout=10)
    body: dict[str, Any]
    try:
        body = res.json()
    except Exception:
        body = {"_raw": res.text[:500]}
    if res.status_code != 200:
        return (
            res.status_code,
            {
                "login_request": {
                    "base": base,
                    "user_id": user_id,
                    "tenant_id": tenant_id or None,
                    "hcode": hcode or None,
                },
                "status": res.status_code,
                "error_body": body,
            },
        )

    user = body.get("user") or {}
    access_token = str(body.get("access_token") or "")
    jwt_payload = _decode_jwt_payload(access_token)

    ctx = MenuPolicyContext(
        account_type=(user.get("account_type") or "").strip() or None,
        build_role=(user.get("build_role") or "").strip() or None,
        warehouse_menu_tier=(user.get("warehouse_menu_tier") or "").strip() or None,
        login_profile=(user.get("login_profile") or "").strip() or None,
        license_keys=frozenset(user.get("license_keys") or []),
        is_super_user=(
            (user.get("role") == "admin")
            or ((user.get("hcode") or "").strip() == "0000")
            or ("*" in (user.get("permissions") or []))
        ),
        active_build_id=(user.get("active_build_id") or "").strip() or None,
    )
    nav = build_nav_payload(ctx)
    visible = [x["id"] for x in nav.get("items", []) if x.get("visible")]
    disabled = [x["id"] for x in nav.get("items", []) if x.get("visible") and x.get("disabled")]

    return (
        200,
        {
            "login_request": {
                "base": base,
                "user_id": user_id,
                "tenant_id": tenant_id or None,
                "hcode": hcode or None,
            },
            "user_claims": {
                "account_type": user.get("account_type"),
                "build_role": user.get("build_role"),
                "warehouse_menu_tier": user.get("warehouse_menu_tier"),
                "login_profile": user.get("login_profile"),
                "menu_shell_hint": user.get("menu_shell_hint"),
                "license_keys_sample": list(user.get("license_keys") or [])[:12],
                "permissions_sample": list(user.get("permissions") or [])[:12],
                "active_build_id": user.get("active_build_id"),
            },
            "jwt_claims": {
                "sid": jwt_payload.get("sid"),
                "account_type": jwt_payload.get("account_type"),
                "build_role": jwt_payload.get("build_role"),
                "warehouse_menu_tier": jwt_payload.get("warehouse_menu_tier"),
                "login_profile": jwt_payload.get("login_profile"),
                "menu_shell_hint": jwt_payload.get("menu_shell_hint"),
            },
            "menu_visibility": {
                "visible_count": len(visible),
                "disabled_count": len(disabled),
                "visible_menu_ids": visible,
                "disabled_menu_ids": disabled,
            },
        },
    )


def _diff_lists(left: list[str], right: list[str]) -> dict[str, list[str]]:
    left_set = set(left)
    right_set = set(right)
    return {
        "left_only": sorted(left_set - right_set),
        "right_only": sorted(right_set - left_set),
        "both": sorted(left_set & right_set),
    }


def _write_output(path: str, payload: dict[str, Any]) -> None:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = _build_parser().parse_args()
    base = (args.base or "").strip().rstrip("/")
    user_id = (args.user_id or "").strip()
    password = (args.password or "").strip()
    tenant_id = (args.tenant_id or "").strip()
    hcode = (args.hcode or "").strip()
    cmp_user_id = (args.compare_user_id or "").strip()
    cmp_password = (args.compare_password or password).strip()
    cmp_tenant_id = (args.compare_tenant_id or tenant_id).strip()
    cmp_hcode = (args.compare_hcode or hcode).strip()

    if not user_id or not password:
        print("[probe] user-id/password 또는 PROBE_USER_ID/PROBE_PASSWORD 가 필요합니다.", file=sys.stderr)
        return 2
    if cmp_user_id and not cmp_password:
        print("[probe] compare-user-id 지정 시 compare-password(또는 password)가 필요합니다.", file=sys.stderr)
        return 2

    status_main, result_main = _probe_login(
        base=base,
        user_id=user_id,
        password=password,
        tenant_id=tenant_id,
        hcode=hcode,
    )

    output: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "mode": "compare" if cmp_user_id else "single",
        "primary": result_main,
    }
    status_codes = [status_main]

    if cmp_user_id:
        status_cmp, result_cmp = _probe_login(
            base=base,
            user_id=cmp_user_id,
            password=cmp_password,
            tenant_id=cmp_tenant_id,
            hcode=cmp_hcode,
        )
        output["compare"] = result_cmp
        status_codes.append(status_cmp)

        primary_visible = list(((result_main.get("menu_visibility") or {}).get("visible_menu_ids") or []))
        compare_visible = list(((result_cmp.get("menu_visibility") or {}).get("visible_menu_ids") or []))
        primary_disabled = list(((result_main.get("menu_visibility") or {}).get("disabled_menu_ids") or []))
        compare_disabled = list(((result_cmp.get("menu_visibility") or {}).get("disabled_menu_ids") or []))
        output["diff"] = {
            "visible_menu_ids": _diff_lists(primary_visible, compare_visible),
            "disabled_menu_ids": _diff_lists(primary_disabled, compare_disabled),
        }

    out_path = (args.out or "").strip()
    if out_path:
        _write_output(out_path, output)
        output["saved_to"] = out_path

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if all(code == 200 for code in status_codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
