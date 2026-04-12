#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DASHBOARD_SRC="$PROJECT_ROOT/dashboard"
DEPLOY_DIR="$PROJECT_ROOT/../delphi-dashboard"
REMOTE_REPO="${DASHBOARD_REPO:-}"

print_usage() {
    cat <<'USAGE'
델파이 포팅 프로젝트 - 대시보드 배포 스크립트

사용법:
  # 최초 설정 (1회)
  ./tools/deploy_dashboard.sh init <GitHub-Public-Repo-URL>
  예: ./tools/deploy_dashboard.sh init https://github.com/speeno/delphi-dashboard.git

  # 대시보드 변경 사항 동기화 및 배포
  ./tools/deploy_dashboard.sh sync

  # 현재 상태 확인
  ./tools/deploy_dashboard.sh status
USAGE
}

cmd_init() {
    local repo_url="$1"

    if [ -d "$DEPLOY_DIR/.git" ]; then
        echo "[INFO] 배포 디렉토리가 이미 존재합니다: $DEPLOY_DIR"
        echo "[INFO] 기존 remote를 업데이트합니다."
        cd "$DEPLOY_DIR"
        git remote set-url origin "$repo_url" 2>/dev/null || git remote add origin "$repo_url"
    else
        echo "[INFO] 배포 디렉토리를 생성합니다: $DEPLOY_DIR"
        mkdir -p "$DEPLOY_DIR"
        cd "$DEPLOY_DIR"
        git init
        git remote add origin "$repo_url"
    fi

    sync_files
    create_dashboard_workflow

    cd "$DEPLOY_DIR"
    git add -A
    git commit -m "Initial dashboard deployment" || echo "[INFO] 변경 사항 없음"
    git branch -M master
    git push -u origin master

    echo ""
    echo "============================================"
    echo " 초기 배포 완료!"
    echo "============================================"
    echo ""
    echo "다음 단계:"
    echo "  1. https://github.com/$(echo "$repo_url" | sed 's|.*github.com/||;s|\.git$||')/settings/pages"
    echo "     → Source: 'GitHub Actions' 선택 → Save"
    echo ""
    echo "  2. Actions 탭에서 워크플로 실행 확인"
    echo ""
    echo "이후 대시보드 업데이트 시:"
    echo "  ./tools/deploy_dashboard.sh sync"
    echo ""
}

cmd_sync() {
    if [ ! -d "$DEPLOY_DIR/.git" ]; then
        echo "[ERROR] 배포 디렉토리가 없습니다. 먼저 init을 실행해주세요."
        echo "  ./tools/deploy_dashboard.sh init <GitHub-Public-Repo-URL>"
        exit 1
    fi

    sync_files
    create_dashboard_workflow

    cd "$DEPLOY_DIR"
    if git diff --quiet && git diff --cached --quiet; then
        echo "[INFO] 변경 사항이 없습니다."
        return
    fi

    git add -A
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Dashboard update: $timestamp"
    git push origin master

    echo ""
    echo "[OK] 대시보드가 업데이트되었습니다."
    echo "     GitHub Actions에서 자동 배포가 진행됩니다."
}

cmd_status() {
    echo "=== 대시보드 배포 상태 ==="
    echo ""

    if [ ! -d "$DEPLOY_DIR/.git" ]; then
        echo "[상태] 미설정 - init을 먼저 실행해주세요."
        return
    fi

    cd "$DEPLOY_DIR"
    local remote_url
    remote_url=$(git remote get-url origin 2>/dev/null || echo "(없음)")
    echo "배포 디렉토리: $DEPLOY_DIR"
    echo "원격 저장소:   $remote_url"
    echo ""

    echo "--- 파일 동기화 비교 ---"
    local src_count dst_count
    src_count=$(find "$DASHBOARD_SRC" -type f | wc -l | tr -d ' ')
    dst_count=$(find "$DEPLOY_DIR" -type f -not -path '*/.git/*' -not -path '*/.github/*' | wc -l | tr -d ' ')
    echo "원본 파일 수:  $src_count"
    echo "배포 파일 수:  $dst_count"
    echo ""

    echo "--- Git 상태 ---"
    git status --short
}

sync_files() {
    echo "[INFO] 대시보드 파일을 동기화합니다..."

    mkdir -p "$DEPLOY_DIR"

    rsync -av --delete \
        --exclude '.git' \
        --exclude '.github' \
        "$DASHBOARD_SRC/" "$DEPLOY_DIR/"

    cp "$PROJECT_ROOT/index.html" "$DEPLOY_DIR/redirect.html" 2>/dev/null || true

    cat > "$DEPLOY_DIR/index.html" <<'INDEXEOF'
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>델파이 웹 포팅 - 프로젝트 대시보드</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header>
    <div class="container">
      <div>
        <h1>델파이 도서 물류 시스템 - 웹 포팅 프로젝트</h1>
        <div class="subtitle">8계층 하네스 엔지니어링 기반 무중단 전환</div>
      </div>
      <div class="badge badge-progress">Sprint 0</div>
    </div>
  </header>
  <main class="container">
    <div id="app">
      <div style="text-align:center;padding:60px;color:var(--text-muted)">데이터를 불러오는 중...</div>
    </div>
  </main>
  <footer>
    <div class="container">
      델파이 웹 포팅 프로젝트 &copy; 2026 | 데이터 업데이트: JSON 편집 &rarr; git push
    </div>
  </footer>
  <script src="js/app.js"></script>
</body>
</html>
INDEXEOF

    echo "[OK] 파일 동기화 완료"
}

create_dashboard_workflow() {
    mkdir -p "$DEPLOY_DIR/.github/workflows"
    cat > "$DEPLOY_DIR/.github/workflows/deploy.yml" <<'WFEOF'
name: Deploy to GitHub Pages

on:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
WFEOF
    echo "[OK] GitHub Actions 워크플로 생성 완료"
}

case "${1:-help}" in
    init)
        if [ -z "${2:-}" ]; then
            echo "[ERROR] GitHub 저장소 URL을 지정해주세요."
            echo "  예: ./tools/deploy_dashboard.sh init https://github.com/speeno/delphi-dashboard.git"
            exit 1
        fi
        cmd_init "$2"
        ;;
    sync)
        cmd_sync
        ;;
    status)
        cmd_status
        ;;
    *)
        print_usage
        ;;
esac
