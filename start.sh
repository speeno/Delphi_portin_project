#!/usr/bin/env bash
# 프로젝트 루트 — 도서물류관리프로그램 backend + frontend 한번에 기동.
#
# 사용:
#   ./start.sh                    # 둘 다 백그라운드
#   ./start.sh backend            # 백엔드만
#   ./start.sh frontend           # 프론트만
#   ./start.sh --fg               # 백엔드 포그라운드(+프론트 백그라운드)
#
# 본 wrapper 는 도서물류관리프로그램/scripts/start.sh 을 그대로 위임합니다 (DRY).

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${ROOT}/도서물류관리프로그램/scripts/start.sh" "$@"
