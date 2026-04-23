#!/usr/bin/env python3
"""Extract WeLove 출판(테이블구조).xls into a UTF-8 schema dictionary.

Parses the multi-block layout where each detail sheet hosts 1~3 tables
side-by-side. Each block starts with a header row containing
['필드명', '<table_name>', 'Size(전)', 'Size(후)', 'c/n'] and ends at the
first blank ``필드명`` cell after fields begin.

Outputs:
  analysis/welove_schema_dictionary.json  - machine readable dictionary
  docs/welove-publish-schema-dictionary.md - human readable summary

Source single source of truth: WeLove_FTP/Welove_인수인계/출판setting/weelove/
출판(테이블구조).xls (MAN-030, SCH-WELOVE-출판).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import xlrd

ROOT = Path(__file__).resolve().parent.parent
XLS = ROOT / "WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls"
JSON_OUT = ROOT / "analysis/welove_schema_dictionary.json"
MD_OUT = ROOT / "docs/welove-publish-schema-dictionary.md"


def _norm(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(value)
    return str(value).strip()


def parse_catalog(sheet) -> list[dict]:
    """Parse the index sheet '테이블' into a flat catalog."""
    catalog: list[dict] = []
    for row in range(sheet.nrows):
        cells = [_norm(sheet.cell_value(row, c)) for c in range(sheet.ncols)]
        # Layout: column 1 holds 'v' marker, column 2 holds code, column 3 caption
        # column 5 'v', column 6 code, column 7 caption (right block)
        for marker_col, code_col, name_col in ((1, 2, 3), (5, 6, 7)):
            if code_col >= len(cells):
                continue
            code = cells[code_col]
            if not code:
                continue
            entry = {
                "table": code,
                "caption_kor": cells[name_col] if name_col < len(cells) else "",
                "changed": cells[marker_col].lower() == "v",
            }
            catalog.append(entry)
    # de-dup keeping the first occurrence
    seen: set[str] = set()
    out = []
    for row in catalog:
        if row["table"] in seen:
            continue
        seen.add(row["table"])
        out.append(row)
    return out


HEADER_TOKENS = {"필드명", "Size(전)", "Size(후)", "c/n"}


def parse_table_sheet(sheet) -> list[dict]:
    """Detect 1~N blocks in a per-table sheet and return their fields."""
    blocks: list[dict] = []
    nrows, ncols = sheet.nrows, sheet.ncols
    if nrows < 3:
        return blocks

    # Header row is typically row 1; row 0 has the table name(s).
    header_row = None
    for r in range(min(5, nrows)):
        cells = [_norm(sheet.cell_value(r, c)) for c in range(ncols)]
        if "필드명" in cells:
            header_row = r
            break
    if header_row is None:
        return blocks

    # Identify block start columns by locating each "필드명" cell on header row.
    header_cells = [_norm(sheet.cell_value(header_row, c)) for c in range(ncols)]
    field_cols = [c for c, v in enumerate(header_cells) if v == "필드명"]

    # The table-name row sits in the row above the header.
    name_row = header_row - 1 if header_row > 0 else header_row

    for col in field_cols:
        # block columns: [필드명, table_or_desc, Size(전), Size(후), c/n]
        if col + 4 >= ncols:
            continue
        # Resolve table name: scan name_row from `col` rightward for a non-empty
        # string that isn't 'Size(...)' nor '필드명'.
        table_name = ""
        for c in range(col, min(col + 5, ncols)):
            cand = _norm(sheet.cell_value(name_row, c))
            if cand and cand not in HEADER_TOKENS:
                table_name = cand
                break
        if not table_name:
            continue

        fields = []
        for r in range(header_row + 1, nrows):
            field_name = _norm(sheet.cell_value(r, col))
            description = _norm(sheet.cell_value(r, col + 1)) if col + 1 < ncols else ""
            size_before = _norm(sheet.cell_value(r, col + 2)) if col + 2 < ncols else ""
            size_after = _norm(sheet.cell_value(r, col + 3)) if col + 3 < ncols else ""
            cn = _norm(sheet.cell_value(r, col + 4)) if col + 4 < ncols else ""

            if not field_name and not description and not size_before:
                # Stop on blank row but allow gaps between blocks
                if fields:
                    # peek one more row; if still empty, finalize block
                    # but keep scanning in case the layout has stray spacers
                    look_ahead_blank = True
                    for rr in range(r + 1, min(r + 3, nrows)):
                        peek = _norm(sheet.cell_value(rr, col))
                        if peek:
                            look_ahead_blank = False
                            break
                    if look_ahead_blank:
                        break
                    continue
                continue
            if field_name in {"필드명"}:
                continue
            fields.append(
                {
                    "field": field_name,
                    "description": description,
                    "size_before": size_before,
                    "size_after": size_after,
                    "char_or_num": cn,
                }
            )
        if fields:
            blocks.append({"table": table_name, "fields": fields})
    return blocks


def merge_blocks(blocks: Iterable[dict]) -> dict[str, list[dict]]:
    """Merge per-table fields across all sheets (a wide table can spill)."""
    merged: dict[str, list[dict]] = {}
    for block in blocks:
        merged.setdefault(block["table"], []).extend(block["fields"])
    return merged


def main() -> int:
    if not XLS.exists():
        print(f"ERROR: source not found: {XLS}")
        return 1

    wb = xlrd.open_workbook(str(XLS))
    catalog = parse_catalog(wb.sheet_by_name("테이블"))

    all_blocks: list[dict] = []
    for name in wb.sheet_names():
        if name == "테이블":
            continue
        sheet = wb.sheet_by_name(name)
        blocks = parse_table_sheet(sheet)
        all_blocks.extend(blocks)

    merged = merge_blocks(all_blocks)

    payload = {
        "source": "WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls",
        "manual_id": "MAN-030",
        "schema_id_prefix": "SCH-WELOVE-출판",
        "encoding": "UTF-8 (extracted from CP949 source via xlrd)",
        "catalog": catalog,
        "tables": [
            {
                "table": table,
                "field_count": len(fields),
                "fields": fields,
            }
            for table, fields in sorted(merged.items())
        ],
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    print(f"wrote {JSON_OUT.relative_to(ROOT)} ({len(merged)} tables, {len(catalog)} catalog rows)")

    # Markdown summary
    lines: list[str] = []
    lines.append("# 출판 테이블 구조 사전 (`SCH-WELOVE-출판-*`)\n")
    lines.append("| 항목 | 내용 |")
    lines.append("|------|------|")
    lines.append("| 작성일 | 2026-04-23 |")
    lines.append(f"| 원천 | [`WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls`](../{XLS.relative_to(ROOT)}) (`MAN-030`) |")
    lines.append("| 추출 도구 | [`tools/extract_welove_schema.py`](../tools/extract_welove_schema.py) |")
    lines.append(f"| JSON 정본 | [`analysis/welove_schema_dictionary.json`](../{JSON_OUT.relative_to(ROOT)}) |")
    lines.append("| 추적 ID | 테이블 단위 `SCH-WELOVE-출판-<TABLE>`, 필드 단위 `SCH-WELOVE-출판-<TABLE>.<field>` |\n")
    lines.append("본 사전은 [`docs/db-schema-porting-readiness.md`](db-schema-porting-readiness.md) 의 컬럼 차이 진단과 [`migration/contracts/*.yaml`](../migration/contracts) 의 `data_access` 단락에 합류한다. 표시 사이즈는 레거시 운영 DB 의 ALTER 흔적(전·후) 을 그대로 보존했다.\n")
    lines.append("## 1. 테이블 카탈로그 (인덱스 시트)\n")
    lines.append("`v` 표기는 원본 시트의 「변경된 테이블」 마킹을 그대로 옮긴 것.\n")
    lines.append("| 변경 | 테이블 | 한글 명칭 |")
    lines.append("|:-:|---|---|")
    for row in catalog:
        marker = "v" if row["changed"] else ""
        lines.append(f"| {marker} | `{row['table']}` | {row['caption_kor']} |")
    lines.append("")
    lines.append("## 2. 테이블별 필드 사전\n")
    lines.append("표기: **Size(전)** = 운영 중 ALTER 이전 값, **Size(후)** = 변경 후. `c/n` = 문자(c) / 숫자(n) 구분 — 빈 값은 사전 미명시.\n")
    for table in sorted(merged):
        fields = merged[table]
        cap = next((c["caption_kor"] for c in catalog if c["table"] == table), "")
        title = f"### `{table}`"
        if cap:
            title += f" — {cap}"
        lines.append(title + "\n")
        lines.append(f"필드 {len(fields)} 개. 추적 ID 접두사: `SCH-WELOVE-출판-{table}`.\n")
        lines.append("| 필드 | 설명 | Size(전) | Size(후) | c/n |")
        lines.append("|---|---|---|---|---|")
        for fld in fields:
            desc = fld["description"].replace("|", "\\|")
            lines.append(
                f"| `{fld['field']}` | {desc} | {fld['size_before']} | {fld['size_after']} | {fld['char_or_num']} |"
            )
        lines.append("")
    lines.append("## 3. 활용\n")
    lines.append("- **컬럼 어댑터** (`*_adapt.py`): 본 사전의 `Size(전)→Size(후)` 변경 흔적이 mysql3 호환 어댑터(DEC-033)의 1차 후보가 된다.\n- **CRUD 동등성**: `crud-backlog.md` 의 갭 표는 본 사전과 `analysis/db_impact_matrix.json` 의 교차 결과(`docs/welove-schema-reconciliation.md`)에 의존한다.\n- **계약 보강**: 마스터 계약(`migration/contracts/master_data.yaml`) 의 `endpoints[*].columns` 는 본 사전 행을 단일 원천으로 인용한다.\n")

    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {MD_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
