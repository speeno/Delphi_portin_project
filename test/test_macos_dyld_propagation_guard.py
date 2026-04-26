"""
macOS SIP DYLD 전파 회귀 가드 (DEC-037 핫픽스).

배경:
- ``_lib.sh`` 가 ``DYLD_FALLBACK_LIBRARY_PATH`` 를 export 해도, ``start.sh`` 가
  ``nohup`` / ``setsid`` 등 ``/usr/bin`` 의 SIP 보호 바이너리를 거치면 macOS 가
  자식 프로세스로 exec 하는 시점에 ``DYLD_*`` 변수를 모두 떼어 낸다.
- 그 결과 WeasyPrint 가 ``libgobject-2.0`` 같은 Homebrew 라이브러리를 못 찾고
  PDF 다운로드가 503 ``PR_ENGINE_UNAVAILABLE`` 로 실패한다.

재발 방지 정책:
1. macOS 분기에서 ``DYLD_FALLBACK_LIBRARY_PATH`` 를 export 한다 (``_lib.sh``).
2. ``start.sh`` 의 백엔드/프런트 백그라운드 기동은 **셸 직접 fork/exec + disown -h**
   패턴만 사용한다. ``nohup`` / ``setsid`` 추가 금지.
3. 위 두 가지를 본 테스트가 정적으로 검증한다 — 누군가 nohup 을 다시 넣으면 빨간불.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "도서물류관리프로그램" / "scripts"
LIB_SH = SCRIPTS_DIR / "_lib.sh"
START_SH = SCRIPTS_DIR / "start.sh"


def _read(path: Path) -> str:
    assert path.exists(), f"필수 스크립트 누락: {path}"
    return path.read_text(encoding="utf-8")


def test_lib_sh_exports_dyld_fallback_for_darwin() -> None:
    """``_lib.sh`` 는 macOS 분기에서 ``DYLD_FALLBACK_LIBRARY_PATH`` 를 export 해야 함."""
    text = _read(LIB_SH)
    assert "uname -s" in text and "Darwin" in text, (
        "macOS 분기 (uname -s == 'Darwin') 가 _lib.sh 에 있어야 함"
    )
    assert "DYLD_FALLBACK_LIBRARY_PATH" in text, (
        "_lib.sh 가 DYLD_FALLBACK_LIBRARY_PATH 를 설정해야 함 (DEC-037)"
    )
    assert "/opt/homebrew/lib" in text, (
        "_lib.sh 의 dyld 검색 경로에 /opt/homebrew/lib 가 포함되어야 함"
    )


def test_start_sh_does_not_use_nohup_or_setsid() -> None:
    """``start.sh`` 에 nohup/setsid 가 다시 들어오면 SIP 가 DYLD 를 떼어 PDF 가 깨짐."""
    text = _read(START_SH)
    sanitized = re.sub(r"#.*", "", text)
    forbidden = ("nohup ", "nohup\t", "setsid ", "setsid\t")
    for token in forbidden:
        assert token not in sanitized, (
            f"start.sh 에 {token.strip()!r} 가 사용됨 — macOS SIP 가 DYLD_* 를 제거해 "
            "WeasyPrint 가 PR_ENGINE_UNAVAILABLE 로 실패한다 (DEC-037 핫픽스). "
            "셸 직접 ``cmd & disown -h $!`` 패턴을 유지하라."
        )


def test_start_sh_uses_disown_for_background_processes() -> None:
    """백엔드/프런트 모두 ``disown -h`` 로 SIGHUP 면역을 부여해야 함."""
    text = _read(START_SH)
    assert "disown -h" in text, (
        "start.sh 의 백그라운드 기동은 ``disown -h`` 로 SIGHUP 면역을 보장해야 함 "
        "(nohup 대체 정책)"
    )
    occurrences = text.count("disown -h")
    assert occurrences >= 2, (
        "backend 와 frontend 양쪽 모두에서 ``disown -h`` 를 사용해야 함 "
        f"(현재 {occurrences} 회)"
    )
