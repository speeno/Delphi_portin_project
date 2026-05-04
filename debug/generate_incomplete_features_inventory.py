#!/usr/bin/env python3
"""
구현되지 못한 기능 인벤토리 산출 — analysis/audit/incomplete-features-inventory.{md,json}

원천:
  - ScreenPlaceholder 사용 Next 라우트 (프론트 app/)
  - dashboard/data/phase2-screen-cards.json — tasks 에 pending|in_progress|blocked
  - form-registry.ts — phase: "preview" 또는 crudParity: "STUB" 근처 id/route
  - form-registry.ts — phase1 이지만 crudParity ∈ {R, RU, STUB} (레거시 대비 부분 동등)
  - docs/crud-backlog.md §2.6 불릿 (참조용)
  - backend app/routers/_stub.py — 고정 메모
  - backend app/routers/*.py — 501 / NOT_IMPLEMENTED / DEC-035 stub grep

사용:
  python3 debug/generate_incomplete_features_inventory.py
  python3 debug/generate_incomplete_features_inventory.py --check  # CI: 산출물이 갱신되지 않았으면 exit 1
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FE_APP = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app"
FORM_REGISTRY = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
PHASE2_CARDS = ROOT / "dashboard" / "data" / "phase2-screen-cards.json"
CRUD_BACKLOG = ROOT / "docs" / "crud-backlog.md"
BACKEND_ROUTERS = ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers"
OUT_MD = ROOT / "analysis" / "audit" / "incomplete-features-inventory.md"
OUT_JSON = ROOT / "analysis" / "audit" / "incomplete-features-inventory.json"

# 백엔드 stub grep 패턴 — 의도적 미구현 응답을 내는 코드만 포착.
_STUB_PATTERNS = (
    "HTTP_503_SERVICE_UNAVAILABLE",  # _stub.py
    "HTTP_501_NOT_IMPLEMENTED",
    "issue_external_stub",            # DEC-035 정산 외부 발행
    "NOT_IMPLEMENTED",                # detail.code
)


# ─── 1. UI placeholder 라우트 ────────────────────────────────────────────────
def _placeholder_routes() -> list[dict]:
    out: list[dict] = []
    if not FE_APP.is_dir():
        return out
    for p in FE_APP.rglob("page.tsx"):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if "ScreenPlaceholder" not in text:
            continue
        out.append(
            {
                "kind": "ui_placeholder",
                "path": str(p.relative_to(ROOT)),
                "route_hint": _guess_next_route_from_page(p),
            }
        )
    return sorted(out, key=lambda x: x["path"])


def _guess_next_route_from_page(p: Path) -> str:
    """src/app/(app)/billing/statements/page.tsx -> /billing/statements (Next App Router)."""
    try:
        rel = p.relative_to(FE_APP)
    except ValueError:
        return "/"
    parts = list(rel.parts)
    if not parts or parts[-1] != "page.tsx":
        return "/"
    parts = parts[:-1]
    parts = [x for x in parts if not (x.startswith("(") and x.endswith(")"))]
    if not parts:
        return "/"
    return "/" + "/".join(parts)


# ─── 2. T1–T8 파이프라인 갭 ────────────────────────────────────────────────
def _phase2_pipeline_gaps() -> list[dict]:
    raw = json.loads(PHASE2_CARDS.read_text(encoding="utf-8"))
    screens = raw.get("screens") or []
    gap_states = frozenset({"pending", "in_progress", "blocked"})
    out: list[dict] = []
    for s in screens:
        tasks = s.get("tasks") or {}
        bad = {k: v for k, v in tasks.items() if v in gap_states}
        if not bad:
            continue
        out.append(
            {
                "kind": "t_pipeline_gap",
                "id": s.get("id"),
                "caption": s.get("caption"),
                "route": s.get("route"),
                "tasks_non_done": bad,
                "blockers": (s.get("scenario") or {}).get("blockers"),
            }
        )
    return out


# ─── 3. form-registry 객체 단위 파싱 ──────────────────────────────────────
def _form_registry_object_window(lines: list[str], id_line_idx: int) -> tuple[int, int]:
    """`id:` 가 속한 `{ ... },` 객체 구간을 괄호 깊이로 잘라낸다."""
    start = id_line_idx
    for back in range(id_line_idx, max(-1, id_line_idx - 8), -1):
        if lines[back].strip() == "{":
            start = back
            break
    depth = 0
    end = id_line_idx
    for k in range(start, len(lines)):
        depth += lines[k].count("{") - lines[k].count("}")
        if depth == 0:
            end = k
            break
    return start, end


def _parse_string_field(window: str, field: str) -> str:
    """blocks 안에서 `field: "..."` 또는 다음 줄에 인용된 문자열을 추출."""
    pattern = rf"^\s*{re.escape(field)}:\s*\"([^\"]*)\""
    m = re.search(pattern, window, re.MULTILINE)
    if m:
        return m.group(1)
    pattern_multi = rf"^\s*{re.escape(field)}:\s*\n\s*\"([^\"]*)\""
    m = re.search(pattern_multi, window, re.MULTILINE)
    return m.group(1) if m else ""


def _iter_form_meta_blocks() -> list[dict]:
    """FormMeta 객체별로 (id/route/phase/crudParity/caption/crudNotes/line)."""
    if not FORM_REGISTRY.is_file():
        return []
    lines = FORM_REGISTRY.read_text(encoding="utf-8").splitlines()
    out: list[dict] = []
    for i, line in enumerate(lines):
        m = re.match(r'\s*id:\s*"([^"]+)"', line)
        if not m:
            continue
        fid = m.group(1)
        s, e = _form_registry_object_window(lines, i)
        window = "\n".join(lines[s : e + 1])
        out.append(
            {
                "id": fid,
                "caption": _parse_string_field(window, "caption"),
                "route": _parse_string_field(window, "route"),
                "phase": _parse_string_field(window, "phase"),
                "crudParity": _parse_string_field(window, "crudParity"),
                "crudNotes": _parse_string_field(window, "crudNotes"),
                "registry_line": i + 1,
            }
        )
    return out


def _form_registry_preview_stub(blocks: list[dict]) -> list[dict]:
    out: list[dict] = []
    for b in blocks:
        reasons: list[str] = []
        if b["phase"] == "preview":
            reasons.append("preview")
        if b["crudParity"] == "STUB":
            reasons.append("STUB")
        if not reasons:
            continue
        out.append(
            {
                "kind": "form_registry_placeholder",
                "id": b["id"],
                "caption": b["caption"],
                "route": b["route"],
                "reasons": sorted(set(reasons)),
                "crudNotes": b["crudNotes"],
                "registry_line": b["registry_line"],
            }
        )
    return sorted(out, key=lambda x: (x["id"], x["route"]))


def _form_registry_phase1_partial(blocks: list[dict]) -> list[dict]:
    """phase1 인데 crudParity ∈ {R, RU, STUB} — 레거시 대비 부분 동등."""
    out: list[dict] = []
    for b in blocks:
        if b["phase"] != "phase1":
            continue
        if b["crudParity"] not in {"R", "RU", "STUB"}:
            continue
        out.append(
            {
                "kind": "crud_phase1_partial",
                "id": b["id"],
                "caption": b["caption"],
                "route": b["route"],
                "crudParity": b["crudParity"],
                "crudNotes": b["crudNotes"],
                "registry_line": b["registry_line"],
            }
        )
    return sorted(out, key=lambda x: (x["crudParity"], x["id"]))


# ─── 4. crud-backlog §2.6 불릿 ────────────────────────────────────────────
def _crud_backlog_stub_bullets() -> list[str]:
    if not CRUD_BACKLOG.is_file():
        return []
    text = CRUD_BACKLOG.read_text(encoding="utf-8")
    m = re.search(
        r"### 2\.6 placeholder / stub 일람\s*\n\n(.*?)\n\n---",
        text,
        re.DOTALL,
    )
    if not m:
        return []
    return [
        line.strip()[2:].strip()
        for line in m.group(1).splitlines()
        if line.strip().startswith("- ")
    ]


# ─── 5. 백엔드 stub ──────────────────────────────────────────────────────
def _backend_stub_grep() -> list[dict]:
    """app/routers/*.py 에서 의도적 미구현 응답 라인."""
    out: list[dict] = []
    if not BACKEND_ROUTERS.is_dir():
        return out
    for py in sorted(BACKEND_ROUTERS.glob("*.py")):
        try:
            for ln, line in enumerate(py.read_text(encoding="utf-8").splitlines(), start=1):
                if any(pat in line for pat in _STUB_PATTERNS):
                    out.append(
                        {
                            "file": str(py.relative_to(ROOT)),
                            "line": ln,
                            "snippet": line.strip(),
                        }
                    )
        except OSError:
            continue
    return out


# ─── 6. 산출 ─────────────────────────────────────────────────────────────
def _build_payload() -> dict[str, Any]:
    blocks = _iter_form_meta_blocks()
    criteria = (
        "본 인벤토리는 계획서 「구현되지 못한 기능 목록」에 따라 "
        "**원천별 합집합** 을 기록한다. "
        "단일 정의가 아니라 (A) UI placeholder (B) T-파이프라인 비완료 "
        "(C) form-registry preview/STUB (D) phase1 이지만 R/RU/STUB 인 부분 동등 "
        "(E) 백엔드 stub grep (F) crud-backlog §2.6 참조 를 모두 포함한다."
    )
    return {
        "criteria": criteria,
        "sources": {
            "ui_placeholder_pages": _placeholder_routes(),
            "phase2_screen_cards_tasks": _phase2_pipeline_gaps(),
            "form_registry_preview_or_stub": _form_registry_preview_stub(blocks),
            "form_registry_phase1_partial": _form_registry_phase1_partial(blocks),
            "backend_stub_grep": _backend_stub_grep(),
            "crud_backlog_section_2_6": _crud_backlog_stub_bullets(),
        },
    }


def _render_md(payload: dict, ts: str) -> str:
    src = payload["sources"]
    lines: list[str] = [
        "# 구현되지 못한 기능 인벤토리 (저장소 자동 산출)",
        "",
        f"생성: `{ts}` (`debug/generate_incomplete_features_inventory.py`)",
        "",
        "## 판정 기준 (합집합)",
        "",
        payload["criteria"],
        "",
        "## 1. UI — `ScreenPlaceholder` 가 붙은 라우트",
        "",
    ]
    for item in src["ui_placeholder_pages"]:
        lines.append(f"- `{item['path']}` → 라우트 추정 `{item['route_hint']}`")
    if not src["ui_placeholder_pages"]:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## 2. T1–T8 — `phase2-screen-cards.json` 에서 아직 done 아닌 task",
            "",
            "> **드리프트 주의:** 카드의 레거시 ID·캡션과 해당 `route` 의 `page.tsx` 실구현 범위가 다를 수 있다. 판단은 API·화면 코드 우선.",
            "",
        ]
    )
    for item in src["phase2_screen_cards_tasks"]:
        lines.append(
            f"- **{item.get('id')}** ({item.get('caption')}) `{item.get('route')}` — {item.get('tasks_non_done')}"
        )
        if item.get("blockers"):
            lines.append(f"  - blockers: {item['blockers']}")
    if not src["phase2_screen_cards_tasks"]:
        lines.append("- (없음)")

    lines.extend(["", "## 3. `form-registry` — preview 또는 STUB", ""])
    for item in src["form_registry_preview_or_stub"]:
        cap = item.get("caption") or "?"
        notes = item.get("crudNotes") or ""
        lines.append(
            f"- `{item['id']}` ({cap}) route `{item.get('route')}` — {item['reasons']} (line {item['registry_line']})"
        )
        if notes:
            lines.append(f"  - notes: {notes}")
    if not src["form_registry_preview_or_stub"]:
        lines.append("- (없음)")

    lines.extend(
        [
            "",
            "## 4. `form-registry` — phase1 이지만 부분 동등 (R / RU / STUB)",
            "",
            "> 레거시 화면은 풀 CRUD 였지만 모던 화면이 조회·부분쓰기에 머문 항목.",
            "",
        ]
    )
    by_parity: dict[str, list[dict]] = {}
    for item in src["form_registry_phase1_partial"]:
        by_parity.setdefault(item["crudParity"], []).append(item)
    for parity in sorted(by_parity):
        lines.append(f"### {parity} ({len(by_parity[parity])}건)")
        for item in by_parity[parity]:
            cap = item.get("caption") or "?"
            notes = item.get("crudNotes") or ""
            lines.append(f"- `{item['id']}` ({cap}) `{item.get('route')}`")
            if notes:
                lines.append(f"  - {notes}")
        lines.append("")
    if not src["form_registry_phase1_partial"]:
        lines.append("- (없음)")

    lines.extend(["", "## 5. 백엔드 stub grep (`app/routers/*.py`)", ""])
    for item in src["backend_stub_grep"]:
        lines.append(f"- `{item['file']}:{item['line']}` — `{item['snippet']}`")
    if not src["backend_stub_grep"]:
        lines.append("- (없음 — 모든 라우터가 정상 응답)")

    lines.extend(["", "## 6. `docs/crud-backlog.md` §2.6 참조 (문서 불릿)", ""])
    for b in src["crud_backlog_section_2_6"]:
        lines.append(f"- {b}")
    if not src["crud_backlog_section_2_6"]:
        lines.append("- (섹션 파싱 실패 시 문서를 직접 확인)")

    lines.extend(
        [
            "",
            "## 갱신·CI",
            "",
            "```bash",
            "python3 debug/generate_incomplete_features_inventory.py            # 갱신",
            "python3 debug/generate_incomplete_features_inventory.py --check    # CI: 미갱신이면 exit 1",
            "```",
            "",
            "산출: `analysis/audit/incomplete-features-inventory.md` · `.json`",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def _read_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="incomplete features inventory generator")
    parser.add_argument(
        "--check",
        action="store_true",
        help="비교만: 디스크 산출물의 sources 가 현재 저장소 상태와 다르면 exit 1",
    )
    args = parser.parse_args(argv)

    payload = _build_payload()
    ts = datetime.now(timezone.utc).isoformat()

    if args.check:
        existing = _read_json(OUT_JSON)
        if existing.get("sources") != payload["sources"]:
            print("FAIL: incomplete-features-inventory.json 이 최신 저장소와 다릅니다.", file=sys.stderr)
            print("  → python3 debug/generate_incomplete_features_inventory.py 로 재생성 후 커밋하세요.", file=sys.stderr)
            return 1
        print("OK: incomplete-features-inventory.json 최신 상태")
        return 0

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    out = {"generatedAt": ts, **payload}
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(_render_md(payload, ts), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
