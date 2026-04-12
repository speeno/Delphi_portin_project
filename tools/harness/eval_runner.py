"""
5축 평가 실행기 (L7 Evaluation Runner)

Eval Case JSON 파일들을 로드하여 자동 평가를 실행하고,
5축(Outcome/Process/UI/Efficiency/Variant) 결과를 집계한다.

평가 모드:
1. DB delta 비교 (Golden Master 기반)
2. API 응답 비교 (HTTP 호출)
3. Validation 메시지 확인
4. 응답 시간 측정

사용법:
  python eval_runner.py <eval_cases_dir> <api_base_url> --output <report_path>

의존성:
  pip install httpx (API 호출 시)
"""

import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path


def load_eval_cases(eval_dir: str) -> list[dict]:
    """Eval Case JSON 파일들을 로드한다."""
    all_cases = []
    for path in Path(eval_dir).glob("*.json"):
        if path.name.startswith("_"):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            all_cases.extend(data)
        elif isinstance(data, dict):
            all_cases.append(data)
    return all_cases


def run_outcome_eval(case: dict, api_base_url: str = None) -> dict:
    """Outcome 평가: DB delta 비교"""
    result = {
        "eval_id": case["eval_id"],
        "axis": "outcome",
        "status": "skip",
        "reason": "",
    }

    if not api_base_url:
        result["status"] = "skip"
        result["reason"] = "API base URL not configured"
        return result

    result["status"] = "pending"
    result["reason"] = "DB delta 비교 대기 (실제 API 호출 필요)"
    return result


def run_process_eval(case: dict) -> dict:
    """Process 평가: validation 수행 확인"""
    result = {
        "eval_id": case["eval_id"],
        "axis": "process",
        "status": "skip",
        "reason": "",
    }

    expected_messages = case.get("expected_messages", [])
    if expected_messages:
        result["status"] = "pending"
        result["reason"] = f"Validation 메시지 {len(expected_messages)}개 확인 대기"
    else:
        result["status"] = "pending"
        result["reason"] = "트랜잭션 경계 검증 대기"

    return result


def run_efficiency_eval(case: dict) -> dict:
    """Efficiency 평가: 응답 시간 / 쿼리 수 검증"""
    result = {
        "eval_id": case["eval_id"],
        "axis": "efficiency",
        "status": "skip",
        "reason": "",
    }

    max_ms = case.get("expected_max_response_ms", 1500)
    max_queries = case.get("expected_max_queries", 10)

    result["status"] = "pending"
    result["reason"] = f"응답시간 < {max_ms}ms, 쿼리 수 < {max_queries} 검증 대기"
    return result


def run_variant_eval(case: dict) -> dict:
    """Variant 평가: 고객사별 분기 테스트"""
    result = {
        "eval_id": case["eval_id"],
        "axis": "variant",
        "status": "skip",
        "reason": "",
    }

    variant = case.get("variant", "default")
    if variant != "default":
        result["status"] = "pending"
        result["reason"] = f"고객사 '{variant}' 분기 테스트 대기"
    else:
        result["status"] = "skip"
        result["reason"] = "기본 분기 (variant eval 대상 아님)"

    return result


def run_eval(cases: list[dict], api_base_url: str = None) -> dict:
    """전체 Eval Case를 실행한다."""
    results = []
    axis_stats = {
        "outcome": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "pending": 0},
        "process": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "pending": 0},
        "uiux": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "pending": 0},
        "efficiency": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "pending": 0},
        "variant": {"total": 0, "pass": 0, "fail": 0, "skip": 0, "pending": 0},
    }

    for case in cases:
        axis = case.get("eval_axis", "outcome")

        if axis == "outcome":
            result = run_outcome_eval(case, api_base_url)
        elif axis == "process":
            result = run_process_eval(case)
        elif axis == "efficiency":
            result = run_efficiency_eval(case)
        elif axis == "variant":
            result = run_variant_eval(case)
        else:
            result = {"eval_id": case["eval_id"], "axis": axis, "status": "skip", "reason": "Unknown axis"}

        results.append(result)

        if axis in axis_stats:
            axis_stats[axis]["total"] += 1
            axis_stats[axis][result["status"]] = axis_stats[axis].get(result["status"], 0) + 1

    for axis, stats in axis_stats.items():
        total = stats["total"]
        if total > 0:
            passed = stats.get("pass", 0)
            stats["pass_rate"] = f"{(passed / total) * 100:.1f}%"
        else:
            stats["pass_rate"] = "N/A"

    return {
        "run_at": datetime.now().isoformat(),
        "total_cases": len(cases),
        "axis_stats": axis_stats,
        "results": results,
    }


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <eval_cases_dir> [api_base_url] [--output report.json]")
        sys.exit(1)

    eval_dir = sys.argv[1]
    api_base_url = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None

    output_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]

    cases = load_eval_cases(eval_dir)
    if not cases:
        print(f"No eval cases found in {eval_dir}")
        sys.exit(0)

    print(f"Running {len(cases)} eval cases...")
    report = run_eval(cases, api_base_url)

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nReport: {output_path}")

    print(f"\n5-Axis Evaluation Summary:")
    for axis, stats in report["axis_stats"].items():
        if stats["total"] > 0:
            print(f"  {axis}: {stats['total']} cases, pass_rate={stats['pass_rate']}")


if __name__ == "__main__":
    main()
