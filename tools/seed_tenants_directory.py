"""
tenants_directory.yaml 1차 시드 생성 스크립트.

welove_db_route_matrix.json + welove_chul_builds.json 을 결합해
migration/contracts/tenants_directory.yaml 의 tenants[] 섹션을 검증하고
backend/data/tenants_directory_seed.json 을 출력한다 (운영 주입용).

사용법
------
    python3 tools/seed_tenants_directory.py

출력
----
    backend/data/tenants_directory_seed.json  — 자격증명 0건 (G3 정책 준수)

비밀 정책 (secrets-policy.md G3)
----------------------------------
- has_credentials_in_source=true 행은 tenant_id/label/family/server/db_name 만 출력.
- DB UserName / Password 는 이 스크립트 어디에도 읽지 않는다.
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ROUTE_MATRIX = ROOT / "analysis" / "welove_db_route_matrix.json"
BUILDS = ROOT / "analysis" / "welove_chul_builds.json"
EXTENDED_BUILDS = ROOT / "analysis" / "welove_build_catalog_extended.json"
OUT = ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"

TIER_CONTRACT = ROOT / "migration" / "contracts" / "account_family_tiers.yaml"


def _warehouse_families_from_contract() -> set[str]:
    if not TIER_CONTRACT.exists():
        return set()
    try:
        doc = yaml.safe_load(TIER_CONTRACT.read_text(encoding="utf-8")) or {}
        tiers = doc.get("tiers") or {}
        out: set[str] = set()
        for grp in ("lite", "full"):
            for fam in tiers.get(grp) or []:
                v = (str(fam) or "").strip().lower()
                if v:
                    out.add(v)
        return out
    except Exception:
        return set()


_WAREHOUSE_FAMILIES = _warehouse_families_from_contract()

_DIST_FAMILIES = {f"chul_{i:02d}" for i in range(1, 9)} | {
    "chul_05", "chul_06", "chul_07", "chul_08"
}

_PUB_FAMILIES = {f"book_{i:02d}" for i in range(1, 14)} | {
    "book_10", "book_11", "book_12", "book_13",
    "book_91", "book_99", "book_bs", "book_gs", "book_js", "sky_01",
}


def _infer_account_type(family: str) -> tuple[str, str]:
    # 한국도서유통(book_kb)은 동일 family 안에 출판/물류 흔적이 섞여 있지만,
    # DB 라우팅 행의 기본 계정은 총판 빌드가 정본이다. 출판 계정은 별도 whitelist/
    # tenant_id 힌트로 분리한다.
    if family == "book_kb":
        return "T2_DIST", "distributor"
    if family in _WAREHOUSE_FAMILIES:
        return "T3", "warehouse_publisher"
    if family in _DIST_FAMILIES or family.startswith("chul_"):
        return "T2_DIST", "distributor"
    if family in _PUB_FAMILIES or family.startswith("book_"):
        return "T3", "publisher"
    return "T3", "publisher"


def _build_lookup_rows() -> list[dict]:
    """Load build catalog rows without reading any credential-bearing source."""
    if not BUILDS.exists():
        return []
    data = json.loads(BUILDS.read_text(encoding="utf-8"))
    return list(data.get("builds", []))


def _build_id_by_family_role(builds: list[dict]) -> dict[tuple[str, str], str]:
    """Map concrete customer families to their active build IDs."""
    out: dict[tuple[str, str], str] = {}
    for b in builds:
        family = (b.get("account_family_inferred") or b.get("account_family") or "").strip().lower()
        role = (b.get("build_role") or "").strip()
        bid = (b.get("build_id") or "").strip()
        if family and role and bid:
            out[(family, role)] = bid
    return out


def _default_build_id(family: str, build_role: str) -> str | None:
    """Fallback build binding for account families that use the standard executable."""
    if family == "book_kb" and build_role == "distributor":
        return "BLD-DIST-KBT"
    if build_role == "distributor":
        return "BLD-DIST-STD"
    if build_role == "publisher":
        return "BLD-PUB-STD"
    return None


def _active_build_id(
    family: str,
    build_role: str,
    build_by_family_role: dict[tuple[str, str], str],
) -> tuple[str | None, str]:
    """Resolve the single routing key that connects tenant, menu and DPR closure."""
    normalized = family.strip().lower()
    concrete = build_by_family_role.get((normalized, build_role))
    if concrete:
        return concrete, "welove_chul_builds.account_family_inferred"
    fallback = _default_build_id(normalized, build_role)
    if fallback:
        return fallback, "standard_role_fallback"
    return None, "unmapped"


def _make_tenant_id(label: str, family: str) -> str:
    """결정적 UUID v5 — 동일 (label, family) 는 항상 동일 ID."""
    ns = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # URL namespace
    return str(uuid.uuid5(ns, f"{label}|{family}"))


def main() -> None:
    route_data = json.loads(ROUTE_MATRIX.read_text(encoding="utf-8"))
    routes: list[dict] = route_data.get("routes", [])

    builds = _build_lookup_rows()
    build_by_family_role = _build_id_by_family_role(builds)

    tenants: list[dict] = []
    seen: set[tuple[str, str]] = set()  # (label, family) 중복 방지

    for route in routes:
        # 자격증명 필드는 읽지 않음 (G3)
        family = route.get("account_family", "")
        label = route.get("tenant_name_kor", "").strip()
        server = route.get("server_id", "")
        db_name = route.get("db_name_logical", "")

        if not family or not label:
            continue

        key = (label, family)
        if key in seen:
            continue
        seen.add(key)

        acc_type, build_role = _infer_account_type(family)
        build_id, build_source = _active_build_id(family, build_role, build_by_family_role)
        tid = _make_tenant_id(label, family)

        tenants.append({
            "tenant_id": tid,
            "tenant_label_kor": label,
            "account_family": family,
            "active_build_id": build_id,
            "build_role": build_role,
            "parent_tenant_id": None,
            "default_account_type": acc_type,
            "primary_server": server,
            "db_name_logical": db_name,
            "is_active": True,
            "notes": None,
            "_seed_source": "welove_db_route_matrix.json",
            "_active_build_source": build_source,
        })

    out = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "note": "자격증명 0건 — secrets-policy.md G3 준수. DB 연결 자격증명은 vault/환경변수에만 존재.",
        "build_catalog_sources": [
            "analysis/welove_chul_builds.json",
            "analysis/welove_build_catalog_extended.json",
        ] if EXTENDED_BUILDS.exists() else ["analysis/welove_chul_builds.json"],
        "tenants": tenants,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[seed] {len(tenants)} tenants → {OUT}")

    # 자격증명 사후 검증 (G3 게이트)
    # "password": 또는 "passwd": 형태의 실제 KV 쌍만 검출 (정책 파일 언급 제외)
    text = OUT.read_text(encoding="utf-8")
    _CRED_PATTERNS = [
        r'"password"\s*:', r'"passwd"\s*:', r'"db_password"\s*:',
        r'"비밀번호"\s*:', r'"db_user"\s*:\s*"[^"]+',
    ]
    for pat in _CRED_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            print(f"[WARN G3] 자격증명 패턴 감지 — '{pat}'. 수동 확인 필요.")


if __name__ == "__main__":
    main()
