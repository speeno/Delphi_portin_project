#!/usr/bin/env python3
"""
?? servers.yaml ??????? ???? SSH ???(??? ??) + MySQL ?????? ????????.
502 ????: API?? ??????? stage=ssh | mysql | config.

???? (backend ?????? ????? ???):
  cd web/seak80-sample/backend && python ../debug/probe_connections.py

???:
  SEAK80_SERVERS_CONFIG=/path/to/servers.yaml python ../debug/probe_connections.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
os.chdir(BACKEND)

# pylint: disable=wrong-import-position
from fastapi import HTTPException

import main as seak_main


def _print_http_exc(label: str, e: HTTPException) -> None:
    d = e.detail
    if isinstance(d, dict):
        stage = d.get("stage", "?")
        msg = d.get("message", d)
        print(f"{label}  FAIL  stage={stage}")
        print(f"         {msg}")
    else:
        print(f"{label}  FAIL  {d}")


def main() -> int:
    cfg = seak_main._load_raw_config()
    servers = cfg.get("servers", [])
    if not isinstance(servers, list):
        print("No servers list in config.")
        return 1

    ok_n = 0
    total = 0
    for s in servers:
        if not isinstance(s, dict):
            continue
        sid = (s.get("id") or "").strip()
        if not sid:
            continue
        total += 1
        label = f"[{sid}]"
        try:
            conn = seak_main._connect(s)
            try:
                conn.ping(reconnect=False)
            finally:
                conn.close()
            print(f"{label}  OK  MySQL ping")
            ok_n += 1
        except HTTPException as e:
            _print_http_exc(label, e)
        except Exception as e:
            print(f"{label}  FAIL  unexpected: {e!r}")

    seak_main.shutdown_all_ssh_tunnels()
    print(f"\nSummary: {ok_n}/{total} ok")
    return 0 if ok_n == total else 2


if __name__ == "__main__":
    raise SystemExit(main())
