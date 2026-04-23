#!/usr/bin/env python3
"""JWT 클레임 진단 — DEC-056 Wave B 운영 도구.

목적
----
브라우저 LocalStorage 에 박힌 access_token 의 claim 을 *서명 검증 없이*
디코드하여 ``role`` / ``permissions`` / ``hcode`` / ``exp`` / ``user_id`` 를 출력.
분기 0 적용 후 admin 사용자가 ``role='admin'`` + ``permissions=['*']`` 으로
재발급 받았는지 즉시 확인 가능.

사용법
------
  python3 debug/show_jwt_claims.py <jwt_token>

또는 stdin:
  echo $TOKEN | python3 debug/show_jwt_claims.py -

주의
----
- 서명 검증은 *수행하지 않음* (claim 진단 목적). 토큰 위변조 검증은 백엔드
  ``app.core.security.decode_token`` 으로만 수행할 것.
- 외부에 절대 토큰을 노출하지 말 것 (운영 토큰은 사용자 권한 그대로 부여됨).
"""
from __future__ import annotations

import base64
import json
import sys
import time
from datetime import datetime
from typing import Any


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def decode_claims(token: str) -> dict[str, Any]:
    parts = token.strip().split(".")
    if len(parts) != 3:
        raise ValueError(
            f"JWT 형식 오류 — '.' 로 분리된 3개 segment 필요 (현재 {len(parts)})"
        )
    payload = _b64url_decode(parts[1])
    return json.loads(payload.decode("utf-8"))


def _format_exp(exp: Any) -> str:
    if not isinstance(exp, (int, float)):
        return str(exp)
    now = time.time()
    delta = int(exp) - int(now)
    iso = datetime.fromtimestamp(int(exp)).isoformat()
    if delta > 0:
        return f"{iso}  (만료까지 {delta}초 = {delta // 60}분)"
    return f"{iso}  (만료됨, {-delta}초 경과)"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: show_jwt_claims.py <jwt_token | ->", file=sys.stderr)
        return 2
    raw = sys.stdin.read() if sys.argv[1] == "-" else sys.argv[1]
    try:
        claims = decode_claims(raw)
    except Exception as exc:  # noqa: BLE001
        print(f"디코드 실패: {exc}", file=sys.stderr)
        return 1

    print("=== JWT 클레임 진단 (서명 미검증) ===")
    keys_first = ["sub", "user_id", "role", "permissions", "hcode", "server_id", "exp", "iat"]
    seen: set[str] = set()
    for k in keys_first:
        if k in claims:
            seen.add(k)
            v = claims[k]
            if k == "exp":
                v = _format_exp(v)
            elif k == "iat" and isinstance(v, (int, float)):
                v = datetime.fromtimestamp(int(v)).isoformat()
            print(f"  {k:<14}: {v}")
    extra = {k: v for k, v in claims.items() if k not in seen}
    if extra:
        print("  --- 기타 ---")
        for k, v in extra.items():
            print(f"  {k:<14}: {v}")

    role = str(claims.get("role") or "")
    perms = claims.get("permissions") or []
    hcode = str(claims.get("hcode") or "")
    is_super = (
        role == "admin"
        or hcode == "0000"
        or (isinstance(perms, list) and "*" in perms)
    )
    print()
    print(f"분기 0 (admin role 매핑) 결과: {'슈퍼유저' if is_super else '일반 사용자'}")
    if not is_super:
        print("  → 분기 0 미발효. admin 이라면:")
        print("    1) 재로그인 (토큰 캐시 만료 대기 또는 강제 로그아웃)")
        print("    2) web_admin.json 의 web_user_roles 에 role-admin 매핑 확인")
        print("    3) BLS_ADMIN_USER_IDS 환경 변수 또는 hcode='0000' 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
