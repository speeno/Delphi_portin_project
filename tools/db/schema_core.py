"""
INFORMATION_SCHEMA 기반 스키마 메타 추출 (데이터/전체 덤프 없음).

mysql-connector 또는 PyMySQL DictCursor와 함께 사용한다.
"""

from __future__ import annotations

from typing import Any


def extract_tables(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT TABLE_NAME, TABLE_TYPE, ENGINE, TABLE_ROWS, TABLE_COMMENT
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
        """,
        (database,),
    )

    return [
        {
            "table_name": row[0],
            "table_type": row[1],
            "engine": row[2],
            "approx_rows": row[3],
            "comment": row[4] or "",
        }
        for row in cursor.fetchall()
    ]


def extract_columns(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT TABLE_NAME, COLUMN_NAME, ORDINAL_POSITION, COLUMN_TYPE,
               IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT, COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """,
        (database,),
    )

    return [
        {
            "table_name": row[0],
            "column_name": row[1],
            "position": row[2],
            "column_type": row[3],
            "nullable": row[4],
            "default_value": str(row[5]) if row[5] is not None else None,
            "comment": row[6] or "",
            "key": row[7] or "",
        }
        for row in cursor.fetchall()
    ]


def extract_keys(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT tc.TABLE_NAME, tc.CONSTRAINT_NAME, tc.CONSTRAINT_TYPE,
               kcu.COLUMN_NAME, kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
          ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
          AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
          AND tc.TABLE_NAME = kcu.TABLE_NAME
        WHERE tc.TABLE_SCHEMA = %s
        ORDER BY tc.TABLE_NAME, tc.CONSTRAINT_NAME
        """,
        (database,),
    )

    return [
        {
            "table_name": row[0],
            "constraint_name": row[1],
            "constraint_type": row[2],
            "column_name": row[3],
            "referenced_table": row[4] or "",
            "referenced_column": row[5] or "",
        }
        for row in cursor.fetchall()
    ]


def extract_indexes(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT TABLE_NAME, INDEX_NAME, NON_UNIQUE, COLUMN_NAME, SEQ_IN_INDEX, INDEX_TYPE
        FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX
        """,
        (database,),
    )

    return [
        {
            "table_name": row[0],
            "index_name": row[1],
            "non_unique": bool(row[2]),
            "column_name": row[3],
            "seq": row[4],
            "index_type": row[5],
        }
        for row in cursor.fetchall()
    ]


def extract_routines(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT ROUTINE_NAME, ROUTINE_TYPE, ROUTINE_DEFINITION, ROUTINE_COMMENT
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE ROUTINE_SCHEMA = %s
        ORDER BY ROUTINE_TYPE, ROUTINE_NAME
        """,
        (database,),
    )

    return [
        {
            "name": row[0],
            "type": row[1],
            "definition": (row[2] or "")[:2000],
            "comment": row[3] or "",
        }
        for row in cursor.fetchall()
    ]


def extract_triggers(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE,
               ACTION_TIMING, ACTION_STATEMENT
        FROM INFORMATION_SCHEMA.TRIGGERS
        WHERE TRIGGER_SCHEMA = %s
        ORDER BY EVENT_OBJECT_TABLE, TRIGGER_NAME
        """,
        (database,),
    )

    return [
        {
            "name": row[0],
            "event": row[1],
            "table_name": row[2],
            "timing": row[3],
            "statement": (row[4] or "")[:2000],
        }
        for row in cursor.fetchall()
    ]


def extract_views(cursor: Any, database: str) -> list[dict]:
    cursor.execute(
        """
        SELECT TABLE_NAME, VIEW_DEFINITION
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
        """,
        (database,),
    )

    return [
        {
            "name": row[0],
            "definition": (row[1] or "")[:2000],
        }
        for row in cursor.fetchall()
    ]


def build_db_impact_matrix(
    tables: list[dict], columns: list[dict], keys: list[dict]
) -> dict[str, Any]:
    table_map: dict[str, Any] = {}
    for t in tables:
        name = t["table_name"]
        table_map[name] = {
            "table_name": name,
            "columns": [],
            "pk_columns": [],
            "fk_references": [],
            "referenced_by": [],
        }

    for c in columns:
        tn = c["table_name"]
        if tn in table_map:
            table_map[tn]["columns"].append(c["column_name"])

    for k in keys:
        tn = k["table_name"]
        if tn not in table_map:
            continue
        if k["constraint_type"] == "PRIMARY KEY":
            table_map[tn]["pk_columns"].append(k["column_name"])
        elif k["constraint_type"] == "FOREIGN KEY" and k["referenced_table"]:
            table_map[tn]["fk_references"].append(
                {
                    "column": k["column_name"],
                    "references_table": k["referenced_table"],
                    "references_column": k["referenced_column"],
                }
            )
            if k["referenced_table"] in table_map:
                table_map[k["referenced_table"]]["referenced_by"].append(
                    {
                        "from_table": tn,
                        "from_column": k["column_name"],
                    }
                )

    return table_map


def extract_modern_full(cursor: Any, database: str) -> dict[str, Any]:
    """INFORMATION_SCHEMA 전부(메타만)."""
    tables = extract_tables(cursor, database)
    columns = extract_columns(cursor, database)
    keys = extract_keys(cursor, database)
    indexes = extract_indexes(cursor, database)
    routines = extract_routines(cursor, database)
    triggers = extract_triggers(cursor, database)
    views = extract_views(cursor, database)
    impact = build_db_impact_matrix(tables, columns, keys)
    summary = {
        "database": database,
        "extraction_mode": "information_schema",
        "tables": len(tables),
        "columns": len(columns),
        "keys": len(keys),
        "indexes": len(indexes),
        "routines": len(routines),
        "triggers": len(triggers),
        "views": len(views),
    }
    return {
        "tables": tables,
        "columns": columns,
        "keys": keys,
        "indexes": indexes,
        "routines": routines,
        "triggers": triggers,
        "views": views,
        "db_impact_matrix": impact,
        "schema_summary": summary,
    }
