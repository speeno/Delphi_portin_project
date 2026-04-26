from __future__ import annotations

import asyncio
import json
import logging
import os
import ssl
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

import aiomqtt

from iot_gateway.config import Settings

if TYPE_CHECKING:
    from iot_gateway.queue_sqlite import PublishQueue

LOG = logging.getLogger(__name__)


def _b_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes", "on")


def _rewrite_topic(settings: Settings, topic: str) -> str:
    if not settings.uplink_topic_prefix:
        return topic
    return f"{settings.uplink_topic_prefix}/{topic}"


def _envelope_if_needed(settings: Settings, topic: str, payload: bytes) -> bytes:
    """Optional JSON envelope with site_id for upstream consumers."""
    if not _b_env("GATEWAY_WRAP_JSON"):
        return payload
    try:
        body = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        body = {"raw_hex": payload.hex()}
    wrapped = {
        "site_id": settings.site_id,
        "gateway_ts": time.time(),
        "topic": topic,
        "payload": body,
    }
    return json.dumps(wrapped, ensure_ascii=False).encode("utf-8")


@dataclass
class OutboundMessage:
    topic: str
    payload: bytes
    qos: int
    retain: bool
    sqlite_row_id: int | None = None


def _qos_value(message: aiomqtt.Message) -> int:
    return int(message.qos)


def _local_client_kwargs(settings: Settings) -> dict:
    kw: dict = {
        "hostname": settings.local_host,
        "port": settings.local_port,
        "identifier": f"gw-local-{settings.site_id}",
    }
    if settings.local_user:
        kw["username"] = settings.local_user
        kw["password"] = settings.local_password or ""
    return kw


def _uplink_client_kwargs(settings: Settings) -> dict:
    kw: dict = {
        "hostname": settings.uplink_host,
        "port": settings.uplink_port,
        "identifier": f"gw-uplink-{settings.site_id}",
    }
    if settings.uplink_tls:
        kw["tls_context"] = ssl.create_default_context()
    if settings.uplink_user:
        kw["username"] = settings.uplink_user
        kw["password"] = settings.uplink_password or ""
    return kw


class MqttBridge:
    """Subscribe to a local MQTT broker (ESP32 → Mosquitto) and publish to uplink broker."""

    def __init__(self, settings: Settings, queue: PublishQueue) -> None:
        self._s = settings
        self._queue = queue
        self._outbound: asyncio.Queue[OutboundMessage] = asyncio.Queue(maxsize=10_000)

    async def run(self) -> None:
        await asyncio.gather(
            self._local_subscribe_loop(),
            self._uplink_publish_loop(),
            self._sqlite_replay_loop(),
        )

    async def _local_subscribe_loop(self) -> None:
        kwargs = _local_client_kwargs(self._s)
        while True:
            try:
                async with aiomqtt.Client(**kwargs) as local:
                    await local.subscribe(self._s.subscribe_pattern, qos=1)
                    LOG.info("local subscribe pattern=%s", self._s.subscribe_pattern)
                    async for message in local.messages:
                        topic = str(message.topic)
                        payload = bytes(message.payload)
                        qos = _qos_value(message)
                        retain = bool(message.retain)
                        out_topic = _rewrite_topic(self._s, topic)
                        out_payload = _envelope_if_needed(self._s, topic, payload)
                        msg = OutboundMessage(
                            topic=out_topic,
                            payload=out_payload,
                            qos=qos,
                            retain=retain,
                            sqlite_row_id=None,
                        )
                        try:
                            self._outbound.put_nowait(msg)
                        except asyncio.QueueFull:
                            LOG.error("outbound queue full; dropping message topic=%s", out_topic)
            except aiomqtt.MqttError as e:
                LOG.warning("local mqtt error: %s — retry in 3s", e)
                await asyncio.sleep(3.0)
            except Exception:
                LOG.exception("local mqtt loop — retry in 3s")
                await asyncio.sleep(3.0)

    async def _uplink_publish_loop(self) -> None:
        kwargs = _uplink_client_kwargs(self._s)
        while True:
            try:
                async with aiomqtt.Client(**kwargs) as uplink:
                    LOG.info("uplink connected %s:%s", self._s.uplink_host, self._s.uplink_port)
                    while True:
                        item = await self._outbound.get()
                        try:
                            await uplink.publish(
                                item.topic,
                                payload=item.payload,
                                qos=item.qos,
                                retain=item.retain,
                            )
                            if item.sqlite_row_id is not None:
                                self._queue.delete(item.sqlite_row_id)
                        except Exception:
                            LOG.warning("uplink publish failed topic=%s", item.topic)
                            if item.sqlite_row_id is None:
                                self._queue.enqueue(
                                    item.topic, item.payload, qos=item.qos, retain=item.retain
                                )
                            else:
                                self._queue.release_inflight(item.sqlite_row_id)
            except aiomqtt.MqttError as e:
                LOG.warning("uplink mqtt error: %s — retry in 3s", e)
                await asyncio.sleep(3.0)
            except Exception:
                LOG.exception("uplink loop — retry in 3s")
                await asyncio.sleep(3.0)

    async def _sqlite_replay_loop(self) -> None:
        while True:
            try:
                claimed = self._queue.claim_batch(50)
                for i, (row_id, topic, payload, qos, retain) in enumerate(claimed):
                    msg = OutboundMessage(
                        topic=topic,
                        payload=payload,
                        qos=qos,
                        retain=retain,
                        sqlite_row_id=row_id,
                    )
                    try:
                        self._outbound.put_nowait(msg)
                    except asyncio.QueueFull:
                        for row_id_rest, *_rest in claimed[i:]:
                            LOG.error(
                                "outbound queue full; releasing sqlite row id=%s", row_id_rest
                            )
                            self._queue.release_inflight(row_id_rest)
                        break
            except Exception:
                LOG.exception("sqlite replay scheduling failed")
            await asyncio.sleep(2.0)
