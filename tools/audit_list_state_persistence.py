"""list 화면 상태 보존 회귀 가드 (DEC-055).

`frontend/src/app/(app)/**/page.tsx` 중 `DataGridPager` 를 import 하는
모든 list 화면이 `useListSession` 도 함께 import 하는지 정적으로 검증한다.

Detail 진입 후 복귀 시 검색조건/페이지 offset 휘발 회귀를 차단하기 위해
모든 list 페이지가 단일 hook(`useListSession`) 으로 sessionStorage 영속화
되어야 한다는 DEC-055 원칙을 정적 grep + allowlist 패턴으로 강제.

분류:
  - covered     : DataGridPager + useListSession 둘 다 import (정상)
  - violation   : DataGridPager 만 import, allowlist 외 (회귀)
  - allowed     : DataGridPager 만 import, allowlist 매칭 (의도적 deferral)
  - skipped     : DataGridPager 미사용 (list 가 아닌 페이지 — 본 audit 대상 외)

사용:
  python3 tools/audit_list_state_persistence.py            # report 만 갱신
  python3 tools/audit_list_state_persistence.py --check    # 신규 위반 시 non-zero exit
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = (
    REPO_ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app" / "(app)"
)
ALLOWLIST_PATH = REPO_ROOT / "legacy-analysis" / "list-state-allowlist.yaml"
REPORT_PATH = REPO_ROOT / "analysis" / "audit" / "list-state-coverage-report.json"


# ───────────────────────── data shapes ─────────────────────────


@dataclass
class PageEntry:
    """list page.tsx 1건 — repo 상대 경로 + 라우트 키."""

    relpath: str  # repo root 기준 상대 경로 (POSIX, audit 출력 안정성)
    route_key: str  # frontend route 기준 ("master.customer", "outbound.orders" …)
    has_pager: bool
    has_session_hook: bool


@dataclass
class Allowlist:
    # route_key → {reason, until}
    deferred: dict[str, dict[str, Any]] = field(default_factory=dict)


# ───────────────────────── loaders ─────────────────────────


_PAGER_RE = re.compile(r"DataGridPager")
# 신규 화면이 use-list-session 의 다른 export 를 쓸 가능성도 고려해 모듈 경로로 매칭.
_HOOK_RE = re.compile(r"@/lib/use-list-session")


def _route_key_from_path(rel: Path) -> str:
    """`frontend/src/app/(app)/master/customer/page.tsx` → `master.customer`.

    동적 세그먼트(`[id]`)·grouping(`(app)`) 은 제거. page.tsx 만 dot-join.
    """
    parts: list[str] = []
    # rel 은 APP_DIR 기준 — `master/customer/page.tsx`
    for seg in rel.parts[:-1]:  # page.tsx 제외
        if seg.startswith("(") and seg.endswith(")"):
            continue  # route group
        if seg.startswith("[") and seg.endswith("]"):
            continue  # dynamic segment (detail page — 본 audit 대상 외이지만 안전망)
        parts.append(seg)
    return ".".join(parts) if parts else "root"


def discover_pages(app_dir: Path = APP_DIR) -> list[PageEntry]:
    entries: list[PageEntry] = []
    for path in sorted(app_dir.rglob("page.tsx")):
        text = path.read_text(encoding="utf-8")
        has_pager = bool(_PAGER_RE.search(text))
        has_hook = bool(_HOOK_RE.search(text))
        rel_app = path.relative_to(app_dir)
        rel_repo = path.relative_to(REPO_ROOT).as_posix()
        entries.append(
            PageEntry(
                relpath=rel_repo,
                route_key=_route_key_from_path(rel_app),
                has_pager=has_pager,
                has_session_hook=has_hook,
            )
        )
    return entries


def load_allowlist(allowlist_path: Path = ALLOWLIST_PATH) -> Allowlist:
    if not allowlist_path.exists():
        return Allowlist()
    raw = yaml.safe_load(allowlist_path.read_text(encoding="utf-8")) or {}
    deferred: dict[str, dict[str, Any]] = {}
    for item in raw.get("deferred_pages", []) or []:
        if isinstance(item, dict) and item.get("route_key"):
            deferred[item["route_key"]] = {
                "reason": item.get("reason", ""),
                "until": item.get("until", ""),
            }
    return Allowlist(deferred=deferred)


# ───────────────────────── core compare ─────────────────────────


def run_audit(
    app_dir: Path = APP_DIR,
    allowlist_path: Path = ALLOWLIST_PATH,
) -> dict[str, Any]:
    pages = discover_pages(app_dir)
    allowlist = load_allowlist(allowlist_path)

    covered: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    allowed: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for p in pages:
        base = {"route_key": p.route_key, "file": p.relpath}
        if not p.has_pager:
            skipped.append(base)
            continue
        if p.has_session_hook:
            covered.append(base)
            continue
        # pager 있음 + hook 없음 → 위반 또는 의도된 deferral
        if p.route_key in allowlist.deferred:
            a = allowlist.deferred[p.route_key]
            allowed.append({**base, "reason": a["reason"], "until": a["until"]})
        else:
            violations.append(base)

    # allowlist 등록됐지만 실제 페이지가 없거나 이미 hook 도입된 stale 정리 힌트
    page_keys_with_pager_no_hook = {
        p.route_key for p in pages if p.has_pager and not p.has_session_hook
    }
    stale_allowlist = sorted(
        k for k in allowlist.deferred if k not in page_keys_with_pager_no_hook
    )

    summary = {
        "total_pages": len(pages),
        "covered": len(covered),
        "violations": len(violations),
        "allowed": len(allowed),
        "skipped": len(skipped),
    }
    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "summary": summary,
        "covered": sorted(covered, key=lambda x: x["route_key"]),
        "violations": sorted(violations, key=lambda x: x["route_key"]),
        "allowed": sorted(allowed, key=lambda x: x["route_key"]),
        "skipped": sorted(skipped, key=lambda x: x["route_key"]),
        "stale_allowlist": stale_allowlist,
    }


def write_report(report: dict[str, Any], path: Path = REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ───────────────────────── helpers (test 노출) ─────────────────────────


def find_covered(report: dict[str, Any], route_key: str) -> dict[str, Any] | None:
    for row in report.get("covered", []):
        if row.get("route_key") == route_key:
            return row
    return None


# ───────────────────────── CLI ─────────────────────────


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="DataGridPager 사용 화면 중 useListSession 미도입 page 가 있으면 non-zero exit.",
    )
    args = parser.parse_args()

    report = run_audit()
    write_report(report)

    s = report["summary"]
    print(
        f"[list-state-coverage] pages={s['total_pages']} covered={s['covered']} "
        f"violations={s['violations']} allowed={s['allowed']} skipped={s['skipped']}"
    )
    if args.check and report["violations"]:
        print(
            "✗ useListSession 미도입 list 화면 발견:",
            ", ".join(e["route_key"] for e in report["violations"]),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
