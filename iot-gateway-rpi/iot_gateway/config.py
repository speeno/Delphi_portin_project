from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _b(name: str, default: bool = False) -> bool:
    v = os.getenv(name, str(default)).strip().lower()
    return v in ("1", "true", "yes", "on")


def _i(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)).strip())
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    site_id: str
    local_host: str
    local_port: int
    local_user: str | None
    local_password: str | None
    uplink_host: str
    uplink_port: int
    uplink_user: str | None
    uplink_password: str | None
    uplink_tls: bool
    subscribe_pattern: str
    uplink_topic_prefix: str
    sqlite_path: str
    log_level: str


def load_settings() -> Settings:
    return Settings(
        site_id=os.getenv("GATEWAY_SITE_ID", "site-unknown").strip(),
        local_host=os.getenv("MQTT_LOCAL_HOST", "127.0.0.1").strip(),
        local_port=_i("MQTT_LOCAL_PORT", 1883),
        local_user=os.getenv("MQTT_LOCAL_USER") or None,
        local_password=os.getenv("MQTT_LOCAL_PASSWORD") or None,
        uplink_host=os.getenv("MQTT_UPLINK_HOST", "mqtt.example.com").strip(),
        uplink_port=_i("MQTT_UPLINK_PORT", 8883),
        uplink_user=os.getenv("MQTT_UPLINK_USER") or None,
        uplink_password=os.getenv("MQTT_UPLINK_PASSWORD") or None,
        uplink_tls=_b("MQTT_UPLINK_TLS", True),
        subscribe_pattern=os.getenv(
            "MQTT_SUBSCRIBE_PATTERN", "warehouse/+/+/+/+"
        ).strip(),
        uplink_topic_prefix=os.getenv("MQTT_UPLINK_TOPIC_PREFIX", "").strip().rstrip("/"),
        sqlite_path=os.getenv("GATEWAY_SQLITE_PATH", "/var/lib/iot-gateway/queue.db").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
    )
