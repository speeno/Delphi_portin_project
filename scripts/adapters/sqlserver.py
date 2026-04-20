"""C15 cut-over validator — SQL Server DataSource (Phase 2 — T6).

허용 쿼리 (시스템/구조)
-----------------------
- COUNT(*) FROM [<table>]                       — VC-1
- 행 fetch + Python sha256 (TOP N)              — VC-2
- TOP N text columns                            — VC-3 sample
- INFORMATION_SCHEMA.COLUMNS                    — VC-4/VC-5

DEC-040/044 — 신규 비즈니스 SQL 0건. pyodbc 는 lazy import.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from typing import Any, Iterator

from scripts.adapters.base import ServerProfile, sanitize_identifier


class SqlServerDataSource:
    """pyodbc 기반 SQL Server 시스템 쿼리 어댑터."""

    DRIVER = "sqlserver"
    _ROW_SAMPLE_LIMIT = 5000
    _DEFAULT_DRIVER_NAME = "ODBC Driver 17 for SQL Server"

    def __init__(self, profile: ServerProfile):
        if profile.driver != self.DRIVER:
            raise ValueError(f"profile driver mismatch: {profile.driver} != {self.DRIVER}")
        self._p = profile
        self._driver_mod = None  # pyodbc lazy

    def _import_driver(self):  # noqa: ANN001
        if self._driver_mod is not None:
            return self._driver_mod
        try:
            import pyodbc  # type: ignore[import-untyped]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"pyodbc not installed — install pyodbc to use {self._p.short()}",
            ) from exc
        self._driver_mod = pyodbc
        return pyodbc

    def _connection_string(self) -> str:
        odbc_driver = self._p.options.get("odbc_driver", self._DEFAULT_DRIVER_NAME)
        encrypt = self._p.options.get("encrypt", "no")
        trust = self._p.options.get("trust_server_certificate", "yes")
        return (
            f"DRIVER={{{odbc_driver}}};"
            f"SERVER={self._p.host},{self._p.port};"
            f"DATABASE={self._p.database};"
            f"UID={self._p.user};"
            f"PWD={self._p.password};"
            f"Encrypt={encrypt};"
            f"TrustServerCertificate={trust};"
        )

    @contextmanager
    def _cursor(self) -> Iterator[Any]:
        odbc = self._import_driver()
        conn = odbc.connect(
            self._connection_string(),
            timeout=int(self._p.options.get("connect_timeout", 15)),
            autocommit=True,
        )
        try:
            cur = conn.cursor()
            try:
                yield cur
            finally:
                cur.close()
        finally:
            conn.close()

    # ─── DataSource 4 method ──────────────────────────────────────
    def fetch_count(self, table: str) -> int:
        t = sanitize_identifier(table, kind="table")
        with self._cursor() as cur:
            cur.execute(f"SELECT COUNT_BIG(*) FROM [{t}]")
            row = cur.fetchone()
            return int(row[0] if row else 0)

    def fetch_checksum(self, table: str, columns: list[str]) -> str:
        t = sanitize_identifier(table, kind="table")
        if columns == ["*"]:
            cols_sql = "*"
        else:
            cols_safe = [sanitize_identifier(c, kind="column") for c in columns]
            cols_sql = ", ".join(f"[{c}]" for c in cols_safe)
        h = hashlib.sha256()
        with self._cursor() as cur:
            cur.execute(f"SELECT TOP {self._ROW_SAMPLE_LIMIT} {cols_sql} FROM [{t}]")
            for row in cur.fetchall():
                for v in row:
                    h.update(repr(v).encode("utf-8"))
        return h.hexdigest()

    def fetch_schema(self, table: str) -> dict[str, str]:
        t = sanitize_identifier(table, kind="table")
        with self._cursor() as cur:
            cur.execute(
                """
                SELECT COLUMN_NAME, DATA_TYPE
                  FROM INFORMATION_SCHEMA.COLUMNS
                 WHERE TABLE_NAME = ?
                """,
                (t,),
            )
            return {str(row[0]): str(row[1]).upper() for row in cur.fetchall()}

    def fetch_sample_text(self, table: str, columns: list[str], limit: int = 100) -> list[str]:
        t = sanitize_identifier(table, kind="table")
        if columns == ["*"]:
            cols_sql = "*"
        else:
            cols_safe = [sanitize_identifier(c, kind="column") for c in columns]
            cols_sql = ", ".join(f"[{c}]" for c in cols_safe)
        n = max(1, min(int(limit), self._ROW_SAMPLE_LIMIT))
        out: list[str] = []
        with self._cursor() as cur:
            cur.execute(f"SELECT TOP {n} {cols_sql} FROM [{t}]")
            for row in cur.fetchall():
                for v in row:
                    if isinstance(v, str):
                        out.append(v)
                    elif isinstance(v, (bytes, bytearray)):
                        try:
                            out.append(v.decode("utf-8"))
                        except Exception:  # noqa: BLE001
                            out.append("<binary>")
        return out
