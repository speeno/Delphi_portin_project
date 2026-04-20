"""C15 cut-over validator — MySQL DataSource (Phase 2 — T6).

허용 쿼리
---------
- COUNT(*) FROM `<table>`                — VC-1
- 행 fetch + Python sha256 (LIMIT 5000)  — VC-2 (column 화이트리스트 검증)
- LIMIT N text columns                   — VC-3 sample
- information_schema.COLUMNS             — VC-4/VC-5 schema

신규 비즈니스 SQL 0건 — DEC-040/044.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from typing import Any, Iterator

from scripts.adapters.base import ServerProfile, sanitize_identifier


class MysqlDataSource:
    """pymysql 기반 시스템 쿼리 어댑터.

    실제 import 는 lazy — pymysql 미설치 환경에서도 본 모듈은 import 가능.
    """

    DRIVER = "mysql"
    _ROW_SAMPLE_LIMIT = 5000   # checksum 계산 시 안전 한도 (메모리 보호)

    def __init__(self, profile: ServerProfile, *, charset: str = "utf8mb4"):
        if profile.driver != self.DRIVER:
            raise ValueError(f"profile driver mismatch: {profile.driver} != {self.DRIVER}")
        self._p = profile
        self._charset = charset
        self._driver_mod = None  # pymysql lazy-loaded

    # ─── 연결 관리 ─────────────────────────────────────────────────
    def _import_driver(self):  # noqa: ANN001 - returns module
        if self._driver_mod is not None:
            return self._driver_mod
        try:
            import pymysql  # type: ignore[import-untyped]
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"pymysql not installed — install pymysql to use {self._p.short()}",
            ) from exc
        self._driver_mod = pymysql
        return pymysql

    @contextmanager
    def _cursor(self) -> Iterator[Any]:
        pm = self._import_driver()
        conn = pm.connect(
            host=self._p.host,
            port=self._p.port,
            user=self._p.user,
            password=self._p.password,
            database=self._p.database,
            charset=self._charset,
            connect_timeout=int(self._p.options.get("connect_timeout", 15)),
            read_timeout=int(self._p.options.get("read_timeout", 120)),
            autocommit=True,
        )
        try:
            with conn.cursor() as cur:
                yield cur
        finally:
            conn.close()

    # ─── DataSource 4 method ──────────────────────────────────────
    def fetch_count(self, table: str) -> int:
        t = sanitize_identifier(table, kind="table")
        with self._cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM `{t}`")
            row = cur.fetchone()
            return int(row[0] if row else 0)

    def fetch_checksum(self, table: str, columns: list[str]) -> str:
        t = sanitize_identifier(table, kind="table")
        if columns == ["*"]:
            cols_sql = "*"
            cols_safe: list[str] = []   # 모든 컬럼이라 정렬 안 함
        else:
            cols_safe = [sanitize_identifier(c, kind="column") for c in columns]
            cols_sql = ", ".join(f"`{c}`" for c in cols_safe)
        h = hashlib.sha256()
        with self._cursor() as cur:
            cur.execute(f"SELECT {cols_sql} FROM `{t}` LIMIT %s", (self._ROW_SAMPLE_LIMIT,))
            for row in cur.fetchall():
                if cols_sql == "*":
                    for v in row:
                        h.update(repr(v).encode("utf-8"))
                else:
                    for v in row:
                        h.update(repr(v).encode("utf-8"))
        return h.hexdigest()

    def fetch_schema(self, table: str) -> dict[str, str]:
        t = sanitize_identifier(table, kind="table")
        with self._cursor() as cur:
            cur.execute(
                """
                SELECT COLUMN_NAME, DATA_TYPE
                  FROM information_schema.COLUMNS
                 WHERE TABLE_SCHEMA = %s
                   AND TABLE_NAME   = %s
                """,
                (self._p.database, t),
            )
            return {str(row[0]): str(row[1]).upper() for row in cur.fetchall()}

    def fetch_sample_text(self, table: str, columns: list[str], limit: int = 100) -> list[str]:
        t = sanitize_identifier(table, kind="table")
        if columns == ["*"]:
            cols_sql = "*"
        else:
            cols_safe = [sanitize_identifier(c, kind="column") for c in columns]
            cols_sql = ", ".join(f"`{c}`" for c in cols_safe)
        out: list[str] = []
        n = max(1, min(int(limit), self._ROW_SAMPLE_LIMIT))
        with self._cursor() as cur:
            cur.execute(f"SELECT {cols_sql} FROM `{t}` LIMIT %s", (n,))
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
