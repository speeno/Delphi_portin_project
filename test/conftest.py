"""pytest 공통 픽스처 — 경로 주입 + default event loop 복구.

배경
-----
- ``unittest.IsolatedAsyncioTestCase`` 는 각 테스트마다 새 event loop 를 만들고
  ``tearDown`` 에서 ``asyncio.set_event_loop(None)`` 으로 닫아 둔다.
- 이후 같은 워커에서 실행되는 일반 동기 테스트가 ``asyncio.get_event_loop()``
  (예: ``asyncio.get_event_loop().run_until_complete(...)`` — `test_c2/c3/c4`
  서비스 단위 검증에서 사용) 를 호출하면 Python 3.10+ 에서
  ``RuntimeError: There is no current event loop in thread 'MainThread'`` 가 발생한다.
- 알파벳 순으로 `IsolatedAsyncioTestCase` 가 더 앞쪽 파일에 등장하기 시작하면(
  예: 신규 ``test_book_sales_optional_hcode.py``, ``test_inventory_ledger_optional.py``)
  C2/C3/C4 서비스 단위 회귀가 일제히 깨지는 격리 회귀가 발생.

조치
-----
- 모든 테스트 시작 직전에 default event loop 가 None 이면 새로 설치한다.
- 스코프 ``function`` + ``autouse`` 로 모든 테스트(동기/비동기) 에 자동 적용 —
  이미 IsolatedAsyncioTestCase 가 자체 loop 를 굴리는 동안에는
  ``set_event_loop`` 호출이 영향을 주지 않으므로 안전.
- 테스트 간 격리 일반화 — DEC-033 회귀 가드 정신(특정 케이스 회귀를 일반 정책으로 묶음)
  을 테스트 인프라에도 적용.
"""

from __future__ import annotations

import asyncio
import sys
import warnings
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_TEST_DIR = Path(__file__).resolve().parent
_BACKEND = _ROOT / "도서물류관리프로그램" / "backend"
for p in (str(_BACKEND), str(_TEST_DIR)):
    if Path(p).name == "backend" and not Path(p).is_dir():
        continue
    if p not in sys.path:
        sys.path.insert(0, p)


@pytest.fixture(autouse=True)
def _ensure_default_event_loop() -> None:
    # Python 3.10+ — get_event_loop() 이 None policy 이면 RuntimeError 또는
    # DeprecationWarning. 직접 policy.get_event_loop() 로 검사하여 둘 다 회피.
    policy = asyncio.get_event_loop_policy()
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            loop = policy.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("loop is closed")
    except (RuntimeError, DeprecationWarning):
        policy.set_event_loop(policy.new_event_loop())
