#!/bin/bash
# 메인 저장소 git push 성공 후 Public 대시보드 저장소로 동기화
# 사용: ./tools/push_with_dashboard_sync.sh [git push 인자 그대로…]
# 예: ./tools/push_with_dashboard_sync.sh
# 예: ./tools/push_with_dashboard_sync.sh origin main

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "[INFO] git push 실행…"
git push "$@"

echo "[INFO] 대시보드 저장소 동기화…"
exec "$ROOT/tools/deploy_dashboard.sh" sync
