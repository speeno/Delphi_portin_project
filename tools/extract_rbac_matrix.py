#!/usr/bin/env python3
"""Extract docs/onboarding-rbac-menu-matrix.md tables into JSON / YAML.

DEC-RBAC-02 단일 원천:
  - 입력: docs/onboarding-rbac-menu-matrix.md (사람 읽는 정본)
  - 출력 1: analysis/rbac_menu_matrix.json (백엔드/문서 회귀)
  - 출력 2: 도서물류관리프로그램/frontend/src/data/rbac_menu_matrix.json (Next.js import)
  - 출력 3: migration/contracts/rbac_menu_matrix.yaml (계약 미러)

추출 대상 표:
  §2 최상위 메뉴 (`ACC-MENU-NAV-*`)
  §3 기초관리 하위 (`ACC-MENU-MASTERS-*`)
  §5 년/월(통계) (`ACC-MENU-YM-*`)
  §7 관리자 콘솔 (`ACC-MENU-ADMIN-*`)

각 행은 다음 schema 로 정규화:
  {
    "id": "ACC-MENU-NAV-07",
    "section": "nav" | "masters" | "year_month_stats" | "admin",
    "route": "/(app)/year-month-stats",
    "caption": "년/월(통계)",
    "account_types": ["T1", "T2_PUB", "T3"],   # ✓ 인 계정 유형 (T2-DIST → T2_DIST 정규화)
    "build_roles": ["publisher"],              # source_builds 의 prefix → 추정 매핑
    "license_keys": ["F11"],                    # Fxx 컬럼이 있을 때만
    "source_builds": ["P-STD", "P-KBT"]
  }

비밀 정책: 본 도구는 자격증명을 읽거나 출력하지 않는다 (G3).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "onboarding-rbac-menu-matrix.md"
ANALYSIS_OUT = ROOT / "analysis" / "rbac_menu_matrix.json"
FRONTEND_OUT = (
    ROOT / "도서물류관리프로그램" / "frontend" / "src" / "data" / "rbac_menu_matrix.json"
)
YAML_OUT = ROOT / "migration" / "contracts" / "rbac_menu_matrix.yaml"

# 상위 account_type 은 T1/T2_DIST/T2_PUB/T3 네 가지만 출력한다.
# T3-LITE / T3-FULL 열은 warehouse_menu_tiers 로만 반영한다.
BASE_ACCOUNT_TYPE_COLS: dict[str, str] = {
    "T1": "T1",
    "T2-DIST": "T2_DIST",
    "T2-PUB": "T2_PUB",
    "T3": "T3",
}
WAREHOUSE_TIER_COLS: dict[str, str] = {
    "T3-LITE": "lite",
    "T3-FULL": "full",
}

# source_builds prefix → build_role 매핑 (정합 출처: §1 한 줄 요약)
BUILD_ROLE_FROM_BUILD = {
    "D-STD": "distributor",
    "D-KBT": "distributor",
    "P-STD": "publisher",
    "P-KBT": "publisher",
    "WH-WL": "warehouse_publisher",
    "WH-MS": "warehouse_publisher",
    "WH-BB": "warehouse_publisher",
}


def read_md() -> str:
    return SRC.read_text(encoding="utf-8")


def split_sections(text: str) -> dict[str, str]:
    """Return mapping of '## N. Title' → body (until next H2).

    Section keys are normalized from headings used by the source doc.
    """
    sections: dict[str, str] = {}
    parts = re.split(r"^##\s+", text, flags=re.MULTILINE)
    for part in parts[1:]:
        head, _, body = part.partition("\n")
        sections[head.strip()] = body
    return sections


_BLANK_MARKERS = {"—", "-", ""}


def _parse_table(body: str, *, expected_id_prefix: str) -> list[dict]:
    """Parse a markdown table into list of cell-row dicts.

    The first row is treated as the header (column names),
    second row as the alignment row (skipped), the rest as data rows.
    Only rows whose first cell starts with backtick + expected_id_prefix
    are considered.
    """
    rows: list[dict] = []
    header: list[str] | None = None
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.startswith("|"):
            if header is not None and not rows:
                # 표 시작 전 스킵
                continue
            if header is not None and rows:
                # 표 종료
                break
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(c) <= set(":-") for c in cells):
            continue  # alignment row
        first = cells[0]
        m = re.match(r"`(" + re.escape(expected_id_prefix) + r"[^`]+)`", first)
        if not m:
            continue
        rec = dict(zip(header, cells))
        rec["__id__"] = m.group(1)
        rows.append(rec)
    return rows


def _is_check(cell: str) -> bool:
    cell = cell.strip().strip("*").strip()
    if not cell or cell in _BLANK_MARKERS:
        return False
    # ✓, ✓ (...) 등은 모두 노출 처리. (TBD) / (MS) 등 괄호 단독은 부분 노출 — 보수적으로 false 처리.
    if cell == "✓":
        return True
    if cell.startswith("✓"):
        return True
    return False


def _route_from_cell(cell: str) -> str:
    m = re.search(r"`([^`]+)`", cell)
    return m.group(1).strip() if m else cell.strip()


def _caption_from_cell(cell: str) -> str:
    return re.sub(r"\s+", " ", cell.strip().strip("*"))


def _sources_from_cell(cell: str) -> list[str]:
    if not cell:
        return []
    cleaned = re.sub(r"\([^)]*\)", "", cell)
    cleaned = cleaned.replace("·", ",").replace("**", "")
    parts = [p.strip() for p in re.split(r"[,/]", cleaned) if p.strip()]
    out: list[str] = []
    for p in parts:
        token = p.split()[0].strip().rstrip(".,;")
        if token in BUILD_ROLE_FROM_BUILD:
            out.append(token)
    seen: set[str] = set()
    deduped: list[str] = []
    for t in out:
        if t in seen:
            continue
        seen.add(t)
        deduped.append(t)
    return deduped


def _license_keys_from_cell(cell: str) -> list[str]:
    if not cell:
        return []
    keys = re.findall(r"\bF\d{2}\b", cell)
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def _build_roles_from_sources(sources: list[str]) -> list[str]:
    roles: list[str] = []
    for s in sources:
        role = BUILD_ROLE_FROM_BUILD.get(s)
        if role and role not in roles:
            roles.append(role)
    return roles


def _section_to_menus(rows: list[dict], section_key: str) -> list[dict]:
    menus: list[dict] = []
    for r in rows:
        rid = r["__id__"]
        cols = list(r.keys())
        # 헤더 컬럼 키는 source 파일에 따라 변동: ID/캡션/라우트/T1.../source_builds/Fxx
        caption = ""
        route = ""
        # 라우트 칼럼 후보
        for k in ("라우트(웹 대응)", "웹 라우트", "화면", "라우트"):
            if k in r:
                route = _route_from_cell(r[k])
                break
        # 캡션 칼럼 후보
        for k in ("캡션", "화면"):
            if k in r:
                caption = _caption_from_cell(r[k])
                break
        # 계정 유형 ✓ 검사 (4대 유형) + 자체 물류 티어
        acc_types: list[str] = []
        for label, norm in BASE_ACCOUNT_TYPE_COLS.items():
            if label in r and _is_check(r[label]):
                acc_types.append(norm)
        has_plain_t3 = "T3" in r and _is_check(r["T3"])
        wh_tiers: list[str] = []
        for label, tier in WAREHOUSE_TIER_COLS.items():
            if label in r and _is_check(r[label]):
                wh_tiers.append(tier)
        if wh_tiers and not has_plain_t3 and "T3" not in acc_types:
            # 자체 물류 전용 행 — 상위 유형은 T3 로 간주
            acc_types.append("T3")
        if has_plain_t3:
            # T3 열이 ✓ 이면 일반 독립 출판 셸과 겸하므로 티어 제한 없음
            wh_tiers = []
        # 결정적 정렬
        acc_types = sorted(set(acc_types))
        wh_tiers = sorted(set(wh_tiers))
        # source_builds
        src_cell = r.get("source_builds", "")
        sources = _sources_from_cell(src_cell)
        # license keys (Fxx 칼럼이 있는 경우만 — MASTERS 표에 존재)
        lic = _license_keys_from_cell(r.get("Fxx", ""))
        menus.append({
            "id": rid,
            "section": section_key,
            "route": route,
            "caption": caption,
            "account_types": acc_types,
            "warehouse_menu_tiers": wh_tiers,
            "build_roles": _build_roles_from_sources(sources),
            "license_keys": lic,
            "source_builds": sources,
        })
    return menus


def parse_matrix(text: str) -> dict:
    sections = split_sections(text)

    def find_section(prefix: str) -> str:
        for k, body in sections.items():
            if k.startswith(prefix):
                return body
        return ""

    nav_body = find_section("2.")
    masters_body = find_section("3.")
    ym_body = find_section("5.")
    admin_body = find_section("7.")

    nav_rows = _parse_table(nav_body, expected_id_prefix="ACC-MENU-NAV-")
    masters_rows = _parse_table(masters_body, expected_id_prefix="ACC-MENU-MASTERS-")
    ym_rows = _parse_table(ym_body, expected_id_prefix="ACC-MENU-YM-")
    admin_rows = _parse_table(admin_body, expected_id_prefix="ACC-MENU-ADMIN-")

    menus: list[dict] = []
    menus += _section_to_menus(nav_rows, "nav")
    menus += _section_to_menus(masters_rows, "masters")
    menus += _section_to_menus(ym_rows, "year_month_stats")
    menus += _section_to_menus(admin_rows, "admin")

    payload = {
        "version": "2026-04-25",
        "source": "docs/onboarding-rbac-menu-matrix.md",
        "extracted_by": "tools/extract_rbac_matrix.py",
        "decision_refs": ["DEC-RBAC-02", "DEC-RBAC-03"],
        "account_types": list(BASE_ACCOUNT_TYPE_COLS.values()),
        "warehouse_menu_tiers": sorted(set(WAREHOUSE_TIER_COLS.values())),
        "build_roles": sorted(set(BUILD_ROLE_FROM_BUILD.values())),
        "menus": menus,
    }
    return payload


def render_yaml(payload: dict) -> str:
    """Render the payload as a minimal yaml mirror without external deps."""
    lines: list[str] = []
    lines.append("# AUTO-GENERATED by tools/extract_rbac_matrix.py — DO NOT EDIT MANUALLY.")
    lines.append("# DEC-RBAC-02 단일 원천: docs/onboarding-rbac-menu-matrix.md")
    lines.append(f"version: \"{payload['version']}\"")
    lines.append(f"source: \"{payload['source']}\"")
    lines.append(f"extracted_by: \"{payload['extracted_by']}\"")
    lines.append("decision_refs:")
    for d in payload["decision_refs"]:
        lines.append(f"  - {d}")
    lines.append("account_types:")
    for a in payload["account_types"]:
        lines.append(f"  - {a}")
    lines.append("warehouse_menu_tiers:")
    for w in payload.get("warehouse_menu_tiers") or []:
        lines.append(f"  - {w}")
    lines.append("build_roles:")
    for b in payload["build_roles"]:
        lines.append(f"  - {b}")
    lines.append("menus:")
    for m in payload["menus"]:
        lines.append(f"  - id: {m['id']}")
        lines.append(f"    section: {m['section']}")
        lines.append(f"    route: \"{m['route']}\"")
        cap = m["caption"].replace("\"", "'")
        lines.append(f"    caption: \"{cap}\"")
        lines.append(f"    account_types: [{', '.join(m['account_types'])}]")
        lines.append(f"    warehouse_menu_tiers: [{', '.join(m.get('warehouse_menu_tiers') or [])}]")
        lines.append(f"    build_roles: [{', '.join(m['build_roles'])}]")
        lines.append(f"    license_keys: [{', '.join(m['license_keys'])}]")
        lines.append(f"    source_builds: [{', '.join(m['source_builds'])}]")
    return "\n".join(lines) + "\n"


def main() -> None:
    text = read_md()
    payload = parse_matrix(text)
    ANALYSIS_OUT.parent.mkdir(parents=True, exist_ok=True)
    FRONTEND_OUT.parent.mkdir(parents=True, exist_ok=True)
    YAML_OUT.parent.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    ANALYSIS_OUT.write_text(json_text + "\n", encoding="utf-8")
    FRONTEND_OUT.write_text(json_text + "\n", encoding="utf-8")
    YAML_OUT.write_text(render_yaml(payload), encoding="utf-8")
    print(f"wrote {ANALYSIS_OUT.relative_to(ROOT)}  ({len(payload['menus'])} menus)")
    print(f"wrote {FRONTEND_OUT.relative_to(ROOT)}")
    print(f"wrote {YAML_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
