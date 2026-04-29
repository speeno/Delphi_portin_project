"""
외부 Open API(ITS / 기상청 단기·특보 / 오피넷) 키 연동 스모크 프로브.

실행 (저장소 루트에서):

    PYTHONPATH=도서물류관리프로그램/backend RUN_OPEN_API_PROBE=1 \\
      python3 test/run_open_api_probe.py

또는 pytest:

    PYTHONPATH=도서물류관리프로그램/backend RUN_OPEN_API_PROBE=1 \\
      python3 -m pytest test/test_open_api_connectivity.py -v

결과: ``test/output/open_api_probe_<timestamp>.json`` 및 ``open_api_probe_latest.json``
(비밀·원문 URL 미포함; 인증키는 set/unset 만 기록)
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# backend 패키지 로드를 위해 호출부에서 PYTHONPATH 설정 필요
from app.core import config
from app.services import its_traffic_client, kma_warning_client, kma_weather_client, open_api_http, opinet_client

PROBE_OUTPUT_DIR = Path(__file__).resolve().parent / "output"

_SEOUL_BBOX = {"min_x": 126.76, "max_x": 127.18, "min_y": 37.42, "max_y": 37.7}


def _flag_set(name: str) -> str:
    v = (os.environ.get(name) or "").strip()
    return "set" if v else "unset"


def _env_snapshot() -> dict[str, str]:
    return {
        "BLS_ITS_API_KEY": _flag_set("BLS_ITS_API_KEY"),
        "BLS_KMA_API_KEY": _flag_set("BLS_KMA_API_KEY"),
        "BLS_KMA_WARNING_API_KEY": _flag_set("BLS_KMA_WARNING_API_KEY"),
        "BLS_OPINET_CODE": _flag_set("BLS_OPINET_CODE"),
        "ITS_TRAFFIC_BASE_URL": (config.ITS_TRAFFIC_BASE_URL or "")[:80],
        "KMA_BASE_URL": (config.KMA_BASE_URL or "")[:120],
        "KMA_WARNING_BASE_URL": (config.KMA_WARNING_BASE_URL or "")[:120],
        "OPINET_API_BASE_URL": (config.OPINET_API_BASE_URL or "")[:80],
    }


def _truncate_keys(obj: Any, depth: int = 0) -> Any:
    """디버그용 요약 — 과도한 중첩·길이 제한."""
    if depth > 6:
        return "…"
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for i, (k, v) in enumerate(obj.items()):
            if i >= 40:
                out["_truncated"] = True
                break
            ks = str(k)
            if ks.lower() in {"servicekey", "apikey", "authorization"}:
                out[ks] = "[redacted]"
            else:
                out[ks] = _truncate_keys(v, depth + 1)
        return out
    if isinstance(obj, list):
        if len(obj) > 15:
            return [_truncate_keys(x, depth + 1) for x in obj[:5]] + [f"… (+{len(obj) - 5} more)"]
        return [_truncate_keys(x, depth + 1) for x in obj]
    if isinstance(obj, str) and len(obj) > 500:
        return obj[:500] + "…"
    return obj


def _sanitize_message(value: Any) -> str:
    raw = str(value or "").strip()
    for secret in (
        config.ITS_API_KEY,
        config.KMA_API_KEY,
        config.KMA_WARNING_API_KEY,
        config.OPINET_CODE,
    ):
        if secret:
            raw = raw.replace(secret, "[redacted]")
    return raw[:240]


def _public_host(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc or parsed.scheme or ""


def _http_probe(url: str, timeout: float) -> tuple[bytes | None, dict[str, Any]]:
    """비밀이 담긴 전체 URL은 저장하지 않고 HTTP/예외 요약만 반환한다."""
    if not url:
        return None, {"ok": False, "error_type": "missing_url"}
    detail: dict[str, Any] = {"host": _public_host(url)}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "book-logistics-dashboard-probe/1.0"})
        with open_api_http.urlopen(req, timeout=timeout) as res:
            raw = res.read(512 * 1024)
            status = getattr(res, "status", None)
            if status is None and hasattr(res, "getcode"):
                status = res.getcode()
            detail.update(
                {
                    "ok": 200 <= int(status or 0) < 300,
                    "http_status": int(status) if status is not None else None,
                    "content_type": res.headers.get("content-type", ""),
                    "bytes": len(raw),
                }
            )
            return raw, detail
    except urllib.error.HTTPError as exc:
        raw = exc.read(128 * 1024)
        detail.update(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error_message": _sanitize_message(exc),
                "http_status": exc.code,
                "content_type": exc.headers.get("content-type", "") if exc.headers else "",
                "bytes": len(raw),
            }
        )
        return raw or None, detail
    except urllib.error.URLError as exc:
        detail.update(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error_message": _sanitize_message(getattr(exc, "reason", exc)),
            }
        )
        return None, detail
    except Exception as exc:
        detail.update(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error_message": _sanitize_message(exc),
            }
        )
        return None, detail


def _parse_public_data_header(raw: bytes) -> dict[str, Any]:
    """공공데이터포털 JSON 의 response.header 요약."""
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except Exception as exc:
        try:
            root = ET.fromstring(raw)
        except Exception:
            return {"parse_error": type(exc).__name__}
        header: dict[str, Any] = {}
        for elem in root.iter():
            tag = elem.tag.rsplit("}", 1)[-1]
            if tag in {"resultCode", "resultMsg", "returnAuthMsg", "returnReasonCode"}:
                header[tag] = elem.text or ""
        return header or {"shape": "xml", "root": root.tag.rsplit("}", 1)[-1]}
    if not isinstance(data, dict):
        return {"shape": type(data).__name__}
    resp = data.get("response")
    if not isinstance(resp, dict):
        return {"top_keys": list(data.keys())[:20]}
    header = resp.get("header")
    if isinstance(header, dict):
        return {
            "resultCode": header.get("resultCode"),
            "resultMsg": header.get("resultMsg"),
        }
    return {"response_keys": list(resp.keys())[:20]}


def probe_its_traffic_live() -> dict[str, Any]:
    r = its_traffic_client.fetch_traffic_result(bbox=_SEOUL_BBOX, forecast=False)
    sample_keys: list[str] = []
    if r.rows:
        first = r.rows[0]
        if isinstance(first, dict):
            sample_keys = list(first.keys())[:24]
    detail: dict[str, Any] = {
        "service": "its_traffic_live",
        "ok": r.status == "ok" and len(r.rows) > 0,
        "status": r.status,
        "message": r.message,
        "http_status": r.http_status,
        "content_type": r.content_type,
        "row_count": len(r.rows),
        "sample_row_keys": sample_keys,
    }
    if not detail["ok"]:
        detail["api_header"] = _probe_its_header(forecast=False)
    return detail


def probe_its_traffic_forecast() -> dict[str, Any]:
    r = its_traffic_client.fetch_traffic_result(bbox=_SEOUL_BBOX, forecast=True)
    sample_keys: list[str] = []
    if r.rows:
        first = r.rows[0]
        if isinstance(first, dict):
            sample_keys = list(first.keys())[:24]
    detail: dict[str, Any] = {
        "service": "its_traffic_forecast",
        "ok": r.status == "ok" and len(r.rows) > 0,
        "status": r.status,
        "message": r.message,
        "http_status": r.http_status,
        "content_type": r.content_type,
        "row_count": len(r.rows),
        "sample_row_keys": sample_keys,
    }
    if not detail["ok"]:
        api_header = _probe_its_header(forecast=True)
        detail["api_header"] = api_header
        header = api_header.get("header") if isinstance(api_header, dict) else None
        if isinstance(header, dict) and str(header.get("resultCode")) == "4004":
            detail["skipped"] = True
            detail["skip_reason"] = "configured ITS forecast endpoint returned 4004 (wrong URL); dashboard falls back to live traffic"
    return detail


def _probe_its_header(*, forecast: bool) -> dict[str, Any]:
    params: dict[str, str] = {
        "apiKey": config.ITS_API_KEY,
        "getType": "json",
        "type": "all",
        "drcType": "all",
    }
    for src, dst in (("min_x", "minX"), ("max_x", "maxX"), ("min_y", "minY"), ("max_y", "maxY")):
        params[dst] = str(_SEOUL_BBOX[src])
    raw, http = _http_probe(
        f"{its_traffic_client._traffic_endpoint(forecast=forecast)}?{urllib.parse.urlencode(params)}",
        config.ITS_REQUEST_TIMEOUT_SEC,
    )
    out = {"http": http}
    if raw:
        try:
            parsed = json.loads(raw.decode("utf-8-sig"))
            if isinstance(parsed, dict) and isinstance(parsed.get("header"), dict):
                out["header"] = _truncate_keys(parsed["header"])
            else:
                out["preview"] = _truncate_keys(parsed)
        except Exception as exc:
            out["parse_error"] = type(exc).__name__
    return out


def probe_kma_short_term() -> dict[str, Any]:
    detail: dict[str, Any] = {
        "service": "kma_vilage_fcst",
        "nx": 60,
        "ny": 127,
    }
    if not config.KMA_API_KEY:
        detail["ok"] = False
        detail["skipped"] = True
        detail["skip_reason"] = "BLS_KMA_API_KEY unset"
        return detail

    base_date, base_time = kma_weather_client._base_datetime()
    common = {"base_date": base_date, "base_time": base_time, "nx": 60, "ny": 127}
    raw_ncst, ncst_http = _http_probe(
        kma_weather_client._service_url("getUltraSrtNcst", common),
        config.KMA_REQUEST_TIMEOUT_SEC,
    )
    header_ncst = _parse_public_data_header(raw_ncst) if raw_ncst else {"raw": None}
    merged = kma_weather_client.fetch_weather(nx=60, ny=127)
    detail["base_date"] = base_date
    detail["base_time"] = base_time
    detail["http_ncst"] = ncst_http
    detail["raw_ncst_header"] = header_ncst
    detail["fetch_weather_ok"] = merged is not None
    if merged:
        detail["summary"] = {
            "temp_c": merged.get("temp_c"),
            "humidity_pct": merged.get("humidity_pct"),
            "rain_mm": merged.get("rain_mm"),
            "precip_type": merged.get("precip_type"),
        }
    code = header_ncst.get("resultCode") if isinstance(header_ncst, dict) else None
    code_s = str(code).strip() if code is not None else ""
    hdr_ok = code_s in {"0", "00"}
    detail["api_result_code"] = code_s or None
    if isinstance(header_ncst, dict) and header_ncst.get("resultMsg"):
        detail["api_result_msg"] = header_ncst.get("resultMsg")
    detail["ok"] = merged is not None or hdr_ok
    if raw_ncst:
        try:
            detail["raw_ncst_preview"] = _truncate_keys(json.loads(raw_ncst.decode("utf-8-sig")))
        except Exception as exc:
            detail["raw_ncst_preview"] = {"note": "json_parse_failed", "error": type(exc).__name__}
    return detail


def probe_kma_warning() -> dict[str, Any]:
    detail: dict[str, Any] = {"service": "kma_warning"}
    if not config.KMA_WARNING_API_KEY:
        detail["ok"] = False
        detail["skipped"] = True
        detail["skip_reason"] = "BLS_KMA_WARNING_API_KEY unset"
        return detail
    from_tm, to_tm = kma_warning_client._tm_window()
    raw, http_detail = _http_probe(
        kma_warning_client._service_url(
            "getPwnCd",
            {"fromTmFc": from_tm, "toTmFc": to_tm, "areaCode": "L1100100"},
        ),
        config.KMA_WARNING_REQUEST_TIMEOUT_SEC,
    )
    detail["time_window"] = {"fromTmFc": from_tm, "toTmFc": to_tm}
    detail["http"] = http_detail
    if not raw:
        detail["ok"] = False
        detail["error"] = "empty_http_response"
        return detail
    hdr = _parse_public_data_header(raw)
    detail["raw_header"] = hdr
    rows = kma_warning_client.parse_items(raw)
    detail["parsed_row_count"] = len(rows)
    code = hdr.get("resultCode") if isinstance(hdr, dict) else None
    code_s = str(code).strip() if code is not None else ""
    hdr_ok = code_s in {"0", "00"}
    detail["api_result_code"] = code_s or None
    if isinstance(hdr, dict) and hdr.get("resultMsg"):
        detail["api_result_msg"] = hdr.get("resultMsg")
    if isinstance(hdr, dict) and code_s and not hdr_ok:
        detail["api_error"] = hdr
    if rows:
        detail["sample_row_keys"] = list(rows[0].keys())[:30]
    warn = kma_warning_client.fetch_warning(nx=60, ny=127)
    detail["fetch_warning_normalized"] = warn is not None
    detail["ok"] = warn is not None or (hdr_ok if code_s else len(rows) > 0)
    return detail


def probe_opinet_diesel() -> dict[str, Any]:
    detail: dict[str, Any] = {"service": "opinet_diesel_national"}
    if not config.OPINET_CODE:
        detail["ok"] = False
        detail["skipped"] = True
        detail["skip_reason"] = "BLS_OPINET_CODE unset"
        return detail
    q = urllib.parse.urlencode({"out": "json", "code": config.OPINET_CODE})
    raw, http_detail = _http_probe(
        f"{config.OPINET_API_BASE_URL}/avgAllPrice.do?{q}",
        config.OPINET_REQUEST_TIMEOUT_SEC,
    )
    detail["http"] = http_detail
    row = opinet_client.fetch_avg_all_diesel()
    detail["ok"] = row is not None
    if row:
        detail["normalized"] = _truncate_keys(row)
    elif raw:
        try:
            parsed = json.loads(raw.decode("utf-8-sig"))
            detail["raw_preview"] = _truncate_keys(parsed)
            if isinstance(parsed, dict):
                rows = opinet_client.parse_oil_rows(parsed)
                detail["parsed_row_count"] = len(rows)
                detail["top_keys"] = list(parsed.keys())[:20]
        except Exception as exc:
            detail["raw_preview"] = {"note": "json_parse_failed", "error": type(exc).__name__}
    return detail


def _outcome(p: dict[str, Any]) -> str:
    if p.get("skipped"):
        return "skipped"
    return "pass" if p.get("ok") else "fail"


def run_all_probes() -> dict[str, Any]:
    """모든 프로브 실행 후 검토용 단일 dict 반환."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    probes = [
        probe_its_traffic_live(),
        probe_its_traffic_forecast(),
        probe_kma_short_term(),
        probe_kma_warning(),
        probe_opinet_diesel(),
    ]
    outcomes = [_outcome(p) for p in probes]
    return {
        "generated_at_utc": ts,
        "run_open_api_probe": os.environ.get("RUN_OPEN_API_PROBE", ""),
        "env": _env_snapshot(),
        "summary": {
            "total": len(probes),
            "passed": sum(1 for x in outcomes if x == "pass"),
            "failed": sum(1 for x in outcomes if x == "fail"),
            "skipped": sum(1 for x in outcomes if x == "skipped"),
        },
        "probes": probes,
    }


def ensure_output_dir() -> Path:
    PROBE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return PROBE_OUTPUT_DIR


def write_reports(report: dict[str, Any]) -> tuple[Path, Path]:
    """타임스탬프 파일 + latest 동시 기록."""
    out = ensure_output_dir()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path_ts = out / f"open_api_probe_{stamp}.json"
    path_latest = out / "open_api_probe_latest.json"
    text = json.dumps(report, ensure_ascii=False, indent=2)
    path_ts.write_text(text, encoding="utf-8")
    path_latest.write_text(text, encoding="utf-8")
    return path_ts, path_latest
