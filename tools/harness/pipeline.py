"""
4계층 하네스 통합 파이프라인

Capture → Test → Compare → Route 파이프라인을 통합 실행한다.

실행 순서:
1. Capture: 캡처된 쿼리/이벤트 데이터 로드
2. Test: Characterization Test + Eval Case 실행
3. Compare: 신/구 결과 비교 (Comparison Harness)
4. Route: 비교 결과 기반 라우팅 결정 (Routing Harness)
5. Report: 대시보드용 결과 리포트 생성

사용법:
  python pipeline.py --eval-dir <eval_cases_dir> --api-url <api_base_url> --output <report_dir>
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path


def load_json(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def step_capture(config: dict) -> dict:
    """Step 1: 캡처 데이터 확인"""
    capture_dir = config.get("capture_dir", "")
    captured_files = list(Path(capture_dir).glob("*.json")) if capture_dir and os.path.exists(capture_dir) else []

    return {
        "step": "capture",
        "status": "ready" if captured_files else "no_data",
        "files": [str(f) for f in captured_files],
        "total_files": len(captured_files),
    }


def step_test(config: dict) -> dict:
    """Step 2: 테스트 실행 결과 확인"""
    eval_dir = config.get("eval_dir", "")
    eval_files = list(Path(eval_dir).glob("*.json")) if eval_dir and os.path.exists(eval_dir) else []

    total_cases = 0
    for f in eval_files:
        if f.name.startswith("_"):
            continue
        data = load_json(str(f))
        if isinstance(data, list):
            total_cases += len(data)

    return {
        "step": "test",
        "status": "ready" if eval_files else "no_cases",
        "eval_files": len(eval_files),
        "total_cases": total_cases,
    }


def step_compare(config: dict) -> dict:
    """Step 3: 비교 결과 확인"""
    comparison_dir = config.get("comparison_dir", "")
    if not comparison_dir or not os.path.exists(comparison_dir):
        return {"step": "compare", "status": "not_configured"}

    result_files = list(Path(comparison_dir).glob("*.jsonl"))
    total_comparisons = 0
    total_matches = 0
    total_mismatches = 0

    for f in result_files:
        with open(f, "r") as fh:
            for line in fh:
                if line.strip():
                    result = json.loads(line)
                    total_comparisons += 1
                    if result.get("match"):
                        total_matches += 1
                    else:
                        total_mismatches += 1

    match_rate = (total_matches / max(total_comparisons, 1)) * 100

    return {
        "step": "compare",
        "status": "active" if result_files else "no_data",
        "total_comparisons": total_comparisons,
        "matches": total_matches,
        "mismatches": total_mismatches,
        "match_rate": f"{match_rate:.1f}%",
    }


def step_route(config: dict) -> dict:
    """Step 4: 라우팅 상태 확인"""
    routing_config_path = config.get("routing_config", "")
    if not routing_config_path or not os.path.exists(routing_config_path):
        return {"step": "route", "status": "not_configured"}

    routing_config = load_json(routing_config_path)
    return {
        "step": "route",
        "status": "active",
        "mode": routing_config.get("mode", "legacy_only"),
        "new_percent": routing_config.get("global_new_percent", 0),
        "mirror_mode": routing_config.get("mirror_mode", False),
    }


def generate_dashboard_data(pipeline_result: dict, output_path: str):
    """대시보드 JSON 데이터를 생성한다."""
    dashboard_data = {
        "pipeline_status": "healthy",
        "last_run": datetime.now().isoformat(),
        "steps": pipeline_result["steps"],
        "summary": {
            "capture_ready": pipeline_result["steps"]["capture"]["status"] == "ready",
            "test_cases": pipeline_result["steps"]["test"].get("total_cases", 0),
            "match_rate": pipeline_result["steps"]["compare"].get("match_rate", "N/A"),
            "routing_mode": pipeline_result["steps"]["route"].get("mode", "unknown"),
            "routing_percent": pipeline_result["steps"]["route"].get("new_percent", 0),
        },
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)


def run_pipeline(config: dict) -> dict:
    """전체 파이프라인을 실행한다."""
    print("=" * 60)
    print("  Harness Pipeline: Capture → Test → Compare → Route")
    print("=" * 60)

    result = {
        "run_at": datetime.now().isoformat(),
        "steps": {},
    }

    for step_name, step_fn in [
        ("capture", step_capture),
        ("test", step_test),
        ("compare", step_compare),
        ("route", step_route),
    ]:
        print(f"\n  [{step_name.upper()}]")
        step_result = step_fn(config)
        result["steps"][step_name] = step_result
        for k, v in step_result.items():
            if k != "step":
                print(f"    {k}: {v}")

    compare_status = result["steps"]["compare"]
    if compare_status.get("mismatches", 0) == 0 and compare_status.get("total_comparisons", 0) > 0:
        result["go_no_go"] = "GO"
        print("\n  [GO/NO-GO] ✓ GO - 비교 불일치 0건")
    elif compare_status.get("total_comparisons", 0) == 0:
        result["go_no_go"] = "PENDING"
        print("\n  [GO/NO-GO] ⏳ PENDING - 비교 데이터 없음")
    else:
        result["go_no_go"] = "NO-GO"
        print(f"\n  [GO/NO-GO] ✗ NO-GO - 불일치 {compare_status.get('mismatches', 0)}건 존재")

    return result


def main():
    parser = argparse.ArgumentParser(description="4계층 하네스 통합 파이프라인")
    parser.add_argument("--capture-dir", default="")
    parser.add_argument("--eval-dir", default="")
    parser.add_argument("--comparison-dir", default="")
    parser.add_argument("--routing-config", default="")
    parser.add_argument("--output", default="pipeline_report.json")
    parser.add_argument("--dashboard-output", default="")
    args = parser.parse_args()

    config = {
        "capture_dir": args.capture_dir,
        "eval_dir": args.eval_dir,
        "comparison_dir": args.comparison_dir,
        "routing_config": args.routing_config,
    }

    result = run_pipeline(config)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n  Pipeline report: {args.output}")

    if args.dashboard_output:
        generate_dashboard_data(result, args.dashboard_output)
        print(f"  Dashboard data: {args.dashboard_output}")


if __name__ == "__main__":
    main()
