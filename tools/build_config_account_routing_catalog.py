#!/usr/bin/env python3
"""레거시 ``Config.Ini`` → 계정(테넌트/빌드)별 서버·DB 카탈로그 빌더.

원천(읽기 전용)
---------------
- ``analysis/welove_config_ini_inventory.json``
  ([`tools/inventory_legacy_config_ini.py`](inventory_legacy_config_ini.py) 산출 — 591 행).
- ``analysis/welove_db_route_matrix.json``                         (운영 라우트 정본 40 routes).
- ``도서물류관리프로그램/backend/data/tenants_directory_seed.json`` (+ 있으면 overlay 병합).
- ``WeLove_FTP/legacy_delphi_routing_defaults.json``               (Chul.pas 호스트/DB 정본 — 선택).

산출
----
- ``analysis/welove_config_account_routing_catalog.json``
  Config.Ini 1 행 = 카탈로그 1 행. 라우팅 결정 우선순위:

    1. ``account_family_inferred`` + matrix ``routes[]`` → primary_server_label / db_name_logical
    2. 동일 family seed tenants → tenant_id / tenant_label_kor
    3. ``build_subpath`` 매칭 Chul.pas row → host_ip → remote_id (matrix 교차 검증)
    4. ``Uses`` / ``Name`` 정규화 fuzzy → seed tenant_label_kor (sources: ``label_fuzzy``)
    5. ``config_kind`` ∈ {infra_mysql, infra_login, root_other} → ``infra_skip``

- ``analysis/welove_config_routing_review_queue.json``
  ``status == "review"`` 행만 SME 입력 큐로 분리.

dry-run overlay 제안 (사람 승인 필수)
--------------------------------------
``--emit-overlay <path>`` 사용 시 ``confidence=high`` 이고 matrix vs seed
``primary_server`` / ``db_name_logical`` 가 어긋나는 케이스만 제안 JSON 으로 출력한다.
실제 ``tenants_directory_overlay.json`` 병합은 [`apply_hcode_isolation_overlay.py`](apply_hcode_isolation_overlay.py)
패턴을 따른 별도 단계 (운영자 승인 후) 에서 진행 — 본 도구는 절대 직접 쓰지 않는다.

비밀 정책 (G3)
---------------
- ``UserName`` / ``Password`` / 호스트 비번을 일체 읽지 않는다 (input 도구들이 이미 G3 준수).
- 출력에 자격증명 0건. 본 도구는 메타·라우팅 라벨만 다룬다.

사용
----
    python3 tools/build_config_account_routing_catalog.py            # dry-run
    python3 tools/build_config_account_routing_catalog.py --apply    # 두 산출 JSON 저장
    python3 tools/build_config_account_routing_catalog.py --apply --emit-overlay /tmp/overlay_proposal.json
    python3 tools/build_config_account_routing_catalog.py --strict   # 행수 != inventory.count 일 때 exit 2
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY = REPO_ROOT / "analysis" / "welove_config_ini_inventory.json"
DEFAULT_MATRIX = REPO_ROOT / "analysis" / "welove_db_route_matrix.json"
DEFAULT_SEED = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)
DEFAULT_OVERLAY = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_overlay.json"
)
DEFAULT_CHUL_DEFAULTS = REPO_ROOT / "WeLove_FTP" / "legacy_delphi_routing_defaults.json"
DEFAULT_CATALOG_OUT = REPO_ROOT / "analysis" / "welove_config_account_routing_catalog.json"
DEFAULT_REVIEW_OUT = REPO_ROOT / "analysis" / "welove_config_routing_review_queue.json"

# ``tenants_directory_service._LABEL_TO_REMOTE_ID`` 와 동기.
_LABEL_TO_REMOTE_ID: dict[str, str] = {
    "서버1": "remote_154",
    "서버2": "remote_155",
    "서버3": "remote_153",
    "서버4": "remote_138",
}

# 카탈로그·overlay 단순화를 위한 status 상수.
STATUS_MATCHED = "matched"
STATUS_PARTIAL = "partial"
STATUS_REVIEW = "review"
STATUS_INFRA_SKIP = "infra_skip"

CONFIDENCE_HIGH = "high"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_LOW = "low"

_INFRA_KINDS = {"infra_mysql", "infra_login", "root_other"}


def label_to_remote_id(label: str | None) -> str | None:
    """``서버3`` 한국어 라벨 → ``remote_153`` (이미 ``remote_*`` 면 그대로)."""
    if not label:
        return None
    s = str(label).strip()
    if not s:
        return None
    if s in _LABEL_TO_REMOTE_ID:
        return _LABEL_TO_REMOTE_ID[s]
    if s.startswith("remote_"):
        return s
    return None


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        logger.warning("cannot load %s: %s", path, exc)
        return None


def _load_inventory_module():
    """``inventory_legacy_config_ini`` 모듈을 import 해 ``_normalize_label`` 재사용."""
    spec = importlib.util.spec_from_file_location(
        "inventory_legacy_config_ini",
        REPO_ROOT / "tools" / "inventory_legacy_config_ini.py",
    )
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("inventory_legacy_config_ini", mod)
    spec.loader.exec_module(mod)
    return mod


def _normalize_label(label: str) -> str:
    mod = _load_inventory_module()
    if mod and hasattr(mod, "_normalize_label"):
        return mod._normalize_label(label)
    return (label or "").strip().lower()


def _matrix_routes_by_family(matrix_doc: Any) -> dict[str, list[dict[str, Any]]]:
    """``account_family`` → routes[] 인덱스 (정본은 list[dict] 형식)."""
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not isinstance(matrix_doc, dict):
        return out
    for r in matrix_doc.get("routes", []) or []:
        af = (r.get("account_family") or "").strip().lower()
        if af:
            out[af].append(r)
    return out


def _seed_tenants_by_family(seed_doc: Any, overlay_doc: Any) -> dict[str, list[dict[str, Any]]]:
    """seed (+ overlay) 의 tenants[] 를 family 별로 그룹화. overlay 우선 병합."""
    by_key: dict[tuple[str, str], dict[str, Any]] = {}

    def _ingest(doc: Any) -> None:
        if not isinstance(doc, dict):
            return
        for t in doc.get("tenants", []) or []:
            key = ((t.get("tenant_id") or "").strip(), (t.get("account_family") or "").strip())
            merged = dict(by_key.get(key, {}))
            merged.update(t)
            by_key[key] = merged

    _ingest(seed_doc)
    _ingest(overlay_doc)
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for t in by_key.values():
        af = (t.get("account_family") or "").strip().lower()
        if af:
            out[af].append(t)
    return out


def _seed_labels(seed_doc: Any, overlay_doc: Any) -> list[tuple[str, dict[str, Any]]]:
    """``(normalized_label, tenant_dict)`` 쌍 — fuzzy 매칭용."""
    out: list[tuple[str, dict[str, Any]]] = []
    seen: set[tuple[str, str]] = set()
    for doc in (seed_doc, overlay_doc):
        if not isinstance(doc, dict):
            continue
        for t in doc.get("tenants", []) or []:
            label = (t.get("tenant_label_kor") or "").strip()
            tid = (t.get("tenant_id") or "").strip()
            key = (tid, label)
            if not label or key in seen:
                continue
            seen.add(key)
            n = _normalize_label(label)
            if n:
                out.append((n, t))
    return out


def _shared_db_index(seed_by_family: dict[str, list[dict[str, Any]]]) -> dict[tuple[str, str], int]:
    """``(primary_server, db_name_logical)`` → 활성 테넌트 수 (DSN-DEC-12 보조)."""
    counts: Counter[tuple[str, str]] = Counter()
    for tenants in seed_by_family.values():
        for t in tenants:
            if not t.get("is_active", True):
                continue
            key = (
                (t.get("primary_server") or "").strip(),
                (t.get("db_name_logical") or "").strip(),
            )
            if key[0] and key[1]:
                counts[key] += 1
    return dict(counts)


def _chul_rows_by_subpath(chul_doc: Any) -> dict[str, dict[str, Any]]:
    """Chul.pas defaults 행을 ``build_subpath`` (Chul.pas 의 부모 디렉터리) 키로 인덱스."""
    out: dict[str, dict[str, Any]] = {}
    if not isinstance(chul_doc, dict):
        return out
    for r in chul_doc.get("rows", []) or []:
        rel_path = (r.get("rel_path") or "").replace("\\", "/")
        if not rel_path:
            continue
        # rel_path = "도서유통-출판/MySQL/.../Chul.pas" → 부모 디렉터리 키
        parent = rel_path.rsplit("/", 1)[0] if "/" in rel_path else ""
        if parent:
            out.setdefault(parent, r)
    return out


def _label_fuzzy_match(
    candidates: list[str], pool: list[tuple[str, dict[str, Any]]]
) -> dict[str, Any] | None:
    """후보 텍스트가 정규화 라벨 풀과 부분 매치되면 첫 매치 tenant 반환."""
    for cand in candidates:
        n = _normalize_label(cand)
        if not n:
            continue
        for label_n, tenant in pool:
            if not label_n:
                continue
            if n == label_n or n in label_n or label_n in n:
                return tenant
    return None


def _route_summary(item: dict[str, Any]) -> dict[str, Any]:
    """카탈로그 ``routing`` 블록 (서버·DB·tenant 식별 라벨)."""
    return {
        "primary_server_label": item.get("primary_server_label") or "",
        "remote_id": item.get("remote_id") or "",
        "db_name_logical": item.get("db_name_logical") or "",
        "tenant_id": item.get("tenant_id") or "",
        "tenant_label_kor": item.get("tenant_label_kor") or "",
        "build_role": item.get("build_role") or "",
        "default_account_type": item.get("default_account_type") or "",
    }


def classify_row(
    row: dict[str, Any],
    *,
    matrix_by_family: dict[str, list[dict[str, Any]]],
    seed_by_family: dict[str, list[dict[str, Any]]],
    seed_label_pool: list[tuple[str, dict[str, Any]]],
    chul_by_subpath: dict[str, dict[str, Any]],
    shared_index: dict[tuple[str, str], int],
) -> dict[str, Any]:
    """단일 인벤토리 행 → 카탈로그 1 행."""
    config_path = (row.get("config_path") or "").strip()
    config_kind = (row.get("config_kind") or "").strip() or "customer_build"
    family = (row.get("account_family_inferred") or "").strip().lower() or None
    build_subpath = (row.get("build_subpath") or "").replace("\\", "/")
    name = (row.get("name") or "").strip()
    uses = (row.get("uses") or "").strip()

    sources: list[str] = []
    reasons: list[str] = []
    routing: dict[str, Any] = {}

    # 0) 인프라/비-고객 빌드 — 즉시 skip
    if config_kind in _INFRA_KINDS:
        return {
            "config_path": config_path,
            "config_kind": config_kind,
            "account_family_inferred": family,
            "customer_folder": row.get("customer_folder", ""),
            "client": _client_meta(row),
            "routing": _route_summary({}),
            "match": {
                "status": STATUS_INFRA_SKIP,
                "confidence": CONFIDENCE_LOW,
                "sources": [],
                "reasons": ["infra_or_root_template"],
            },
            "shared_db": {"is_shared": False, "needs_hcode_guard": False},
        }

    # 1) family + matrix → 1차 라우팅
    matrix_route: dict[str, Any] | None = None
    if family and family in matrix_by_family:
        matrix_route = matrix_by_family[family][0]
        sources.append("path_family")
        sources.append("matrix")
        primary_label = (matrix_route.get("server_id") or "").strip()
        routing["primary_server_label"] = primary_label
        routing["remote_id"] = label_to_remote_id(primary_label) or ""
        routing["db_name_logical"] = (matrix_route.get("db_name_logical") or "").strip()
        if not routing["remote_id"]:
            reasons.append("unknown_primary_server_label")

    # 2) seed tenants — tenant_id / tenant_label / build_role 보강
    seed_tenant: dict[str, Any] | None = None
    seed_candidates_for_family: list[dict[str, Any]] = (
        seed_by_family.get(family, []) if family else []
    )
    if seed_candidates_for_family:
        # primary_server 일치하는 후보 우선
        target_label = routing.get("primary_server_label", "")
        if target_label:
            for t in seed_candidates_for_family:
                if (t.get("primary_server") or "").strip() == target_label:
                    seed_tenant = t
                    break
        if seed_tenant is None:
            seed_tenant = seed_candidates_for_family[0]
        sources.append("seed")
        routing.setdefault("primary_server_label", (seed_tenant.get("primary_server") or "").strip())
        routing.setdefault("db_name_logical", (seed_tenant.get("db_name_logical") or "").strip())
        if not routing.get("remote_id"):
            routing["remote_id"] = label_to_remote_id(routing.get("primary_server_label")) or ""
        routing["tenant_id"] = (seed_tenant.get("tenant_id") or "").strip()
        routing["tenant_label_kor"] = (seed_tenant.get("tenant_label_kor") or "").strip()
        routing["build_role"] = (seed_tenant.get("build_role") or "").strip()
        routing["default_account_type"] = (seed_tenant.get("default_account_type") or "").strip()
        if len(seed_candidates_for_family) > 1:
            reasons.append("family_has_multiple_seed_tenants")

    # 3) Chul.pas 교차 검증 (선택)
    chul_row = chul_by_subpath.get(build_subpath)
    if chul_row:
        sources.append("chul_pas")
        chul_remote = (chul_row.get("remote_id") or "").strip()
        chul_db = (chul_row.get("database") or "").strip()
        cur_remote = routing.get("remote_id", "")
        cur_db = routing.get("db_name_logical", "")
        if chul_remote and cur_remote and chul_remote != cur_remote:
            reasons.append("chul_remote_id_mismatch")
        if chul_db and cur_db and chul_db != cur_db:
            reasons.append("chul_db_name_mismatch")
        if not cur_remote and chul_remote:
            routing["remote_id"] = chul_remote
        if not cur_db and chul_db:
            routing["db_name_logical"] = chul_db
        unknown_host = (chul_row.get("unknown_host_ip") or "").strip()
        if unknown_host:
            reasons.append(f"chul_unknown_host_ip:{unknown_host}")

    # 4) label fuzzy (보조 — DSN-DEC-06: 단독 결정 금지)
    fuzzy_tenant: dict[str, Any] | None = None
    if not seed_tenant:
        fuzzy_tenant = _label_fuzzy_match([uses, name, row.get("customer_folder", "")], seed_label_pool)
        if fuzzy_tenant:
            sources.append("label_fuzzy")
            routing.setdefault(
                "primary_server_label", (fuzzy_tenant.get("primary_server") or "").strip()
            )
            routing.setdefault(
                "db_name_logical", (fuzzy_tenant.get("db_name_logical") or "").strip()
            )
            if not routing.get("remote_id"):
                routing["remote_id"] = label_to_remote_id(routing.get("primary_server_label")) or ""
            routing["tenant_id"] = (fuzzy_tenant.get("tenant_id") or "").strip()
            routing["tenant_label_kor"] = (fuzzy_tenant.get("tenant_label_kor") or "").strip()
            routing.setdefault("build_role", (fuzzy_tenant.get("build_role") or "").strip())
            routing.setdefault(
                "default_account_type", (fuzzy_tenant.get("default_account_type") or "").strip()
            )

    # 5) shared_db
    pkey = (
        routing.get("primary_server_label", ""),
        routing.get("db_name_logical", ""),
    )
    is_shared = bool(pkey[0] and pkey[1] and shared_index.get(pkey, 0) >= 2)
    needs_hcode_guard = is_shared and bool(seed_tenant)
    if needs_hcode_guard and seed_tenant is not None:
        if not (
            seed_tenant.get("hcode_in")
            or seed_tenant.get("hcode_pattern")
            or seed_tenant.get("hcode_prefix")
        ):
            reasons.append("shared_db_no_hcode_guard")

    # status / confidence 결정
    has_matrix = "matrix" in sources
    has_seed = "seed" in sources
    has_family = bool(family)
    only_label = sources == ["label_fuzzy"]

    if has_matrix and has_seed:
        status = STATUS_MATCHED
        confidence = CONFIDENCE_HIGH if not reasons else CONFIDENCE_MEDIUM
    elif has_matrix and not has_seed:
        status = STATUS_MATCHED
        confidence = CONFIDENCE_MEDIUM
        reasons.append("seed_missing_for_family")
    elif has_seed and not has_matrix:
        status = STATUS_MATCHED
        confidence = CONFIDENCE_MEDIUM
        reasons.append("matrix_missing_for_family")
    elif has_family:
        status = STATUS_PARTIAL
        confidence = CONFIDENCE_LOW
        reasons.append("family_not_in_matrix_or_seed")
    elif fuzzy_tenant or only_label:
        status = STATUS_REVIEW
        confidence = CONFIDENCE_LOW
        reasons.append("label_fuzzy_only")
    else:
        status = STATUS_REVIEW
        confidence = CONFIDENCE_LOW
        reasons.append("no_family_no_label_match")

    return {
        "config_path": config_path,
        "config_kind": config_kind,
        "account_family_inferred": family,
        "customer_folder": row.get("customer_folder", ""),
        "client": _client_meta(row),
        "routing": _route_summary(routing),
        "match": {
            "status": status,
            "confidence": confidence,
            "sources": _dedup_keep_order(sources),
            "reasons": _dedup_keep_order(reasons),
        },
        "shared_db": {
            "is_shared": is_shared,
            "needs_hcode_guard": needs_hcode_guard,
        },
    }


def _client_meta(row: dict[str, Any]) -> dict[str, str]:
    """카탈로그용 [Client] 메타 (자격증명 0건)."""
    return {
        "name": row.get("name", ""),
        "uses": row.get("uses", ""),
        "base": row.get("base", ""),
        "port": row.get("port", ""),
        "pcip1": row.get("pcip1", ""),
    }


def _dedup_keep_order(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for s in seq:
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def build_catalog(
    inventory: list[dict[str, Any]],
    *,
    matrix_doc: Any,
    seed_doc: Any,
    overlay_doc: Any,
    chul_doc: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """카탈로그·review_queue·summary 일괄 산출."""
    matrix_by_family = _matrix_routes_by_family(matrix_doc)
    seed_by_family = _seed_tenants_by_family(seed_doc, overlay_doc)
    seed_label_pool = _seed_labels(seed_doc, overlay_doc)
    chul_by_subpath = _chul_rows_by_subpath(chul_doc)
    shared_index = _shared_db_index(seed_by_family)

    catalog: list[dict[str, Any]] = []
    for row in inventory:
        catalog.append(
            classify_row(
                row,
                matrix_by_family=matrix_by_family,
                seed_by_family=seed_by_family,
                seed_label_pool=seed_label_pool,
                chul_by_subpath=chul_by_subpath,
                shared_index=shared_index,
            )
        )

    review_queue = [r for r in catalog if r["match"]["status"] == STATUS_REVIEW]

    status_counts = Counter(r["match"]["status"] for r in catalog)
    confidence_counts = Counter(r["match"]["confidence"] for r in catalog)
    family_counts = Counter(
        r["account_family_inferred"] for r in catalog if r.get("account_family_inferred")
    )
    summary = {
        "total_configs": len(catalog),
        "status_counts": dict(status_counts),
        "confidence_counts": dict(confidence_counts),
        "distinct_families": len(family_counts),
        "review_queue_count": len(review_queue),
        "shared_db_rows": sum(1 for r in catalog if r["shared_db"]["is_shared"]),
        "shared_db_no_hcode_guard_rows": sum(
            1 for r in catalog if r["shared_db"]["needs_hcode_guard"]
            and "shared_db_no_hcode_guard" in r["match"]["reasons"]
        ),
    }
    return catalog, review_queue, summary


def emit_overlay_proposals(catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """``confidence=high`` 인데 matrix vs seed 라우팅 라벨이 어긋난 행만 제안.

    DSN-DEC-06 의 ``label_fuzzy`` 단독 결정은 제외 — overlay 후보가 아니다.
    실제 overlay 머지는 [`apply_hcode_isolation_overlay.py`](apply_hcode_isolation_overlay.py)
    패턴을 따른 별도 도구에서 진행 (본 도구는 dry-run 만).
    """
    out: list[dict[str, Any]] = []
    for r in catalog:
        match = r.get("match") or {}
        if match.get("confidence") != CONFIDENCE_HIGH:
            continue
        sources = match.get("sources") or []
        if "matrix" not in sources or "seed" not in sources:
            continue
        reasons = match.get("reasons") or []
        if not any(
            x in reasons for x in ("chul_remote_id_mismatch", "chul_db_name_mismatch")
        ):
            continue
        out.append(
            {
                "tenant_id": r["routing"]["tenant_id"],
                "account_family": r["account_family_inferred"],
                "primary_server": r["routing"]["primary_server_label"],
                "db_name_logical": r["routing"]["db_name_logical"],
                "config_path": r["config_path"],
                "reasons": reasons,
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY))
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    parser.add_argument("--seed", default=str(DEFAULT_SEED))
    parser.add_argument("--overlay", default=str(DEFAULT_OVERLAY))
    parser.add_argument("--chul-defaults", default=str(DEFAULT_CHUL_DEFAULTS))
    parser.add_argument("--catalog-out", default=str(DEFAULT_CATALOG_OUT))
    parser.add_argument("--review-out", default=str(DEFAULT_REVIEW_OUT))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="JSON 파일 두 개 (catalog, review_queue) 를 디스크에 저장",
    )
    parser.add_argument(
        "--emit-overlay",
        type=Path,
        default=None,
        help="dry-run overlay 제안을 JSON 으로 저장 (apply 와 무관)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="catalog 행수가 inventory.count 와 다르면 exit 2 (CI 가드)",
    )
    args = parser.parse_args(argv)

    inv_doc = _load_json(Path(args.inventory))
    if not isinstance(inv_doc, dict):
        sys.stderr.write(f"[ERR] inventory not found: {args.inventory}\n")
        return 2
    items = list(inv_doc.get("items") or [])
    inventory_count = inv_doc.get("count", len(items))

    matrix_doc = _load_json(Path(args.matrix))
    seed_doc = _load_json(Path(args.seed))
    overlay_doc = _load_json(Path(args.overlay))
    chul_doc = _load_json(Path(args.chul_defaults))

    catalog, review_queue, summary = build_catalog(
        items,
        matrix_doc=matrix_doc,
        seed_doc=seed_doc,
        overlay_doc=overlay_doc,
        chul_doc=chul_doc,
    )

    catalog_payload = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "inventory": str(args.inventory),
            "matrix": str(args.matrix),
            "seed": str(args.seed),
            "overlay": str(args.overlay) if Path(args.overlay).exists() else None,
            "chul_defaults": str(args.chul_defaults) if Path(args.chul_defaults).exists() else None,
        },
        "secrets_policy": "G3 — no credentials, no host secrets",
        "summary": summary,
        "items": catalog,
    }
    review_payload = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "review_queue_count": len(review_queue),
            "total_configs": len(catalog),
        },
        "items": review_queue,
    }

    if args.apply:
        Path(args.catalog_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.catalog_out).write_text(
            json.dumps(catalog_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        Path(args.review_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.review_out).write_text(
            json.dumps(review_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] catalog       → {args.catalog_out} ({len(catalog)} 행)")
        print(f"[OK] review queue  → {args.review_out} ({len(review_queue)} 행)")
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        sys.stderr.write("[DRY] use --apply to save\n")

    if args.emit_overlay is not None:
        proposals = emit_overlay_proposals(catalog)
        overlay_payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "note": (
                "dry-run only — apply는 별도 단계 (운영 승인 필요). "
                "DSN-DEC-12 가드와 무관."
            ),
            "count": len(proposals),
            "proposals": proposals,
        }
        args.emit_overlay.parent.mkdir(parents=True, exist_ok=True)
        args.emit_overlay.write_text(
            json.dumps(overlay_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] overlay (dry) → {args.emit_overlay} ({len(proposals)} 제안)")

    print(f"     summary: {json.dumps(summary, ensure_ascii=False)}")

    if args.strict and len(catalog) != int(inventory_count or 0):
        sys.stderr.write(
            f"[ERR] catalog rows {len(catalog)} != inventory.count {inventory_count}\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
