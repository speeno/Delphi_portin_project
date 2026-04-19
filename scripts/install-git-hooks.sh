#!/usr/bin/env bash
# Delphi_porting 저장소 루트에서 실행: core.hooksPath 를 scripts/git-hooks 로 설정합니다.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "error: ${ROOT} 는 git 저장소가 아닙니다." >&2
  exit 1
fi

HOOK_DIR="scripts/git-hooks"
if [[ ! -f "${ROOT}/${HOOK_DIR}/pre-push" ]]; then
  echo "error: ${HOOK_DIR}/pre-push 가 없습니다." >&2
  exit 1
fi

chmod +x "${ROOT}/${HOOK_DIR}/pre-push"
git config core.hooksPath "$HOOK_DIR"

echo "설정 완료: core.hooksPath=$(git config core.hooksPath) (이 저장소 전용)"
echo ""
echo "다음: 제품 폴더(도서물류관리프로그램)을 비공개 GitHub 에 연결"
echo "  cd \"${ROOT}/도서물류관리프로그램\""
echo "  git remote add private git@github.com:YOUR_ORG/YOUR_PRIVATE_REPO.git"
echo "  git push -u private main"
echo ""
echo "원격 이름은 private 우선, 없으면 origin 이 사용됩니다."
echo "상위 git push 시 제품 저장소 동기화를 건너뛰려면:"
echo "  SKIP_PRODUCT_REPO_PUSH=1 git push"
