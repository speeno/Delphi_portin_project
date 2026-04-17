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


def _probe_mysql3_routines(query_fn: Any, database: str) -> tuple[list[dict], str]:
    """MySQL 3.23에서 저장 루틴 수집을 시도한다. 실패하면 사유를 기록."""
    probes = [
        ("mysql.proc", f"SELECT name, type, body FROM mysql.proc WHERE db = '{database}'"),
        ("SHOW PROCEDURE STATUS", f"SHOW PROCEDURE STATUS WHERE Db = '{database}'"),
        ("SHOW FUNCTION STATUS", f"SHOW FUNCTION STATUS WHERE Db = '{database}'"),
    ]
    routines: list[dict] = []
    errors: list[str] = []
    for label, sql in probes:
        try:
            rows = query_fn(sql)
            for r in rows:
                name = r.get("name") or r.get("Name") or r.get("NAME") or ""
                rtype = r.get("type") or r.get("Type") or r.get("TYPE") or "PROCEDURE"
                body = r.get("body") or r.get("Body") or ""
                if name:
                    routines.append({
                        "name": str(name),
                        "type": str(rtype),
                        "definition": str(body)[:2000],
                        "comment": f"[mysql3 probe: {label}]",
                    })
        except Exception as exc:
            errors.append(f"{label}: {type(exc).__name__}: {str(exc)[:200]}")

    if routines:
        return routines, "collected"
    if errors:
        return [], f"uncollectable — {'; '.join(errors)}"
    return [], "uncollectable — no probe returned data"


def _probe_mysql3_triggers(query_fn: Any, database: str) -> tuple[list[dict], str]:
    """MySQL 3.23에서 트리거 수집을 시도한다 (3.23에는 트리거 없을 가능성 높음)."""
    probes = [
        ("SHOW TRIGGERS", "SHOW TRIGGERS"),
        ("INFORMATION_SCHEMA.TRIGGERS", f"SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_TIMING, ACTION_STATEMENT FROM INFORMATION_SCHEMA.TRIGGERS WHERE TRIGGER_SCHEMA = '{database}'"),
    ]
    triggers: list[dict] = []
    errors: list[str] = []
    for label, sql in probes:
        try:
            rows = query_fn(sql)
            for r in rows:
                name = r.get("Trigger") or r.get("TRIGGER_NAME") or r.get("trigger") or ""
                tbl = r.get("Table") or r.get("EVENT_OBJECT_TABLE") or r.get("table") or ""
                event = r.get("Event") or r.get("EVENT_MANIPULATION") or ""
                timing = r.get("Timing") or r.get("ACTION_TIMING") or ""
                stmt = r.get("Statement") or r.get("ACTION_STATEMENT") or ""
                if name:
                    triggers.append({
                        "name": str(name),
                        "table_name": str(tbl),
                        "event": str(event),
                        "timing": str(timing),
                        "statement": str(stmt)[:2000],
                    })
        except Exception as exc:
            errors.append(f"{label}: {type(exc).__name__}: {str(exc)[:200]}")

    if triggers:
        return triggers, "collected"
    if errors:
        return [], f"uncollectable — {'; '.join(errors)}"
    return [], "uncollectable — MySQL 3.23 does not support triggers"


def _probe_mysql3_views(query_fn: Any, database: str) -> tuple[list[dict], str]:
    """MySQL 3.23에서 뷰 수집을 시도한다 (3.23에는 뷰가 없으므로 빈 결과 예상)."""
    try:
        rows = query_fn(f"SELECT TABLE_NAME, VIEW_DEFINITION FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = '{database}'")
        views = []
        for r in rows:
            name = r.get("TABLE_NAME") or ""
            defn = r.get("VIEW_DEFINITION") or ""
            if name:
                views.append({"name": str(name), "definition": str(defn)[:2000]})
        if views:
            return views, "collected"
        return [], "uncollectable — no views found (MySQL 3.23 does not support views)"
    except Exception as exc:
        return [], f"uncollectable — {type(exc).__name__}: {str(exc)[:200]}"


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

    routines, routines_probe = _probe_mysql3_routines(query_fn, database)
    triggers, triggers_probe = _probe_mysql3_triggers(query_fn, database)
    views, views_probe = _probe_mysql3_views(query_fn, database)

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
        "routines": len(routines),
        "triggers": len(triggers),
        "views": len(views),
        "routines_probe": routines_probe,
        "triggers_probe": triggers_probe,
        "views_probe": views_probe,
    }
    return {
        "tables": tables,
        "columns": columns,
        "keys": keys,
        "indexes": indexes,
        "routines": routines,
        "triggers": triggers,
        "views": views,
        "table_ddl": table_create,
        "db_impact_matrix": impact,
        "schema_summary": summary,
    }
