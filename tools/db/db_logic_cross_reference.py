#!/usr/bin/env python3
"""
DB 비즈니스 로직 교차 참조 빌더

델파이 정적 분석 산출물(query_catalog / event_flow / pas_inventory)과
DB 스키마 인벤토리(routines / triggers / views)를 조인하여,
화면·기능 단위로 "어떤 DB 로직이 관련되는가"를 추적하는 교차맵 JSON을 생성한다.

사용법
------
  python3 tools/db/db_logic_cross_reference.py \\
      --analysis-dir analysis \\
      --schema-dir debug/output/schema \\
      --output analysis/db_logic_cross_reference.json

  # captured_queries.json이 있으면 --capture로 합류
  python3 tools/db/db_logic_cross_reference.py \\
      --analysis-dir analysis --schema-dir debug/output/schema \\
      --capture debug/output/captured_queries.json \\
      --output analysis/db_logic_cross_reference.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load(path: str | Path) -> list | dict:
    p = Path(path)
    if not p.is_file():
        return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _collect_db_objects(schema_dir: Path) -> dict:
    """서버별 routines/triggers/views를 통합."""
    db_objects: dict = {"routines": {}, "triggers": {}, "views": {}}
    if not schema_dir.is_dir():
        return db_objects
    for sub in sorted(schema_dir.iterdir()):
        bundle_path = sub / "schema_bundle.json"
        if not bundle_path.is_file():
            continue
        bundle = _load(bundle_path)
        sid = sub.name
        for r in bundle.get("routines", []):
            key = r.get("name", "")
            if key:
                db_objects["routines"].setdefault(key, []).append({**r, "_server": sid})
        for t in bundle.get("triggers", []):
            key = t.get("name", "")
            if key:
                db_objects["triggers"].setdefault(key, []).append({**t, "_server": sid})
        for v in bundle.get("views", []):
            key = v.get("name", "")
            if key:
                db_objects["views"].setdefault(key, []).append({**v, "_server": sid})
    return db_objects


def _extract_call_targets(sql: str) -> list[str]:
    """SQL 문자열에서 CALL/EXEC 대상 루틴 이름을 추출."""
    targets = set()
    for m in re.finditer(r'\bCALL\s+`?(\w+)`?', sql, re.IGNORECASE):
        targets.add(m.group(1))
    for m in re.finditer(r'\bEXEC(?:UTE)?\s+`?(\w+)`?', sql, re.IGNORECASE):
        targets.add(m.group(1))
    return sorted(targets)


def _extract_tables_from_sql(sql: str) -> list[str]:
    """SQL에서 테이블 이름 추출 (간이)."""
    tables = set()
    for p in [
        re.compile(r'\bFROM\s+`?(\w+)`?', re.IGNORECASE),
        re.compile(r'\bJOIN\s+`?(\w+)`?', re.IGNORECASE),
        re.compile(r'\bINTO\s+`?(\w+)`?', re.IGNORECASE),
        re.compile(r'\bUPDATE\s+`?(\w+)`?', re.IGNORECASE),
        re.compile(r'\bDELETE\s+FROM\s+`?(\w+)`?', re.IGNORECASE),
    ]:
        for m in p.finditer(sql):
            tables.add(m.group(1))
    return sorted(tables)


def build_cross_reference(
    analysis_dir: Path,
    db_objects: dict,
    captured_queries: list[dict],
) -> dict:
    query_catalog = _load(analysis_dir / "query_catalog.json")
    event_flow = _load(analysis_dir / "event_flow.json")
    pas_inventory = _load(analysis_dir / "pas_inventory.json")

    unit_form_map: dict[str, str] = {}
    for pas in pas_inventory:
        unit = pas.get("unit_name", "")
        for eh in pas.get("event_handlers", []):
            cls = eh.get("class", "")
            if cls and unit:
                unit_form_map[unit] = cls

    trigger_table_map: dict[str, list[dict]] = {}
    for _name, entries in db_objects.get("triggers", {}).items():
        for entry in entries:
            tbl = entry.get("table_name", "")
            if tbl:
                trigger_table_map.setdefault(tbl, []).append(entry)

    view_names = set(db_objects.get("views", {}).keys())
    routine_names = set(db_objects.get("routines", {}).keys())

    table_refs: dict[str, dict] = {}

    for sq in query_catalog:
        sql = sq.get("sql", "")
        unit = sq.get("unit", "")
        sql_type = sq.get("type", "UNKNOWN")
        form = unit_form_map.get(unit, "")
        tables = sq.get("tables", []) or _extract_tables_from_sql(sql)
        call_targets = _extract_call_targets(sql)

        for tbl in tables:
            rec = table_refs.setdefault(tbl, {
                "table_name": tbl,
                "is_view": tbl in view_names,
                "units": [],
                "forms": [],
                "operations": {"SELECT": 0, "INSERT": 0, "UPDATE": 0, "DELETE": 0, "CALL": 0},
                "triggered_by": [],
                "routine_calls": [],
                "captured_queries": [],
            })
            if unit and unit not in rec["units"]:
                rec["units"].append(unit)
            if form and form not in rec["forms"]:
                rec["forms"].append(form)
            if sql_type in rec["operations"]:
                rec["operations"][sql_type] += 1

        for target in call_targets:
            for tbl in tables:
                rec = table_refs.get(tbl) or table_refs.setdefault(tbl, {
                    "table_name": tbl, "is_view": False, "units": [],
                    "forms": [], "operations": {"SELECT": 0, "INSERT": 0, "UPDATE": 0, "DELETE": 0, "CALL": 0},
                    "triggered_by": [], "routine_calls": [], "captured_queries": [],
                })
                if target not in rec["routine_calls"]:
                    rec["routine_calls"].append(target)

    for tbl, triggers in trigger_table_map.items():
        rec = table_refs.get(tbl)
        if rec is None:
            rec = {
                "table_name": tbl, "is_view": False, "units": [],
                "forms": [], "operations": {"SELECT": 0, "INSERT": 0, "UPDATE": 0, "DELETE": 0, "CALL": 0},
                "triggered_by": [], "routine_calls": [], "captured_queries": [],
            }
            table_refs[tbl] = rec
        for t in triggers:
            info = {
                "trigger_name": t.get("name", ""),
                "event": t.get("event", ""),
                "timing": t.get("timing", ""),
                "server": t.get("_server", ""),
            }
            if info not in rec["triggered_by"]:
                rec["triggered_by"].append(info)

    for cq in captured_queries:
        sql = cq.get("sql", "")
        tables = cq.get("tables", []) or _extract_tables_from_sql(sql)
        for tbl in tables:
            rec = table_refs.get(tbl)
            if rec is None:
                rec = {
                    "table_name": tbl, "is_view": tbl in view_names, "units": [],
                    "forms": [], "operations": {"SELECT": 0, "INSERT": 0, "UPDATE": 0, "DELETE": 0, "CALL": 0},
                    "triggered_by": [], "routine_calls": [], "captured_queries": [],
                }
                table_refs[tbl] = rec
            norm = cq.get("normalized", sql[:200])
            if norm not in rec["captured_queries"]:
                rec["captured_queries"].append(norm)

    orphan_routines = []
    referenced_routines = set()
    for rec in table_refs.values():
        referenced_routines.update(rec["routine_calls"])
    for rname in routine_names:
        if rname not in referenced_routines:
            orphan_routines.append({
                "name": rname,
                "servers": [e["_server"] for e in db_objects["routines"][rname]],
                "note": "DB에 존재하나 델파이 SQL에서 호출 미발견(동적 SQL·외부 호출 가능성 조사 필요)",
            })

    orphan_views = []
    referenced_views = {tbl for tbl, rec in table_refs.items() if rec["is_view"]}
    for vname in view_names:
        if vname not in referenced_views:
            orphan_views.append({
                "name": vname,
                "servers": [e["_server"] for e in db_objects["views"][vname]],
                "note": "DB에 뷰로 존재하나 델파이 SQL에서 참조 미발견",
            })

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "table_cross_reference": dict(sorted(table_refs.items())),
        "orphan_routines": orphan_routines,
        "orphan_views": orphan_views,
        "summary": {
            "tables_referenced": len(table_refs),
            "tables_with_triggers": sum(1 for r in table_refs.values() if r["triggered_by"]),
            "tables_with_routine_calls": sum(1 for r in table_refs.values() if r["routine_calls"]),
            "tables_that_are_views": sum(1 for r in table_refs.values() if r["is_view"]),
            "orphan_routines": len(orphan_routines),
            "orphan_views": len(orphan_views),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="DB 비즈니스 로직 교차 참조 빌더")
    ap.add_argument("--analysis-dir", default=str(_REPO_ROOT / "analysis"))
    ap.add_argument("--schema-dir", default=str(_REPO_ROOT / "debug" / "output" / "schema"))
    ap.add_argument("--capture", default=None, help="captured_queries.json 경로 (선택)")
    ap.add_argument("--output", default=str(_REPO_ROOT / "analysis" / "db_logic_cross_reference.json"))
    args = ap.parse_args()

    db_objects = _collect_db_objects(Path(args.schema_dir))
    captured = _load(args.capture) if args.capture else []

    xref = build_cross_reference(Path(args.analysis_dir), db_objects, captured)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(xref, ensure_ascii=False, indent=2), encoding="utf-8")

    s = xref["summary"]
    print(f"[OK] 교차맵: 테이블 {s['tables_referenced']}건")
    print(f"     트리거 영향 {s['tables_with_triggers']} · 루틴 호출 {s['tables_with_routine_calls']} · 뷰 {s['tables_that_are_views']}")
    print(f"     미참조 루틴(orphan) {s['orphan_routines']} · 미참조 뷰 {s['orphan_views']}")
    print(f"     → {out}")


if __name__ == "__main__":
    main()
