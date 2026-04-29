"""
RUN_OPEN_API_PROBE=1 일 때만 외부 Open API 에 실제 요청하고,
``test/output/open_api_probe_latest.json`` 에 결과를 기록한다.

CI 기본은 스킵 (키·네트워크 없음).

    PYTHONPATH=도서물류관리프로그램/backend RUN_OPEN_API_PROBE=1 \\
      python3 -m pytest test/test_open_api_connectivity.py -v
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from open_api_probe import PROBE_OUTPUT_DIR, run_all_probes, write_reports

_ENABLED = os.environ.get("RUN_OPEN_API_PROBE", "").strip().lower() in {"1", "true", "yes"}


_STRICT = os.environ.get("RUN_OPEN_API_PROBE_STRICT", "").strip().lower() in {"1", "true", "yes"}


@pytest.mark.skipif(not _ENABLED, reason="RUN_OPEN_API_PROBE 미설정 — 라이브 외부 API 호출 생략")
def test_open_api_probe_live_and_save_report() -> None:
    """실제 호출 후 JSON 저장. 개별 실패는 리포트로 검토; STRICT 일 때만 실패 처리."""
    report = run_all_probes()
    ts_path, latest_path = write_reports(report)

    assert ts_path.is_file()
    assert latest_path.is_file()
    data = json.loads(latest_path.read_text(encoding="utf-8"))
    assert "generated_at_utc" in data
    assert "probes" in data and isinstance(data["probes"], list)
    assert len(data["probes"]) >= 5

    failed = [p for p in data["probes"] if not p.get("ok") and not p.get("skipped")]
    if failed and _STRICT:
        pytest.fail(
            "RUN_OPEN_API_PROBE_STRICT=1 — 프로브 실패: "
            + json.dumps(failed, ensure_ascii=False)
            + f" | 전체: {latest_path}",
        )


def test_open_api_probe_report_schema_when_disabled() -> None:
    """프로브 미실행 시에도 모듈·출력 디렉터리 정의가 깨지지 않음."""
    assert PROBE_OUTPUT_DIR.name == "output"
