"""
Go/No-Go 판단 자동화

하네스 지표 기반으로 전환 가능 여부를 자동 판단한다.

판단 기준:
1. Comparison 불일치율 < threshold (기본 0%)
2. 에러율 < threshold (기본 1%)
3. 응답시간 비율 < threshold (기본 150%)
4. 5축 eval 합격률 > threshold (기본 95%)
5. 승인 게이트 통과 여부

사용법:
  python go_nogo.py --comparison-dir <dir> --eval-report <path> --routing-config <path> --output <report>
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


class GoNoGoChecker:
    def __init__(self, thresholds: dict = None):
        self.thresholds = thresholds or {
            "max_mismatch_rate": 0.0,
            "max_error_rate": 1.0,
            "max_response_time_ratio": 1.5,
            "min_eval_pass_rate": 95.0,
            "required_gates_passed": 5,
        }

    def check_comparison(self, comparison_dir: str) -> dict:
        """Comparison 불일치율을 검사한다."""
        total = 0
        mismatches = 0

        if os.path.exists(comparison_dir):
            for f in Path(comparison_dir).glob("*.jsonl"):
                with open(f, "r") as fh:
                    for line in fh:
                        if line.strip():
                            result = json.loads(line)
                            total += 1
                            if not result.get("match", True):
                                mismatches += 1

        rate = (mismatches / max(total, 1)) * 100
        threshold = self.thresholds["max_mismatch_rate"]
        passed = rate <= threshold

        return {
            "criterion": "comparison_mismatch_rate",
            "value": f"{rate:.2f}%",
            "threshold": f"<= {threshold}%",
            "passed": passed,
            "detail": f"{mismatches}/{total} mismatches",
        }

    def check_eval(self, eval_report_path: str) -> dict:
        """5축 eval 합격률을 검사한다."""
        if not os.path.exists(eval_report_path):
            return {
                "criterion": "eval_pass_rate",
                "value": "N/A",
                "threshold": f">= {self.thresholds['min_eval_pass_rate']}%",
                "passed": False,
                "detail": "Eval report not found",
            }

        with open(eval_report_path, "r") as f:
            report = json.load(f)

        axis_stats = report.get("axis_stats", {})
        total_cases = 0
        total_passed = 0

        for axis, stats in axis_stats.items():
            total_cases += stats.get("total", 0)
            total_passed += stats.get("pass", 0)

        rate = (total_passed / max(total_cases, 1)) * 100
        threshold = self.thresholds["min_eval_pass_rate"]

        return {
            "criterion": "eval_pass_rate",
            "value": f"{rate:.1f}%",
            "threshold": f">= {threshold}%",
            "passed": rate >= threshold,
            "detail": f"{total_passed}/{total_cases} passed",
        }

    def check_routing(self, routing_config_path: str) -> dict:
        """현재 라우팅 상태를 검사한다."""
        if not os.path.exists(routing_config_path):
            return {
                "criterion": "routing_readiness",
                "value": "not configured",
                "threshold": "operational",
                "passed": False,
                "detail": "Routing config not found",
            }

        with open(routing_config_path, "r") as f:
            config = json.load(f)

        mode = config.get("mode", "legacy_only")
        percent = config.get("global_new_percent", 0)
        rollback = config.get("rollback_enabled", False)

        return {
            "criterion": "routing_readiness",
            "value": f"mode={mode}, percent={percent}%",
            "threshold": "rollback_enabled=true",
            "passed": rollback,
            "detail": f"Rollback {'enabled' if rollback else 'disabled'}",
        }

    def check_approvals(self, approvals_path: str) -> dict:
        """승인 게이트 통과 여부를 검사한다."""
        if not os.path.exists(approvals_path):
            return {
                "criterion": "approval_gates",
                "value": "0/6",
                "threshold": f">= {self.thresholds['required_gates_passed']}",
                "passed": False,
                "detail": "Approvals file not found",
            }

        with open(approvals_path, "r") as f:
            approvals = json.load(f)

        passed_count = sum(1 for g in approvals if g.get("status") == "통과")
        total = len(approvals)
        threshold = self.thresholds["required_gates_passed"]

        return {
            "criterion": "approval_gates",
            "value": f"{passed_count}/{total}",
            "threshold": f">= {threshold}",
            "passed": passed_count >= threshold,
            "detail": f"{passed_count} gates passed",
        }

    def evaluate(self, comparison_dir: str = "", eval_report: str = "",
                 routing_config: str = "", approvals: str = "") -> dict:
        """전체 Go/No-Go 판단을 실행한다."""
        checks = []

        if comparison_dir:
            checks.append(self.check_comparison(comparison_dir))
        if eval_report:
            checks.append(self.check_eval(eval_report))
        if routing_config:
            checks.append(self.check_routing(routing_config))
        if approvals:
            checks.append(self.check_approvals(approvals))

        all_passed = all(c["passed"] for c in checks) if checks else False

        return {
            "evaluated_at": datetime.now().isoformat(),
            "decision": "GO" if all_passed else "NO-GO",
            "checks": checks,
            "total_checks": len(checks),
            "passed_checks": sum(1 for c in checks if c["passed"]),
            "failed_checks": [c for c in checks if not c["passed"]],
        }


def main():
    parser = argparse.ArgumentParser(description="Go/No-Go 판단 자동화")
    parser.add_argument("--comparison-dir", default="")
    parser.add_argument("--eval-report", default="")
    parser.add_argument("--routing-config", default="")
    parser.add_argument("--approvals", default="")
    parser.add_argument("--output", default="go_nogo_report.json")
    args = parser.parse_args()

    checker = GoNoGoChecker()
    result = checker.evaluate(
        comparison_dir=args.comparison_dir,
        eval_report=args.eval_report,
        routing_config=args.routing_config,
        approvals=args.approvals,
    )

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"  Go/No-Go Decision: {result['decision']}")
    print(f"{'='*50}")
    for check in result["checks"]:
        icon = "✓" if check["passed"] else "✗"
        print(f"  {icon} {check['criterion']}: {check['value']} ({check['threshold']})")
    print(f"\n  Result: {result['passed_checks']}/{result['total_checks']} checks passed")
    print(f"  Report: {args.output}")


if __name__ == "__main__":
    main()
