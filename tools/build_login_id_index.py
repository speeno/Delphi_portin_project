#!/usr/bin/env python3
"""DSN-DEC-09 — login_id 인덱스 빌더 (운영자 수동 실행 + 야간 배치 권장).

목적
----
4 운영 서버 (`remote_138`/`remote_153`/`remote_154`/`remote_155`) 의 모든 테넌트
``\<db\>.Id_Logn`` 을 in-process ``execute_query`` 로 스캔해 ``login_id_index.json`` 을
산출한다. 이 인덱스가 ``DSN-DEC-09`` 의 라우팅 정본.

비밀 정책 (docs/secrets-policy.md G3)
------------------------------------
- 본 도구는 ``Gcode`` / ``Hcode`` 만 SELECT 한다 (``Gpass`` 등 비밀번호 컬럼 제외).
- 출력 파일 ``backend/data/login_id_index.json`` 은 ``backend/data/`` 폴더 전체가
  ``.gitignore`` 로 제외되어 있으므로 git 추적 위험 없음.
- ``servers.yaml`` 의 DB 자격증명은 운영자 PC 한정 보존 (vault 외부 유지).

사용
----
    # 1) dry run — 어떤 라우트가 스캔될지만 출력 (DB 미접근)
    python3 tools/build_login_id_index.py

    # 2) 실제 스캔 + 인덱스 빌드
    python3 tools/build_login_id_index.py --apply

    # 3) custom 출력 경로
    BLS_LOGIN_ID_INDEX_PATH=/tmp/idx.json python3 tools/build_login_id_index.py --apply

전제
----
- ``도서물류관리프로그램/backend/servers.yaml`` 에 4 서버 자격증명 + (필요 시)
  SSH 터널 설정이 채워져 있어야 함.
- 운영자 root 권한이 모든 테넌트 DB 에 cross-DB SELECT 가능해야 함 (운영 표준).
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "도서물류관리프로그램" / "backend"


def _ensure_backend_on_path() -> None:
    sys.path.insert(0, str(BACKEND))


def _print_routes(routes: list[dict[str, str]]) -> None:
    if not routes:
        print("⚠ tenants_directory 에서 라우트를 추출하지 못했습니다.")
        print("   → seed/overlay 가 비어있거나, primary_server 라벨이 알려진 매핑에 없습니다.")
        return
    print(f"📋 스캔 대상 라우트 = {len(routes)} 개")
    print(f"{'#':>3} {'remote_id':<14} {'db_name':<24} {'tenant_id':<24} {'family':<14}")
    print("-" * 80)
    for i, r in enumerate(routes, 1):
        print(
            f"{i:>3} {r.get('remote_id',''):<14} {r.get('db_name',''):<24} "
            f"{r.get('tenant_id',''):<24} {r.get('account_family',''):<14}"
        )


async def _async_main(apply_changes: bool) -> int:
    _ensure_backend_on_path()
    from app.services import login_id_index_service  # noqa: E402

    routes = login_id_index_service._collect_routes_from_directory()
    _print_routes(routes)

    if not apply_changes:
        print()
        print("ℹ️  dry-run 모드입니다. 실제 스캔/쓰기를 하려면 --apply 옵션을 추가하세요.")
        return 0

    print()
    print("⏳ 4 서버 라이브 스캔 시작 (Gcode/Hcode 만 SELECT — 비밀번호 미수집)...")
    stats = await login_id_index_service.rebuild()
    print()
    print("✅ 인덱스 빌드 완료")
    print(f"   - rows           = {stats['rows']}")
    print(f"   - unique_gcode   = {stats['unique_gcode']}")
    print(f"   - ambiguous      = {stats['ambiguous']}  (동명 ID — hcode 보조 입력 필요)")
    print(f"   - built_at       = {stats['built_at']}")
    print(f"   - 출력 경로      = {login_id_index_service.LOGIN_ID_INDEX_PATH}")
    if stats["errors"]:
        print()
        print(f"⚠ 라우트 단위 실패 {len(stats['errors'])} 건 (인덱스는 부분 신선도로 저장됨):")
        for e in stats["errors"]:
            print(f"   - {e['remote_id']}/{e['db_name']}: {e['error']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="DSN-DEC-09 login_id_index 빌더 (Gcode/Hcode 전용, 비밀번호 미수집)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="실제 4 서버 라이브 스캔 + 인덱스 파일 쓰기",
    )
    args = parser.parse_args()
    return asyncio.run(_async_main(args.apply))


if __name__ == "__main__":
    sys.exit(main())
