#!/usr/bin/env python3
"""
구현되지 못한 기능 인벤토리 산출 — analysis/audit/incomplete-features-inventory.{md,json}

원천:
  - ScreenPlaceholder 사용 Next 라우트 (프론트 app/)
  - dashboard/data/phase2-screen-cards.json — tasks 에 pending|in_progress|blocked
  - form-registry.ts — phase: "preview" 또는 crudParity: "STUB" 근처 id/route
  - docs/crud-backlog.md §2.6 불릿 (참조용)
  - backend app/routers/_stub.py — 고정 메모

실행: 저장소 루트에서
  python3 debug/generate_incomplete_features_inventory.py
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FE_APP = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "app"  # page.tsx 기준 상대 경로에 (app) 그룹 포함
FORM_REGISTRY = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
PHASE2_CARDS = ROOT / "dashboard" / "data" / "phase2-screen-cards.json"
CRUD_BACKLOG = ROOT / "docs" / "crud-backlog.md"
OUT_MD = ROOT / "analysis" / "audit" / "incomplete-features-inventory.md"
OUT_JSON = ROOT / "analysis" / "audit" / "incomplete-features-inventory.json"


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
    """src/app/(app)/billing/statements/page.tsx -> /billing/statements (Next App Router)"""
    try:
        rel = p.relative_to(FE_APP)
    except ValueError:
        return "/"
    parts = list(rel.parts)
    if not parts or parts[-1] != "page.tsx":
        return "/"
    parts = parts[:-1]
    # (app) 등 라우트 그룹은 URL 에 나오지 않음
    parts = [x for x in parts if not (x.startswith("(") and x.endswith(")"))]
    if not parts:
        return "/"
    return "/" + "/".join(parts)


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


def _form_registry_object_window(lines: list[str], id_line_idx: int) -> tuple[int, int]:
    """`id:` 가 속한 `{ ... },` 객체 구간을 괄호 깊이로 잘라낸다 (다음 FormMeta 로 누수 방지)."""
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


def _form_registry_preview_stub() -> list[dict]:
    """각 FormMeta 객체 블록 안에서만 preview·STUB 탐지."""
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
        reasons: list[str] = []
        if 'phase: "preview"' in window:
            reasons.append("preview")
        if 'crudParity: "STUB"' in window:
            reasons.append("STUB")
        if not reasons:
            continue
        route_m = re.search(r"^\s*route:\s*\"([^\"]+)\"", window, re.MULTILINE)
        route = route_m.group(1) if route_m else ""
        out.append(
            {
                "kind": "form_registry_placeholder",
                "id": fid,
                "route": route,
                "reasons": sorted(set(reasons)),
                "registry_line": i + 1,
            }
        )
    return sorted(out, key=lambda x: (x.get("id") or "", x.get("route") or ""))


def _crud_backlog_stub_bullets() -> list[str]:
    if not CRUD_BACKLOG.is_file():
        return []
    text = CRUD_BACKLOG.read_text(encoding="utf-8")
    # ### 2.6 placeholder / stub 일람 ... 다음 목록까지
    m = re.search(
        r"### 2\.6 placeholder / stub 일람\s*\n\n(.*?)\n\n---",
        text,
        re.DOTALL,
    )
    if not m:
        return []
    chunk = m.group(1)
    bullets = []
    for line in chunk.splitlines():
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets


def _backend_stub_notes() -> dict:
    return {
        "kind": "backend_stub",
        "router_file": "도서물류관리프로그램/backend/app/routers/_stub.py",
        "pattern": "GET /api/v1/_stub/{name} -> 503 NOT_IMPLEMENTED",
        "notes": "정산 세금 외부 발행 등 DEC-035 stub 은 settlement 라우터 주석 참고",
    }


def main() -> None:
    criteria = (
        "본 인벤토리는 계획서 「구현되지 못한 기능 목록」에 따라 "
        "**원천별 합집합** 을 기록한다. "
        "단일 정의가 아니라 (A) UI placeholder (B) T-파이프라인 비완료 "
        "(C) form-registry preview/STUB (D) 백엔드 범용 stub (E) crud-backlog §2.6 참조 "
        "를 모두 포함한다."
    )

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "criteria": criteria,
        "sources": {
            "ui_placeholder_pages": _placeholder_routes(),
            "phase2_screen_cards_tasks": _phase2_pipeline_gaps(),
            "form_registry_preview_or_stub": _form_registry_preview_stub(),
            "backend_generic_stub": _backend_stub_notes(),
            "crud_backlog_section_2_6": _crud_backlog_stub_bullets(),
        },
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# 구현되지 못한 기능 인벤토리 (저장소 자동 산출)",
        "",
        f"생성: `{payload['generatedAt']}` (`debug/generate_incomplete_features_inventory.py`)",
        "",
        "## 판정 기준 (합집합)",
        "",
        criteria,
        "",
        "## 1. UI — `ScreenPlaceholder` 가 붙은 라우트",
        "",
    ]
    for item in payload["sources"]["ui_placeholder_pages"]:
        lines.append(f"- `{item['path']}` → 라우트 추정 `{item['route_hint']}`")
    if not payload["sources"]["ui_placeholder_pages"]:
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
    for item in payload["sources"]["phase2_screen_cards_tasks"]:
        tid = item.get("id")
        cap = item.get("caption")
        r = item.get("route")
        td = item.get("tasks_non_done")
        lines.append(f"- **{tid}** ({cap}) `{r}` — {td}")
        if item.get("blockers"):
            lines.append(f"  - blockers: {item['blockers']}")
    if not payload["sources"]["phase2_screen_cards_tasks"]:
        lines.append("- (없음)")
    lines.extend(["", "## 3. `form-registry` — preview 또는 STUB", ""])
    for item in payload["sources"]["form_registry_preview_or_stub"]:
        lines.append(
            f"- `{item.get('id')}` route `{item.get('route')}` — {item.get('reasons')} (line {item.get('registry_line')})"
        )
    if not payload["sources"]["form_registry_preview_or_stub"]:
        lines.append("- (없음)")
    lines.extend(["", "## 4. 백엔드 범용 stub", ""])
    b = payload["sources"]["backend_generic_stub"]
    lines.append(f"- 파일: `{b['router_file']}`")
    lines.append(f"- 패턴: {b['pattern']}")
    lines.append(f"- 비고: {b['notes']}")
    lines.extend(["", "## 5. `docs/crud-backlog.md` §2.6 참조 (문서 불릿)", ""])
    for b in payload["sources"]["crud_backlog_section_2_6"]:
        lines.append(f"- {b}")
    if not payload["sources"]["crud_backlog_section_2_6"]:
        lines.append("- (섹션 파싱 실패 시 문서를 직접 확인)")
    lines.extend(
        [
            "",
            "## 갱신 방법",
            "",
            "```bash",
            "python3 debug/generate_incomplete_features_inventory.py",
            "```",
            "",
            "산출: `analysis/audit/incomplete-features-inventory.md` · `.json`",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
