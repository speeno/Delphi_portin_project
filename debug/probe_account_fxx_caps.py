#!/usr/bin/env python3
"""계정별 Id_Logn Fxx 전수 덤프 + caps 매트릭스 (Phase A — account-menu-fxx-rbac).

레거시 메뉴/기능 권한은 로그인 행별 ``Id_Logn.Fxx`` (F11~F89, O/R/X) 로 결정한다.
게이팅 키는 4-tuple ``Hcode+Gname+Gcode+Gpass`` (``Base01.pas`` ``Seek_Uses``).

본 스크립트는 **read-only** 로 전 서버 Id_Logn 을 스캔해 다음 산출물을 만든다.

- ``analysis/audit/account-menu-fxx-all.json`` — 전 로그인 행 Fxx + 파생 caps
- ``analysis/audit/account-menu-fxx-5019.json`` — 교문사(5019)·경리부·교문사 전자책(5097) 집중 diff
- f-컬럼 인벤토리·카탈로그 정합·5097 overlay/manifest 미등록 갭 기록

라이브 DB 필요 — CI 자동 실행 X. 운영자가 read-only 환경에서 수동 실행.

사용
----
    PYTHONPATH=도서물류관리프로그램/backend \\
        python3 debug/probe_account_fxx_caps.py

    # 서버·출력 경로 지정
    PYTHONPATH=도서물류관리프로그램/backend \\
        python3 debug/probe_account_fxx_caps.py \\
        --servers remote_138,remote_153,remote_154,remote_155 \\
        --out-all analysis/audit/account-menu-fxx-all.json \\
        --out-focus analysis/audit/account-menu-fxx-5019.json

    # (선택) 집중 계정 JWT 클레임 비교 — 자격증명은 환경변수만
    PROBE_BASE=http://localhost:8000 \\
    PROBE_GYOMUNSA_PASSWORD=... PROBE_GYEONGRI_PASSWORD=... PROBE_EBOOK_PASSWORD=... \\
        python3 debug/probe_account_fxx_caps.py --jwt-probe
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

DEFAULT_SERVERS = ("remote_138", "remote_153", "remote_154", "remote_155")
OUT_ALL_DEFAULT = ROOT / "analysis" / "audit" / "account-menu-fxx-all.json"
OUT_FOCUS_DEFAULT = ROOT / "analysis" / "audit" / "account-menu-fxx-5019.json"

DATA = BACKEND / "data"
TENANTS_OVERLAY = DATA / "tenants_directory_overlay.json"
TENANTS_SEED = DATA / "tenants_directory_seed.json"
ACCOUNT_OVERLAY = DATA / "account_directory_overlay.json"
LOGIN_ID_INDEX = DATA / "login_id_index.json"
PARITY_MANIFEST = ROOT / "migration" / "contracts" / "tenant_master_parity_manifest.yaml"

FOCUS_LOGINS = ("교문사", "경리부", "교문사 전자책")
FOCUS_HCODES = ("5019", "5097")

# 카탈로그 §1+§4 정본 fkey 집합 (오프라인 폴백·정합 검사용).
_CATALOG_FKEYS_FALLBACK: frozenset[str] = frozenset(
    {
        "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F18r", "F19",
        "F21", "F22", "F23", "F24", "F25", "F26", "F27", "F28", "F29",
        "F31", "F32", "F33", "F34", "F35", "F36", "F37", "F38", "F39",
        "F41", "F42", "F43", "F44", "F45", "F46", "F47", "F48", "F49",
        "F50", "F51", "F52", "F53", "F54", "F55", "F56", "F57", "F58", "F59",
        "F51e", "F52e", "F53e", "F90", "F91", "F92",
    }
)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_str(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, bytes):
        return val.decode("euc-kr", errors="replace").strip()
    return str(val).strip()


def _gpass_fingerprint(gpass: Any) -> str:
    """비밀번호 원문 저장 없이 4-key 정합용 짧은 지문."""
    raw = _safe_str(gpass)
    if not raw:
        return "empty"
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:16]


def _load_catalog_fkeys() -> frozenset[str]:
    try:
        from app.services import admin_service  # noqa: PLC0415

        keys = {
            str(row.get("fkey") or "").strip()
            for row in admin_service.list_legacy_permission_map()
            if row.get("fkey")
        }
        return frozenset(keys) if keys else _CATALOG_FKEYS_FALLBACK
    except Exception:
        return _CATALOG_FKEYS_FALLBACK


def _load_catalog_index() -> dict[str, str]:
    try:
        from app.services.auth_service import _load_legacy_permission_index  # noqa: PLC0415

        return _load_legacy_permission_index()
    except Exception:
        from app.services import admin_service  # noqa: PLC0415

        try:
            return {
                str(row["fkey"]): str(row["permission_code"])
                for row in admin_service._DEFAULT_LEGACY_PERMISSION_MAP
            }
        except Exception:
            return {}


def derive_fkey_caps(fxx_val: str) -> dict[str, bool]:
    """레거시 O/R/X → read/write/print caps (print = read-level).

    DEC-RBAC-04 Phase 1 정합 — 본 함수는 백엔드 단일 정본
    [`app.core.fxx_caps.derive_fkey_caps`](../도서물류관리프로그램/backend/app/core/fxx_caps.py)
    의 얇은 thin re-export 다 (probe 가 백엔드 sys.path 에 들어 있으므로 import 가능).
    구 시그니처(`fxx_val: str`) 를 보존해 회귀 가드 `test_probe_account_fxx_caps` 는 무수정 통과.
    """
    from app.core.fxx_caps import derive_fkey_caps as _derive  # noqa: PLC0415
    return _derive(fxx_val)


def derive_account_derivation(
    fxx: dict[str, str],
    catalog: dict[str, str],
) -> dict[str, Any]:
    from app.core.auth_provider import parse_fxx_row  # noqa: PLC0415
    from app.services.auth_service import (  # noqa: PLC0415
        _merge_fxx_to_permissions,
        infer_login_profile,
        menu_shell_hint_for_login_profile,
        merge_license_keys,
    )

    # parse_fxx_row 는 이미 정규화된 fxx 에도 무해.
    norm = parse_fxx_row({k: v for k, v in fxx.items()})
    role, permissions = _merge_fxx_to_permissions(norm, catalog)
    login_profile = infer_login_profile(norm)
    license_keys = merge_license_keys([], norm)

    caps_by_fkey: dict[str, dict[str, bool]] = {}
    caps_by_permission: dict[str, dict[str, bool]] = {}
    unmapped_fkeys: list[str] = []

    for fkey, val in sorted(norm.items()):
        caps_by_fkey[fkey] = derive_fkey_caps(val)
        if fkey not in catalog:
            unmapped_fkeys.append(fkey)
            continue
        code = catalog[fkey]
        v = (val or "").strip().upper()
        if v == "O":
            perm_cap = {"read": True, "write": True, "print": True}
        elif v == "R":
            if code.endswith(".write"):
                read_code = code[: -len(".write")] + ".read"
                perm_cap = {"read": True, "write": False, "print": True}
                caps_by_permission[read_code] = {"read": True, "write": False, "print": True}
            else:
                perm_cap = {"read": True, "write": False, "print": True}
        else:
            perm_cap = {"read": False, "write": False, "print": False}
        caps_by_permission[code] = perm_cap

    return {
        "role": role or None,
        "permissions": permissions,
        "license_keys": license_keys,
        "login_profile": login_profile,
        "menu_shell_hint": menu_shell_hint_for_login_profile(login_profile),
        "caps_by_fkey": caps_by_fkey,
        "caps_by_permission": caps_by_permission,
        "unmapped_fkeys": sorted(unmapped_fkeys),
    }


def build_four_key(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "hcode": _safe_str(row.get("hcode") or row.get("Hcode")),
        "gname": _safe_str(row.get("gname") or row.get("Gname")),
        "gcode": _safe_str(row.get("gcode") or row.get("Gcode")),
        "gpass_fingerprint": _gpass_fingerprint(row.get("gpass") or row.get("Gpass")),
    }


def inventory_f_columns(column_rows: list[dict[str, Any]], catalog_fkeys: frozenset[str]) -> dict[str, Any]:
    from app.core.auth_provider import _normalize_fxx_column_name  # noqa: PLC0415

    raw_cols: list[str] = []
    normalized: list[str] = []
    for r in column_rows:
        col = _safe_str(r.get("Field") or r.get("field"))
        if not col:
            continue
        raw_cols.append(col)
        fkey = _normalize_fxx_column_name(col)
        if fkey:
            normalized.append(fkey)

    norm_set = sorted(set(normalized))
    in_db_not_catalog = sorted(set(norm_set) - catalog_fkeys)
    in_catalog_not_db = sorted(catalog_fkeys - set(norm_set))
    matched = sorted(set(norm_set) & catalog_fkeys)

    return {
        "raw_f_columns": sorted(raw_cols),
        "normalized_fkeys": norm_set,
        "catalog_alignment": {
            "matched_count": len(matched),
            "matched_sample": matched[:20],
            "in_db_not_in_catalog": in_db_not_catalog,
            "in_catalog_not_in_db": in_catalog_not_db,
        },
    }


async def _fetch_id_logn_columns(server_id: str) -> list[dict[str, Any]]:
    from app.core.db import execute_query  # noqa: PLC0415

    return await execute_query(server_id, "SHOW COLUMNS FROM Id_Logn", ())


async def _fetch_id_logn_rows(server_id: str) -> list[dict[str, Any]]:
    from app.core.db import execute_query  # noqa: PLC0415

    return await execute_query(server_id, "SELECT * FROM Id_Logn ORDER BY id", ())


def _row_to_account_entry(row: dict[str, Any], catalog: dict[str, str]) -> dict[str, Any]:
    from app.core.auth_provider import parse_fxx_row  # noqa: PLC0415

    fxx = parse_fxx_row(row)
    four_key = build_four_key(row)
    derived = derive_account_derivation(fxx, catalog)
    return {
        "id": row.get("id") or row.get("Id"),
        "four_key": four_key,
        "hname": _safe_str(row.get("hname") or row.get("Hname")),
        "gmemo": _safe_str(row.get("gmemo") or row.get("Gmemo")),
        "fxx": fxx,
        "derived": derived,
    }


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _collect_hcode_in_from_tenants() -> dict[str, list[dict[str, Any]]]:
    """hcode → tenant 행 목록 (seed+overlay 병합)."""
    seed_rows = _load_json(TENANTS_SEED).get("tenants") or []
    overlay_rows = _load_json(TENANTS_OVERLAY).get("tenants") or []
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for row in seed_rows:
        key = (
            str(row.get("tenant_id") or "").strip(),
            str(row.get("account_family") or "").strip(),
        )
        merged[key] = dict(row)
    for row in overlay_rows:
        key = (
            str(row.get("tenant_id") or "").strip(),
            str(row.get("account_family") or "").strip(),
        )
        base = dict(merged.get(key, {}))
        base.update(row)
        merged[key] = base

    by_hcode: dict[str, list[dict[str, Any]]] = {}
    for row in merged.values():
        hcode_in = row.get("hcode_in") or []
        if isinstance(hcode_in, str):
            hcode_in = [hcode_in]
        for hc in hcode_in:
            hc_s = str(hc or "").strip()
            if not hc_s:
                continue
            by_hcode.setdefault(hc_s, []).append(
                {
                    "tenant_id": row.get("tenant_id"),
                    "label": row.get("label") or row.get("tenant_slug"),
                    "account_family": row.get("account_family"),
                    "hcode_in": list(hcode_in),
                }
            )
    return by_hcode


def audit_tenant_registration_gaps(
    *,
    hcode: str,
    login_id: str,
    hname: str | None = None,
) -> dict[str, Any]:
    """5097 등 격리 키의 overlay/manifest/index 미등록 갭."""
    gaps: list[dict[str, Any]] = []
    hcode_s = (hcode or "").strip()
    login_s = (login_id or "").strip()

    tenants_by_hcode = _collect_hcode_in_from_tenants()
    if hcode_s and hcode_s not in tenants_by_hcode:
        gaps.append(
            {
                "registry": "tenants_directory_overlay",
                "status": "missing_hcode_in",
                "detail": f"hcode {hcode_s} 가 seed+overlay hcode_in 에 없음",
            }
        )
    elif hcode_s in tenants_by_hcode:
        gaps.append(
            {
                "registry": "tenants_directory_overlay",
                "status": "registered",
                "tenants": tenants_by_hcode[hcode_s],
            }
        )

    manifest = {}
    if PARITY_MANIFEST.is_file():
        manifest = yaml.safe_load(PARITY_MANIFEST.read_text(encoding="utf-8")) or {}
    parity_cases = manifest.get("cases") or []
    parity_match = [
        c
        for c in parity_cases
        if str(c.get("canonical_hq_hcode") or "").strip() == hcode_s
        or login_s in str(c.get("label") or "")
        or (hname and hname in str(c.get("label") or ""))
    ]
    if not parity_match:
        gaps.append(
            {
                "registry": "tenant_master_parity_manifest",
                "status": "no_case",
                "detail": f"hcode={hcode_s} login={login_s!r} 전용 parity case 없음",
            }
        )
    else:
        gaps.append(
            {
                "registry": "tenant_master_parity_manifest",
                "status": "registered",
                "cases": [c.get("case") for c in parity_match],
            }
        )

    account_overrides = _load_json(ACCOUNT_OVERLAY).get("overrides") or []
    acct_match = [
        o
        for o in account_overrides
        if str(o.get("gcode") or "").strip() == login_s
        or str(o.get("hcode") or "").strip() == hcode_s
    ]
    if not acct_match:
        gaps.append(
            {
                "registry": "account_directory_overlay",
                "status": "missing",
                "detail": f"gcode={login_s!r} hcode={hcode_s} override 없음",
            }
        )
    else:
        gaps.append(
            {
                "registry": "account_directory_overlay",
                "status": "registered",
                "overrides": acct_match,
            }
        )

    index_doc = _load_json(LOGIN_ID_INDEX)
    index_entry = (index_doc.get("by_login_id") or {}).get(login_s)
    if index_entry is None:
        gaps.append(
            {
                "registry": "login_id_index",
                "status": "missing",
                "detail": f"login_id {login_s!r} 없음",
            }
        )
    else:
        index_hcode = ""
        if isinstance(index_entry, dict):
            index_hcode = str(index_entry.get("hcode") or "").strip()
        elif isinstance(index_entry, list) and index_entry:
            index_hcode = str((index_entry[0] or {}).get("hcode") or "").strip()
        wrong_tid_note = None
        if hcode_s and index_hcode and index_hcode != hcode_s:
            wrong_tid_note = f"index hcode={index_hcode} ≠ live hcode={hcode_s}"
        gaps.append(
            {
                "registry": "login_id_index",
                "status": "present",
                "entry_hcode": index_hcode or None,
                "note": wrong_tid_note,
            }
        )

    return {
        "login_id": login_s,
        "hcode": hcode_s,
        "hname": hname,
        "gaps": gaps,
        "has_blocking_gap": any(
            g.get("status") in ("missing_hcode_in", "no_case", "missing")
            for g in gaps
            if g.get("registry")
            in (
                "tenants_directory_overlay",
                "tenant_master_parity_manifest",
                "account_directory_overlay",
            )
        ),
    }


def _diff_fxx(left: dict[str, str], right: dict[str, str]) -> dict[str, Any]:
    keys = sorted(set(left) | set(right))
    only_left: dict[str, str] = {}
    only_right: dict[str, str] = {}
    value_diff: dict[str, dict[str, str]] = {}
    for k in keys:
        lv = left.get(k)
        rv = right.get(k)
        if lv and not rv:
            only_left[k] = lv
        elif rv and not lv:
            only_right[k] = rv
        elif lv != rv:
            value_diff[k] = {"left": lv or "", "right": rv or ""}
    return {
        "only_left": only_left,
        "only_right": only_right,
        "value_diff": value_diff,
        "same_count": sum(1 for k in keys if left.get(k) == right.get(k) and left.get(k)),
    }


def _find_focus_accounts(all_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for server_id, srv in (all_payload.get("servers") or {}).items():
        for entry in srv.get("login_rows") or []:
            gcode = (entry.get("four_key") or {}).get("gcode") or ""
            hcode = (entry.get("four_key") or {}).get("hcode") or ""
            if gcode in FOCUS_LOGINS or hcode in FOCUS_HCODES:
                key = gcode or f"hcode:{hcode}"
                prev = found.get(key)
                # 동일 login 이 여러 서버에 있으면 remote_153 우선(교문사 집중 케이스).
                if prev is None or server_id == "remote_153":
                    found[key] = {
                        "server_id": server_id,
                        "database": srv.get("database"),
                        **entry,
                    }
    return found


def _build_focus_payload(all_payload: dict[str, Any]) -> dict[str, Any]:
    accounts = _find_focus_accounts(all_payload)
    diffs: dict[str, Any] = {}
    keys = sorted(accounts)
    for i, left_key in enumerate(keys):
        for right_key in keys[i + 1 :]:
            pair = f"{left_key}_vs_{right_key}"
            diffs[pair] = _diff_fxx(
                accounts[left_key].get("fxx") or {},
                accounts[right_key].get("fxx") or {},
            )

    registration_gaps: dict[str, Any] = {}
    ebook = accounts.get("교문사 전자책")
    if ebook:
        registration_gaps["hcode_5097"] = audit_tenant_registration_gaps(
            hcode=(ebook.get("four_key") or {}).get("hcode") or "5097",
            login_id="교문사 전자책",
            hname=ebook.get("hname"),
        )
    elif "5097" in FOCUS_HCODES:
        registration_gaps["hcode_5097"] = audit_tenant_registration_gaps(
            hcode="5097",
            login_id="교문사 전자책",
            hname=None,
        )

    gyomunsa = accounts.get("교문사")
    gyeongri = accounts.get("경리부")
    hcode_5019_diff = None
    if gyomunsa and gyeongri:
        hcode_5019_diff = _diff_fxx(
            gyomunsa.get("fxx") or {},
            gyeongri.get("fxx") or {},
        )

    return {
        "generated_at": all_payload.get("generated_at"),
        "source": str(OUT_ALL_DEFAULT.relative_to(ROOT)),
        "focus_logins": list(FOCUS_LOGINS),
        "focus_hcodes": list(FOCUS_HCODES),
        "accounts": accounts,
        "fxx_diff": diffs,
        "hcode_5019_gyomunsa_vs_gyeongri": hcode_5019_diff,
        "tenant_registration_gaps": registration_gaps,
    }


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


def _jwt_password_for(login_id: str) -> str:
    """자격증명 우선순위 — PROBE_* → BLS_PARITY_B4(교문사) → PROBE_PASSWORD."""
    keys_by_login: dict[str, list[str]] = {
        "교문사": ["PROBE_GYOMUNSA_PASSWORD", "BLS_PARITY_B4_PASSWORD", "PROBE_PASSWORD"],
        "경리부": ["PROBE_GYEONGRI_PASSWORD", "PROBE_PASSWORD"],
        "교문사 전자책": ["PROBE_EBOOK_PASSWORD", "PROBE_PASSWORD"],
    }
    for key in keys_by_login.get(login_id, ["PROBE_PASSWORD"]):
        val = (os.environ.get(key) or "").strip()
        if val:
            return val
    return ""


def _probe_jwt_claims(base: str) -> dict[str, Any]:
    try:
        import requests  # type: ignore[import-not-found]
    except ImportError:
        return {"error": "requests 패키지 없음 — pip install requests"}

    from app.core.config import load_config  # noqa: PLC0415

    load_config(force=True)

    probes = [
        (
            (os.environ.get("BLS_PARITY_B4_USER") or "교문사").strip() or "교문사",
            _jwt_password_for("교문사"),
        ),
        ("경리부", _jwt_password_for("경리부")),
        ("교문사 전자책", _jwt_password_for("교문사 전자책")),
    ]
    out: dict[str, Any] = {"base": base, "accounts": {}}
    for user_id, password in probes:
        if not password:
            out["accounts"][user_id] = {"skipped": True, "reason": "password env 미설정"}
            continue
        try:
            res = requests.post(
                f"{base.rstrip('/')}/api/v1/auth/login",
                json={"userId": user_id, "password": password},
                timeout=15,
            )
            body = res.json() if res.headers.get("content-type", "").startswith("application/json") else {}
        except Exception as exc:
            out["accounts"][user_id] = {"error": str(exc)}
            continue
        if res.status_code != 200:
            out["accounts"][user_id] = {"status": res.status_code, "error_body": body}
            continue
        user = body.get("user") or {}
        jwt_payload = _decode_jwt_payload(str(body.get("access_token") or ""))
        out["accounts"][user_id] = {
            "status": 200,
            "user_claims": {
                "account_type": user.get("account_type"),
                "build_role": user.get("build_role"),
                "warehouse_menu_tier": user.get("warehouse_menu_tier"),
                "login_profile": user.get("login_profile"),
                "menu_shell_hint": user.get("menu_shell_hint"),
                "hcode": user.get("hcode"),
                "tenant_id": user.get("tenant_id"),
                "license_keys_sample": list(user.get("license_keys") or [])[:16],
                "permissions_sample": list(user.get("permissions") or [])[:16],
            },
            "jwt_claims": {
                k: jwt_payload.get(k)
                for k in (
                    "sid",
                    "account_type",
                    "build_role",
                    "warehouse_menu_tier",
                    "login_profile",
                    "menu_shell_hint",
                    "hcode",
                    "tenant_id",
                )
            },
        }
    return out


async def probe_server(
    server_id: str,
    *,
    catalog: dict[str, str],
    catalog_fkeys: frozenset[str],
) -> dict[str, Any]:
    from app.core.config import get_server_profile  # noqa: PLC0415

    profile = get_server_profile(server_id) or {}
    out: dict[str, Any] = {
        "server_id": server_id,
        "label": profile.get("label"),
        "database": profile.get("database") or profile.get("db"),
        "mysql3_protocol": bool(profile.get("mysql3_protocol")),
    }
    try:
        col_rows = await _fetch_id_logn_columns(server_id)
        out["f_column_inventory"] = inventory_f_columns(col_rows, catalog_fkeys)
        rows = await _fetch_id_logn_rows(server_id)
        out["login_row_count"] = len(rows)
        out["login_rows"] = [_row_to_account_entry(r, catalog) for r in rows]
        out["ok"] = True
    except Exception as exc:
        out["ok"] = False
        out["error"] = f"{type(exc).__name__}: {exc}"
        out["login_rows"] = []
    return out


async def run_probe(
    server_ids: list[str],
    *,
    jwt_probe: bool = False,
    api_base: str = "",
) -> dict[str, Any]:
    from app.core.config import load_config  # noqa: PLC0415

    load_config(force=True)
    catalog = _load_catalog_index()
    catalog_fkeys = _load_catalog_fkeys()

    servers: dict[str, Any] = {}
    for sid in server_ids:
        servers[sid] = await probe_server(sid, catalog=catalog, catalog_fkeys=catalog_fkeys)

    payload: dict[str, Any] = {
        "generated_at": _utc_iso(),
        "schema_version": "1.0.0",
        "purpose": "Phase A — Id_Logn Fxx 전수 덤프 + caps (account-menu-fxx-rbac)",
        "catalog_fkey_count": len(catalog_fkeys),
        "servers": servers,
        "summary": {
            "server_count": len(server_ids),
            "servers_ok": sum(1 for s in servers.values() if s.get("ok")),
            "servers_failed": [sid for sid, s in servers.items() if not s.get("ok")],
            "partial": any(not s.get("ok") for s in servers.values()),
            "total_login_rows": sum(int(s.get("login_row_count") or 0) for s in servers.values()),
            "focus_hcodes": list(FOCUS_HCODES),
        },
    }

    # 전역 5097 갭 (라이브 행에서 hname 보강).
    ebook_row = None
    for srv in servers.values():
        for entry in srv.get("login_rows") or []:
            if (entry.get("four_key") or {}).get("gcode") == "교문사 전자책":
                ebook_row = entry
                break
    payload["tenant_registration_gaps"] = {
        "hcode_5097": audit_tenant_registration_gaps(
            hcode="5097",
            login_id="교문사 전자책",
            hname=(ebook_row or {}).get("hname"),
        )
    }

    if jwt_probe:
        base = (api_base or os.environ.get("PROBE_BASE") or "http://localhost:8000").strip()
        payload["jwt_probe"] = _probe_jwt_claims(base)

    return payload


def _merge_payload(existing: dict[str, Any], fresh: dict[str, Any], probed_ids: list[str]) -> dict[str, Any]:
    """기존 산출물에 이번에 probe 한 서버 결과만 병합."""
    merged = dict(existing)
    merged["generated_at"] = fresh.get("generated_at") or _utc_iso()
    merged["schema_version"] = fresh.get("schema_version") or merged.get("schema_version")
    merged["purpose"] = fresh.get("purpose") or merged.get("purpose")
    merged["catalog_fkey_count"] = fresh.get("catalog_fkey_count") or merged.get("catalog_fkey_count")

    servers: dict[str, Any] = dict(merged.get("servers") or {})
    for sid in probed_ids:
        if sid in fresh.get("servers", {}):
            servers[sid] = fresh["servers"][sid]
    merged["servers"] = servers

    all_ids = sorted(servers.keys())
    merged["summary"] = {
        "server_count": len(all_ids),
        "servers_ok": sum(1 for s in servers.values() if s.get("ok")),
        "servers_failed": [sid for sid, s in servers.items() if not s.get("ok")],
        "partial": any(not s.get("ok") for s in servers.values()),
        "total_login_rows": sum(int(s.get("login_row_count") or 0) for s in servers.values()),
        "focus_hcodes": list(FOCUS_HCODES),
        "probed_this_run": probed_ids,
    }

    # ebook hname 은 최신 라이브 행 우선.
    ebook_row = None
    for srv in servers.values():
        for entry in srv.get("login_rows") or []:
            if (entry.get("four_key") or {}).get("gcode") == "교문사 전자책":
                ebook_row = entry
                break
    merged["tenant_registration_gaps"] = {
        "hcode_5097": audit_tenant_registration_gaps(
            hcode="5097",
            login_id="교문사 전자책",
            hname=(ebook_row or {}).get("hname"),
        )
    }

    if "jwt_probe" in fresh:
        merged["jwt_probe"] = fresh["jwt_probe"]
    return merged


def _load_existing_payload(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Id_Logn Fxx 전수 덤프 + caps 매트릭스 (Phase A)")
    p.add_argument(
        "--servers",
        default=",".join(DEFAULT_SERVERS),
        help=f"쉼표 구분 server_id (기본: {','.join(DEFAULT_SERVERS)})",
    )
    p.add_argument("--out-all", default=str(OUT_ALL_DEFAULT), help="전수 매트릭스 출력 경로")
    p.add_argument("--out-focus", default=str(OUT_FOCUS_DEFAULT), help="5019/5097 집중 diff 출력 경로")
    p.add_argument(
        "--jwt-probe",
        action="store_true",
        help="집중 계정 /auth/login JWT 클레임 수집 (PROBE_*_PASSWORD 환경변수)",
    )
    p.add_argument("--api-base", default=os.environ.get("PROBE_BASE", "http://localhost:8000"))
    p.add_argument(
        "--merge-existing",
        action="store_true",
        help="기존 out-all JSON 에 이번 --servers 결과만 병합 (부분 재실행용)",
    )
    return p


def main() -> int:
    args = _build_parser().parse_args()
    server_ids = [s.strip() for s in (args.servers or "").split(",") if s.strip()]
    if not server_ids:
        print("[probe_account_fxx_caps] --servers 가 비어 있습니다.", file=sys.stderr)
        return 2

    out_all = Path(args.out_all)
    out_focus = Path(args.out_focus)
    if not out_all.is_absolute():
        out_all = ROOT / out_all
    if not out_focus.is_absolute():
        out_focus = ROOT / out_focus

    fresh_payload = asyncio.run(
        run_probe(server_ids, jwt_probe=bool(args.jwt_probe), api_base=args.api_base)
    )
    if args.merge_existing:
        existing = _load_existing_payload(out_all)
        all_payload = _merge_payload(existing, fresh_payload, server_ids) if existing else fresh_payload
    else:
        all_payload = fresh_payload

    focus_payload = _build_focus_payload(all_payload)
    if "jwt_probe" in all_payload:
        focus_payload["jwt_probe"] = all_payload["jwt_probe"]

    _write_json(out_all, all_payload)
    _write_json(out_focus, focus_payload)

    summary = all_payload.get("summary") or {}
    ok_count = int(summary.get("servers_ok") or 0)
    server_count = int(summary.get("server_count") or len(server_ids))
    total_rows = int(summary.get("total_login_rows") or 0)
    probed_ok = sum(1 for s in fresh_payload.get("servers", {}).values() if s.get("ok"))
    gap = all_payload.get("tenant_registration_gaps", {}).get("hcode_5097", {})
    gap_flag = gap.get("has_blocking_gap")

    print(
        f"[probe_account_fxx_caps] probed_ok={probed_ok}/{len(server_ids)} "
        f"aggregate_ok={ok_count}/{server_count} login_rows={total_rows}"
    )
    print(f"[probe_account_fxx_caps] wrote {out_all}")
    print(f"[probe_account_fxx_caps] wrote {out_focus}")
    print(f"[probe_account_fxx_caps] hcode_5097 blocking_gap={gap_flag}")

    if probed_ok < len(server_ids):
        failed = [sid for sid, s in fresh_payload.get("servers", {}).items() if not s.get("ok")]
        print(f"[probe_account_fxx_caps] FAILED servers (this run): {failed}", file=sys.stderr)
        for sid in failed:
            print(f"  - {sid}: {fresh_payload['servers'][sid].get('error')}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
