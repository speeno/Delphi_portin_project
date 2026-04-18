#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
화면 카드 자동 생성 빌더 (analysis/screen_cards/<form>.md + INDEX.md).

설계 근거: docs/screen-cards-generation-plan.md §2~§4
입력: analysis/*.json 7종 + (선택) analysis/form_layouts/<form>.json
        + (선택) debug/output/captured_queries_*.json
출력: analysis/screen_cards/<form>.md (1폼 1장) + INDEX.md (전체)
       + (선택) analysis/screen_cards/_stats.json

사용:
  python3 tools/analysis/screen_card_builder.py --form Subu00 --rebuild-index
  python3 tools/analysis/screen_card_builder.py                      # 전체 폼
  python3 tools/analysis/screen_card_builder.py --form Subu00 --with-capture debug/output/captured_queries_*.json

설계 원칙(SRP):
  - 본 모듈은 "조립" 만 담당: 기존 analysis/*.json을 읽어 마크다운 직조립.
  - PAS/DFM 재파싱은 하지 않음 (tools/run_analysis.py 결과 재사용).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import glob
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = REPO_ROOT / "analysis"
DEFAULT_OUT_DIR = ANALYSIS_DIR / "screen_cards"
LAYOUTS_DIR = ANALYSIS_DIR / "form_layouts"

# -------------------------------------------------------------
# 0. JSON 로딩 (가벼운 캐시)
# -------------------------------------------------------------

_CACHE: dict[str, Any] = {}


def _load(name: str) -> Any:
    if name not in _CACHE:
        path = ANALYSIS_DIR / name
        if not path.exists():
            _CACHE[name] = None
        else:
            with path.open("r", encoding="utf-8") as f:
                _CACHE[name] = json.load(f)
    return _CACHE[name]


# -------------------------------------------------------------
# 1. 폼 ↔ 유닛(PAS) 매핑
# -------------------------------------------------------------


def _form_unit(form_entry: dict) -> str:
    """form_inventory[].file 의 stem(.dfm 제거)을 unit 으로 사용.

    예) /.../legacy_source/Chul.dfm → 'Chul'
    """
    return Path(form_entry["file"]).stem


def _all_form_entries() -> list[dict]:
    inv = _load("form_inventory.json") or []
    return inv


def _list_form_names() -> list[str]:
    return sorted({e["form_name"] for e in _all_form_entries()})


def _form_entries_by_name(form_name: str) -> list[dict]:
    return [e for e in _all_form_entries() if e["form_name"] == form_name]


# -------------------------------------------------------------
# 2. 섹션 빌더 — 표준 구성 §0~§9
# -------------------------------------------------------------


def _md_table(headers: list[str], rows: Iterable[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def _section_summary(form_name: str, entries: list[dict],
                     events: list[dict], queries: list[dict],
                     impact_for_form: list[dict],
                     validations: list[dict],
                     scenario_match: str | None) -> str:
    if not entries:
        return f"## 0. 한눈 요약\n- (form_inventory에 등재되지 않음)\n"

    files = [e["file"] for e in entries]
    pas_files = [str(Path(f).with_suffix(".pas")) for f in files]
    total_components = sum(e.get("component_count", 0) for e in entries)
    total_events = sum(e.get("event_count", 0) for e in entries)
    component_summary: dict[str, int] = {}
    for e in entries:
        for k, v in (e.get("component_summary") or {}).items():
            component_summary[k] = component_summary.get(k, 0) + v
    top_components = ", ".join(
        f"{k}×{v}" for k, v in sorted(component_summary.items(), key=lambda kv: -kv[1])[:6]
    )

    impact_tables = sorted({row.get("table") for row in impact_for_form if row.get("table")})

    lines = [
        "## 0. 한눈 요약",
        f"- 파일(DFM): {', '.join(files) or '-'}",
        f"- 파일(PAS 추정): {', '.join(pas_files) or '-'}",
        f"- 컴포넌트 수: **{total_components}** / 이벤트 수: **{total_events}** / form 등록 수: **{len(entries)}**",
        f"- 주요 컴포넌트: {top_components or '-'}",
        f"- 핵심 SQL 수: **{len(queries)}** / 영향 테이블 수: **{len(impact_tables)}** / 검증 규칙 수: **{len(validations)}**",
        f"- 매핑 시나리오: **{scenario_match or '-'}**",
        "",
    ]
    return "\n".join(lines)


def _section_ui(form_name: str, entries: list[dict]) -> str:
    if not entries:
        return "## 1. UI 구성\n- (form_inventory 누락)\n"
    lines = ["## 1. UI 구성"]
    for e in entries:
        lines.append(f"### {e['form_class']} — {e['file']}")
        cs = e.get("component_summary") or {}
        if cs:
            rows = sorted(cs.items(), key=lambda kv: -kv[1])
            lines.append(_md_table(["component_type", "count"], rows))
        lines.append(f"- component_count: {e.get('component_count')}, event_count: {e.get('event_count')}")
        lines.append("")

    layout_path = LAYOUTS_DIR / f"{form_name}.json"
    if layout_path.exists():
        try:
            data = json.loads(layout_path.read_text(encoding="utf-8"))
            comps = data.get("components") or data.get("tree") or []
            count = len(comps) if isinstance(comps, list) else "?"
            lines.append(f"- 레이아웃 메타: `analysis/form_layouts/{form_name}.json` (top-level components: {count})")
        except Exception as exc:
            lines.append(f"- 레이아웃 메타 읽기 실패: {exc}")
    else:
        lines.append(f"- 레이아웃 메타: (없음 — `analysis/form_layouts/{form_name}.json` 미생성)")
    lines.append("")
    return "\n".join(lines)


def _section_events(form_name: str, events: list[dict]) -> str:
    if not events:
        return "## 2. 이벤트 흐름\n- (event_flow 매칭 0건)\n"
    by_event: dict[str, list[dict]] = {}
    for ev in events:
        by_event.setdefault(ev.get("event", "?"), []).append(ev)
    lines = ["## 2. 이벤트 흐름", f"- 핸들러 합계: **{len(events)}** / 이벤트 종류: **{len(by_event)}**", ""]

    rows = []
    for event_name, items in sorted(by_event.items(), key=lambda kv: -len(kv[1])):
        sample = items[0]
        rows.append([event_name, len(items), sample.get("component"), sample.get("handler")])
    lines.append(_md_table(["event", "count", "예시 component", "예시 handler"], rows[:25]))
    if len(rows) > 25:
        lines.append(f"\n_(상위 25종만 표기, 전체 {len(rows)}종)_")
    lines.append("")
    return "\n".join(lines)


def _section_data_access(form_name: str, queries: list[dict]) -> str:
    if not queries:
        return "## 3. 데이터 액세스 (SQL)\n- (query_catalog 매칭 0건)\n"
    by_type: dict[str, int] = {}
    by_table: dict[str, int] = {}
    for q in queries:
        by_type[q.get("type", "?")] = by_type.get(q.get("type", "?"), 0) + 1
        for t in q.get("tables") or []:
            by_table[t] = by_table.get(t, 0) + 1

    lines = ["## 3. 데이터 액세스 (SQL)",
             f"- SQL 합계: **{len(queries)}**, 타입 분포: " + ", ".join(f"{k}×{v}" for k, v in sorted(by_type.items())),
             "",
             "### 영향 테이블 (작업 빈도)",
             _md_table(["table", "count"], sorted(by_table.items(), key=lambda kv: -kv[1])[:20]),
             "",
             "### 주요 SQL (line 오름차순 상위 15개)"]

    for q in sorted(queries, key=lambda x: x.get("line", 0))[:15]:
        sql = (q.get("sql") or "").strip().replace("\n", " ")
        if len(sql) > 200:
            sql = sql[:200] + "…"
        lines.append(f"- L{q.get('line')} **{q.get('type')}** `{', '.join(q.get('tables') or [])}` — `{sql}`")
    if len(queries) > 15:
        lines.append(f"\n_(상위 15건 표기, 전체 {len(queries)}건은 `analysis/query_catalog.json` 참조)_")
    lines.append("")
    return "\n".join(lines)


def _section_db_impact(form_name: str, impact_for_form: list[dict]) -> str:
    if not impact_for_form:
        return "## 4. DB 영향\n- (db_impact_matrix 매칭 0건)\n"
    rows = [[r["table"], r.get("C", 0), r.get("R", 0), r.get("U", 0), r.get("D", 0),
             r.get("total", 0), "✓" if r.get("write_access") else ""]
            for r in sorted(impact_for_form, key=lambda x: -x.get("total", 0))]
    lines = [
        "## 4. DB 영향",
        f"- 본 폼이 접근하는 테이블: **{len(rows)}**",
        _md_table(["table", "C", "R", "U", "D", "total", "write?"], rows[:30]),
    ]
    if len(rows) > 30:
        lines.append(f"\n_(상위 30개, 전체 {len(rows)}개)_")
    lines.append("- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.")
    lines.append("")
    return "\n".join(lines)


def _section_validations(form_name: str, validations: list[dict]) -> str:
    if not validations:
        return "## 5. 검증 규칙\n- (validation_rules 매칭 0건)\n"
    lines = ["## 5. 검증 규칙", f"- 합계: **{len(validations)}**", ""]
    rows = []
    for v in sorted(validations, key=lambda x: x.get("line", 0))[:20]:
        msg = (v.get("message") or "").replace("\n", " ")
        if len(msg) > 80:
            msg = msg[:80] + "…"
        rows.append([v.get("line"), v.get("type"), msg])
    lines.append(_md_table(["line", "type", "message"], rows))
    if len(validations) > 20:
        lines.append(f"\n_(상위 20건, 전체 {len(validations)}건)_")
    lines.append("")
    return "\n".join(lines)


def _section_variants(form_name: str, variants: list[dict]) -> str:
    if not variants:
        return "## 6. 고객사 분기\n- (customer_variants 매칭 0건)\n"
    lines = ["## 6. 고객사 분기"]
    for v in variants:
        lines.append(f"- L{v.get('line')} `{v.get('variant_value')}` — `{v.get('code', '').strip()}`")
    lines.append("")
    return "\n".join(lines)


def _section_oq_gap_dec(form_name: str) -> str:
    return "\n".join([
        "## 7. 관련 OQ·GAP·DEC",
        f"- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)",
        f"- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)",
        f"- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)",
        f"- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.",
        "",
    ])


def _section_print_scanner(form_name: str) -> str:
    return "\n".join([
        "## 8. 인쇄·바코드 연관",
        f"- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)",
        f"- (수동) 위 문서에서 form `{form_name}` 또는 인접 unit 검색.",
        "",
    ])


def _section_checklist(form_name: str, scenario_match: str | None,
                       capture_count: int) -> str:
    contract_glob = list((REPO_ROOT / "migration" / "contracts").glob("*.yaml"))
    contract_present = "[x]" if any(form_name.lower() in p.name.lower() or
                                     (scenario_match or "").lower() in p.name.lower()
                                     for p in contract_glob) else "[ ]"
    threshold_present = "[x]" if (REPO_ROOT / "docs" / "eval-axes-and-dod-draft.md").exists() else "[ ]"
    capture_present = "[x]" if capture_count > 0 else "[ ]"
    return "\n".join([
        "## 9. 포팅 체크리스트(자동 생성)",
        f"- {contract_present} 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: {scenario_match or '-'})",
        f"- {threshold_present} 5축 임계값(eval-axes-and-dod-draft.md) 정의됨",
        f"- {capture_present} 본 화면 SQL 이 query_capture 로 보강됨 ({capture_count}건 매칭)",
        "",
    ])


# -------------------------------------------------------------
# 3. 시나리오 매핑 (best-effort)
# -------------------------------------------------------------


def _scenario_for(form_name: str) -> str | None:
    path = REPO_ROOT / "dashboard" / "data" / "porting-screens.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    for sc in data.get("scenarios") or []:
        delphi = sc.get("delphi") or {}
        primary_form = delphi.get("primary_form") or delphi.get("form") or ""
        related = delphi.get("related_forms") or delphi.get("forms") or []
        candidates = [primary_form, *related]
        candidates_norm = {c.lstrip("T") for c in candidates if c}
        if form_name in candidates or form_name in candidates_norm:
            return f"{sc.get('id')} {sc.get('name')}"
        primary_unit = (delphi.get("primary_unit") or "").lower()
        if form_name.lower() in primary_unit:
            return f"{sc.get('id')} {sc.get('name')}"
    return None


# -------------------------------------------------------------
# 4. 캡처 매칭 (선택)
# -------------------------------------------------------------


def _capture_match_count(form_name: str, capture_files: list[str]) -> int:
    if not capture_files:
        return 0
    queries = _queries_for_form(form_name)
    sqls = {(q.get("sql") or "").strip().lower() for q in queries}
    matched = 0
    for cf in capture_files:
        try:
            data = json.loads(Path(cf).read_text(encoding="utf-8"))
        except Exception:
            continue
        items = data if isinstance(data, list) else data.get("queries") or []
        for it in items:
            sql = (it.get("sql") or it.get("query") or "").strip().lower()
            if sql in sqls:
                matched += 1
    return matched


# -------------------------------------------------------------
# 5. 데이터 슬라이싱 헬퍼
# -------------------------------------------------------------


def _events_for_form(form_name: str) -> list[dict]:
    ev = _load("event_flow.json") or []
    return [e for e in ev if e.get("form") == form_name]


def _queries_for_form(form_name: str) -> list[dict]:
    qc = _load("query_catalog.json") or []
    units = {_form_unit(e) for e in _form_entries_by_name(form_name)}
    return [q for q in qc if q.get("unit") in units]


def _impact_for_form(form_name: str) -> list[dict]:
    impact = _load("db_impact_matrix.json") or {}
    crud = impact.get("crud_matrix") or []
    return [r for r in crud if form_name in (r.get("forms") or [])]


def _validations_for_form(form_name: str) -> list[dict]:
    vr = _load("validation_rules.json") or []
    units = {_form_unit(e) for e in _form_entries_by_name(form_name)}
    return [v for v in vr if v.get("unit") in units]


def _variants_for_form(form_name: str) -> list[dict]:
    cv = _load("customer_variants.json") or []
    units = {_form_unit(e) for e in _form_entries_by_name(form_name)}
    return [c for c in cv if c.get("unit") in units]


# -------------------------------------------------------------
# 6. 카드 1장 빌드
# -------------------------------------------------------------


def build_card(form_name: str, capture_files: list[str] | None = None) -> tuple[str, dict]:
    entries = _form_entries_by_name(form_name)
    events = _events_for_form(form_name)
    queries = _queries_for_form(form_name)
    impact = _impact_for_form(form_name)
    validations = _validations_for_form(form_name)
    variants = _variants_for_form(form_name)
    scenario = _scenario_for(form_name)
    capture_n = _capture_match_count(form_name, capture_files or [])

    form_class = entries[0]["form_class"] if entries else "unknown"
    title = f"# 화면 카드: {form_name} ({form_class})\n"

    parts = [
        title,
        f"_생성: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — `tools/analysis/screen_card_builder.py`_",
        "",
        _section_summary(form_name, entries, events, queries, impact, validations, scenario),
        _section_ui(form_name, entries),
        _section_events(form_name, events),
        _section_data_access(form_name, queries),
        _section_db_impact(form_name, impact),
        _section_validations(form_name, validations),
        _section_variants(form_name, variants),
        _section_oq_gap_dec(form_name),
        _section_print_scanner(form_name),
        _section_checklist(form_name, scenario, capture_n),
    ]
    md = "\n".join(parts)

    stats = {
        "form_name": form_name,
        "form_class": form_class,
        "scenario": scenario,
        "components": sum(e.get("component_count", 0) for e in entries),
        "events": len(events),
        "sql": len(queries),
        "tables": len(impact),
        "validations": len(validations),
        "variants": len(variants),
        "capture_matched": capture_n,
    }
    return md, stats


# -------------------------------------------------------------
# 7. INDEX 빌드
# -------------------------------------------------------------


def build_index(stats_list: list[dict]) -> str:
    lines = [
        "# 화면 카드 INDEX",
        "",
        f"_생성: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — 자동 갱신_",
        "",
        f"- 총 카드 수: **{len(stats_list)}**",
        "",
        _md_table(
            ["form_name", "form_class", "scenario", "components", "events", "sql", "tables", "capture"],
            [[f"[{s['form_name']}]({s['form_name']}.md)", s["form_class"], s["scenario"] or "-",
              s["components"], s["events"], s["sql"], s["tables"], s["capture_matched"]]
             for s in sorted(stats_list, key=lambda x: x["form_name"])],
        ),
        "",
        "_본 인덱스는 `tools/analysis/screen_card_builder.py --rebuild-index` 로 갱신됩니다._",
        "",
    ]
    return "\n".join(lines)


# -------------------------------------------------------------
# 8. CLI
# -------------------------------------------------------------


def _expand_capture_paths(patterns: list[str]) -> list[str]:
    out: list[str] = []
    for p in patterns:
        out.extend(glob.glob(p))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="화면 카드 자동 생성 빌더")
    ap.add_argument("--form", help="단일 폼만 생성 (예: Subu00). 미지정 시 전체.")
    ap.add_argument("--out", default=str(DEFAULT_OUT_DIR), help="출력 디렉터리")
    ap.add_argument("--with-capture", action="append", default=[],
                    help="query_capture 결과 JSON glob (반복 지정 가능)")
    ap.add_argument("--rebuild-index", action="store_true", help="INDEX.md 도 재생성")
    ap.add_argument("--write-stats", action="store_true", help="_stats.json 갱신")
    args = ap.parse_args(argv)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    capture_files = _expand_capture_paths(args.with_capture)
    if args.with_capture and not capture_files:
        print(f"[warn] --with-capture 패턴에 매칭된 파일 0건: {args.with_capture}", file=sys.stderr)

    if not (ANALYSIS_DIR / "form_inventory.json").exists():
        print(f"[error] {ANALYSIS_DIR / 'form_inventory.json'} 가 없습니다. tools/run_analysis.py 먼저 실행하세요.", file=sys.stderr)
        return 2

    targets = [args.form] if args.form else _list_form_names()
    stats_list: list[dict] = []
    for fname in targets:
        if not _form_entries_by_name(fname):
            print(f"[warn] form_inventory에 '{fname}' 없음 — 건너뜀", file=sys.stderr)
            continue
        md, stats = build_card(fname, capture_files)
        out = out_dir / f"{fname}.md"
        out.write_text(md, encoding="utf-8")
        stats_list.append(stats)
        print(f"[ok] {out.relative_to(REPO_ROOT)}")

    if args.rebuild_index:
        if not args.form:
            all_stats = stats_list
        else:
            existing_stats_path = out_dir / "_stats.json"
            if existing_stats_path.exists():
                try:
                    prev = json.loads(existing_stats_path.read_text(encoding="utf-8"))
                except Exception:
                    prev = []
                merged: dict[str, dict] = {s["form_name"]: s for s in prev}
                for s in stats_list:
                    merged[s["form_name"]] = s
                all_stats = list(merged.values())
            else:
                all_stats = stats_list
        idx = build_index(all_stats)
        (out_dir / "INDEX.md").write_text(idx, encoding="utf-8")
        print(f"[ok] {(out_dir / 'INDEX.md').relative_to(REPO_ROOT)}")

    if args.write_stats and stats_list:
        (out_dir / "_stats.json").write_text(
            json.dumps(stats_list, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"[ok] {(out_dir / '_stats.json').relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
