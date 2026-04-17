#!/usr/bin/env python3
"""
DB 비즈니스 로직 인벤토리 리포터

스키마 추출 번들(schema_bundle.json)에서 routines/triggers/views/keys를
읽어 Markdown 인벤토리 + JSON 요약을 생성한다.

사용법
------
  # 단일 서버
  python3 tools/db/db_logic_reporter.py --bundle debug/output/schema/remote_138/schema_bundle.json

  # 전체 서버(디렉터리 스캔)
  python3 tools/db/db_logic_reporter.py --schema-dir debug/output/schema

  # 출력 기본: docs/db-business-logic-inventory.md + analysis/db_logic_inventory.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load_bundle(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _collect_bundles(schema_dir: Path) -> list[tuple[str, dict]]:
    """schema_dir 아래 서버별 schema_bundle.json을 모두 수집."""
    results = []
    if not schema_dir.is_dir():
        return results
    for sub in sorted(schema_dir.iterdir()):
        bundle_path = sub / "schema_bundle.json"
        if bundle_path.is_file():
            results.append((sub.name, _load_bundle(bundle_path)))
    return results


def _constraint_rules(keys: list[dict]) -> list[dict]:
    """FK / UNIQUE / CHECK 등 선언적 규칙만 추출."""
    rules = []
    seen = set()
    for k in keys:
        ct = k.get("constraint_type", "")
        if ct in ("PRIMARY KEY", "INDEX"):
            continue
        ident = (k["table_name"], k["constraint_name"], k["column_name"])
        if ident in seen:
            continue
        seen.add(ident)
        rules.append(k)
    return rules


def build_inventory(bundles: list[tuple[str, dict]]) -> dict:
    """서버별 번들 → 통합 인벤토리 dict."""
    inventory: dict = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "servers": [],
    }
    for server_id, bundle in bundles:
        summary = bundle.get("schema_summary", {})
        routines = bundle.get("routines", [])
        triggers = bundle.get("triggers", [])
        views = bundle.get("views", [])
        keys = bundle.get("keys", [])
        constraint_rules = _constraint_rules(keys)

        fk_list = [k for k in keys if k.get("constraint_type") == "FOREIGN KEY"]
        unique_list = [k for k in keys if k.get("constraint_type") == "UNIQUE"]

        extraction_mode = summary.get("extraction_mode", "unknown")
        uncollectable = extraction_mode == "mysql3_show_meta"

        entry = {
            "server_id": server_id,
            "extraction_mode": extraction_mode,
            "uncollectable_note": (
                "MySQL 3.23: INFORMATION_SCHEMA 미지원 — routines/triggers/views 자동 수집 불가. "
                "DBA 수동 확인 또는 mysql.proc 직접 조회 필요."
                if uncollectable
                else None
            ),
            "tables_count": summary.get("tables", 0),
            "routines_count": len(routines),
            "triggers_count": len(triggers),
            "views_count": len(views),
            "fk_count": len(fk_list),
            "unique_count": len(unique_list),
            "routines": routines,
            "triggers": triggers,
            "views": views,
            "foreign_keys": fk_list,
            "unique_constraints": unique_list,
            "constraint_rules": constraint_rules,
        }
        inventory["servers"].append(entry)

    return inventory


def render_markdown(inventory: dict) -> str:
    """인벤토리 dict → Markdown 문자열."""
    lines: list[str] = []
    lines.append("# DB 비즈니스 로직 인벤토리")
    lines.append("")
    lines.append(f"**자동 생성:** {inventory['generated_at']}  ")
    lines.append("**도구:** `tools/db/db_logic_reporter.py`  ")
    lines.append("**원칙:** 전체 DB dump·데이터 없음. 메타(INFORMATION_SCHEMA / SHOW)만 사용.")
    lines.append("")

    lines.append("## 서버별 요약")
    lines.append("")
    lines.append("| 서버 ID | 추출 모드 | 테이블 | 루틴 | 트리거 | 뷰 | FK | UNIQUE | 비고 |")
    lines.append("|---------|-----------|--------|------|--------|-----|-----|--------|------|")
    for s in inventory["servers"]:
        note = "⚠ 3.23 미수집" if s["uncollectable_note"] else "—"
        lines.append(
            f"| {s['server_id']} | {s['extraction_mode']} | {s['tables_count']} "
            f"| {s['routines_count']} | {s['triggers_count']} | {s['views_count']} "
            f"| {s['fk_count']} | {s['unique_count']} | {note} |"
        )
    lines.append("")

    for s in inventory["servers"]:
        lines.append(f"## {s['server_id']}")
        lines.append("")

        if s["uncollectable_note"]:
            lines.append(f"> **한계:** {s['uncollectable_note']}")
            lines.append("")

        if s["routines"]:
            lines.append("### 저장 루틴 (PROCEDURE / FUNCTION)")
            lines.append("")
            lines.append("| 이름 | 유형 | 정의(앞부분) | 비고 | 포팅 상태 |")
            lines.append("|------|------|-------------|------|-----------|")
            for r in s["routines"]:
                defn = (r.get("definition") or "")[:120].replace("\n", " ").replace("|", "\\|")
                lines.append(
                    f"| {r['name']} | {r['type']} | `{defn}` | {r.get('comment', '')} | 미검토 |"
                )
            lines.append("")

        if s["triggers"]:
            lines.append("### 트리거 (TRIGGER)")
            lines.append("")
            lines.append("| 이름 | 테이블 | 이벤트 | 타이밍 | 정의(앞부분) | 포팅 상태 |")
            lines.append("|------|--------|--------|--------|-------------|-----------|")
            for t in s["triggers"]:
                stmt = (t.get("statement") or "")[:120].replace("\n", " ").replace("|", "\\|")
                lines.append(
                    f"| {t['name']} | {t['table_name']} | {t['event']} | {t['timing']} "
                    f"| `{stmt}` | 미검토 |"
                )
            lines.append("")

        if s["views"]:
            lines.append("### 뷰 (VIEW)")
            lines.append("")
            lines.append("| 이름 | 정의(앞부분) | 포팅 상태 |")
            lines.append("|------|-------------|-----------|")
            for v in s["views"]:
                defn = (v.get("definition") or "")[:150].replace("\n", " ").replace("|", "\\|")
                lines.append(f"| {v['name']} | `{defn}` | 미검토 |")
            lines.append("")

        if s["foreign_keys"]:
            lines.append("### 외래키 (FOREIGN KEY)")
            lines.append("")
            lines.append("| 테이블 | 제약 이름 | 컬럼 | 참조 테이블 | 참조 컬럼 |")
            lines.append("|--------|----------|------|-----------|----------|")
            for fk in s["foreign_keys"]:
                lines.append(
                    f"| {fk['table_name']} | {fk['constraint_name']} | {fk['column_name']} "
                    f"| {fk['referenced_table']} | {fk['referenced_column']} |"
                )
            lines.append("")

        if s["unique_constraints"]:
            lines.append("### UNIQUE 제약")
            lines.append("")
            lines.append("| 테이블 | 제약 이름 | 컬럼 |")
            lines.append("|--------|----------|------|")
            for u in s["unique_constraints"]:
                lines.append(f"| {u['table_name']} | {u['constraint_name']} | {u['column_name']} |")
            lines.append("")

        if not any([s["routines"], s["triggers"], s["views"], s["foreign_keys"], s["unique_constraints"]]):
            if s["uncollectable_note"]:
                lines.append("DB 로직 객체 자동 수집 불가 (MySQL 3.23). DBA 수동 확인 필요.")
            else:
                lines.append("이 서버에서는 루틴·트리거·뷰·FK·UNIQUE 객체가 발견되지 않았습니다.")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 다음 조치")
    lines.append("")
    lines.append("1. 각 항목의 **포팅 상태**를 검토 후 갱신 (미검토 → 포팅 불필요 / 포팅 필요 / 완료).")
    lines.append("2. 3.23 인스턴스는 DBA 수동 확인 후 이 문서에 수기 추가.")
    lines.append("3. 교차맵(`analysis/db_logic_cross_reference.json`)과 함께 사용해 화면별 영향 확인.")
    lines.append("4. 갭 리포트(`docs/db-logic-porting-gap-report.md`) 주기 갱신.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="DB 비즈니스 로직 인벤토리 리포터")
    ap.add_argument("--bundle", help="단일 schema_bundle.json 경로")
    ap.add_argument("--schema-dir", help="서버별 bundle이 들어 있는 상위 디렉터리")
    ap.add_argument("--md-out", default=None, help="Markdown 출력 경로")
    ap.add_argument("--json-out", default=None, help="JSON 출력 경로")
    args = ap.parse_args()

    bundles: list[tuple[str, dict]] = []
    if args.schema_dir:
        bundles = _collect_bundles(Path(args.schema_dir))
    elif args.bundle:
        p = Path(args.bundle)
        server_id = p.parent.name
        bundles = [(server_id, _load_bundle(p))]
    else:
        default_dir = _REPO_ROOT / "debug" / "output" / "schema"
        if default_dir.is_dir():
            bundles = _collect_bundles(default_dir)
        if not bundles:
            print("[ERROR] --bundle 또는 --schema-dir을 지정하거나 debug/output/schema/를 준비하세요.", file=sys.stderr)
            sys.exit(1)

    if not bundles:
        print("[WARN] 번들을 찾지 못했습니다.", file=sys.stderr)
        sys.exit(1)

    inventory = build_inventory(bundles)

    md_path = Path(args.md_out) if args.md_out else _REPO_ROOT / "docs" / "db-business-logic-inventory.md"
    json_path = Path(args.json_out) if args.json_out else _REPO_ROOT / "analysis" / "db_logic_inventory.json"

    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    md_path.write_text(render_markdown(inventory), encoding="utf-8")
    json_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")

    total_r = sum(s["routines_count"] for s in inventory["servers"])
    total_t = sum(s["triggers_count"] for s in inventory["servers"])
    total_v = sum(s["views_count"] for s in inventory["servers"])
    print(f"[OK] 서버 {len(inventory['servers'])}대 · 루틴 {total_r} · 트리거 {total_t} · 뷰 {total_v}")
    print(f"     MD  → {md_path}")
    print(f"     JSON → {json_path}")


if __name__ == "__main__":
    main()
