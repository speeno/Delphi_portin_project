"""tools/db/schema_diff.py 비교 로직 스모크 테스트."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "db"))

from schema_diff import compare  # noqa: E402


def _write_bundle(path: Path, tables, columns) -> None:
    path.mkdir(parents=True, exist_ok=True)
    summary = {
        "database": "db",
        "extraction_mode": "test",
        "tables": len(tables),
        "columns": len(columns),
        "keys": 0,
        "indexes": 0,
        "routines": 0,
        "triggers": 0,
        "views": 0,
    }
    bundle = {
        "schema_summary": summary,
        "tables": tables,
        "columns": columns,
        "keys": [],
        "indexes": [],
        "routines": [],
        "triggers": [],
        "views": [],
    }
    (path / "schema_bundle.json").write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def test_schema_diff_identical(tmp_path: Path) -> None:
    d = tmp_path / "a"
    tables = [
        {
            "table_name": "T1",
            "table_type": "BASE TABLE",
            "engine": "InnoDB",
            "approx_rows": 0,
            "comment": "",
        }
    ]
    columns = [
        {
            "table_name": "T1",
            "column_name": "id",
            "position": 1,
            "column_type": "int(11)",
            "nullable": "NO",
            "default_value": None,
            "comment": "",
            "key": "PRI",
        }
    ]
    _write_bundle(d, tables, columns)
    b1 = json.loads((d / "schema_bundle.json").read_text(encoding="utf-8"))
    r = compare(b1, b1, "a", "a")
    assert r["summary"]["only_in_left"] == 0
    assert r["summary"]["only_in_right"] == 0
    assert r["summary"]["column_issue_count"] == 0


def test_schema_diff_extra_table(tmp_path: Path) -> None:
    left = tmp_path / "L"
    right = tmp_path / "R"
    base_table = [
        {
            "table_name": "T1",
            "table_type": "BASE TABLE",
            "engine": "InnoDB",
            "approx_rows": 0,
            "comment": "",
        }
    ]
    col = [
        {
            "table_name": "T1",
            "column_name": "id",
            "position": 1,
            "column_type": "int(11)",
            "nullable": "NO",
            "default_value": None,
            "comment": "",
            "key": "PRI",
        }
    ]
    _write_bundle(left, base_table, col)
    _write_bundle(
        right,
        base_table
        + [
            {
                "table_name": "T2",
                "table_type": "BASE TABLE",
                "engine": "InnoDB",
                "approx_rows": 0,
                "comment": "",
            }
        ],
        col,
    )
    b_l = json.loads((left / "schema_bundle.json").read_text(encoding="utf-8"))
    b_r = json.loads((right / "schema_bundle.json").read_text(encoding="utf-8"))
    r = compare(b_l, b_r, "L", "R")
    assert "T2" in r["only_in_right_tables"]
    assert r["summary"]["only_in_right"] == 1
