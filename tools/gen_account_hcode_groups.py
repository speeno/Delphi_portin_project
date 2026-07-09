#!/usr/bin/env python3
"""계정코드(hcode) 동일 계정 묶음 인벤토리 생성기.

교문사↔경리부(5019)처럼 **같은 (서버, 테넌트DB, Hcode)** 를 공유하는 로그인 계정들을
조직 단위로 묶어 md 문서로 정리한다.

- 입력: 도서물류관리프로그램/backend/data/login_id_index.json (로그인 라우팅 인덱스)
- 보강: 각 테넌트 DB 의 Id_Logn 전체(Hcode/Hname/Gcode/Gname) 라이브 조회(읽기 전용,
  실패 시 해당 라우트는 인덱스 정보만으로 격하) — 비밀번호(Gpass)는 조회하지 않는다.
- 출력: analysis/audit/account-hcode-groups.md

실행 (백엔드 디렉터리 기준):
    cd 도서물류관리프로그램/backend && python3 ../../tools/gen_account_hcode_groups.py
"""
from __future__ import annotations

import asyncio
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, ".")
from app.core.db import execute_query  # noqa: E402
from app.core.tenant_db_context import (  # noqa: E402
    clear_tenant_db_context_for_tests,
    set_tenant_db_context,
)

HUB = Path(__file__).resolve().parents[1]
OUT = HUB / "analysis" / "audit" / "account-hcode-groups.md"


def _s(v) -> str:
    return str(v or "").strip()


async def main() -> None:
    idx = json.load(open("data/login_id_index.json"))["by_login_id"]

    # 인덱스에 등장하는 모든 (서버, DB) 라우트
    routes: set[tuple[str, str]] = set()
    index_logins: dict[tuple[str, str], set[str]] = defaultdict(set)
    for login, cands in idx.items():
        for c in cands:
            key = (_s(c.get("remote_id")), _s(c.get("db_name")))
            routes.add(key)
            index_logins[key].add(login)

    # 라우트별 Id_Logn 전체 로드 (소형 테이블 40~800행) — Gpass 미조회.
    rows_by_route: dict[tuple[str, str], list[dict]] = {}
    failed: list[tuple[tuple[str, str], str]] = []
    for sid, db in sorted(routes):
        clear_tenant_db_context_for_tests()
        set_tenant_db_context(sid, db)
        try:
            rows = await execute_query(
                sid, "SELECT Hcode, Hname, Gcode, Gname FROM Id_Logn", (),
            )
            rows_by_route[(sid, db)] = rows
        except Exception as exc:  # noqa: BLE001
            failed.append(((sid, db), f"{type(exc).__name__}: {str(exc)[:60]}"))
            rows_by_route[(sid, db)] = []

    # (라우트, hcode) 그룹핑
    lines: list[str] = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines += [
        "# 계정코드(Hcode) 동일 계정 묶음 인벤토리",
        "",
        f"- 생성: {now} — `tools/gen_account_hcode_groups.py` (재생성 가능, 수기 편집 금지)",
        "- 기준: 같은 **(서버, 테넌트 DB, Hcode)** 를 공유하는 로그인 계정 = 한 조직의 계정 묶음",
        "  (예: 교문사 5019 — 대표 계정과 경리부 등 부서 계정이 동일 코드).",
        "- 원천: `login_id_index.json` + 각 테넌트 DB `Id_Logn`(Hcode/Hname/Gcode/Gname,",
        "  비밀번호 미조회). `(인덱스밖)` 표기는 Id_Logn 에는 있으나 로그인 인덱스에 아직",
        "  등재되지 않은 계정(해당 ID 로 웹 로그인 이력 없음).",
        "",
    ]

    grand_groups = grand_multi = grand_accounts = 0
    for (sid, db) in sorted(rows_by_route.keys()):
        rows = rows_by_route[(sid, db)]
        if not rows and (sid, db) in dict(failed):
            lines += [f"## {sid} / {db}", "", f"> 조회 실패: {dict(failed)[(sid, db)]}", ""]
            continue
        by_hcode: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            hc = _s(r.get("Hcode"))
            if hc:
                by_hcode[hc].append(r)
        multi = {h: m for h, m in by_hcode.items() if len(m) >= 2}
        singles = len(by_hcode) - len(multi)
        grand_groups += len(by_hcode)
        grand_multi += len(multi)
        grand_accounts += len(rows)

        lines += [
            f"## {sid} / {db}",
            "",
            f"- 계정 {len(rows)}개 / 코드 {len(by_hcode)}개 — **복수 계정 코드 {len(multi)}개**, 단일 계정 코드 {singles}개",
            "",
        ]
        if not multi:
            continue
        lines += ["| Hcode | 조직명(Hname) | 계정 수 | 로그인 ID (사용자명) |", "|---|---|---|---|"]
        indexed = index_logins.get((sid, db), set())
        for hc in sorted(multi, key=lambda h: (-len(multi[h]), h)):
            members = multi[hc]
            hname = next((_s(m.get("Hname")) for m in members if _s(m.get("Hname"))), "")
            cells = []
            for m in sorted(members, key=lambda x: _s(x.get("Gcode"))):
                gc, gn = _s(m.get("Gcode")), _s(m.get("Gname"))
                tag = "" if gc in indexed else " (인덱스밖)"
                cells.append(f"`{gc}`{f' ({gn})' if gn and gn != gc else ''}{tag}")
            lines.append(f"| `{hc}` | {hname} | {len(members)} | {', '.join(cells)} |")
        lines.append("")

    lines += [
        "---",
        "",
        f"**전체 요약** — 계정 {grand_accounts}개 / 코드 {grand_groups}개 / "
        f"복수-계정 코드 {grand_multi}개 / 조회 실패 라우트 {len(failed)}개",
        "",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"written: {OUT}")
    print(f"계정 {grand_accounts} / 코드 {grand_groups} / 복수-계정 코드 {grand_multi} / 실패 {len(failed)}")


if __name__ == "__main__":
    asyncio.run(main())
