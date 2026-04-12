"""
전체 정적 분석 파이프라인 실행기

Sprint 1의 정적 분석(L2) 도구를 순차적으로 실행하여
10대 표준 산출물 #1~#6을 자동 생성한다.

실행 순서:
1. .dpr 파서 → 프로젝트 구조 + 유닛 의존 관계
2. .dfm 파서 → Form Inventory(#1) + Event Flow Map(#2)
3. .pas 파서 → SQL Catalog(#3) + Validation Rules(#5) + Customer Variants(#6)
4. Legacy Object Catalog 빌더 → 통합 카탈로그
5. 분석 요약 보고서 생성

사용법:
  python run_analysis.py <delphi_source_dir>
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
INVENTORY_DIR = os.path.join(PROJECT_ROOT, "inventory")
ANALYSIS_DIR = os.path.join(PROJECT_ROOT, "analysis")


def run_step(name: str, cmd: list[str]) -> bool:
    print(f"\n{'='*60}")
    print(f"  Step: {name}")
    print(f"  Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"  WARNING: {name} exited with code {result.returncode}")
        return False
    return True


def generate_summary_report():
    """분석 요약 보고서를 생성한다."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "deliverables": {},
    }

    deliverable_files = {
        "#1 Form Inventory": os.path.join(ANALYSIS_DIR, "form_inventory.json"),
        "#2 Event Flow Map": os.path.join(ANALYSIS_DIR, "event_flow.json"),
        "#3 SQL Catalog": os.path.join(ANALYSIS_DIR, "query_catalog.json"),
        "#4 DB Impact Matrix": os.path.join(ANALYSIS_DIR, "db_impact_matrix.json"),
        "#5 Validation Rules": os.path.join(ANALYSIS_DIR, "validation_rules.json"),
        "#6 Customer Variants": os.path.join(ANALYSIS_DIR, "customer_variants.json"),
    }

    for name, path in deliverable_files.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            count = len(data) if isinstance(data, list) else len(data.keys()) if isinstance(data, dict) else 0
            report["deliverables"][name] = {
                "status": "완료",
                "file": path,
                "item_count": count,
            }
        else:
            report["deliverables"][name] = {
                "status": "미생성",
                "file": path,
                "item_count": 0,
            }

    catalog_path = os.path.join(ANALYSIS_DIR, "legacy_object_catalog.json")
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
        report["legacy_object_catalog"] = {
            "total_objects": len(catalog),
            "risk_distribution": {},
        }
        for obj in catalog:
            r = obj.get("risk_level", "unknown")
            report["legacy_object_catalog"]["risk_distribution"][r] = (
                report["legacy_object_catalog"]["risk_distribution"].get(r, 0) + 1
            )

    summary_path = os.path.join(ANALYSIS_DIR, "sprint1_report.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nSprint 1 Report: {summary_path}")
    return report


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <delphi_source_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    if not os.path.isdir(source_dir):
        print(f"Error: {source_dir} is not a directory")
        sys.exit(1)

    os.makedirs(INVENTORY_DIR, exist_ok=True)
    os.makedirs(ANALYSIS_DIR, exist_ok=True)

    python = sys.executable
    parsers = os.path.join(TOOLS_DIR, "parsers")

    steps = [
        (
            "1. DPR 파서 (프로젝트 구조)",
            [python, os.path.join(parsers, "dpr_parser.py"), source_dir, os.path.join(INVENTORY_DIR, "dpr_files.json")],
        ),
        (
            "2. DFM 파서 (Form Inventory #1 + Event Flow Map #2)",
            [python, os.path.join(parsers, "dfm_parser.py"), source_dir, ANALYSIS_DIR],
        ),
        (
            "3. PAS 파서 (SQL Catalog #3 + Validation Rules #5 + Customer Variants #6)",
            [python, os.path.join(parsers, "pas_parser.py"), source_dir, ANALYSIS_DIR],
        ),
        (
            "4. Legacy Object Catalog 빌더",
            [python, os.path.join(TOOLS_DIR, "catalog_builder.py"), ANALYSIS_DIR, os.path.join(ANALYSIS_DIR, "legacy_object_catalog.json")],
        ),
    ]

    print(f"Starting analysis pipeline for: {source_dir}")
    print(f"Output directories:")
    print(f"  Inventory: {INVENTORY_DIR}")
    print(f"  Analysis: {ANALYSIS_DIR}")

    for name, cmd in steps:
        run_step(name, cmd)

    report = generate_summary_report()

    print(f"\n{'='*60}")
    print("  Analysis Pipeline Complete!")
    print(f"{'='*60}")
    print("\nDeliverables Status:")
    for name, info in report.get("deliverables", {}).items():
        print(f"  {name}: {info['status']} ({info['item_count']} items)")


if __name__ == "__main__":
    main()
