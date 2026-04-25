#!/usr/bin/env python3
"""레거시 라우팅 JSON → tenants_directory_seed.json 병합 (DSN-DEC-11).

병합 정책
---------
1. **운영 우선 보존** — 동일 ``account_family`` 가 운영 시드에 이미 있으면 운영 row 를
   그대로 둔다. 다만 레거시 라우팅이 운영 시드와 다르면 ``notes`` 에 한 줄
   경고를 추가하고 ``_legacy_chul_pas_meta`` 를 부착한다(추후 검증용).
2. **신규 충원** — 운영 시드에 없는 family 는 신규 row 로 추가한다.
   - ``tenant_id`` = UUIDv5(NS_LEGACY_TENANT, account_family) — 멱등성 보장.
   - ``_seed_source`` = ``"legacy_chul_pas"``.
   - ``confidence`` 가 ``low`` 이면 ``is_active=False`` 로 두어 라우팅에서
     자동 사용되지 않게 한다(운영자가 검증 후 수동 활성화).
3. **family 추론 실패** (Database/family 비어 있음) → skip + 리포트.

사용
----
    python3 tools/merge_legacy_routing_into_seed.py            # dry-run 리포트
    python3 tools/merge_legacy_routing_into_seed.py --apply    # 시드 갱신
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WELOVE = ROOT / "WeLove_FTP"
DEFAULT_LEGACY_JSON = WELOVE / "legacy_delphi_routing_defaults.json"
DEFAULT_SEED_JSON = (
    ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)

# 고정 namespace — 동일 account_family 는 항상 동일 tenant_id 를 갖도록 보장.
# DSN-DEC-11. 임의 변경 금지(변경 시 모든 자동 생성 tenant_id 가 바뀜).
NS = uuid.UUID("8e3b8a3c-1d8c-4b91-9d8a-1eaca1cf45a5")


def stable_tenant_id(account_family: str) -> str:
    return str(uuid.uuid5(NS, f"legacy_chul_pas:{account_family}"))


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _build_role_for_family(family: str) -> str:
    """family prefix 로 build_role 추정.

    - ``book_*``  → publisher
    - ``chul_*``  → distributor
    - 그 외       → distributor (보수적 기본 — 운영자 검증 필요)
    """
    f = (family or "").lower()
    if f.startswith("book_"):
        return "publisher"
    if f.startswith("chul_"):
        return "distributor"
    return "distributor"


def _default_account_type(build_role: str) -> str:
    return "T3" if build_role == "publisher" else "T2_DIST"


def _label_for_remote_id(remote_id: str) -> str:
    """tenants_directory_service 의 _LABEL_TO_REMOTE_ID 와 동기 (정본은 서비스 측)."""
    table = {
        "remote_154": "서버1",
        "remote_155": "서버2",
        "remote_153": "서버3",
        "remote_138": "서버4",
    }
    return table.get(remote_id, remote_id)


def _index_seed(seed_tenants: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """family → 첫 번째 매치 row (동일 family 복수 시 첫 번째 우선)."""
    out: dict[str, dict[str, Any]] = {}
    for t in seed_tenants:
        fam = (t.get("account_family") or "").strip()
        if fam and fam not in out:
            out[fam] = t
    return out


def _legacy_meta(legacy_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "build_folder": legacy_row.get("build_folder", ""),
        "host_ip": legacy_row.get("host_ip", ""),
        "remote_id": legacy_row.get("remote_id", ""),
        "unknown_host_ip": legacy_row.get("unknown_host_ip", ""),
        "mismatch_note": legacy_row.get("mismatch_note", ""),
        "confidence": legacy_row.get("confidence", "low"),
        "low_confidence_reasons": list(legacy_row.get("low_confidence_reasons", []) or []),
    }


def _aggregate_legacy(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """family → row 목록. 같은 family 가 여러 빌드에 등장할 수 있으므로 모음.

    high confidence row 가 있으면 우선, 모두 low 면 첫 번째.
    """
    grouped: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        fam = (r.get("account_family") or "").strip()
        if not fam:
            continue
        grouped.setdefault(fam, []).append(r)
    return grouped


def _pick_authoritative(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """동일 family 의 여러 빌드 row 에서 정본 후보 1건 선정."""
    for r in rows:
        if r.get("confidence") == "high" and r.get("remote_id") and r.get("database"):
            return r
    return rows[0]


def merge(
    seed_payload: dict[str, Any],
    legacy_payload: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """seed + legacy → 새 seed_payload, 변경 리포트 반환.

    ``seed_payload`` 는 변경하지 않는다(불변). 새 dict 를 만들어서 반환.
    """
    seed_tenants: list[dict[str, Any]] = list(seed_payload.get("tenants", []) or [])
    legacy_rows: list[dict[str, Any]] = list(legacy_payload.get("rows", []) or [])

    seed_index = _index_seed(seed_tenants)
    legacy_groups = _aggregate_legacy(legacy_rows)

    new_tenants: list[dict[str, Any]] = []
    new_count = 0
    conflict_count = 0
    skipped_no_family = 0
    annotated_count = 0
    conflicts: list[dict[str, Any]] = []
    new_families: list[str] = []
    skipped_low: list[str] = []

    seed_by_id: dict[str, dict[str, Any]] = {}
    for fam, rows in legacy_groups.items():
        if not fam:
            skipped_no_family += 1
            continue
        chosen = _pick_authoritative(rows)
        if fam in seed_index:
            existing = dict(seed_index[fam])
            seed_remote_label = (existing.get("primary_server") or "").strip()
            seed_db = (existing.get("db_name_logical") or "").strip()
            legacy_remote = chosen.get("remote_id") or ""
            legacy_label = _label_for_remote_id(legacy_remote) if legacy_remote else ""
            legacy_db = chosen.get("database") or ""
            mismatch = (
                bool(legacy_label and seed_remote_label and legacy_label != seed_remote_label)
                or bool(legacy_db and seed_db and legacy_db != seed_db)
            )
            if mismatch:
                conflict_count += 1
                conflicts.append(
                    {
                        "account_family": fam,
                        "seed": {"primary_server": seed_remote_label, "db": seed_db},
                        "legacy": {"primary_server": legacy_label, "db": legacy_db},
                        "build_folder": chosen.get("build_folder", ""),
                    }
                )
                warn = (
                    f"[legacy_chul_pas] routing differs: legacy={legacy_label}/{legacy_db} "
                    f"vs seed={seed_remote_label}/{seed_db} (build={chosen.get('build_folder','')})"
                )
                prev_notes = (existing.get("notes") or "").strip()
                existing["notes"] = (
                    f"{prev_notes}\n{warn}".strip() if prev_notes else warn
                )
                existing["_legacy_chul_pas_meta"] = _legacy_meta(chosen)
                annotated_count += 1
            else:
                if "_legacy_chul_pas_meta" not in existing:
                    existing["_legacy_chul_pas_meta"] = _legacy_meta(chosen)
                    annotated_count += 1
            seed_by_id[(existing.get("tenant_id") or "")] = existing
        else:
            confidence = chosen.get("confidence") or "low"
            remote_id = chosen.get("remote_id") or ""
            db_name = chosen.get("database") or ""
            primary_label = _label_for_remote_id(remote_id) if remote_id else ""
            build_role = _build_role_for_family(fam)
            label_kor = (chosen.get("build_folder") or fam).strip() or fam
            new_row = {
                "tenant_id": stable_tenant_id(fam),
                "tenant_label_kor": label_kor,
                "account_family": fam,
                "active_build_id": None,
                "build_role": build_role,
                "parent_tenant_id": None,
                "default_account_type": _default_account_type(build_role),
                "primary_server": primary_label,
                "db_name_logical": db_name,
                # confidence=low 는 자동 라우팅에서 빠지도록 비활성화 시드.
                "is_active": confidence == "high",
                "notes": (
                    "[legacy_chul_pas] auto-imported"
                    + (" (low confidence — operator review required)" if confidence != "high" else "")
                ),
                "_seed_source": "legacy_chul_pas",
                "confidence": confidence,
                "_legacy_chul_pas_meta": _legacy_meta(chosen),
            }
            new_tenants.append(new_row)
            new_count += 1
            new_families.append(fam)
            if confidence != "high":
                skipped_low.append(fam)

    merged_tenants: list[dict[str, Any]] = []
    for t in seed_tenants:
        tid = (t.get("tenant_id") or "").strip()
        merged_tenants.append(seed_by_id.get(tid, t))
    merged_tenants.extend(new_tenants)

    new_payload = dict(seed_payload)
    new_payload["tenants"] = merged_tenants
    new_payload["generated_at"] = datetime.now(timezone.utc).isoformat()
    notes_existing = new_payload.get("note") or ""
    legacy_marker = "DSN-DEC-11 legacy_chul_pas merged"
    if legacy_marker not in notes_existing:
        new_payload["note"] = (notes_existing + " | " + legacy_marker).strip(" |")

    report = {
        "seed_tenants_before": len(seed_tenants),
        "seed_tenants_after": len(merged_tenants),
        "legacy_families_total": len(legacy_groups),
        "newly_added": new_count,
        "newly_added_inactive_low_confidence": len(skipped_low),
        "annotated_existing": annotated_count,
        "routing_conflicts": conflict_count,
        "skipped_no_family": skipped_no_family,
        "new_families": new_families,
        "low_confidence_inactive": skipped_low,
        "conflicts": conflicts,
    }
    return new_payload, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__ or "")
    parser.add_argument("--legacy", type=Path, default=DEFAULT_LEGACY_JSON)
    parser.add_argument("--seed", type=Path, default=DEFAULT_SEED_JSON)
    parser.add_argument("--apply", action="store_true", help="시드를 실제로 갱신")
    args = parser.parse_args(argv)

    seed = _load_json(args.seed)
    legacy = _load_json(args.legacy)
    if not seed:
        sys.stderr.write(f"[ERR] seed not found: {args.seed}\n")
        return 2
    if not legacy:
        sys.stderr.write(f"[ERR] legacy not found: {args.legacy}\n")
        return 2

    new_payload, report = merge(seed, legacy)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.apply:
        backup = args.seed.with_suffix(args.seed.suffix + ".bak")
        backup.write_bytes(args.seed.read_bytes())
        args.seed.write_text(
            json.dumps(new_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        sys.stderr.write(
            f"[OK] seed updated: {args.seed.relative_to(ROOT)} "
            f"(backup at {backup.relative_to(ROOT)})\n"
        )
    else:
        sys.stderr.write("[DRY] use --apply to update seed\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
