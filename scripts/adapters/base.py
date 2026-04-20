"""adapters 공용 — 식별자 sanitizer + 서버 프로필 로더.

서버 프로필
-----------
- 우선순위: ENV (`BLS_C15_PROFILES`) > 명시 경로 > 기본 (도서물류관리프로그램/backend/servers.yaml).
- 자격(password) 은 YAML 안에 두지 말고 env 만 허용 — `BLS_C15_PWD__<server_id>` 또는
  YAML 의 `password_env: VAR_NAME` 키.

식별자 sanitizer
----------------
- 화이트리스트: ``[A-Za-z][A-Za-z0-9_]{0,62}`` (DB/스키마/테이블/컬럼 공통).
- 화이트리스트 미통과 시 ``ValueError`` — 어떤 quoting 도 시도하지 않는다.
- 본 sanitizer 는 비즈니스 SQL 신설을 막는 정적 가드와 함께 동작 — 시스템/구조
  쿼리에서만 식별자를 동적 삽입한다.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE_PATHS = (
    Path(os.environ.get("BLS_C15_PROFILES", "")) if os.environ.get("BLS_C15_PROFILES") else None,
    ROOT / "도서물류관리프로그램" / "backend" / "servers.yaml",
)

_IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,62}$")


def sanitize_identifier(name: str, *, kind: str = "identifier") -> str:
    """화이트리스트 검증된 식별자만 통과시킨다 (실패 시 ValueError)."""
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"invalid {kind}: {name!r}")
    return name


@dataclass
class ServerProfile:
    """단일 서버 접속 프로필 (본 패키지 안에서만 사용)."""

    id: str
    driver: str   # "mysql" | "sqlserver"
    host: str
    port: int
    user: str
    password: str
    database: str
    options: dict[str, Any]

    def short(self) -> str:
        return f"{self.driver}://{self.user}@{self.host}:{self.port}/{self.database}"


def _read_yaml(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"profile yaml not found: {path}")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        text = raw.decode("utf-8-sig")
    else:
        for enc in ("utf-8", "cp949", "euc-kr"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:  # pragma: no cover - defensive
            text = raw.decode("utf-8", errors="replace")
    return yaml.safe_load(text) or {}


def _resolve_password(server_id: str, raw: Mapping[str, Any]) -> str:
    """YAML 의 `password_env` 또는 표준 env 변수에서 비밀번호 조회."""
    env_var = raw.get("password_env") or f"BLS_C15_PWD__{server_id}"
    val = os.environ.get(str(env_var))
    if val is None:
        raise RuntimeError(
            f"missing password env var for {server_id}: {env_var} (set or update profile)",
        )
    return val


def resolve_profile(server_id: str, *, path: Path | None = None) -> ServerProfile:
    """``servers.yaml`` 에서 한 서버 프로필을 읽어 정규화."""
    candidate_paths = [path] if path else [p for p in DEFAULT_PROFILE_PATHS if p]
    last_err: Exception | None = None
    for p in candidate_paths:
        try:
            data = _read_yaml(p)
            break
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    else:
        raise RuntimeError(f"unable to load any profile yaml; last error: {last_err}")

    servers = data.get("servers") or []
    raw = next((s for s in servers if s.get("id") == server_id), None)
    if not raw:
        raise KeyError(f"server profile not found: {server_id}")

    driver = (raw.get("driver") or raw.get("type") or "mysql").lower()
    if driver not in ("mysql", "sqlserver"):
        raise ValueError(f"unsupported driver for {server_id}: {driver!r}")

    return ServerProfile(
        id=server_id,
        driver=driver,
        host=str(raw.get("host", "127.0.0.1")),
        port=int(raw.get("port", 3306 if driver == "mysql" else 1433)),
        user=str(raw.get("user", "")),
        password=_resolve_password(server_id, raw),
        database=str(raw.get("database", "")),
        options=dict(raw.get("options") or {}),
    )
