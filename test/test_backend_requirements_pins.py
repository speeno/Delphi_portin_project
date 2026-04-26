"""
backend/requirements.txt 핀 회귀 가드.

이 테스트는 SSH 터널 + 통합 로그인(DSN-DEC-08) 의 외부 의존성 핀이 무너져
``auth.login`` 이 외부 라이브러리 비호환으로 깨지는 회귀를 막는다.

핀 사유 (변경 시 본 docstring 도 함께 갱신):
- ``paramiko<4`` : paramiko 4.0.0 은 ``DSSKey`` 모듈 속성을 제거했으나
  ``sshtunnel<=0.4.0`` 의 ``SSHTunnelForwarder.get_keys`` 가 여전히
  ``paramiko.DSSKey`` 를 참조한다. 새 venv 에서 paramiko 4.x 가 끌려오면
  ``ssh_tunnels.mysql_connect_host_port`` → ``Fwd(...)`` 호출이
  ``AttributeError`` 로 죽고 모든 원격 인증이 실패한다.
- ``python-multipart``, ``prometheus-client`` : ``app.main`` import 단계에서
  필요한 런타임 의존성. 누락 시 백엔드가 부팅되지 않아 401/500 이전에
  서버 자체가 안 뜬다.
- ``weasyprint`` : DEC-037 PDF 엔진 단일. 미설치 시 PR_ENGINE_UNAVAILABLE.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REQ_PATH = REPO_ROOT / "도서물류관리프로그램" / "backend" / "requirements.txt"


def _read_pins() -> dict[str, str]:
    """``name`` (lowercased, no extras) → 원본 spec 라인."""
    pins: dict[str, str] = {}
    for raw in REQ_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        name = re.split(r"[\[<>=!~ ]", line, maxsplit=1)[0].strip().lower()
        if name:
            pins[name] = line
    return pins


def test_paramiko_pinned_below_4_for_sshtunnel_compat() -> None:
    """paramiko 4.x 는 DSSKey 제거 → sshtunnel 0.4.0 비호환 (회귀 가드)."""
    pins = _read_pins()
    spec = pins.get("paramiko")
    assert spec is not None, "paramiko 가 requirements.txt 에 명시되어 있어야 함"
    assert "<4" in spec.replace(" ", ""), (
        f"paramiko 는 sshtunnel 호환을 위해 <4 로 핀되어야 함. 현재: {spec!r}"
    )


def test_runtime_imports_are_listed() -> None:
    """백엔드 부팅에 필요한 임포트 의존성 누락 가드."""
    pins = _read_pins()
    for required in (
        "fastapi",
        "uvicorn[standard]".split("[", 1)[0],  # uvicorn
        "pydantic",
        "aiomysql",
        "paramiko",
        "sshtunnel",
        "python-multipart",
        "prometheus-client",
        "weasyprint",
    ):
        assert required in pins, f"requirements.txt 에 {required!r} 누락"
