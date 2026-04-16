"""
델파이 폼 정의 파일(.dfm) 파서

.dfm 파일에서 다음을 추출한다:
- 폼 클래스 및 컴포넌트 트리
- 이벤트 바인딩 (OnClick, OnChange 등)
- 컴포넌트 유형별 분류 (TButton, TDBGrid, TEdit 등)
- 이벤트 핸들러와 .pas 프로시저 매핑

사용법:
  python dfm_parser.py <source_dir> <output_dir>
"""

import re
import json
import sys
import os
from pathlib import Path
from typing import Any

from delphi_source_encoding import read_delphi_source

from delphi_string_normalize import normalize_delphi_display_string
from dfm_grid_columns import extract_grid_columns
from dfm_layout_ir import enrich_layout_document
from dfm_merge_blocks import merge_property_blocks

# 레이아웃 JSON/HTML용으로보낼 속성(좌표·표시·폰트 관련 위주)
LAYOUT_EXPORT_KEYS = frozenset({
    "Left", "Top", "Width", "Height", "Caption", "Text", "Hint", "TabOrder",
    "Visible", "Enabled", "Align", "Anchors", "BorderStyle", "ClientWidth", "ClientHeight",
    "Color", "Constraints", "Margins", "AlignWithMargins", "WordWrap", "ReadOnly",
    "PixelsPerInch", "NumGlyphs",
})


def find_dfm_files(source_dir: str) -> list[str]:
    """소문자·대문자 확장자 모두 수집(중복 경로 제거)."""
    root = Path(source_dir)
    paths: set[Path] = set()
    for pat in ("*.dfm", "*.DFM"):
        paths.update(root.rglob(pat))
    return sorted(str(p) for p in paths)


def is_binary_dfm_text(content: str) -> bool:
    """텍스트 스트림 기준 이진 DFM(TPF0 헤더) 여부."""
    head = content[:64].lstrip("\ufeff\r\n \t")
    return head.startswith("TPF0")


def parse_component(lines: list[str], index: int, depth: int = 0) -> tuple[dict, int]:
    """재귀적으로 컴포넌트 트리를 파싱한다."""
    first_line = lines[index].strip()

    obj_match = re.match(r'(?:object|inherited)\s+(\w+)\s*:\s*(\w+)', first_line)
    if not obj_match:
        return None, index + 1

    comp = {
        "name": obj_match.group(1),
        "type": obj_match.group(2),
        "depth": depth,
        "properties": {},
        "events": {},
        "children": [],
    }

    i = index + 1
    while i < len(lines):
        line = lines[i].strip()

        if line == "end":
            return comp, i + 1

        child_match = re.match(r'(?:object|inherited)\s+(\w+)\s*:\s*(\w+)', line)
        if child_match:
            child, i = parse_component(lines, i, depth + 1)
            if child:
                comp["children"].append(child)
            continue

        prop_match = re.match(r"([\w.]+)\s*=\s*(.*)", line, re.DOTALL)
        if prop_match:
            prop_name = prop_match.group(1)
            prop_value = prop_match.group(2).strip()

            if prop_name.startswith("On"):
                comp["events"][prop_name] = prop_value
            else:
                comp["properties"][prop_name] = prop_value

        i += 1

    return comp, i


def parse_dfm_file(filepath: str) -> dict:
    content = read_delphi_source(filepath)

    if is_binary_dfm_text(content):
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "binary_dfm_unsupported",
            "component_count": 0,
            "event_count": 0,
            "components": [],
            "events": [],
            "component_summary": {},
            "parse_error": "binary TPF0 DFM — 텍스트 변환 후 파싱하세요",
        }

    lines = merge_property_blocks(content.splitlines())
    root = _parse_first_root(lines)

    if not root:
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "unknown",
            "component_count": 0,
            "event_count": 0,
            "components": [],
            "events": [],
            "component_summary": {},
        }

    all_components = []
    all_events = []
    type_counts: dict[str, int] = {}

    def collect(comp: dict):
        comp_type = comp["type"]
        type_counts[comp_type] = type_counts.get(comp_type, 0) + 1

        all_components.append({
            "name": comp["name"],
            "type": comp_type,
            "depth": comp["depth"],
            "event_count": len(comp["events"]),
        })

        for event_name, handler_name in comp["events"].items():
            all_events.append({
                "component": comp["name"],
                "component_type": comp_type,
                "event": event_name,
                "handler": handler_name,
            })

        for child in comp.get("children", []):
            collect(child)

    collect(root)

    return {
        "file": filepath,
        "form_name": root["name"],
        "form_class": root["type"],
        "component_count": len(all_components),
        "event_count": len(all_events),
        "components": all_components,
        "events": all_events,
        "component_summary": type_counts,
    }


def build_event_flow(dfm_results: list[dict]) -> list[dict]:
    """전체 폼의 이벤트 바인딩을 이벤트 흐름 맵으로 변환한다."""
    flows = []
    for dfm in dfm_results:
        for event in dfm["events"]:
            flows.append({
                "form": dfm["form_name"],
                "form_class": dfm["form_class"],
                "component": event["component"],
                "component_type": event["component_type"],
                "event": event["event"],
                "handler": event["handler"],
                "file": dfm["file"],
            })
    return flows


def filter_layout_properties(properties: dict) -> dict:
    """레이아웃·표시에 쓰이는 속성만 남긴다(Font.* / Items.* 는 줄·블록 단위로 수집)."""
    out: dict[str, Any] = {}
    for k, v in properties.items():
        if k in LAYOUT_EXPORT_KEYS:
            if k in ("Caption", "Text", "Hint") and isinstance(v, str):
                out[k] = normalize_delphi_display_string(v)
            else:
                out[k] = v
        elif k.startswith("Font."):
            out[k] = v
        elif k.startswith("Items"):
            out[k] = v
        elif k.endswith(".Data"):
            out[k] = v
    return out


def layout_tree(comp: dict) -> dict:
    """파싱된 컴포넌트 트리를 레이아웃 JSON용 노드로 변환한다."""
    props = comp.get("properties", {})
    lay = filter_layout_properties(props)
    cols_blob = props.get("Columns")
    if isinstance(cols_blob, str) and re.search(r"(?i)\bitem\b", cols_blob):
        gc = extract_grid_columns(cols_blob)
        if gc:
            lay["grid_columns"] = gc
    return {
        "name": comp["name"],
        "type": comp["type"],
        "depth": comp["depth"],
        "layout": lay,
        "events": dict(comp.get("events", {})),
        "children": [layout_tree(c) for c in comp.get("children", [])],
    }


def _parse_first_root(lines: list[str]) -> dict | None:
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i].strip()
        if re.match(r"(?:object|inherited)\s+\w+\s*:\s*\w+", line):
            root, _ = parse_component(lines, i)
            return root
        i += 1
    return None


def parse_dfm_component_tree(filepath: str) -> dict | None:
    """
    레이아웃 필터 없이 폼 루트 컴포넌트 dict 전체를 반환한다(감사·도구용).
    이진 DFM이거나 루트가 없으면 None.
    """
    content = read_delphi_source(filepath)
    if is_binary_dfm_text(content):
        return None
    lines = merge_property_blocks(content.splitlines())
    return _parse_first_root(lines)


def parse_dfm_layout(filepath: str) -> dict:
    """
    단일 .dfm에서 좌표·캡션 등 레이아웃용 트리를 만든다.
    (form_inventory에는 포함되지 않음 — dfm_layout_export 등에서 사용)
    """
    content = read_delphi_source(filepath)

    if is_binary_dfm_text(content):
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "binary_dfm_unsupported",
            "root": None,
            "parse_error": "binary TPF0 DFM — 텍스트 변환 후 파싱하세요",
        }

    lines = merge_property_blocks(content.splitlines())
    root = _parse_first_root(lines)

    if not root:
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "unknown",
            "root": None,
        }

    doc = {
        "file": filepath,
        "form_name": root["name"],
        "form_class": root["type"],
        "root": layout_tree(root),
    }
    enrich_layout_document(doc)
    return doc


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    dfm_files = find_dfm_files(source_dir)
    if not dfm_files:
        # 산출물 경로를 항상 남겨 sprint1_report·catalog_builder와 일치시킨다(빈 트리도 동일 형식).
        print(f"WARNING: No .dfm files found under {source_dir}; writing empty #1/#2 outputs.")
        inv_path = os.path.join(output_dir, "form_inventory.json")
        flow_path = os.path.join(output_dir, "event_flow.json")
        summary_path = os.path.join(output_dir, "dfm_summary.json")
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        with open(flow_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        empty_summary = {
            "total_dfm_files": 0,
            "total_forms": 0,
            "total_components": 0,
            "total_events": 0,
            "form_classes": {},
        }
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(empty_summary, f, ensure_ascii=False, indent=2)
        print(f"  Form Inventory: {inv_path}")
        print(f"  Event Flow Map: {flow_path}")
        sys.exit(0)

    print(f"Parsing {len(dfm_files)} .dfm files...")
    results = []
    for f in dfm_files:
        try:
            results.append(parse_dfm_file(f))
        except Exception as e:
            print(f"  Error parsing {f}: {e}")

    form_inventory = []
    for r in results:
        form_inventory.append({
            "form_name": r["form_name"],
            "form_class": r["form_class"],
            "file": r["file"],
            "component_count": r["component_count"],
            "event_count": r["event_count"],
            "component_summary": r["component_summary"],
        })

    inv_path = os.path.join(output_dir, "form_inventory.json")
    with open(inv_path, "w", encoding="utf-8") as f:
        json.dump(form_inventory, f, ensure_ascii=False, indent=2)

    event_flow = build_event_flow(results)
    flow_path = os.path.join(output_dir, "event_flow.json")
    with open(flow_path, "w", encoding="utf-8") as f:
        json.dump(event_flow, f, ensure_ascii=False, indent=2)

    summary = {
        "total_dfm_files": len(results),
        "total_forms": len(form_inventory),
        "total_components": sum(r["component_count"] for r in results),
        "total_events": sum(r["event_count"] for r in results),
        "form_classes": {},
    }
    for r in results:
        fc = r["form_class"]
        summary["form_classes"][fc] = summary["form_classes"].get(fc, 0) + 1

    summary_path = os.path.join(output_dir, "dfm_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nDFM analysis complete:")
    print(f"  Forms: {summary['total_forms']}")
    print(f"  Components: {summary['total_components']}")
    print(f"  Event bindings: {summary['total_events']}")
    print(f"\nOutputs:")
    print(f"  Form Inventory: {inv_path}")
    print(f"  Event Flow Map: {flow_path}")


if __name__ == "__main__":
    main()
