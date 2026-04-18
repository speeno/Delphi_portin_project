#!/usr/bin/env bash
# 프로젝트 루트 — 도서물류관리프로그램 backend + frontend 한번에 중지.
#
# 사용:
#   ./stop.sh                     # 둘 다
#   ./stop.sh backend             # 백엔드만
#   ./stop.sh frontend            # 프론트만
#   ./stop.sh --force             # SIGKILL 즉시 (비권장)

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${ROOT}/도서물류관리프로그램/scripts/stop.sh" "$@"
