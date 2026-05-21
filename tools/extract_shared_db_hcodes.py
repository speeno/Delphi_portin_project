#!/usr/bin/env python3
"""DSN-DEC-12 — 공유 DB 좌표별 DISTINCT Hcode 후보 추출 (시드 격리 키 입력 보조).

목적
----
[`login_id_index.json`](../도서물류관리프로그램/backend/data/login_id_index.json) 또는
운영자가 라이브 DB에서 추출한 동등 JSON을 입력 받아, ``(server_id, db_name)`` 좌표마다
**DISTINCT Hcode 목록 + 사용자 수**를 정리해 SME 매핑 입력용 템플릿
``analysis/welove_shared_db_hcode_candidates.json`` 을 만든다.

산출물 형식
-----------
```json
{
  "generated_at": "...",
  "source_index_path": "...",
  "source_index_built_at": "...",
  "candidates": [
    {
      "remote_id": "remote_153",
      "db_name": "chul_09_db",
      "is_shared_db": true,
      "shared_count": 4,
      "tenants_in_seed": [
        {"tenant_id": "...", "tenant_label_kor": "교문사", ...},
        ...
      ],
      "distinct_hcodes": [
        {"hcode": "9001", "user_count": 12, "sample_logins": ["...", "..."]}
      ],
      "sme_mapping_template": {
        "<tenant_id_1>": {"hcode_in": []},
        ...
      }
    },
    ...
  ]
}
```

비밀 정책 (G3)
---------------
- 본 도구는 ``Gcode``/``Hcode``/메타만 읽는다 (``login_id_index.json`` 자체가 비밀번호 0건).
- 출력 JSON 의 ``sample_logins`` 는 디버깅 용도 — 운영자가 필요 시 SAMPLE_LOGINS_LIMIT=0 으로 끌 수 있다.

사용
----
    python3 tools/extract_shared_db_hcodes.py
    python3 tools/extract_shared_db_hcodes.py --include-singletons
    python3 tools/extract_shared_db_hcodes.py --sample-limit 0   # 샘플 미포함
    python3 tools/extract_shared_db_hcodes.py --out /tmp/cand.json

후속 절차
---------
1. 본 도구 실행 → ``analysis/welove_shared_db_hcode_candidates.json`` 생성.
2. SME 가 ``sme_mapping_template`` 의 ``hcode_in`` 리스트를 채움 (또는 ``hcode_pattern`` /
   ``hcode_prefix`` / ``parent_tenant_id`` 로 변경).
3. ``tools/apply_hcode_isolation_overlay.py`` 를 실행해 채워진 템플릿을
   ``backend/data/tenants_directory_overlay.json`` 으로 병합.
4. ``tools/audit_welove_routing_consistency.py --strict`` 가 0충돌이 되도록 검증.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "login_id_index.json"
)
DEFAULT_SEED_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)
DEFAULT_OUT_PATH = REPO_ROOT / "analysis" / "welove_shared_db_hcode_candidates.json"


@dataclass
class HcodeStat:
    hcode: str
    user_count: int
    sample_logins: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _coordinate_hcodes(
    index_doc: dict[str, Any],
    *,
    sample_limit: int,
) -> dict[tuple[str, str], list[HcodeStat]]:
    """``(remote_id, db_name)`` → 정렬된 HcodeStat 목록."""
    by_login = index_doc.get("by_login_id") or {}
    if not isinstance(by_login, dict):
        return {}

    bucket: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for login_id, entries in by_login.items():
        if not isinstance(entries, list):
            continue
        for e in entries:
            if not isinstance(e, dict):
                continue
            rid = (e.get("remote_id") or "").strip()
            dbn = (e.get("db_name") or "").strip()
            hc = (e.get("hcode") or "").strip()
            if not rid or not dbn:
                continue
            slot = bucket.setdefault((rid, dbn), {})
            row = slot.setdefault(hc, {"hcode": hc, "user_count": 0, "samples": []})
            row["user_count"] += 1
            if sample_limit > 0 and len(row["samples"]) < sample_limit:
                row["samples"].append(str(login_id))

    out: dict[tuple[str, str], list[HcodeStat]] = {}
    for key, slot in bucket.items():
        rows = sorted(slot.values(), key=lambda r: (-r["user_count"], r["hcode"]))
        out[key] = [
            HcodeStat(hcode=r["hcode"], user_count=r["user_count"], sample_logins=r["samples"])
            for r in rows
        ]
    return out


def _seed_tenants_by_coordinate(
    seed_doc: dict[str, Any],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """``primary_server`` 라벨을 ``remote_*`` 로 정규화해 좌표별 그룹."""
    label_to_remote_id = {
        "서버1": "remote_154",
        "서버2": "remote_155",
        "서버3": "remote_153",
        "서버4": "remote_138",
    }
    by_coord: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for t in seed_doc.get("tenants") or []:
        if not t.get("is_active", True):
            continue
        srv_label = (t.get("primary_server") or "").strip()
        rid = label_to_remote_id.get(srv_label, srv_label)
        dbn = (t.get("db_name_logical") or "").strip()
        if not rid or not dbn:
            continue
        by_coord.setdefault((rid, dbn), []).append(t)
    return by_coord


def build_report(
    *,
    index_doc: dict[str, Any],
    seed_doc: dict[str, Any],
    sample_limit: int,
    include_singletons: bool,
) -> dict[str, Any]:
    coord_hcodes = _coordinate_hcodes(index_doc, sample_limit=sample_limit)
    seed_by_coord = _seed_tenants_by_coordinate(seed_doc)

    all_keys = set(coord_hcodes) | set(seed_by_coord)
    candidates: list[dict[str, Any]] = []
    for key in sorted(all_keys):
        rid, dbn = key
        seed_rows = seed_by_coord.get(key, [])
        is_shared = len(seed_rows) >= 2
        if not is_shared and not include_singletons:
            continue
        hcode_rows = coord_hcodes.get(key, [])
        sme_template: dict[str, dict[str, Any]] = {}
        for st in seed_rows:
            tid = (st.get("tenant_id") or "").strip()
            if not tid:
                continue
            sme_template[tid] = {
                "tenant_label_kor": st.get("tenant_label_kor") or "",
                "isolation_hint": "FILL_ONE_OF: hcode_in / hcode_pattern / hcode_prefix / parent_tenant_id",
                "hcode_in": [],
                "hcode_pattern": "",
                "hcode_prefix": "",
                "parent_tenant_id": st.get("parent_tenant_id") or "",
                "_observed_distinct_hcodes": [r.hcode for r in hcode_rows],
            }
        candidates.append(
            {
                "remote_id": rid,
                "db_name": dbn,
                "is_shared_db": is_shared,
                "shared_count": len(seed_rows),
                "tenants_in_seed": [
                    {
                        "tenant_id": st.get("tenant_id"),
                        "tenant_label_kor": st.get("tenant_label_kor"),
                        "account_family": st.get("account_family"),
                        "build_role": st.get("build_role"),
                        "default_account_type": st.get("default_account_type"),
                        "parent_tenant_id": st.get("parent_tenant_id"),
                    }
                    for st in seed_rows
                ],
                "distinct_hcodes": [
                    {
                        "hcode": r.hcode,
                        "user_count": r.user_count,
                        "sample_logins": r.sample_logins,
                    }
                    for r in hcode_rows
                ],
                "sme_mapping_template": sme_template,
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_index_path": str(index_doc.get("__source_path__", "")),
        "source_index_built_at": index_doc.get("built_at", ""),
        "stats": {
            "coordinates_total": len(all_keys),
            "shared_db_coordinates": sum(1 for k in all_keys if len(seed_by_coord.get(k, [])) >= 2),
            "candidates_emitted": len(candidates),
        },
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--index", default=str(DEFAULT_INDEX_PATH))
    parser.add_argument("--seed", default=str(DEFAULT_SEED_PATH))
    parser.add_argument("--out", default=str(DEFAULT_OUT_PATH))
    parser.add_argument("--sample-limit", type=int, default=3)
    parser.add_argument(
        "--include-singletons",
        action="store_true",
        help="단독 DB 좌표(공유 아님) 도 출력에 포함",
    )
    args = parser.parse_args(argv)

    index_path = Path(args.index)
    seed_path = Path(args.seed)
    out_path = Path(args.out)

    if not index_path.exists():
        print(f"[ERR] login_id_index.json not found: {index_path}", file=sys.stderr)
        return 2
    index_doc = _read_json(index_path)
    index_doc["__source_path__"] = str(index_path)
    seed_doc = _read_json(seed_path) if seed_path.exists() else {}

    report = build_report(
        index_doc=index_doc,
        seed_doc=seed_doc,
        sample_limit=max(0, args.sample_limit),
        include_singletons=args.include_singletons,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] wrote {out_path}")
    print(f"  coordinates_total       = {report['stats']['coordinates_total']}")
    print(f"  shared_db_coordinates   = {report['stats']['shared_db_coordinates']}")
    print(f"  candidates_emitted      = {report['stats']['candidates_emitted']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
