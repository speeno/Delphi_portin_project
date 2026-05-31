#!/usr/bin/env python3
"""WeLove 레거시 라우팅 매트릭스 ↔ 운영 테넌트 시드 정합 감사 (DSN-DEC-08/12).

목적
----
[`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) 와
[`도서물류관리프로그램/backend/data/tenants_directory_seed.json`](../도서물류관리프로그램/backend/data/tenants_directory_seed.json)
를 1:1 비교해 다음 충돌 카테고리를 분류 출력한다 — [docs/welove-login-tenant-audit-samples.md](../docs/welove-login-tenant-audit-samples.md) §3 와 1:1 매핑.

| 코드 | 의미 |
|------|------|
| `SHARED_COORD_NO_HCODE_GUARD` | 같은 `(server_id, db_name)` 좌표의 공유 DB 인데 시드에 격리 키 부재 (실제 P0) |
| `SHARED_DB_CROSS_SERVER` | DB명은 같지만 서버가 달라 런타임은 `server_id` 로 단일화 가능한 정보성 항목 |
| `MATRIX_NOT_IN_SEED` | 매트릭스에 있는데 시드에 누락 |
| `SEED_NOT_IN_MATRIX` | 시드에만 있고 매트릭스에 없음 (신규 운영 테넌트 후보) |
| `PRIMARY_SERVER_MISMATCH` | 동일 라벨인데 `primary_server` 가 다름 |
| `DB_NAME_LOGICAL_MISMATCH` | 동일 라벨인데 `db_name_logical` 이 다름 |
| `DB_NAME_LOGICAL_MISSING` | 매트릭스에서 `db_name_logical` 빈 항목 |

비밀 정책
---------
- 자격증명 / 비밀번호 / 토큰 일체 미참조.
- 매트릭스 / 시드 모두 메타 전용. 본 도구는 read-only.

사용
----
    python3 tools/audit_welove_routing_consistency.py
    python3 tools/audit_welove_routing_consistency.py --json
    python3 tools/audit_welove_routing_consistency.py --strict   # 충돌 1건이라도 있으면 exit 1

회귀 가드: ``test/test_welove_routing_consistency.py`` 가 본 도구의 결과를 import 해
``SHARED_COORD_NO_HCODE_GUARD`` 0 건 정책을 강제할 수 있다 (운영 정착 후 확장).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_MATRIX_PATH = _REPO_ROOT / "analysis" / "welove_db_route_matrix.json"
_DEFAULT_SEED_PATH = (
    _REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)
_DEFAULT_OVERLAY_PATH = (
    _REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_overlay.json"
)


@dataclass
class ConsistencyFinding:
    code: str
    label: str
    detail: str
    matrix_row: dict[str, Any] | None = None
    seed_row: dict[str, Any] | None = None


@dataclass
class ConsistencyReport:
    findings: list[ConsistencyFinding] = field(default_factory=list)
    matrix_count: int = 0
    seed_count: int = 0

    def by_code(self) -> dict[str, list[ConsistencyFinding]]:
        out: dict[str, list[ConsistencyFinding]] = {}
        for f in self.findings:
            out.setdefault(f.code, []).append(f)
        return out

    def has_critical(self) -> bool:
        critical = {
            "SHARED_COORD_NO_HCODE_GUARD",
            "PRIMARY_SERVER_MISMATCH",
            "DB_NAME_LOGICAL_MISMATCH",
        }
        return any(f.code in critical for f in self.findings)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _matrix_routes(matrix_doc: dict[str, Any]) -> list[dict[str, Any]]:
    return list(matrix_doc.get("routes") or [])


def _seed_tenants(seed_doc: dict[str, Any]) -> list[dict[str, Any]]:
    return list(seed_doc.get("tenants") or [])


def _label_key(label: str) -> str:
    return (label or "").strip()


_SERVER_LABEL_TO_REMOTE_ID: dict[str, str] = {
    "서버1": "remote_154",
    "서버2": "remote_155",
    "서버3": "remote_153",
    "서버4": "remote_138",
}


def _server_key(value: str | None) -> str:
    """`서버1`/`remote_154` 표기를 같은 좌표 키로 정규화."""
    raw = (value or "").strip()
    return _SERVER_LABEL_TO_REMOTE_ID.get(raw, raw)


def _has_isolation_key(row: dict[str, Any]) -> bool:
    """DSN-DEC-12 격리 키가 하나라도 있으면 True."""
    hcode_in = row.get("hcode_in")
    if isinstance(hcode_in, list) and any(str(v).strip() for v in hcode_in):
        return True
    isolation_keys = [
        str(row.get("hcode_pattern") or "").strip(),
        str(row.get("hcode_prefix") or "").strip(),
        str(row.get("parent_tenant_id") or "").strip(),
        str(row.get("dist_tenant_id") or "").strip(),
    ]
    return any(isolation_keys)


def _is_guard_exempt(row: dict[str, Any]) -> bool:
    """본사/총판처럼 정의상 다중 가시성이 허용되는 계정은 격리 키 감사 제외."""
    return (row.get("default_account_type") or "") in ("T1", "T2_DIST")


def audit(matrix_doc: dict[str, Any], seed_doc: dict[str, Any]) -> ConsistencyReport:
    """단일 책임: matrix vs seed 비교만. 부수 IO 없음 (테스트 친화)."""
    report = ConsistencyReport()
    routes = _matrix_routes(matrix_doc)
    tenants = _seed_tenants(seed_doc)
    report.matrix_count = len(routes)
    report.seed_count = len(tenants)

    seed_by_label: dict[str, list[dict[str, Any]]] = {}
    for t in tenants:
        seed_by_label.setdefault(_label_key(t.get("tenant_label_kor")), []).append(t)

    matrix_by_label: dict[str, list[dict[str, Any]]] = {}
    for r in routes:
        matrix_by_label.setdefault(_label_key(r.get("tenant_name_kor")), []).append(r)

    db_name_to_seed_rows: dict[str, list[dict[str, Any]]] = {}
    coord_to_seed_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for t in tenants:
        dbn = (t.get("db_name_logical") or "").strip()
        if not dbn:
            continue
        db_name_to_seed_rows.setdefault(dbn, []).append(t)
        sid = _server_key(t.get("primary_server"))
        if sid:
            coord_to_seed_rows.setdefault((sid, dbn), []).append(t)

    # 1) 매트릭스 → 시드 비교
    for r in routes:
        label = _label_key(r.get("tenant_name_kor"))
        dbn = (r.get("db_name_logical") or "").strip()
        if not dbn:
            report.findings.append(
                ConsistencyFinding(
                    code="DB_NAME_LOGICAL_MISSING",
                    label=label,
                    detail=f"매트릭스 row 의 db_name_logical 비어있음 (account_family={r.get('account_family')})",
                    matrix_row=r,
                )
            )
            continue
        seed_matches = seed_by_label.get(label, [])
        if not seed_matches:
            report.findings.append(
                ConsistencyFinding(
                    code="MATRIX_NOT_IN_SEED",
                    label=label,
                    detail=(
                        f"매트릭스에 있는 라벨이 시드에 없음 — "
                        f"server={r.get('server_id')} db={dbn} family={r.get('account_family')}"
                    ),
                    matrix_row=r,
                )
            )
            continue
        for st in seed_matches:
            mp = (r.get("server_id") or "").strip()
            sp = (st.get("primary_server") or "").strip()
            if mp and sp and mp != sp:
                report.findings.append(
                    ConsistencyFinding(
                        code="PRIMARY_SERVER_MISMATCH",
                        label=label,
                        detail=f"matrix.primary_server={mp} ≠ seed.primary_server={sp}",
                        matrix_row=r,
                        seed_row=st,
                    )
                )
            sd = (st.get("db_name_logical") or "").strip()
            if dbn and sd and dbn != sd:
                report.findings.append(
                    ConsistencyFinding(
                        code="DB_NAME_LOGICAL_MISMATCH",
                        label=label,
                        detail=f"matrix.db_name_logical={dbn} ≠ seed.db_name_logical={sd}",
                        matrix_row=r,
                        seed_row=st,
                    )
                )

    # 2) 시드 → 매트릭스 (시드 only)
    for st in tenants:
        label = _label_key(st.get("tenant_label_kor"))
        if label and label not in matrix_by_label:
            report.findings.append(
                ConsistencyFinding(
                    code="SEED_NOT_IN_MATRIX",
                    label=label,
                    detail=(
                        f"시드에만 존재 — 신규 운영 테넌트 후보. "
                        f"family={st.get('account_family')} db={st.get('db_name_logical')}"
                    ),
                    seed_row=st,
                )
            )

    # 3a) SHARED_COORD_NO_HCODE_GUARD — 같은 server+DB 좌표에서 공유 DB 인데 격리 키 부재.
    # 런타임 ownership guard 도 server_id + db_name 으로 후보를 잡으므로 이것이 실제 P0.
    for (sid, dbn), seed_rows in coord_to_seed_rows.items():
        if len(seed_rows) <= 1:
            continue
        for st in seed_rows:
            if _has_isolation_key(st):
                continue
            if _is_guard_exempt(st):
                continue
            report.findings.append(
                ConsistencyFinding(
                    code="SHARED_COORD_NO_HCODE_GUARD",
                    label=_label_key(st.get("tenant_label_kor")),
                    detail=(
                        f"공유 좌표 ({sid}, {dbn}) 인데 시드에 hcode_in/hcode_pattern/"
                        f"hcode_prefix/parent_tenant_id 등 격리 키 부재. "
                        f"좌표 내 공유 라벨 수={len(seed_rows)}"
                    ),
                    seed_row=st,
                )
            )

    # 3b) SHARED_DB_CROSS_SERVER — DB명은 공유지만 server_id 로 단일화 가능한 정보성 항목.
    for dbn, seed_rows in db_name_to_seed_rows.items():
        if len(seed_rows) <= 1:
            continue
        coord_sizes = {
            (_server_key(st.get("primary_server")), dbn): len(
                coord_to_seed_rows.get((_server_key(st.get("primary_server")), dbn), [])
            )
            for st in seed_rows
        }
        if any(size >= 2 for size in coord_sizes.values()):
            continue
        for st in seed_rows:
            if _has_isolation_key(st) or _is_guard_exempt(st):
                continue
            report.findings.append(
                ConsistencyFinding(
                    code="SHARED_DB_CROSS_SERVER",
                    label=_label_key(st.get("tenant_label_kor")),
                    detail=(
                        f"DB명({dbn})은 여러 테넌트가 공유하지만 server_id 좌표가 달라 "
                        f"런타임은 단일화 가능. 장기적으로 hcode 격리 키 보강 권장."
                    ),
                    seed_row=st,
                )
            )

    return report


def _format_text_report(report: ConsistencyReport) -> str:
    lines: list[str] = []
    lines.append(f"매트릭스 row = {report.matrix_count}")
    lines.append(f"시드     row = {report.seed_count}")
    lines.append(f"발견 충돌    = {len(report.findings)}")
    lines.append("")
    grouped = report.by_code()
    if not grouped:
        lines.append("✅ 충돌 없음")
        return "\n".join(lines)
    for code in sorted(grouped.keys()):
        items = grouped[code]
        lines.append(f"[{code}]  {len(items)} 건")
        for f in items[:50]:
            lines.append(f"  - ({f.label}) {f.detail}")
        if len(items) > 50:
            lines.append(f"  ... (+{len(items) - 50} more)")
        lines.append("")
    return "\n".join(lines)


def _serialize_finding(f: ConsistencyFinding) -> dict[str, Any]:
    return {
        "code": f.code,
        "label": f.label,
        "detail": f.detail,
        "matrix_row": f.matrix_row,
        "seed_row": f.seed_row,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WeLove 라우팅 매트릭스 ↔ 시드 정합 감사 (DSN-DEC-12)")
    parser.add_argument("--matrix", default=str(_DEFAULT_MATRIX_PATH), help="welove_db_route_matrix.json 경로")
    parser.add_argument(
        "--seed",
        default=str(_DEFAULT_SEED_PATH),
        help="tenants_directory_seed.json 경로",
    )
    parser.add_argument(
        "--overlay",
        default=str(_DEFAULT_OVERLAY_PATH),
        help="tenants_directory_overlay.json 경로 (존재 시 시드와 병합 = 런타임 유효 디렉터리)",
    )
    parser.add_argument(
        "--no-overlay",
        action="store_true",
        help="overlay 병합 비활성화 (시드 단독 감사)",
    )
    parser.add_argument("--json", action="store_true", help="JSON 으로 출력")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="critical 충돌(SHARED_COORD_NO_HCODE_GUARD/PRIMARY_SERVER_MISMATCH/DB_NAME_LOGICAL_MISMATCH) 1건이라도 있으면 exit 1",
    )
    args = parser.parse_args(argv)

    matrix_doc = _load_json(Path(args.matrix))
    seed_doc = _load_json(Path(args.seed))

    # DSN-DEC-12 — 런타임은 시드+overlay 를 (tenant_id, account_family) 키로 병합해
    # 유효 디렉터리를 만든다(tenants_directory_service._merge_tenants). 감사도 동일
    # 유효 뷰를 평가해야 overlay 로 채운 hcode_in 격리 키가 반영된다.
    # (시드 단독 평가는 overlay 메커니즘으로 해소한 격리를 영구 critical 로 오탐.)
    overlay_path = Path(args.overlay)
    if not args.no_overlay and overlay_path.exists():
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from apply_hcode_isolation_overlay import _merge_overlay, _read_json

        overlay_doc = _read_json(overlay_path)
        overlay_rows = list(overlay_doc.get("tenants") or [])
        if overlay_rows:
            seed_doc = dict(seed_doc)
            seed_doc["tenants"] = _merge_overlay(
                list(seed_doc.get("tenants") or []), overlay_rows
            )

    report = audit(matrix_doc, seed_doc)

    if args.json:
        print(
            json.dumps(
                {
                    "matrix_count": report.matrix_count,
                    "seed_count": report.seed_count,
                    "findings": [_serialize_finding(f) for f in report.findings],
                    "has_critical": report.has_critical(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(_format_text_report(report))

    if args.strict and report.has_critical():
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
