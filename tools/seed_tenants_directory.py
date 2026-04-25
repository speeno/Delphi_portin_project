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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTE_MATRIX = ROOT / "analysis" / "welove_db_route_matrix.json"
BUILDS = ROOT / "analysis" / "welove_chul_builds.json"
OUT = ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"

# account_family → (default_account_type, default_build_role)
_FAMILY_TYPE_MAP: dict[str, tuple[str, str]] = {
    "chul_09": ("T3", "warehouse_publisher"),
    "book_21": ("T3", "warehouse_publisher"),
    "book_07": ("T3", "warehouse_publisher"),
    "book_kb": ("T2_DIST", "distributor"),
    # chul_* 계열은 기본 T2_DIST (총판)
}

_DIST_FAMILIES = {f"chul_{i:02d}" for i in range(1, 9)} | {
    "chul_05", "chul_06", "chul_07", "chul_08"
}

_PUB_FAMILIES = {f"book_{i:02d}" for i in range(1, 14)} | {
    "book_10", "book_11", "book_12", "book_13",
    "book_91", "book_99", "book_bs", "book_gs", "book_js", "sky_01",
}


def _infer_account_type(family: str) -> tuple[str, str]:
    if family in _FAMILY_TYPE_MAP:
        return _FAMILY_TYPE_MAP[family]
    if family in _DIST_FAMILIES or family.startswith("chul_"):
        return "T2_DIST", "distributor"
    if family in _PUB_FAMILIES or family.startswith("book_"):
        return "T3", "publisher"
    return "T3", "publisher"


def _make_tenant_id(label: str, family: str) -> str:
    """결정적 UUID v5 — 동일 (label, family) 는 항상 동일 ID."""
    ns = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # URL namespace
    return str(uuid.uuid5(ns, f"{label}|{family}"))


def main() -> None:
    route_data = json.loads(ROUTE_MATRIX.read_text(encoding="utf-8"))
    routes: list[dict] = route_data.get("routes", [])

    build_data = json.loads(BUILDS.read_text(encoding="utf-8"))
    builds: list[dict] = build_data.get("builds", [])

    # build_id lookup by account_family + build_role
    build_by_family_role: dict[tuple[str, str], str] = {}
    for b in builds:
        family = b.get("account_family") or ""
        role = b.get("build_role") or ""
        bid = b.get("build_id") or ""
        if family and role and bid:
            build_by_family_role[(family, role)] = bid

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
        build_id = build_by_family_role.get((family, build_role))
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
        })

    out = {
        "schema_version": "1.0.0",
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "note": "자격증명 0건 — secrets-policy.md G3 준수. DB 연결 자격증명은 vault/환경변수에만 존재.",
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
