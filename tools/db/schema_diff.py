#!/usr/bin/env python3
"""
두 스키마 추출 디렉터리(schema_bundle.json 또는 tables/columns.json)를 비교한다.

데이터 덤프 없이 메타 JSON만 비교한다.

사용법
------
  python3 tools/db/schema_diff.py debug/output/schema/remote_138 debug/output/schema/remote_153
  python3 tools/db/schema_diff.py dirA dirB -o debug/output/schema/diff-report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_bundle(dir_path: Path) -> dict[str, Any]:
    bundle_path = dir_path / "schema_bundle.json"
    if bundle_path.is_file():
        return json.loads(bundle_path.read_text(encoding="utf-8"))
    tables = json.loads((dir_path / "tables.json").read_text(encoding="utf-8"))
    columns = json.loads((dir_path / "columns.json").read_text(encoding="utf-8"))
    keys = json.loads((dir_path / "keys.json").read_text(encoding="utf-8"))
    indexes = json.loads((dir_path / "indexes.json").read_text(encoding="utf-8"))
    summary_path = dir_path / "schema_summary.json"
    summary = (
        json.loads(summary_path.read_text(encoding="utf-8"))
        if summary_path.is_file()
        else {}
    )
    out: dict[str, Any] = {
        "schema_summary": summary,
        "tables": tables,
        "columns": columns,
        "keys": keys,
        "indexes": indexes,
    }
    ddl = dir_path / "table_ddl.json"
    if ddl.is_file():
        out["table_ddl"] = json.loads(ddl.read_text(encoding="utf-8"))
    return out


def _table_names(tables: list[dict]) -> set[str]:
    return {t["table_name"] for t in tables}


def _column_sig(col: dict) -> tuple:
    return (
        col["table_name"],
        col["column_name"],
        str(col.get("position", "")),
        str(col.get("column_type", "")),
        str(col.get("nullable", "")),
        str(col.get("default_value", "")),
        str(col.get("key", "")),
    )


def _column_map(columns: list[dict]) -> dict[tuple[str, str], tuple]:
    return {(c["table_name"], c["column_name"]): _column_sig(c) for c in columns}


def compare(left: dict[str, Any], right: dict[str, Any], left_label: str, right_label: str) -> dict[str, Any]:
    lt = left.get("tables") or []
    rt = right.get("tables") or []
    l_names = _table_names(lt)
    r_names = _table_names(rt)

    only_left = sorted(l_names - r_names)
    only_right = sorted(r_names - l_names)
    common = sorted(l_names & r_names)

    lcols = _column_map(left.get("columns") or [])
    rcols = _column_map(right.get("columns") or [])

    column_mismatches: list[dict[str, Any]] = []
    for t in common:
        l_keys = {k for k in lcols if k[0] == t}
        r_keys = {k for k in rcols if k[0] == t}
        for k in sorted(l_keys - r_keys):
            column_mismatches.append(
                {"kind": "column_only_left", "table": t, "column": k[1]}
            )
        for k in sorted(r_keys - l_keys):
            column_mismatches.append(
                {"kind": "column_only_right", "table": t, "column": k[1]}
            )
        for k in sorted(l_keys & r_keys):
            if lcols[k] != rcols[k]:
                column_mismatches.append(
                    {
                        "kind": "column_def_diff",
                        "table": t,
                        "column": k[1],
                        "left": lcols[k],
                        "right": rcols[k],
                    }
                )

    ddl_diff: list[dict[str, Any]] = []
    lddl = {d["table_name"]: d.get("create_sql", "") for d in (left.get("table_ddl") or [])}
    rddl = {d["table_name"]: d.get("create_sql", "") for d in (right.get("table_ddl") or [])}
    for t in common:
        if t in lddl and t in rddl and lddl[t] != rddl[t]:
            ddl_diff.append({"table": t, "left_len": len(lddl[t]), "right_len": len(rddl[t])})

    return {
        "left": left_label,
        "right": right_label,
        "summary": {
            "tables_left": len(l_names),
            "tables_right": len(r_names),
            "only_in_left": len(only_left),
            "only_in_right": len(only_right),
            "common_tables": len(common),
            "column_issue_count": len(column_mismatches),
            "ddl_diff_count": len(ddl_diff),
        },
        "only_in_left_tables": only_left,
        "only_in_right_tables": only_right,
        "column_issues": column_mismatches,
        "ddl_len_mismatch_tables": ddl_diff,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="스키마 메타 디렉터리 두 개 비교")
    ap.add_argument("dir_a", type=Path, help="첫 번째 추출 디렉터리")
    ap.add_argument("dir_b", type=Path, help="두 번째 추출 디렉터리")
    ap.add_argument("-o", "--output", type=Path, default=None, help="JSON 리포트 저장 경로")
    args = ap.parse_args()

    if not args.dir_a.is_dir() or not args.dir_b.is_dir():
        print("[ERROR] 두 인자 모두 존재하는 디렉터리여야 합니다.", file=sys.stderr)
        sys.exit(1)

    a = _load_bundle(args.dir_a)
    b = _load_bundle(args.dir_b)
    report = compare(a, b, str(args.dir_a), str(args.dir_b))

    text_lines = [
        f"# Schema diff",
        f"- left: `{report['left']}`",
        f"- right: `{report['right']}`",
        "",
        "## 요약",
        "",
        f"- tables: left={report['summary']['tables_left']}, right={report['summary']['tables_right']}",
        f"- only in left: {report['summary']['only_in_left']}",
        f"- only in right: {report['summary']['only_in_right']}",
        f"- common tables: {report['summary']['common_tables']}",
        f"- column issues: {report['summary']['column_issue_count']}",
        f"- DDL length mismatches (legacy): {report['summary']['ddl_diff_count']}",
        "",
    ]
    if report["only_in_left_tables"][:30]:
        text_lines.append("## Only in left (sample)")
        for t in report["only_in_left_tables"][:30]:
            text_lines.append(f"- {t}")
        text_lines.append("")
    if report["only_in_right_tables"][:30]:
        text_lines.append("## Only in right (sample)")
        for t in report["only_in_right_tables"][:30]:
            text_lines.append(f"- {t}")
        text_lines.append("")

    out_json = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out_json, encoding="utf-8")
        md_path = args.output.with_suffix(".md")
        md_path.write_text("\n".join(text_lines), encoding="utf-8")
        print(f"[OK] JSON → {args.output}")
        print(f"     MD  → {md_path}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
