"""
Routing Harness (Strangler Fig 프록시)

요청을 레거시 시스템(델파이)과 신규 시스템(웹 API)으로 분기한다.
Feature Toggle / 퍼센트 기반 / 사용자 그룹 기반 라우팅을 지원하며,
즉시 롤백 메커니즘을 제공한다.

핵심 기능:
1. 라우팅 결정 (레거시 vs 신규)
2. 라우팅 결정 로그 기록
3. Feature Toggle 연동
4. 퍼센트 기반 점진적 전환
5. 즉시 롤백

사용법 (FastAPI 미들웨어로 실행):
  uvicorn routing_harness:app --port 8080

의존성:
  pip install fastapi uvicorn httpx
"""

import json
import os
import time
import random
import hashlib
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger("routing_harness")

CONFIG_PATH = os.environ.get(
    "ROUTING_CONFIG",
    os.path.join(os.path.dirname(__file__), "routing_config.json"),
)


class RoutingConfig:
    """라우팅 설정 관리자"""

    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.config = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return self._default_config()

    def _default_config(self) -> dict:
        return {
            "mode": "legacy_only",
            "legacy_base_url": "http://localhost:8081",
            "new_base_url": "http://localhost:8082",
            "global_new_percent": 0,
            "feature_toggles": {},
            "user_groups": {
                "pilot": [],
                "beta": [],
            },
            "rollback_enabled": True,
            "mirror_mode": False,
        }

    def reload(self):
        self.config = self._load()

    def save(self):
        os.makedirs(os.path.dirname(self.config_path) or ".", exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    @property
    def mode(self) -> str:
        return self.config.get("mode", "legacy_only")

    @mode.setter
    def mode(self, value: str):
        self.config["mode"] = value
        self.save()

    @property
    def global_new_percent(self) -> int:
        return self.config.get("global_new_percent", 0)

    @global_new_percent.setter
    def global_new_percent(self, value: int):
        self.config["global_new_percent"] = max(0, min(100, value))
        self.save()

    def get_feature_toggle(self, feature: str) -> dict:
        return self.config.get("feature_toggles", {}).get(feature, {"enabled": False})

    def set_feature_toggle(self, feature: str, enabled: bool, percent: int = 100):
        if "feature_toggles" not in self.config:
            self.config["feature_toggles"] = {}
        self.config["feature_toggles"][feature] = {"enabled": enabled, "percent": percent}
        self.save()

    def is_pilot_user(self, user_id: str) -> bool:
        return user_id in self.config.get("user_groups", {}).get("pilot", [])


class RoutingDecisionLog:
    """라우팅 결정 로그"""

    def __init__(self, log_dir: str = None):
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), "routing_logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, decision: dict):
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(self.log_dir, f"routing_{date_str}.jsonl")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(decision, ensure_ascii=False) + "\n")


class RoutingHarness:
    """라우팅 하네스 코어"""

    def __init__(self, config: RoutingConfig = None):
        self.config = config or RoutingConfig()
        self.decision_log = RoutingDecisionLog()

    def decide(self, path: str, method: str, user_id: str = "", headers: dict = None) -> dict:
        """
        라우팅 결정을 내린다.
        Returns: {"target": "legacy"|"new"|"mirror", "reason": str}
        """
        mode = self.config.mode
        decision = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "method": method,
            "user_id": user_id,
            "target": "legacy",
            "reason": "",
        }

        if mode == "legacy_only":
            decision["target"] = "legacy"
            decision["reason"] = "mode=legacy_only"

        elif mode == "new_only":
            decision["target"] = "new"
            decision["reason"] = "mode=new_only"

        elif mode == "mirror":
            decision["target"] = "mirror"
            decision["reason"] = "mode=mirror (shadow comparison)"

        elif mode == "feature_toggle":
            feature_key = self._path_to_feature(path)
            toggle = self.config.get_feature_toggle(feature_key)
            if toggle.get("enabled", False):
                percent = toggle.get("percent", 100)
                if self._should_route_new(user_id, percent):
                    decision["target"] = "new"
                    decision["reason"] = f"feature_toggle={feature_key}, percent={percent}"
                else:
                    decision["target"] = "legacy"
                    decision["reason"] = f"feature_toggle={feature_key}, below percent={percent}"
            else:
                decision["target"] = "legacy"
                decision["reason"] = f"feature_toggle={feature_key}, disabled"

        elif mode == "percent":
            percent = self.config.global_new_percent
            if self.config.is_pilot_user(user_id):
                decision["target"] = "new"
                decision["reason"] = f"pilot_user={user_id}"
            elif self._should_route_new(user_id, percent):
                decision["target"] = "new"
                decision["reason"] = f"percent={percent}"
            else:
                decision["target"] = "legacy"
                decision["reason"] = f"below percent={percent}"

        self.decision_log.log(decision)
        return decision

    def rollback(self):
        """즉시 롤백: 모든 트래픽을 레거시로 전환"""
        self.config.mode = "legacy_only"
        self.config.global_new_percent = 0
        self.decision_log.log({
            "timestamp": datetime.now().isoformat(),
            "event": "ROLLBACK",
            "reason": "Emergency rollback triggered",
        })
        logger.warning("ROLLBACK: All traffic routed to legacy")

    def set_percent(self, percent: int):
        """점진적 전환 비율 설정"""
        self.config.mode = "percent"
        self.config.global_new_percent = percent
        self.decision_log.log({
            "timestamp": datetime.now().isoformat(),
            "event": "PERCENT_CHANGE",
            "new_percent": percent,
        })

    def _path_to_feature(self, path: str) -> str:
        parts = path.strip("/").split("/")
        return ".".join(parts[:3]) if len(parts) >= 3 else ".".join(parts)

    def _should_route_new(self, user_id: str, percent: int) -> bool:
        if percent >= 100:
            return True
        if percent <= 0:
            return False
        if user_id:
            hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100
            return hash_val < percent
        return random.randint(0, 99) < percent


def create_default_config():
    """기본 라우팅 설정 파일을 생성한다."""
    config = RoutingConfig()
    config.save()
    print(f"Default routing config created: {config.config_path}")
    return config


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        create_default_config()
    else:
        config = create_default_config()
        harness = RoutingHarness(config)

        print("\nRouting Harness Test:")
        for mode in ["legacy_only", "percent", "mirror", "new_only"]:
            config.mode = mode
            if mode == "percent":
                config.global_new_percent = 50
            decision = harness.decide("/api/inbound/create", "POST", "user001")
            print(f"  mode={mode}: target={decision['target']}, reason={decision['reason']}")

        print("\nRollback test:")
        config.mode = "percent"
        config.global_new_percent = 50
        harness.rollback()
        decision = harness.decide("/api/inbound/create", "POST", "user001")
        print(f"  After rollback: target={decision['target']}")
