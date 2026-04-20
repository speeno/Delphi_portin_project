#!/usr/bin/env python3
"""
frf_legacy_usage_extractor — 레거시 Pascal/.dfm 소스에서 ``.frf`` 호출 사이트 매핑 추출.

목적
====
98 정본 ``.frf`` 가 어떤 Pascal unit / TfrReport 컴포넌트 / OnGetValue 핸들러
/ 데이터셋 컬럼에 의해 적재·바인딩되는지 자동 산출. C7 운영 컴파일러
(``print_ir_compiler``) 가 IR 의 expressions_dictionary 를 채울 때 컬럼 이름
원본을 추적하기 위한 진실의 원천 (single source of truth).

추출 패턴
=========
1. ``LoadFromFile(GetExecPath + 'Report\\<NAME>.frf')`` — 적재 사이트.
2. ``OnGetValue = <handler>`` 또는 ``frReportXX_YY.OnGetValue`` 핸들러.
3. ``frReportXX_YYGetValue(...)`` 함수 본문 안의
   ``if VarName = '<column>' then ParValue := <table>.FieldByName('<col>')``
   패턴 → (column → dataset.column) 매핑.
4. ``.dfm`` 의 ``object frReportXX_YY: TfrReport`` 정의 — 컴포넌트 위치.

산출
====
- ``analysis/print_specs/frf_legacy_usage_map.md`` (사람이 읽는 표).
- ``analysis/print_specs/frf_legacy_usage_map.json`` (도구 친화 구조).

사용
====
::

    python3 tools/analysis/frf_legacy_usage_extractor.py
    python3 tools/analysis/frf_legacy_usage_extractor.py --json-only
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_ROOT = REPO_ROOT / "legacy_delphi_source" / "legacy_source"
CANONICAL_REPORT_DIR = LEGACY_ROOT / "Report"
OUT_DIR = REPO_ROOT / "analysis" / "print_specs"


LOAD_PAT = re.compile(
    r"(?P<comp>fr[A-Za-z_]\w*)\.LoadFromFile\s*\(\s*[^)]*Report[\\/](?P<frf>[^'\"]+\.frf)",
    re.IGNORECASE,
)
# `With Tong60.frReportXX_YY do begin` 다음 LoadFromFile(...) 패턴.
LOAD_BARE_PAT = re.compile(
    r"LoadFromFile\s*\(\s*[^)]*Report[\\/](?P<frf>[^'\"]+\.frf)",
    re.IGNORECASE,
)
WITH_REPORT_PAT = re.compile(
    r"\bWith\s+(?:[A-Za-z_]\w*\.)?(?P<comp>fr[A-Za-z_]\w*)\s+do\b",
    re.IGNORECASE,
)
FIND_OBJECT_PAT = re.compile(
    r"FindObject\s*\(\s*'(?P<obj>[^']+)'\s*\)\s*\.Memo\.Text\s*:?=\s*"
    r"(?P<source>[^;\n]+);",
    re.IGNORECASE,
)
PROC_PAT = re.compile(
    r"procedure\s+T[A-Za-z_]\w*\.(?P<proc>[A-Za-z_]\w*)\b", re.IGNORECASE
)
GETVALUE_HANDLER_PAT = re.compile(
    r"(?P<comp>fr[A-Za-z_]\w*)\.OnGetValue\s*:?=\s*(?P<handler>[A-Za-z_]\w*)",
    re.IGNORECASE,
)
GETVALUE_PROC_PAT = re.compile(
    r"procedure\s+T[A-Za-z_]\w*\.(?P<handler>fr[A-Za-z_]\w*GetValue)\b",
    re.IGNORECASE,
)
FIELD_BIND_PAT = re.compile(
    r"VarName\s*=\s*'(?P<col>[^']+)'\s*then\s*ParValue\s*:?=\s*"
    r"(?P<table>[A-Za-z_]\w*)\.FieldByName\s*\(\s*'(?P<field>[^']+)'\s*\)",
    re.IGNORECASE | re.DOTALL,
)
DATASET_ASSIGN_PAT = re.compile(
    r"(?:[A-Za-z_]\w*\.)?(?P<dbds>fr[A-Za-z_]*DBDataSet\w*)\.DataSet\s*:?=\s*"
    r"(?P<src>[A-Za-z_]\w*)",
    re.IGNORECASE,
)
DFM_REPORT_OBJ_PAT = re.compile(
    r"object\s+(?P<comp>fr[A-Za-z_]\w*)\s*:\s*TfrReport\b", re.IGNORECASE
)
DFM_DATASET_PAT = re.compile(
    r"object\s+(?P<comp>[A-Za-z_]\w*)\s*:\s*"
    r"(?P<cls>T(?:fr)?(?:DBDataSet|Table|Query|ClientDataSet))\b",
    re.IGNORECASE,
)


@dataclass
class FrfUsage:
    frf: str
    load_sites: list[tuple[str, str, int]] = field(default_factory=list)
    components: set[str] = field(default_factory=set)
    handlers: set[str] = field(default_factory=set)
    field_bindings: list[tuple[str, str, str]] = field(default_factory=list)
    dfm_units: set[str] = field(default_factory=set)
    procedures: set[str] = field(default_factory=set)
    find_object_targets: list[tuple[str, str]] = field(default_factory=list)


def collect_canonical_frfs() -> list[str]:
    return sorted(p.name for p in CANONICAL_REPORT_DIR.glob("*.frf"))


def iter_legacy_pas_dfm() -> list[Path]:
    """``.pas`` / ``.dfm`` 만 (백업 ``~pas`` 는 제외)."""
    files: list[Path] = []
    for ext in ("pas", "dfm"):
        for p in LEGACY_ROOT.rglob(f"*.{ext}"):
            if "~" in p.name:
                continue
            files.append(p)
    return files


def _last_match_before(pattern: re.Pattern, text: str, pos: int) -> re.Match | None:
    """``text[:pos]`` 안에서 마지막 ``pattern`` 매치 — context-walk 용."""
    last = None
    for m in pattern.finditer(text, 0, pos):
        last = m
    return last


def _alias_targets(canonical: list[str], loaded_name: str) -> list[str]:
    """``LoadFromFile`` 가 참조한 파일명을 정본 이름으로 정규화.

    예: ``Report_2_11.frf`` (적재) ↔ ``Report_2_11-.frf`` (정본 이름).
    정본에 동일명이 있으면 자기 자신, 없으면 ``base-`` 접두로 매칭되는
    정본을 모두 반환.
    """
    if loaded_name in canonical:
        return [loaded_name]
    stem = loaded_name.removesuffix(".frf")
    return [c for c in canonical if c.startswith(stem + "-")]


def extract_usage(canonical: list[str]) -> dict[str, FrfUsage]:
    usage = {f: FrfUsage(frf=f) for f in canonical}

    for path in iter_legacy_pas_dfm():
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        rel = str(path.relative_to(REPO_ROOT))

        # 1) 명시 `frReportXX.LoadFromFile(...)` 패턴.
        for m in LOAD_PAT.finditer(text):
            raw_name = Path(m.group("frf")).name
            comp = m.group("comp")
            line = text.count("\n", 0, m.start()) + 1
            for frf_name in _alias_targets(canonical, raw_name):
                usage[frf_name].load_sites.append((rel, comp, line))
                usage[frf_name].components.add(comp)
                usage[frf_name].dfm_units.add(rel)
                if path.suffix.lower() == ".pas":
                    pm = _last_match_before(PROC_PAT, text, m.start())
                    if pm:
                        usage[frf_name].procedures.add(pm.group("proc"))
                    lo = max(0, m.start() - 100)
                    hi = min(len(text), m.end() + 2000)
                    for fm in FIND_OBJECT_PAT.finditer(text, lo, hi):
                        usage[frf_name].find_object_targets.append(
                            (fm.group("obj"), fm.group("source").strip())
                        )
                    # ``frDBDataSetXX.DataSet := <src>`` 패턴 — 묵시 데이터셋 바인딩.
                    for dm in DATASET_ASSIGN_PAT.finditer(text, lo, hi):
                        usage[frf_name].field_bindings.append(
                            (dm.group("dbds"), dm.group("src"), "*")
                        )

        # 2) `With ... do begin .. LoadFromFile(...)` 패턴 — context walk.
        if path.suffix.lower() == ".pas":
            for m in LOAD_BARE_PAT.finditer(text):
                raw_name = Path(m.group("frf")).name
                aliases = _alias_targets(canonical, raw_name)
                if not aliases:
                    continue
                line = text.count("\n", 0, m.start()) + 1
                wm = _last_match_before(WITH_REPORT_PAT, text, m.start())
                comp = wm.group("comp") if wm else "(unknown)"
                pm = _last_match_before(PROC_PAT, text, m.start())
                lo = max(0, m.start() - 100)
                hi = min(len(text), m.end() + 2000)
                for frf_name in aliases:
                    already = any(
                        rel == s[0] and abs(line - s[2]) < 2
                        for s in usage[frf_name].load_sites
                    )
                    if already:
                        continue
                    if pm:
                        usage[frf_name].procedures.add(pm.group("proc"))
                    usage[frf_name].load_sites.append((rel, comp, line))
                    usage[frf_name].components.add(comp)
                    usage[frf_name].dfm_units.add(rel)
                    for fm in FIND_OBJECT_PAT.finditer(text, lo, hi):
                        usage[frf_name].find_object_targets.append(
                            (fm.group("obj"), fm.group("source").strip())
                        )
                    for dm in DATASET_ASSIGN_PAT.finditer(text, lo, hi):
                        usage[frf_name].field_bindings.append(
                            (dm.group("dbds"), dm.group("src"), "*")
                        )

        if path.suffix.lower() == ".dfm":
            for m in DFM_REPORT_OBJ_PAT.finditer(text):
                comp = m.group("comp")
                for u in usage.values():
                    if comp in u.components:
                        u.dfm_units.add(rel)

    # OnGetValue handlers + field bindings — Pascal 본문 분석.
    handler_to_components: dict[str, set[str]] = collections.defaultdict(set)
    handler_to_bindings: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)

    for path in iter_legacy_pas_dfm():
        if path.suffix.lower() != ".pas":
            continue
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue

        for m in GETVALUE_HANDLER_PAT.finditer(text):
            handler_to_components[m.group("handler")].add(m.group("comp"))

        for m in GETVALUE_PROC_PAT.finditer(text):
            handler = m.group("handler")
            body_start = m.end()
            body_end = text.find("\nprocedure ", body_start)
            if body_end == -1:
                body_end = len(text)
            body = text[body_start:body_end]
            for fm in FIELD_BIND_PAT.finditer(body):
                handler_to_bindings[handler].append(
                    (fm.group("col"), fm.group("table"), fm.group("field"))
                )

    # 매핑 부착: handler → components → frf usage.
    for handler, comps in handler_to_components.items():
        bindings = handler_to_bindings.get(handler, [])
        for comp in comps:
            for u in usage.values():
                if comp in u.components:
                    u.handlers.add(handler)
                    u.field_bindings.extend(bindings)

    # 베이스 양식 → 하이픈 변형 (-1, -2, -N) 상속.
    # 예: ``Report_2_13-1.frf`` 는 ``Report_2_13.frf`` 와 동일 컴포넌트/핸들러
    # /바인딩으로 적재. (서브 페이지 / 카피 본).
    _propagate_to_variants(usage)

    return usage


_VARIANT_RE = re.compile(r"^(?P<base>.+?)-(?:\d+|[A-Za-z])?\.frf$", re.IGNORECASE)


def _propagate_to_variants(usage: dict[str, FrfUsage]) -> None:
    for name, u in list(usage.items()):
        m = _VARIANT_RE.match(name)
        if not m:
            continue
        base = m.group("base") + ".frf"
        bu = usage.get(base)
        if bu is None or not bu.load_sites:
            continue
        # 변형이 자체적으로 매핑이 비어있을 때만 상속 (덮어쓰기 X).
        if u.load_sites or u.handlers or u.field_bindings:
            continue
        for site in bu.load_sites:
            u.load_sites.append((site[0], site[1] + " (inherited)", site[2]))
        u.components |= bu.components
        u.handlers |= bu.handlers
        u.field_bindings.extend(bu.field_bindings)
        u.dfm_units |= bu.dfm_units
        u.procedures |= bu.procedures
        u.find_object_targets.extend(bu.find_object_targets)


def usage_to_dict(u: FrfUsage) -> dict:
    return {
        "frf": u.frf,
        "load_sites": [
            {"file": rel, "component": comp, "line": ln}
            for (rel, comp, ln) in u.load_sites
        ],
        "components": sorted(u.components),
        "handlers": sorted(u.handlers),
        "procedures": sorted(u.procedures),
        "dfm_units": sorted(u.dfm_units),
        "find_object_targets": [
            {"object": obj, "source": src}
            for (obj, src) in sorted(set(u.find_object_targets))
        ],
        "field_bindings": [
            {"frf_var": col, "dataset": tbl, "column": fld}
            for (col, tbl, fld) in sorted(set(u.field_bindings))
        ],
        "fill_ratio": _coverage(u),
    }


def _coverage(u: FrfUsage) -> float:
    """채움률 — load + (handler|procedure) + (binding|find_object) 셋."""
    have = sum([
        bool(u.load_sites),
        bool(u.handlers or u.procedures),
        bool(u.field_bindings or u.find_object_targets),
    ])
    return round(have / 3.0, 4)


def render_markdown(usage: dict[str, FrfUsage]) -> str:
    lines: list[str] = []
    lines.append("# FRF 레거시 호출 사이트 매핑 (자동 추출)\n")
    lines.append(
        "본 문서는 [`tools/analysis/frf_legacy_usage_extractor.py`]"
        "(../../tools/analysis/frf_legacy_usage_extractor.py) 가 생성한다. "
        "수동 편집 ❌.\n"
    )
    lines.append(
        "- 정본 디렉터리: `legacy_delphi_source/legacy_source/Report/` (98 건)\n"
        "- 추출 패턴: `LoadFromFile`, `OnGetValue`, `FieldByName`, "
        "`object frReportXX_YY: TfrReport`.\n"
    )

    total = len(usage)
    fully = sum(1 for u in usage.values() if _coverage(u) >= 0.9)
    partial = sum(1 for u in usage.values() if 0.0 < _coverage(u) < 0.9)
    empty = sum(1 for u in usage.values() if _coverage(u) == 0.0)
    lines.append("## 채움률 요약\n")
    lines.append(f"- 정본 총 {total} 건")
    lines.append(f"- 풀-매핑 (load+procedure+binding) ≥ 90%: **{fully}** 건 "
                 f"({fully * 100 // total}%)")
    lines.append(f"- 부분 매핑: **{partial}** 건")
    lines.append(f"- 매핑 0: **{empty}** 건\n")
    if empty:
        lines.append("### 매핑 0 사유 (수동 분석)\n")
        lines.append(
            "- ``-1`` / ``-2`` / ``-N`` 접미 변형 (예: ``Report_2_13-1.frf``,"
            " ``Report_4_51-1.frf``): 베이스 양식 (``Report_2_13.frf``,"
            " ``Report_4_51.frf``) 의 *서브 페이지/카피* 로 동적 선택. 따라서"
            " ``LoadFromFile`` 에 *문자열로 등장하지 않음* 이 정상.\n"
            "- ``계산서.frf``: ``Tong06.dfm`` 의 ``frReport49_01.ReportForm = {…}``"
            " 안에 BLOB 으로 *임베드* (``StoreInDFM = True``). 적재는 form-create"
            " 시점에 자동.\n"
            "- 일부 ``Report_6_*`` / ``Report_3_43`` 등: 현재 메뉴에서 미연결"
            " (legacy 가지치기 후 죽은 양식 가능성).\n"
        )

    # 호출 흐름 mermaid (대표 5종 — 가장 많이 적재되는 것).
    top_loaded = sorted(
        usage.values(), key=lambda u: -len(u.load_sites)
    )[:5]
    if top_loaded:
        lines.append("## 호출 흐름 (top 5 적재)\n")
        lines.append("```mermaid")
        lines.append("flowchart LR")
        seen_edges: set[tuple[str, str, str]] = set()
        _safe = lambda s: re.sub(r"[^A-Za-z0-9_]", "_", s)
        for u in top_loaded:
            for rel, comp, _ln in u.load_sites[:3]:
                pas_unit = Path(rel).stem
                # 'inherited' suffix 등 부가 표시는 노드 라벨에서 제거.
                comp_clean = comp.split(" ", 1)[0]
                edge = (pas_unit, comp_clean, u.frf)
                if edge in seen_edges:
                    continue
                seen_edges.add(edge)
                lines.append(
                    f"  {_safe(pas_unit)}[{pas_unit}.pas] --> "
                    f"{_safe(comp_clean)}[{comp_clean}] --> "
                    f"{_safe(u.frf)}[{u.frf}]"
                )
        lines.append("```\n")

    # 정본별 표.
    lines.append("## 정본 매핑 표\n")
    lines.append(
        "| FRF | 적재 unit (.pas) | TfrReport 컴포넌트 | 호출 procedure | "
        "Memo 바인딩 / 핸들러 | 채움률 |"
    )
    lines.append("| --- | --- | --- | --- | --- | ---: |")
    for name in sorted(usage):
        u = usage[name]
        units = ", ".join(sorted({Path(s[0]).name for s in u.load_sites})) or "—"
        comps = ", ".join(sorted(u.components)) or "—"
        procs = ", ".join(sorted(u.procedures)[:5]) or "—"
        # binding 우선순위: OnGetValue 핸들러 > FindObject 타겟.
        binds_lines: list[str] = []
        if u.handlers:
            binds_lines.append("handlers: " + ", ".join(sorted(u.handlers)[:3]))
        if u.field_bindings:
            uniq = sorted({f"{tbl}.{fld}" for (_c, tbl, fld) in u.field_bindings})
            binds_lines.append(
                "fields: " + ", ".join(uniq[:5])
                + (f" … (+{len(uniq) - 5})" if len(uniq) > 5 else "")
            )
        if u.find_object_targets:
            objs = sorted({obj for (obj, _) in u.find_object_targets})
            binds_lines.append(
                "FindObject: " + ", ".join(objs[:5])
                + (f" … (+{len(objs) - 5})" if len(objs) > 5 else "")
            )
        binds = "<br>".join(binds_lines) or "—"
        lines.append(
            f"| `{name}` | {units} | {comps} | {procs} | {binds} | "
            f"{int(_coverage(u) * 100)}% |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-only", action="store_true", help="markdown 생략, json 만 출력.")
    args = ap.parse_args(argv)

    canonical = collect_canonical_frfs()
    usage = extract_usage(canonical)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "frf_legacy_usage_map.json"
    md_path = OUT_DIR / "frf_legacy_usage_map.md"

    json_payload = {
        "canonical_count": len(canonical),
        "by_frf": {name: usage_to_dict(usage[name]) for name in sorted(usage)},
    }
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2),
                         encoding="utf-8")

    if not args.json_only:
        md_path.write_text(render_markdown(usage), encoding="utf-8")

    print(json.dumps({
        "canonical_count": len(canonical),
        "fully_mapped": sum(1 for u in usage.values() if _coverage(u) >= 0.9),
        "partial_mapped": sum(1 for u in usage.values() if 0.0 < _coverage(u) < 0.9),
        "empty_mapped": sum(1 for u in usage.values() if _coverage(u) == 0.0),
        "json": str(json_path.relative_to(REPO_ROOT)),
        "md": str(md_path.relative_to(REPO_ROOT)) if not args.json_only else None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
