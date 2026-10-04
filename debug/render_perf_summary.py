#!/usr/bin/env python3
"""운영(Render) 로그의 `perf` 줄을 모아 느린 화면 순위를 낸다 (DEC-377).

백엔드가 요청마다 남기는 한 줄:
    perf GET /api/v1/reports/book-sales 200 1234ms db=12/980ms [SLOW]

사용:
    python3 debug/render_perf_summary.py --start 2026-10-05T00:00:00Z --end 2026-10-05T09:00:00Z
    python3 debug/render_perf_summary.py --hours 3            # 최근 3시간
    python3 debug/render_perf_summary.py --hours 9 --top 30 --min-count 3

- API 키는 파일에서 읽는다(기본 `keyrender`, `RENDER_API_KEY_FILE` 로 변경). **키를 출력하지 않는다.**
- 로그 API 는 요청이 잦으면 429 — 10분 창으로 나눠 받고 요청 사이를 띄운다.
- 받은 로그는 저장하지 않는다(고객 데이터가 섞여 있다) — 집계만 출력.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

OWNER = os.environ.get("RENDER_OWNER_ID", "tea-d6slnrs50q8c73fltbo0")
SERVICE = os.environ.get("RENDER_SERVICE_ID", "srv-d84vjdt8nd3s73dbhq20")
KEY_FILE = Path(os.environ.get("RENDER_API_KEY_FILE", Path(__file__).resolve().parents[1] / "keyrender"))
PERF_RE = re.compile(r"perf (\w+) (\S+) (\d+) (\d+)ms db=(\d+)/(\d+)ms")
# 전표 키 · 코드처럼 요청마다 달라지는 경로 조각을 하나로 묶는다.
_VARIABLE_SEGMENT = re.compile(r"/(?:[^/]*[|%][^/]*|\d[\w.\-]*)(?=/|$)")


def _ctx() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore[import-not-found]

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


def _fetch(key: str, start: str, end: str, ctx: ssl.SSLContext) -> list[dict]:
    out: list[dict] = []
    s, e = start, end
    for _page in range(80):
        q = urllib.parse.urlencode([
            ("ownerId", OWNER), ("resource", SERVICE), ("startTime", s), ("endTime", e),
            ("direction", "forward"), ("limit", "100"),
        ])
        req = urllib.request.Request(
            f"https://api.render.com/v1/logs?{q}",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        )
        data = None
        for attempt in range(8):
            try:
                time.sleep(2.2)
                with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
                    data = json.load(r)
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 429:
                    time.sleep(20 + attempt * 10)
                    continue
                print(f"HTTP {exc.code}", file=sys.stderr)
                break
            except Exception as exc:  # noqa: BLE001
                print(f"ERR {type(exc).__name__}", file=sys.stderr)
                time.sleep(5)
        if data is None:
            break
        logs = data.get("logs") or []
        out.extend(logs)
        if not data.get("hasMore") or not logs:
            break
        s, e = data.get("nextStartTime") or s, data.get("nextEndTime") or e
    return out


def _route(path: str) -> str:
    return _VARIABLE_SEGMENT.sub("/{…}", urllib.parse.unquote(path))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--hours", type=float, default=3.0)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--min-count", type=int, default=1)
    args = ap.parse_args()
    if not KEY_FILE.is_file():
        print(f"API 키 파일이 없습니다: {KEY_FILE}", file=sys.stderr)
        return 2
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    end = datetime.fromisoformat(args.end.replace("Z", "+00:00")) if args.end else datetime.now(timezone.utc)
    start = datetime.fromisoformat(args.start.replace("Z", "+00:00")) if args.start else end - timedelta(hours=args.hours)
    ctx = _ctx()
    rows: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
    t = start
    while t < end:
        t2 = min(t + timedelta(minutes=10), end)
        for log in _fetch(key, t.strftime("%Y-%m-%dT%H:%M:%SZ"), t2.strftime("%Y-%m-%dT%H:%M:%SZ"), ctx):
            m = PERF_RE.search(log.get("message") or "")
            if m:
                rows[f"{m.group(1)} {_route(m.group(2))}"].append((int(m.group(4)), int(m.group(5)), int(m.group(6))))
        t = t2
    if not rows:
        print("perf 줄이 없습니다(기간 · 배포 버전 확인).")
        return 0
    table = []
    for route, vals in rows.items():
        if len(vals) < args.min_count:
            continue
        durs = sorted(v[0] for v in vals)
        p95 = durs[min(len(durs) - 1, int(len(durs) * 0.95))]
        table.append((sum(durs), route, len(vals), int(statistics.median(durs)), p95, max(durs),
                      round(statistics.mean(v[1] for v in vals), 1), int(statistics.mean(v[2] for v in vals))))
    table.sort(reverse=True)
    print(f"기간 {start:%m-%d %H:%M}Z ~ {end:%m-%d %H:%M}Z · 경로 {len(table)}개 · 총 시간 큰 순")
    print(f"{'총시간s':>8} {'횟수':>5} {'중간ms':>7} {'p95ms':>7} {'최대ms':>7} {'조회수':>6} {'DBms':>6}  경로")
    for total, route, n, med, p95, mx, qn, dbms in table[: args.top]:
        print(f"{total / 1000:>8.1f} {n:>5} {med:>7} {p95:>7} {mx:>7} {qn:>6} {dbms:>6}  {route}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
