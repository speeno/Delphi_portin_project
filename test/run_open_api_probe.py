#!/usr/bin/env python3
"""Open API 연동 스모크 프로브 CLI — 결과를 test/output/ 에 JSON 저장.

사용:

    PYTHONPATH=도서물류관리프로그램/backend RUN_OPEN_API_PROBE=1 \\
      python3 test/run_open_api_probe.py

레포 루트 `.env` 에 키가 있으면 `app.core.config` 의 load_dotenv 로 주입됩니다.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_BACKEND = _ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

_probe_path = Path(__file__).resolve().parent / "open_api_probe.py"
_spec = importlib.util.spec_from_file_location("open_api_probe", _probe_path)
if _spec is None or _spec.loader is None:
    raise RuntimeError("open_api_probe 로드 실패")
_probe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_probe)


def main() -> int:
    if (_ROOT / ".env").is_file():
        pass
    report = _probe.run_all_probes()
    ts_path, latest_path = _probe.write_reports(report)
    print(f"Wrote {ts_path}")
    print(f"Wrote {latest_path}")
    sm = report.get("summary") or {}
    print(
        f"Summary: passed={sm.get('passed')} failed={sm.get('failed')} "
        f"skipped={sm.get('skipped')} total={sm.get('total')}",
    )
    # 결과 파일 검토용 — 종료 코드는 실패해도 0 (선택 Strict 는 pytest RUN_OPEN_API_PROBE_STRICT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
