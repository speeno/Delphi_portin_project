#!/usr/bin/env bash
# 프로젝트 루트 — 도서물류관리프로그램 backend + frontend 상태.

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${ROOT}/도서물류관리프로그램/scripts/status.sh" "$@"
