#!/usr/bin/env python3
"""Entry point for Raspberry Pi: run from this directory without pip install."""

from __future__ import annotations

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from iot_gateway.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
