"""
델파이 프로젝트 파일(.dpr) 파서

.dpr 파일에서 uses 절을 파싱하여 유닛 의존 관계를 추출한다.
프로젝트 구조와 유닛 간 관계 그래프의 기초 데이터를 생성한다.

사용법:
  python dpr_parser.py <source_dir> <output_path>
"""

import re
import json
import sys
import os
from pathlib import Path


def find_dpr_files(source_dir: str) -> list[str]:
    return sorted(str(p) for p in Path(source_dir).rglob("*.dpr"))


def parse_uses_clause(content: str) -> list[dict]:
    """uses 절에서 유닛 이름과 in 절(파일 경로)을 추출한다."""
    uses_pattern = re.compile(
        r'\buses\b(.*?);', re.DOTALL | re.IGNORECASE
    )
    units = []
    for match in uses_pattern.finditer(content):
        clause = match.group(1)
        unit_pattern = re.compile(
            r"(\w+)\s*(?:in\s*'([^']*)')?\s*(?:,|$)", re.IGNORECASE
        )
        for unit_match in unit_pattern.finditer(clause):
            name = unit_match.group(1)
            filepath = unit_match.group(2) or ""
            units.append({"name": name, "path": filepath})
    return units


def parse_dpr_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    program_match = re.search(r'\bprogram\s+(\w+)\s*;', content, re.IGNORECASE)
    program_name = program_match.group(1) if program_match else Path(filepath).stem

    uses = parse_uses_clause(content)

    return {
        "file": filepath,
        "program_name": program_name,
        "units": uses,
        "unit_count": len(uses),
        "file_size": os.path.getsize(filepath),
        "line_count": content.count("\n") + 1,
    }


def build_dependency_graph(dpr_results: list[dict]) -> dict:
    """프로젝트 파일들에서 유닛 의존 관계 그래프를 생성한다."""
    all_units = set()
    edges = []

    for dpr in dpr_results:
        prog = dpr["program_name"]
        all_units.add(prog)
        for unit in dpr["units"]:
            all_units.add(unit["name"])
            edges.append({"from": prog, "to": unit["name"]})

    return {
        "nodes": sorted(all_units),
        "edges": edges,
        "total_nodes": len(all_units),
        "total_edges": len(edges),
    }


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_path>")
        sys.exit(1)

    source_dir = sys.argv[1]
    output_path = sys.argv[2]

    dpr_files = find_dpr_files(source_dir)
    if not dpr_files:
        print(f"No .dpr files found in {source_dir}")
        sys.exit(0)

    results = [parse_dpr_file(f) for f in dpr_files]
    dep_graph = build_dependency_graph(results)

    output = {
        "source_dir": source_dir,
        "dpr_files": results,
        "dependency_graph": dep_graph,
        "summary": {
            "total_dpr_files": len(results),
            "total_units_referenced": dep_graph["total_nodes"],
        },
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Parsed {len(results)} .dpr files -> {output_path}")
    print(f"  Total units referenced: {dep_graph['total_nodes']}")


if __name__ == "__main__":
    main()
