"""
하네스 → 운영 인프라 전환

Sprint 6에서 4계층 하네스를 운영 도구로 전환한다:
- Capture Harness → Audit Log
- Comparison Harness → CI 회귀 테스트
- Test Harness → CI/CD 자동 테스트
- Routing Harness → A/B 테스트 / Canary 인프라

사용법:
  python operationalize.py --action <audit|ci|canary|status> --config <path>
"""

import json
import os
import sys
import argparse
from datetime import datetime


class HarnessOperationalizer:
    """하네스를 운영 인프라로 전환한다."""

    def __init__(self, project_root: str = ""):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.status_path = os.path.join(self.project_root, "ops", "harness_ops_status.json")
        os.makedirs(os.path.dirname(self.status_path), exist_ok=True)

    def _load_status(self) -> dict:
        if os.path.exists(self.status_path):
            with open(self.status_path, "r") as f:
                return json.load(f)
        return {
            "capture_to_audit": {"status": "pending", "converted_at": None},
            "comparison_to_ci": {"status": "pending", "converted_at": None},
            "test_to_cicd": {"status": "pending", "converted_at": None},
            "routing_to_canary": {"status": "pending", "converted_at": None},
        }

    def _save_status(self, status: dict):
        with open(self.status_path, "w") as f:
            json.dump(status, f, indent=2, ensure_ascii=False)

    def convert_capture_to_audit(self) -> dict:
        """Capture Harness → Audit Log 전환"""
        audit_config = {
            "source": "capture_harness",
            "destination": "audit_log",
            "log_format": "jsonl",
            "retention_days": 365,
            "log_fields": [
                "timestamp", "user_id", "action", "table", "sql_type",
                "affected_rows", "request_id", "session_id",
            ],
            "storage": {
                "type": "file",
                "path": os.path.join(self.project_root, "ops", "audit_logs"),
                "rotation": "daily",
            },
        }

        config_path = os.path.join(self.project_root, "ops", "audit_config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(audit_config, f, indent=2)

        status = self._load_status()
        status["capture_to_audit"] = {"status": "converted", "converted_at": datetime.now().isoformat()}
        self._save_status(status)

        return {"success": True, "message": "Capture → Audit Log 전환 완료", "config": config_path}

    def convert_comparison_to_ci(self) -> dict:
        """Comparison Harness → CI 회귀 테스트 전환"""
        ci_config = {
            "source": "comparison_harness",
            "destination": "ci_regression_test",
            "schedule": "on_push",
            "test_suite": "regression",
            "comparison_mode": "snapshot",
            "snapshot_dir": os.path.join(self.project_root, "ops", "regression_snapshots"),
            "fail_on_mismatch": True,
            "report_format": "junit",
        }

        config_path = os.path.join(self.project_root, "ops", "ci_regression_config.json")
        with open(config_path, "w") as f:
            json.dump(ci_config, f, indent=2)

        status = self._load_status()
        status["comparison_to_ci"] = {"status": "converted", "converted_at": datetime.now().isoformat()}
        self._save_status(status)

        return {"success": True, "message": "Comparison → CI 회귀 테스트 전환 완료", "config": config_path}

    def convert_test_to_cicd(self) -> dict:
        """Test Harness → CI/CD 자동 테스트 전환"""
        cicd_config = {
            "source": "test_harness",
            "destination": "cicd_pipeline",
            "trigger": "on_push",
            "stages": [
                {"name": "unit_test", "command": "pytest tests/unit/"},
                {"name": "integration_test", "command": "pytest tests/integration/"},
                {"name": "eval_test", "command": "python tools/harness/eval_runner.py migration/test-cases/"},
                {"name": "golden_master_check", "command": "python tools/harness/golden_master.py compare --before snapshots/golden.json --after snapshots/current.json --output reports/golden_compare.json"},
            ],
            "fail_policy": "fail_fast",
        }

        config_path = os.path.join(self.project_root, "ops", "cicd_config.json")
        with open(config_path, "w") as f:
            json.dump(cicd_config, f, indent=2)

        status = self._load_status()
        status["test_to_cicd"] = {"status": "converted", "converted_at": datetime.now().isoformat()}
        self._save_status(status)

        return {"success": True, "message": "Test → CI/CD 자동 테스트 전환 완료", "config": config_path}

    def convert_routing_to_canary(self) -> dict:
        """Routing Harness → Canary 배포 인프라 전환"""
        canary_config = {
            "source": "routing_harness",
            "destination": "canary_deployment",
            "strategy": "canary",
            "canary_percent": 5,
            "promotion_criteria": {
                "min_duration_minutes": 30,
                "max_error_rate": 0.5,
                "max_latency_p99_ms": 2000,
            },
            "auto_rollback": True,
            "feature_flags_enabled": True,
        }

        config_path = os.path.join(self.project_root, "ops", "canary_config.json")
        with open(config_path, "w") as f:
            json.dump(canary_config, f, indent=2)

        status = self._load_status()
        status["routing_to_canary"] = {"status": "converted", "converted_at": datetime.now().isoformat()}
        self._save_status(status)

        return {"success": True, "message": "Routing → Canary 배포 전환 완료", "config": config_path}

    def status(self) -> dict:
        """전환 상태를 확인한다."""
        status = self._load_status()
        all_converted = all(v["status"] == "converted" for v in status.values())
        return {
            "overall": "완료" if all_converted else "진행중",
            "conversions": status,
        }


def main():
    parser = argparse.ArgumentParser(description="하네스 → 운영 인프라 전환")
    parser.add_argument("--action", choices=["audit", "ci", "cicd", "canary", "all", "status"], required=True)
    parser.add_argument("--project-root", default="")
    args = parser.parse_args()

    ops = HarnessOperationalizer(args.project_root)

    if args.action == "status":
        print(json.dumps(ops.status(), indent=2, ensure_ascii=False))
    elif args.action == "audit":
        print(json.dumps(ops.convert_capture_to_audit(), indent=2))
    elif args.action == "ci":
        print(json.dumps(ops.convert_comparison_to_ci(), indent=2))
    elif args.action == "cicd":
        print(json.dumps(ops.convert_test_to_cicd(), indent=2))
    elif args.action == "canary":
        print(json.dumps(ops.convert_routing_to_canary(), indent=2))
    elif args.action == "all":
        print("Converting all harnesses to operational infrastructure...")
        print(json.dumps(ops.convert_capture_to_audit(), indent=2))
        print(json.dumps(ops.convert_comparison_to_ci(), indent=2))
        print(json.dumps(ops.convert_test_to_cicd(), indent=2))
        print(json.dumps(ops.convert_routing_to_canary(), indent=2))
        print("\nFinal status:")
        print(json.dumps(ops.status(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
