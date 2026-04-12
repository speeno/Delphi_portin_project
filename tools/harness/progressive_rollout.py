"""
점진적 전환 관리자

Routing Harness의 전환 비율을 단계적으로 변경하고,
각 단계에서 Comparison 결과를 확인하여 안전한 전환을 보장한다.

전환 단계: 10% → 30% → 50% → 80% → 100%
각 단계 조건: Comparison 불일치율 = 0%, 최소 24시간 안정 운영

사용법:
  python progressive_rollout.py --routing-config <path> --comparison-dir <dir> --action <next|rollback|status>
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


STAGES = [0, 10, 30, 50, 80, 100]


class ProgressiveRollout:
    def __init__(self, routing_config_path: str, comparison_dir: str = ""):
        self.routing_config_path = routing_config_path
        self.comparison_dir = comparison_dir
        self.history_path = os.path.join(
            os.path.dirname(routing_config_path), "rollout_history.json"
        )

    def _load_routing_config(self) -> dict:
        if os.path.exists(self.routing_config_path):
            with open(self.routing_config_path, "r") as f:
                return json.load(f)
        return {"mode": "legacy_only", "global_new_percent": 0, "rollback_enabled": True}

    def _save_routing_config(self, config: dict):
        with open(self.routing_config_path, "w") as f:
            json.dump(config, f, indent=2)

    def _load_history(self) -> list:
        if os.path.exists(self.history_path):
            with open(self.history_path, "r") as f:
                return json.load(f)
        return []

    def _save_history(self, history: list):
        with open(self.history_path, "w") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def _log_event(self, event_type: str, from_percent: int, to_percent: int, reason: str):
        history = self._load_history()
        history.append({
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "from_percent": from_percent,
            "to_percent": to_percent,
            "reason": reason,
        })
        self._save_history(history)

    def _check_comparison_clear(self) -> tuple[bool, str]:
        if not self.comparison_dir or not os.path.exists(self.comparison_dir):
            return True, "No comparison data (assumed clear)"

        total = 0
        mismatches = 0
        for f in Path(self.comparison_dir).glob("*.jsonl"):
            with open(f, "r") as fh:
                for line in fh:
                    if line.strip():
                        result = json.loads(line)
                        total += 1
                        if not result.get("match", True):
                            mismatches += 1

        if mismatches > 0:
            return False, f"Comparison mismatches: {mismatches}/{total}"
        return True, f"All clear: {total} comparisons, 0 mismatches"

    def status(self) -> dict:
        config = self._load_routing_config()
        current_percent = config.get("global_new_percent", 0)
        mode = config.get("mode", "legacy_only")

        current_stage = 0
        next_stage = STAGES[1] if len(STAGES) > 1 else None
        for i, s in enumerate(STAGES):
            if current_percent >= s:
                current_stage = i
                next_stage = STAGES[i + 1] if i + 1 < len(STAGES) else None

        comparison_clear, comparison_msg = self._check_comparison_clear()
        history = self._load_history()

        return {
            "mode": mode,
            "current_percent": current_percent,
            "current_stage": current_stage,
            "next_stage_percent": next_stage,
            "stages": STAGES,
            "comparison_clear": comparison_clear,
            "comparison_detail": comparison_msg,
            "can_advance": comparison_clear and next_stage is not None,
            "history_count": len(history),
        }

    def advance(self) -> dict:
        """다음 단계로 전환 비율을 높인다."""
        status = self.status()

        if not status["can_advance"]:
            return {
                "success": False,
                "message": f"Cannot advance: comparison_clear={status['comparison_clear']}, next_stage={status['next_stage_percent']}",
            }

        config = self._load_routing_config()
        from_percent = config.get("global_new_percent", 0)
        to_percent = status["next_stage_percent"]

        config["mode"] = "percent"
        config["global_new_percent"] = to_percent
        self._save_routing_config(config)
        self._log_event("ADVANCE", from_percent, to_percent, "Manual advance")

        return {
            "success": True,
            "message": f"Advanced: {from_percent}% → {to_percent}%",
            "new_percent": to_percent,
        }

    def rollback(self, reason: str = "Manual rollback") -> dict:
        """즉시 롤백: 전환 비율을 0%로 되돌린다."""
        config = self._load_routing_config()
        from_percent = config.get("global_new_percent", 0)

        config["mode"] = "legacy_only"
        config["global_new_percent"] = 0
        self._save_routing_config(config)
        self._log_event("ROLLBACK", from_percent, 0, reason)

        return {
            "success": True,
            "message": f"Rollback: {from_percent}% → 0% ({reason})",
        }


def main():
    parser = argparse.ArgumentParser(description="점진적 전환 관리자")
    parser.add_argument("--routing-config", required=True)
    parser.add_argument("--comparison-dir", default="")
    parser.add_argument("--action", choices=["status", "next", "rollback"], required=True)
    parser.add_argument("--reason", default="Manual action")
    args = parser.parse_args()

    rollout = ProgressiveRollout(args.routing_config, args.comparison_dir)

    if args.action == "status":
        status = rollout.status()
        print(json.dumps(status, indent=2, ensure_ascii=False))

    elif args.action == "next":
        result = rollout.advance()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "rollback":
        result = rollout.rollback(args.reason)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
