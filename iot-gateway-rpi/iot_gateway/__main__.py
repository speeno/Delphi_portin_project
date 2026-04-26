"""Run: python -m iot_gateway  (from iot-gateway-rpi directory, after pip install -e . or PYTHONPATH=.)"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Allow `python iot_gateway/__main__.py` from package dir without install
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from iot_gateway.bridge import MqttBridge
from iot_gateway.config import load_settings
from iot_gateway.queue_sqlite import PublishQueue


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


async def _amain() -> None:
    settings = load_settings()
    _setup_logging(settings.log_level)
    log = logging.getLogger("iot_gateway")
    log.info("starting gateway site_id=%s", settings.site_id)
    queue = PublishQueue(settings.sqlite_path)
    try:
        bridge = MqttBridge(settings, queue)
        await bridge.run()
    finally:
        queue.close()


def main() -> None:
    try:
        asyncio.run(_amain())
    except KeyboardInterrupt:
        logging.getLogger("iot_gateway").info("stopped by user")


if __name__ == "__main__":
    main()
