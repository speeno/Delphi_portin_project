"""
Comparison Harness (신/구 동시 실행 비교)

동일한 요청을 레거시 시스템과 신규 시스템 양쪽에 전송하고,
응답과 DB 변경사항을 자동으로 비교한다.

동작 모드:
1. Shadow Mode: 레거시 응답을 반환하되, 신규 결과는 비교만
2. Active Mode: 신규 응답을 반환하되, 레거시와 비교 로그 기록

비교 대상:
- HTTP 응답 본문
- HTTP 상태 코드
- DB delta (테이블별 변경사항)
- 응답 시간

사용법:
  python comparison_harness.py --config comparison_config.json

의존성:
  pip install httpx
"""

import json
import os
import time
import hashlib
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger("comparison_harness")


class ComparisonResult:
    """비교 결과"""

    def __init__(self, request_id: str, path: str, method: str):
        self.request_id = request_id
        self.path = path
        self.method = method
        self.timestamp = datetime.now().isoformat()
        self.legacy_response = None
        self.new_response = None
        self.legacy_time_ms = 0
        self.new_time_ms = 0
        self.diffs = []
        self.match = True
        self.severity = "none"

    def add_diff(self, diff_type: str, field: str, legacy_val: Any, new_val: Any, severity: str = "warning"):
        self.diffs.append({
            "type": diff_type,
            "field": field,
            "legacy": str(legacy_val)[:500],
            "new": str(new_val)[:500],
            "severity": severity,
        })
        self.match = False
        if severity == "critical" or self.severity == "critical":
            self.severity = "critical"
        elif severity == "error" or self.severity == "error":
            self.severity = "error"
        else:
            self.severity = "warning"

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "path": self.path,
            "method": self.method,
            "timestamp": self.timestamp,
            "match": self.match,
            "severity": self.severity,
            "diff_count": len(self.diffs),
            "diffs": self.diffs,
            "legacy_time_ms": self.legacy_time_ms,
            "new_time_ms": self.new_time_ms,
            "time_diff_ms": self.new_time_ms - self.legacy_time_ms,
        }


class ComparisonHarness:
    """Comparison Harness 코어"""

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.results_dir = self.config.get("results_dir", "comparison_results")
        os.makedirs(self.results_dir, exist_ok=True)
        self.alert_threshold = self.config.get("alert_threshold", 0.01)

    def compare_responses(
        self,
        request_id: str,
        path: str,
        method: str,
        legacy_status: int,
        legacy_body: dict,
        legacy_time_ms: float,
        new_status: int,
        new_body: dict,
        new_time_ms: float,
    ) -> ComparisonResult:
        """HTTP 응답을 비교한다."""
        result = ComparisonResult(request_id, path, method)
        result.legacy_response = legacy_body
        result.new_response = new_body
        result.legacy_time_ms = legacy_time_ms
        result.new_time_ms = new_time_ms

        if legacy_status != new_status:
            result.add_diff("status_code", "http_status", legacy_status, new_status, "critical")

        self._compare_dict(result, legacy_body, new_body, "body")

        time_ratio = new_time_ms / max(legacy_time_ms, 1)
        if time_ratio > 1.5:
            result.add_diff("performance", "response_time", f"{legacy_time_ms}ms", f"{new_time_ms}ms", "warning")

        self._save_result(result)
        return result

    def compare_db_delta(
        self,
        request_id: str,
        path: str,
        legacy_delta: dict,
        new_delta: dict,
    ) -> ComparisonResult:
        """DB 변경사항을 비교한다."""
        result = ComparisonResult(request_id, path, "DB_DELTA")

        all_tables = set(list(legacy_delta.keys()) + list(new_delta.keys()))
        for table in all_tables:
            leg = legacy_delta.get(table, {})
            new = new_delta.get(table, {})

            if leg != new:
                result.add_diff("db_delta", f"table.{table}", leg, new, "critical")

        self._save_result(result)
        return result

    def _compare_dict(self, result: ComparisonResult, legacy: Any, new: Any, prefix: str):
        if type(legacy) != type(new):
            result.add_diff("type_mismatch", prefix, type(legacy).__name__, type(new).__name__, "error")
            return

        if isinstance(legacy, dict):
            all_keys = set(list(legacy.keys()) + list(new.keys()))
            for key in all_keys:
                if key not in legacy:
                    result.add_diff("missing_in_legacy", f"{prefix}.{key}", None, new[key], "warning")
                elif key not in new:
                    result.add_diff("missing_in_new", f"{prefix}.{key}", legacy[key], None, "error")
                else:
                    self._compare_dict(result, legacy[key], new[key], f"{prefix}.{key}")
        elif isinstance(legacy, list):
            if len(legacy) != len(new):
                result.add_diff("array_length", prefix, len(legacy), len(new), "warning")
            for i in range(min(len(legacy), len(new))):
                self._compare_dict(result, legacy[i], new[i], f"{prefix}[{i}]")
        else:
            if legacy != new:
                severity = "critical" if prefix.endswith((".id", ".total", ".amount", ".qty")) else "warning"
                result.add_diff("value_mismatch", prefix, legacy, new, severity)

    def _save_result(self, result: ComparisonResult):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.results_dir, f"comparison_{date_str}.jsonl")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")

    def generate_report(self, date_str: str = None) -> dict:
        """일자별 비교 결과 리포트를 생성한다."""
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        filepath = os.path.join(self.results_dir, f"comparison_{date_str}.jsonl")
        if not os.path.exists(filepath):
            return {"date": date_str, "total": 0, "matches": 0, "mismatches": 0}

        results = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line))

        total = len(results)
        matches = sum(1 for r in results if r.get("match", False))
        mismatches = total - matches

        severity_counts = {}
        diff_type_counts = {}
        for r in results:
            sev = r.get("severity", "none")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            for d in r.get("diffs", []):
                dt = d.get("type", "unknown")
                diff_type_counts[dt] = diff_type_counts.get(dt, 0) + 1

        return {
            "date": date_str,
            "total": total,
            "matches": matches,
            "mismatches": mismatches,
            "match_rate": f"{(matches / max(total, 1)) * 100:.1f}%",
            "severity_distribution": severity_counts,
            "diff_type_distribution": diff_type_counts,
        }


if __name__ == "__main__":
    harness = ComparisonHarness({"results_dir": "/tmp/comparison_test"})

    print("Comparison Harness Test:")

    result1 = harness.compare_responses(
        "req-001", "/api/inbound/create", "POST",
        200, {"success": True, "data": {"id": 1, "qty": 10}}, 150,
        200, {"success": True, "data": {"id": 1, "qty": 10}}, 180,
    )
    print(f"  Test 1 (identical): match={result1.match}")

    result2 = harness.compare_responses(
        "req-002", "/api/inbound/create", "POST",
        200, {"success": True, "data": {"id": 1, "qty": 10}}, 150,
        200, {"success": True, "data": {"id": 1, "qty": 11}}, 180,
    )
    print(f"  Test 2 (qty diff): match={result2.match}, diffs={len(result2.diffs)}")

    result3 = harness.compare_responses(
        "req-003", "/api/inbound/create", "POST",
        200, {"success": True}, 100,
        500, {"success": False, "error": "server error"}, 300,
    )
    print(f"  Test 3 (status diff): match={result3.match}, severity={result3.severity}")

    report = harness.generate_report()
    print(f"\n  Report: {report}")
