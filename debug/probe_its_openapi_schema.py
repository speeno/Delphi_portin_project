#!/usr/bin/env python3
"""ITS OpenAPI 응답 스키마 안전 프로브.

원문 응답과 인증키를 파일에 저장하지 않는다. 출력은 status, content-type,
최상위 key, 샘플 row key 만 포함한다.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any


BASE_URL = os.environ.get("BLS_ITS_TRAFFIC_BASE_URL", "https://openapi.its.go.kr:9443").rstrip("/")
TRAFFIC_PATH = os.environ.get("BLS_ITS_TRAFFIC_SERVICE_PATH", "/trafficInfo")
FORECAST_PATH = os.environ.get("BLS_ITS_FORECAST_SERVICE_PATH", "/fcTrafficInfo")


def _url(path: str, api_key: str) -> str:
    endpoint = path if path.startswith(("http://", "https://")) else f"{BASE_URL}/{path.lstrip('/')}"
    params = {
        "apiKey": api_key,
        "getType": "json",
        "type": "all",
        "drcType": "all",
        "minX": os.environ.get("BLS_ITS_PROBE_MIN_X", "126.76"),
        "maxX": os.environ.get("BLS_ITS_PROBE_MAX_X", "127.18"),
        "minY": os.environ.get("BLS_ITS_PROBE_MIN_Y", "37.42"),
        "maxY": os.environ.get("BLS_ITS_PROBE_MAX_Y", "37.70"),
    }
    return f"{endpoint}?{urllib.parse.urlencode(params)}"


def _flatten_json_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("items", "item", "body", "response", "data"):
        nested = _flatten_json_items(payload.get(key))
        if nested:
            return nested
    return [payload]


def _xml_row_keys(raw: bytes) -> list[str]:
    root = ET.fromstring(raw)
    for elem in root.iter():
        children = list(elem)
        if children:
            return [c.tag.rsplit("}", 1)[-1] for c in children][:40]
    return []


def probe(name: str, path: str, api_key: str) -> dict[str, Any]:
    url = _url(path, api_key)
    req = urllib.request.Request(url, headers={"User-Agent": "book-logistics-dashboard-probe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10.0) as res:  # noqa: S310 - operator-provided public endpoint
            raw = res.read(512 * 1024)
            status = getattr(res, "status", None) or res.getcode()
            content_type = res.headers.get("content-type", "")
    except Exception as exc:
        return {"name": name, "ok": False, "error_type": type(exc).__name__}

    out: dict[str, Any] = {
        "name": name,
        "ok": 200 <= int(status or 0) < 300,
        "status": status,
        "content_type": content_type,
        "bytes": len(raw),
    }
    try:
        if "xml" in content_type.lower() or raw.lstrip().startswith(b"<"):
            out["sample_row_keys"] = _xml_row_keys(raw)
        else:
            parsed = json.loads(raw.decode("utf-8-sig"))
            out["top_keys"] = list(parsed.keys())[:40] if isinstance(parsed, dict) else []
            rows = _flatten_json_items(parsed)
            out["sample_row_keys"] = list(rows[0].keys())[:40] if rows else []
            out["sample_count_detected"] = len(rows)
    except Exception as exc:
        out["parse_error_type"] = type(exc).__name__
    return out


def main() -> int:
    api_key = os.environ.get("BLS_ITS_API_KEY", "").strip()
    if not api_key:
        print("BLS_ITS_API_KEY is required", file=sys.stderr)
        return 2
    results = [
        probe("trafficInfo", TRAFFIC_PATH, api_key),
        probe("fcTraffic", FORECAST_PATH, api_key),
    ]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
