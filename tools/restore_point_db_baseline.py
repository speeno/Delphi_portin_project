#!/usr/bin/env python3
"""복원 포인트 DB 기준선 — Id_Logn 행수 + Web_* 사이드테이블 목록 (읽기 전용).

이메일 기준 북이오웍스 계정 전환(ACM/DEC-235)은 ``Id_Logn`` 을 쓰지 않는다(ACM-INV-1).
본 도구는 그 전제를 운영 DB 에서 확인·대조하기 위한 **비밀 0건** 스냅샷을 만든다.

    python3 tools/restore_point_db_baseline.py                       # remote_138 캡처 → stdout
    python3 tools/restore_point_db_baseline.py --out analysis/audit/x.json
    python3 tools/restore_point_db_baseline.py --compare analysis/audit/restore-point-pre-email-account-2026-09-03.json

``--compare`` 는 DB 별 Id_Logn 행수 차이와 신규/삭제된 Web_* 테이블을 출력하고,
차이가 있으면 종료 코드 1 (복원 검증·DoD "Id_Logn diff 0건" 게이트).
캡처 항목: DB 이름 · Id_Logn 행수 · ``Web_`` 접두 테이블명. Gpass/자격증명은 SELECT 하지 않는다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

_SKIP_DBS = {"information_schema", "mysql", "performance_schema", "test"}


async def capture(server_id: str) -> dict:
    from app.core.db import close_all_pools, execute_query  # noqa: PLC0415

    out: dict = {
        "server_id": server_id,
        "captured_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "databases": {},
    }
    try:
        ver = await execute_query(server_id, "SELECT VERSION() AS v", ())
        out["mysql_version"] = str((ver or [{}])[0].get("v", ""))
        dbs = await execute_query(server_id, "SHOW DATABASES", ())
        for row in dbs or []:
            db = str(list(row.values())[0])
            if db in _SKIP_DBS:
                continue
            entry: dict = {}
            try:
                has = await execute_query(server_id, f"SHOW TABLES FROM `{db}` LIKE 'Id_Logn'", ())
                if has:
                    cnt = await execute_query(server_id, f"SELECT COUNT(*) AS n FROM `{db}`.Id_Logn", ())
                    entry["id_logn_rows"] = int((cnt or [{}])[0].get("n", 0))
                web = await execute_query(server_id, f"SHOW TABLES FROM `{db}` LIKE %s", ("Web\\_%",))
                entry["web_tables"] = sorted(str(list(r.values())[0]) for r in web or [] if r)
            except Exception as exc:  # noqa: BLE001 — DB 단위 오류는 기록하고 계속
                entry["error"] = type(exc).__name__
            if "id_logn_rows" in entry or entry.get("web_tables") or "error" in entry:
                out["databases"][db] = entry
    finally:
        await close_all_pools()
    out["summary"] = {
        "dbs_with_id_logn": sum(1 for e in out["databases"].values() if "id_logn_rows" in e),
        "id_logn_rows_total": sum(e.get("id_logn_rows", 0) for e in out["databases"].values()),
        "web_account_tables_present": sorted(
            {t for e in out["databases"].values() for t in e.get("web_tables", []) if t.startswith("Web_Account")}
        ),
    }
    return out


def compare(baseline: dict, current: dict) -> int:
    diffs = 0
    b_dbs, c_dbs = baseline.get("databases", {}), current.get("databases", {})
    for db in sorted(set(b_dbs) | set(c_dbs)):
        b, c = b_dbs.get(db, {}), c_dbs.get(db, {})
        if b.get("id_logn_rows") != c.get("id_logn_rows"):
            diffs += 1
            print(f"[DIFF] {db}: Id_Logn rows {b.get('id_logn_rows')} -> {c.get('id_logn_rows')}")
        added = sorted(set(c.get("web_tables", [])) - set(b.get("web_tables", [])))
        removed = sorted(set(b.get("web_tables", [])) - set(c.get("web_tables", [])))
        if added or removed:
            diffs += 1
            print(f"[DIFF] {db}: Web_* tables +{added} -{removed}")
    print("[OK] 기준선과 동일" if diffs == 0 else f"[FAIL] 차이 {diffs}건")
    return 0 if diffs == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--server", default="remote_138", help="servers.yaml 의 server id (기본 remote_138)")
    ap.add_argument("--out", help="캡처 JSON 저장 경로 (미지정 시 stdout)")
    ap.add_argument("--compare", help="기준선 JSON 과 대조 (차이 있으면 exit 1)")
    args = ap.parse_args()

    current = asyncio.run(capture(args.server))
    if args.compare:
        baseline = json.loads(Path(args.compare).read_text(encoding="utf-8"))
        return compare(baseline, current)
    text = json.dumps(current, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"saved {args.out}: {current['summary']}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
