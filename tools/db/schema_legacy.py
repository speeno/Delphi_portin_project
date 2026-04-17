"""
MySQL 3.x / INFORMATION_SCHEMA 미지원 환경용 스키마 메타 추출.

데이터 행은 조회하지 않으며 SHOW TABLES / SHOW FIELDS / SHOW KEYS /
SHOW CREATE TABLE 결과만 사용한다 (전체 DB 덤프 없음).
"""

from __future__ import annotations

from typing import Any


def _first_cell(row: dict[str, Any]) -> str:
    if not row:
        return ""
    v = next(iter(row.values()))
    return str(v).strip() if v is not None else ""


def _esc_ident(name: str) -> str:
    return "`" + name.replace("`", "``") + "`"


def extract_mysql3_meta(
    query_fn: Any, database: str, *, create_sql_max: int = 12000
) -> dict[str, Any]:
    """
    query_fn(sql) -> list[dict]  (예: functools.partial(query_mysql3, conn, charset=...))
    """
    # 핸드셰이크에서 DB가 이미 선택된 것을 전제로 SHOW TABLES 만 사용
    rows = query_fn("SHOW TABLES")
    table_names: list[str] = []
    for r in rows:
        name = _first_cell(r)
        if name:
            table_names.append(name)

    tables: list[dict] = []
    columns: list[dict] = []
    keys: list[dict] = []
    indexes: list[dict] = []
    table_create: list[dict] = []

    for i, tname in enumerate(sorted(table_names), start=1):
        tables.append(
            {
                "table_name": tname,
                "table_type": "BASE TABLE",
                "engine": "",
                "approx_rows": None,
                "comment": "",
            }
        )

        fields = query_fn(f"SHOW FIELDS FROM {_esc_ident(tname)}")
        for pos, row in enumerate(fields, start=1):
            fn = row.get("Field") or row.get("field")
            typ = row.get("Type") or row.get("type")
            null_raw = row.get("Null") or row.get("null") or "YES"
            key_raw = row.get("Key") or row.get("key") or ""
            default = row.get("Default")
            if default is not None and not isinstance(default, str):
                default = str(default)
            extra = row.get("Extra") or row.get("extra") or ""
            columns.append(
                {
                    "table_name": tname,
                    "column_name": str(fn),
                    "position": pos,
                    "column_type": str(typ),
                    "nullable": "YES" if str(null_raw).upper() == "YES" else "NO",
                    "default_value": default,
                    "comment": str(extra) if extra else "",
                    "key": str(key_raw),
                }
            )

        # SHOW INDEX / KEYS — 3.23 호환
        try:
            krows = query_fn(f"SHOW KEYS FROM {_esc_ident(tname)}")
        except Exception:
            krows = []

        seen_key: set[tuple[str, str, str]] = set()
        for kr in krows:
            non_unique = int(kr.get("Non_unique", kr.get("non_unique", 1)))
            key_name = str(kr.get("Key_name", kr.get("key_name", "")))
            col_name = str(kr.get("Column_name", kr.get("column_name", "")))
            seq = int(kr.get("Seq_in_index", kr.get("seq_in_index", 1)))
            if key_name == "PRIMARY":
                ctype = "PRIMARY KEY"
            elif non_unique == 0:
                ctype = "UNIQUE"
            else:
                ctype = "INDEX"
            dedupe = (tname, key_name, col_name)
            if dedupe in seen_key:
                continue
            seen_key.add(dedupe)
            keys.append(
                {
                    "table_name": tname,
                    "constraint_name": key_name,
                    "constraint_type": ctype,
                    "column_name": col_name,
                    "referenced_table": "",
                    "referenced_column": "",
                }
            )
            indexes.append(
                {
                    "table_name": tname,
                    "index_name": key_name,
                    "non_unique": bool(non_unique),
                    "column_name": col_name,
                    "seq": seq,
                    "index_type": "BTREE",
                }
            )

        try:
            crt = query_fn(f"SHOW CREATE TABLE {_esc_ident(tname)}")
            if crt:
                row0 = crt[0]
                create_sql = ""
                for k, v in row0.items():
                    if k and str(k).lower().replace(" ", "") in (
                        "createtable",
                        "create_table",
                    ):
                        create_sql = str(v or "")
                        break
                if not create_sql:
                    create_sql = _first_cell(row0)
                table_create.append(
                    {
                        "table_name": tname,
                        "create_sql": create_sql[:create_sql_max],
                    }
                )
        except Exception:
            table_create.append({"table_name": tname, "create_sql": ""})

    import sys
    from pathlib import Path

    _d = Path(__file__).resolve().parent
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))
    import schema_core as _sc

    impact = _sc.build_db_impact_matrix(tables, columns, keys)
    summary = {
        "database": database,
        "extraction_mode": "mysql3_show_meta",
        "tables": len(tables),
        "columns": len(columns),
        "keys": len(keys),
        "indexes": len(indexes),
        "routines": 0,
        "triggers": 0,
        "views": 0,
    }
    return {
        "tables": tables,
        "columns": columns,
        "keys": keys,
        "indexes": indexes,
        "routines": [],
        "triggers": [],
        "views": [],
        "table_ddl": table_create,
        "db_impact_matrix": impact,
        "schema_summary": summary,
    }
