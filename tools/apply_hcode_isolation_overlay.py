#!/usr/bin/env python3
"""DSN-DEC-12 — SME가 채운 격리 키 템플릿을 tenants_directory_overlay.json 으로 병합.

입력
----
[`extract_shared_db_hcodes.py`](extract_shared_db_hcodes.py) 가 만든
``analysis/welove_shared_db_hcode_candidates.json`` 의 ``sme_mapping_template`` 을
SME 가 직접 채운 결과 (또는 동일 스키마의 별 파일).

병합 규칙
---------
- ``hcode_in`` / ``hcode_pattern`` / ``hcode_prefix`` / ``parent_tenant_id`` 중 하나
  이상이 채워진 tenant_id 만 overlay 로 emit.
- 기존 시드 row 의 ``tenant_id`` + ``account_family`` 키와 동일하면 ``_merge_tenants``
  가 overlay 우선으로 덮어씀 ([`tenants_directory_service._merge_tenants`](../도서물류관리프로그램/backend/app/services/tenants_directory_service.py)).
- overlay 파일이 이미 있으면 동일 키 row 만 업데이트, 그 외 row 는 보존.

비밀 정책
---------
- 본 도구는 ``hcode``/``tenant_id`` 메타만 다루며 자격증명을 일체 읽지 않는다.

사용
----
    # dry-run (기본) — overlay 변경 결과를 stdout 으로만 출력
    python3 tools/apply_hcode_isolation_overlay.py \
        --filled analysis/welove_shared_db_hcode_candidates.json

    # apply — 실제 overlay 파일에 기록
    python3 tools/apply_hcode_isolation_overlay.py \
        --filled analysis/welove_shared_db_hcode_candidates.json --apply

    # 검증
    python3 tools/audit_welove_routing_consistency.py --strict

회귀 가드
---------
- 본 도구의 머지 로직은 ``test/test_apply_hcode_isolation_overlay.py`` 가 단위 테스트한다.
- ``tenants_directory_service`` 의 ``_merge_tenants`` 와 동일 키 시맨틱을 따른다 (DRY).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OVERLAY_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_overlay.json"
)
DEFAULT_SEED_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)


_ALLOWED_ISOLATION_KEYS: tuple[str, ...] = (
    "hcode_in",
    "hcode_pattern",
    "hcode_prefix",
    "parent_tenant_id",
)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _seed_lookup(seed_doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """tenant_id → seed row (account_family 포함) 매핑."""
    out: dict[str, dict[str, Any]] = {}
    for t in seed_doc.get("tenants") or []:
        tid = (t.get("tenant_id") or "").strip()
        if tid:
            out[tid] = t
    return out


def _normalize_filled_template(
    filled_doc: dict[str, Any],
    seed_lookup: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """SME 가 채운 ``sme_mapping_template`` 을 overlay row 리스트로 정규화.

    각 row 는 ``tenant_id`` + ``account_family`` (시드에서 인용) + 격리 키만 포함.
    """
    rows: list[dict[str, Any]] = []
    for c in filled_doc.get("candidates") or []:
        templ = c.get("sme_mapping_template") or {}
        for tid, fields in templ.items():
            tid = (tid or "").strip()
            if not tid:
                continue
            isolation: dict[str, Any] = {}
            # hcode_in (list[str]) — 빈 리스트는 미설정으로 간주
            hin = fields.get("hcode_in")
            if isinstance(hin, list) and any((str(v).strip() for v in hin)):
                isolation["hcode_in"] = [str(v).strip() for v in hin if str(v).strip()]
            for k in ("hcode_pattern", "hcode_prefix", "parent_tenant_id"):
                v = fields.get(k)
                if isinstance(v, str) and v.strip():
                    isolation[k] = v.strip()
            if not isolation:
                # SME 가 아직 안 채운 row → skip (placeholder 만 있는 케이스)
                continue
            seed_row = seed_lookup.get(tid)
            if not seed_row:
                # 시드에 없는 tenant_id 면 overlay 만으로 라우팅하기 어렵다 — 경고 후 skip.
                print(
                    f"[WARN] tenant_id={tid} not found in seed; skipping (add seed row first)",
                    file=sys.stderr,
                )
                continue
            row = {
                "tenant_id": tid,
                "account_family": (seed_row.get("account_family") or "").strip(),
                **isolation,
                "_dsn_dec_12": True,
                "_applied_at": datetime.now(timezone.utc).isoformat(),
            }
            rows.append(row)
    return rows


def _merge_overlay(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """동일 (tenant_id, account_family) row 는 incoming 으로 격리 키만 덮어씀."""
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for r in existing:
        key = ((r.get("tenant_id") or "").strip(), (r.get("account_family") or "").strip())
        by_key[key] = dict(r)
    for r in incoming:
        key = ((r.get("tenant_id") or "").strip(), (r.get("account_family") or "").strip())
        merged = dict(by_key.get(key, {}))
        # 격리 키만 갱신, 기타 운영 필드는 보존.
        for k in (*_ALLOWED_ISOLATION_KEYS, "_dsn_dec_12", "_applied_at"):
            if k in r:
                merged[k] = r[k]
        merged["tenant_id"] = key[0]
        merged["account_family"] = key[1]
        by_key[key] = merged
    return list(by_key.values())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--filled", required=True, help="SME 가 채운 candidates JSON")
    parser.add_argument("--seed", default=str(DEFAULT_SEED_PATH))
    parser.add_argument("--overlay", default=str(DEFAULT_OVERLAY_PATH))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="기본 dry-run; --apply 시 overlay 파일을 실제로 갱신",
    )
    args = parser.parse_args(argv)

    filled = _read_json(Path(args.filled))
    if not filled:
        print(f"[ERR] cannot read filled template: {args.filled}", file=sys.stderr)
        return 2
    seed = _read_json(Path(args.seed))
    seed_lookup = _seed_lookup(seed)

    incoming = _normalize_filled_template(filled, seed_lookup)
    if not incoming:
        print("[INFO] 채워진 격리 키가 없음 — overlay 미변경.")
        return 0

    overlay_path = Path(args.overlay)
    existing_doc = _read_json(overlay_path)
    existing_rows = list(existing_doc.get("tenants") or [])
    merged = _merge_overlay(existing_rows, incoming)

    payload = {
        "schema_version": existing_doc.get("schema_version", "1.1.0"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "note": "DSN-DEC-12 — 공유 DB 격리 키 overlay (자격증명 0건).",
        "tenants": merged,
    }

    print(f"[PLAN] {len(incoming)} row 를 overlay 에 반영 → {overlay_path}")
    if not args.apply:
        print("--- dry-run preview (use --apply to write) ---")
        print(json.dumps(payload, ensure_ascii=False, indent=2)[:4000])
        return 0
    overlay_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = overlay_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(overlay_path)
    print(f"[OK] wrote {overlay_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
