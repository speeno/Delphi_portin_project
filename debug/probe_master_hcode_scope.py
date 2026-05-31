#!/usr/bin/env python3
"""마스터 Hcode 스코프 라이브 도출 (DSN-DEC-12 overlay 데이터 + 레거시 SQL 정합).

용도 (두 가지, 계정 무관)
-------------------------
1. **overlay hcode_in 도출** — 공유 좌표(예: remote_153/chul_09_db)에서 G1_Ggeo /
   G4_Book 의 distinct Hcode 히스토그램을 뽑아, 특정 창고(warehouse) 테넌트가
   소관하는 Hcode 집합을 운영자가 확정 → tenants_directory overlay 의 ``hcode_in`` 에
   기록할 수 있게 한다. (apply_hcode_isolation_overlay.py 입력 보조)
2. **레거시 SQL 스코프 정합** — ``--hcode`` 를 주면 G4_Book/G1_Ggeo 를 Hcode 필터
   유/무로 COUNT 해, 레거시 Subu14 가 Hcode WHERE 없이 전건을 보여주는지(전체) vs
   웹이 scope_hcode 로 좁히는지(부분) 의 차이를 수치로 드러낸다.

MySQL 3.23 호환 (multi-db-compat 룰)
------------------------------------
- 파생 테이블/CAST/CASE 미사용. ``SELECT Hcode, COUNT(*) ... GROUP BY Hcode`` 만 사용.
- 앱과 동일한 ``app.core.db.execute_query`` 경로로 실행(서버별 풀·3.23 어댑터 재사용).

라이브 DB 필요 — CI 자동 실행 X. 운영자가 read-only 자격 환경에서 수동 실행.

사용
----
    PYTHONPATH=도서물류관리프로그램/backend \
        python3 debug/probe_master_hcode_scope.py --server remote_153 --family chul_09 \
            --hcode 5056 --out analysis/audit/master-hcode-scope-remote153-chul09.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

# 마스터 테이블 → Hcode 컬럼 (권위 사전 기준).
_TABLES = {
    "G1_Ggeo": "Hcode",
    "G4_Book": "Hcode",
}


async def _hcode_histogram(server_id: str, table: str, hcode_col: str) -> list[dict[str, Any]]:
    from app.core.db import execute_query

    sql = f"SELECT {hcode_col} AS hcode, COUNT(*) AS n FROM {table} GROUP BY {hcode_col} ORDER BY n DESC"
    rows = await execute_query(server_id, sql, [])
    return [{"hcode": _s(r.get("hcode")), "n": int(r.get("n") or 0)} for r in rows]


async def _count(server_id: str, table: str, where_sql: str, params: list[Any]) -> int:
    from app.core.db import execute_query

    rows = await execute_query(server_id, f"SELECT COUNT(*) AS n FROM {table} {where_sql}", params)
    return int((rows[0] or {}).get("n") or 0) if rows else 0


def _s(v: Any) -> str:
    return "" if v is None else str(v).strip()


def _norm_name(v: Any) -> str:
    """이름 비교용 정규화 — strip + 내부 공백 1칸 축약 (euckr/공백 변이 흡수)."""
    s = _s(v)
    return " ".join(s.split())


# 엑셀 baseline → 라이브 테이블 매핑 (gcode/이름 컬럼).
_XREF = {
    "books": {"table": "G4_Book", "hcode_col": "Hcode", "gcode_col": "Gcode", "name_col": "Gname"},
    "customers": {"table": "G1_Ggeo", "hcode_col": "Hcode", "gcode_col": "Gcode", "name_col": "Gname"},
}


async def _baseline_xref_one(server_id: str, baseline_path: Path, spec: dict[str, str]) -> dict[str, Any]:
    """엑셀 baseline gcode 를 라이브 테이블과 교차조회해 소관 Hcode 를 역산.

    복합 PK(Gcode+Hcode)로 한 gcode 가 여러 Hcode 에 걸칠 수 있으므로,
    **이름(Gname) 일치**로 교문사 소유 행을 특정한다 (gcode 단독은 모호).
    """
    from app.core.sql_mysql3 import in_clause_lookup

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    name_by_gcode: dict[str, str] = baseline.get("by_gcode_name", {})
    gcodes = list(name_by_gcode.keys())

    table, hcol, gcol, ncol = spec["table"], spec["hcode_col"], spec["gcode_col"], spec["name_col"]
    rows = await in_clause_lookup(
        server_id,
        sql_template=f"SELECT {gcol} AS gcode, {hcol} AS hcode, {ncol} AS gname "
                     f"FROM {table} WHERE {gcol} IN ({{placeholders}})",
        keys=gcodes,
        chunk_size=400,
    )
    # gcode -> [(hcode, normalized_name)]
    by_gcode: dict[str, list[tuple[str, str]]] = {}
    for r in rows:
        gc = _s(r.get("gcode"))
        by_gcode.setdefault(gc, []).append((_s(r.get("hcode")), _norm_name(r.get("gname"))))

    name_match_tally: dict[str, int] = {}
    any_match_tally: dict[str, int] = {}
    matched_by_name = 0
    matched_by_gcode = 0
    unmatched: list[str] = []
    for gc, excel_name in name_by_gcode.items():
        cands = by_gcode.get(gc) or []
        if not cands:
            unmatched.append(gc)
            continue
        matched_by_gcode += 1
        for hc, _n in cands:
            any_match_tally[hc] = any_match_tally.get(hc, 0) + 1
        en = _norm_name(excel_name)
        name_hits = [hc for (hc, nm) in cands if nm == en]
        if name_hits:
            matched_by_name += 1
            # 동일 이름이 여러 Hcode 면 첫 매치만(보수). 일반적으로 1건.
            name_match_tally[name_hits[0]] = name_match_tally.get(name_hits[0], 0) + 1

    def _sorted(d: dict[str, int]) -> list[dict[str, Any]]:
        return [{"hcode": k, "n": v} for k, v in sorted(d.items(), key=lambda kv: kv[1], reverse=True)]

    return {
        "table": table,
        "excel_count": len(gcodes),
        "matched_by_gcode": matched_by_gcode,
        "matched_by_name": matched_by_name,
        "unmatched_gcode_count": len(unmatched),
        "unmatched_sample": unmatched[:15],
        # 이름 일치 기준 Hcode 분포(가장 결정적) — 합이 matched_by_name.
        "name_match_hcode_tally": _sorted(name_match_tally),
        # gcode 일치(이름 무관) Hcode 분포 — 복합 PK 중복 진단용.
        "any_match_hcode_tally": _sorted(any_match_tally),
        # 소관 Hcode 집합 후보 = 이름 일치 tally 의 키.
        "derived_hcode_in": sorted(name_match_tally.keys()),
    }


async def _run(args) -> dict[str, Any]:
    out: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "server_id": args.server,
        "account_family": args.family,
        "hcode_filter": args.hcode,
        "tables": {},
    }
    for table, hcol in _TABLES.items():
        info: dict[str, Any] = {}
        hist = await _hcode_histogram(args.server, table, hcol)
        info["distinct_hcode_count"] = len(hist)
        info["total_rows"] = sum(h["n"] for h in hist)
        info["top_hcodes"] = hist[:30]
        if args.hcode:
            scoped = await _count(args.server, table, f"WHERE {hcol}=%s", [args.hcode])
            unscoped = info["total_rows"]
            info["scoped_count"] = scoped
            info["unscoped_count"] = unscoped
            info["scope_ratio"] = round(scoped / unscoped, 4) if unscoped else None
            info["legacy_scope_hint"] = (
                "filtered_subset" if 0 < scoped < unscoped else
                "all_rows_one_hcode" if scoped == unscoped and unscoped > 0 else
                "empty"
            )
        out["tables"][table] = info

    if args.baseline_xref:
        bdir = Path(args.baseline_dir)
        xref: dict[str, Any] = {"slug": args.baseline_xref}
        for kind, spec in _XREF.items():
            bpath = bdir / f"{args.baseline_xref}_{kind}.json"
            if bpath.exists():
                xref[kind] = await _baseline_xref_one(args.server, bpath, spec)
            else:
                xref[kind] = {"skipped": True, "reason": f"baseline not found: {bpath.name}"}
        out["baseline_xref"] = xref
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    p.add_argument("--server", required=True, help="server_id (예: remote_153)")
    p.add_argument("--family", default="", help="account_family (기록용)")
    p.add_argument("--hcode", default="", help="필터 검증할 Hcode (예: 5056)")
    p.add_argument("--baseline-xref", default="", help="엑셀 baseline slug (예: gyomunsa) — gcode→Hcode 역산")
    p.add_argument("--baseline-dir", default=str(ROOT / "debug" / "baselines"),
                   help="baseline json 디렉터리 (기본 debug/baselines)")
    p.add_argument("--out", default="/tmp/master_hcode_scope.json")
    args = p.parse_args(argv)

    async def _run_and_cleanup(a):
        try:
            return await _run(a)
        finally:
            try:
                from app.core.db import close_all_pools
                await close_all_pools()
            except Exception:  # noqa: BLE001
                pass

    try:
        report = asyncio.run(_run_and_cleanup(args))
    except Exception as e:  # noqa: BLE001
        print(f"[ERR] live query failed: {type(e).__name__}: {e}", file=sys.stderr)
        print("  (라이브 DB 접근/자격증명이 필요합니다 — read-only 환경에서 실행)", file=sys.stderr)
        return 2

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {args.out}")
    for table, info in report["tables"].items():
        line = f"  {table}: distinct_hcode={info['distinct_hcode_count']} total_rows={info['total_rows']}"
        if args.hcode:
            line += f" scoped({args.hcode})={info.get('scoped_count')} hint={info.get('legacy_scope_hint')}"
        print(line)
    if report.get("baseline_xref"):
        xr = report["baseline_xref"]
        print(f"  baseline_xref[{xr.get('slug')}]:")
        for kind in ("books", "customers"):
            x = xr.get(kind) or {}
            if x.get("skipped"):
                print(f"    {kind}: skipped ({x.get('reason')})")
                continue
            tally = ", ".join(f"{t['hcode']}:{t['n']}" for t in x.get("name_match_hcode_tally", [])[:6])
            print(f"    {kind}[{x.get('table')}]: excel={x.get('excel_count')} "
                  f"name_matched={x.get('matched_by_name')} unmatched={x.get('unmatched_gcode_count')} "
                  f"derived_hcode_in={x.get('derived_hcode_in')}")
            print(f"      name_match_hcode_tally: {tally}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
