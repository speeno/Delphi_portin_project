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


def find_dfm_files(source_dir: str) -> list[str]:
    return sorted(str(p) for p in Path(source_dir).rglob("*.dfm"))


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

        prop_match = re.match(r'(\w+)\s*=\s*(.*)', line)
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
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    lines = content.split("\n")

    root = None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'(?:object|inherited)\s+\w+\s*:\s*\w+', line):
            root, i = parse_component(lines, i)
            break
        i += 1

    if not root:
        return {
            "file": filepath,
            "form_name": Path(filepath).stem,
            "form_class": "unknown",
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


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    dfm_files = find_dfm_files(source_dir)
    if not dfm_files:
        print(f"No .dfm files found in {source_dir}")
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
