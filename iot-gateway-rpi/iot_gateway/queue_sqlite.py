from __future__ import annotations

import sqlite3
import time
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS pending_publish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    payload BLOB NOT NULL,
    qos INTEGER NOT NULL DEFAULT 1,
    retain INTEGER NOT NULL DEFAULT 0,
    created_at REAL NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    inflight INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_pending_created ON pending_publish(created_at);
CREATE INDEX IF NOT EXISTS idx_pending_inflight ON pending_publish(inflight, id);
"""


class PublishQueue:
    """SQLite-backed store for MQTT messages when uplink is unavailable."""

    def __init__(self, path: str) -> None:
        self._path = Path(path)
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.executescript(SCHEMA)
        self._conn.commit()
        self._migrate_inflight_column()

    def _migrate_inflight_column(self) -> None:
        cur = self._conn.execute("PRAGMA table_info(pending_publish)")
        cols = {row[1] for row in cur.fetchall()}
        if "inflight" not in cols:
            try:
                self._conn.execute(
                    "ALTER TABLE pending_publish ADD COLUMN inflight INTEGER NOT NULL DEFAULT 0"
                )
                self._conn.commit()
            except sqlite3.OperationalError:
                pass

    def close(self) -> None:
        self._conn.close()

    def enqueue(self, topic: str, payload: bytes, qos: int = 1, retain: bool = False) -> None:
        self._conn.execute(
            "INSERT INTO pending_publish (topic, payload, qos, retain, created_at, inflight) "
            "VALUES (?,?,?,?,?,0)",
            (topic, payload, qos, 1 if retain else 0, time.time()),
        )
        self._conn.commit()

    def claim_batch(self, limit: int = 50) -> list[tuple[int, str, bytes, int, bool]]:
        """Mark rows as inflight=1 and return them for scheduling to uplink."""
        self._conn.execute("BEGIN IMMEDIATE")
        cur = self._conn.execute(
            "SELECT id, topic, payload, qos, retain FROM pending_publish "
            "WHERE inflight = 0 ORDER BY id ASC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        ids = [int(r[0]) for r in rows]
        for row_id in ids:
            self._conn.execute(
                "UPDATE pending_publish SET inflight = 1 WHERE id = ?", (row_id,)
            )
        self._conn.commit()
        return [(int(r[0]), str(r[1]), bytes(r[2]), int(r[3]), bool(r[4])) for r in rows]

    def release_inflight(self, row_id: int) -> None:
        self._conn.execute(
            "UPDATE pending_publish SET inflight = 0, attempts = attempts + 1 WHERE id = ?",
            (row_id,),
        )
        self._conn.commit()

    def delete(self, row_id: int) -> None:
        self._conn.execute("DELETE FROM pending_publish WHERE id = ?", (row_id,))
        self._conn.commit()

    def bump_attempt(self, row_id: int) -> None:
        self._conn.execute(
            "UPDATE pending_publish SET attempts = attempts + 1 WHERE id = ?", (row_id,)
        )
        self._conn.commit()
