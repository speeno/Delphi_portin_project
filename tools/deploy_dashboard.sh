#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DASHBOARD_SRC="$PROJECT_ROOT/dashboard"
DEPLOY_DIR="${DASHBOARD_DEPLOY_DIR:-$PROJECT_ROOT/../delphi-dashboard}"
DEFAULT_REPO_SLUG="speeno/delphi-dashboard"

print_usage() {
    cat <<'USAGE'
델파이 포팅 프로젝트 - 대시보드 배포 스크립트

사용법:
  # (1) GitHub에 Public 저장소가 없을 때 — gh CLI로 생성
  ./tools/deploy_dashboard.sh create-repo [owner/repo]
  기본값: speeno/delphi-dashboard

  # (2) 최초 배포: 파일 동기화 + 커밋 + push
  ./tools/deploy_dashboard.sh init <URL 또는 owner/repo>
  예: ./tools/deploy_dashboard.sh init speeno/delphi-dashboard
  예: ./tools/deploy_dashboard.sh init https://github.com/speeno/delphi-dashboard.git

  # (3) GitHub Pages를 GitHub Actions로 활성화 (push 후 1회)
  ./tools/deploy_dashboard.sh enable-pages [owner/repo]

  # (4) 이후 대시보드 변경 시
  ./tools/deploy_dashboard.sh sync

  # 로컬에만 동기화 (push 없음, 형제 폴더에 복사)
  ./tools/deploy_dashboard.sh prepare

  # 상태 확인
  ./tools/deploy_dashboard.sh status

한 줄로 처음부터 끝까지 (gh 로그인 필요):
  ./tools/deploy_dashboard.sh bootstrap [owner/repo]
USAGE
}

normalize_repo_url() {
    local input="$1"
    if [[ "$input" =~ ^https?:// ]]; then
        echo "$input"
        return
    fi
    local slug="${input%.git}"
    echo "https://github.com/${slug}.git"
}

repo_slug_from_url() {
    local url="$1"
    echo "$url" | sed -E 's|.*github.com[:/]||;s|\.git$||'
}

ensure_gh() {
    command -v gh >/dev/null 2>&1 || {
        echo "[ERROR] gh CLI가 없습니다. https://cli.github.com 설치 후 로그인하세요."
        exit 1
    }
    gh auth status >/dev/null 2>&1 || {
        echo "[ERROR] gh auth login 이 필요합니다."
        exit 1
    }
}

cmd_create_repo() {
    local slug="${1:-$DEFAULT_REPO_SLUG}"
    ensure_gh
    if gh repo view "$slug" >/dev/null 2>&1; then
        echo "[INFO] 저장소가 이미 있습니다: https://github.com/${slug}"
        return 0
    fi
    echo "[INFO] Public 저장소 생성: $slug"
    gh repo create "$slug" --public \
        --description "델파이 웹 포팅 프로젝트 대시보드 (GitHub Pages)" \
        --disable-wiki --disable-issues
    echo "[OK] 생성 완료: https://github.com/${slug}"
}

cmd_enable_pages() {
    local slug="${1:-$DEFAULT_REPO_SLUG}"
    ensure_gh
    echo "[INFO] GitHub Pages 소스: GitHub Actions 로 설정 시도..."
    if gh api "repos/${slug}/pages" >/dev/null 2>&1; then
        echo "[INFO] Pages 사이트가 이미 있습니다. 웹에서 Source가 GitHub Actions인지 확인하세요."
        gh api "repos/${slug}/pages" -q '.build_type // .source // .' 2>/dev/null || true
        return 0
    fi
    gh api -X POST "repos/${slug}/pages" \
        -f build_type=workflow \
        && echo "[OK] Pages 활성화(build_type=workflow) 요청 완료." \
        || {
            echo "[WARN] API로 Pages 생성이 거부되었을 수 있습니다."
            echo "       https://github.com/${slug}/settings/pages 에서 Source → GitHub Actions 를 수동 선택하세요."
        }
}

cmd_bootstrap() {
    local slug="${1:-$DEFAULT_REPO_SLUG}"
    cmd_create_repo "$slug"
    local url
    url="$(normalize_repo_url "$slug")"
    cmd_init "$url"
    sleep 2
    cmd_enable_pages "$slug" || true
    echo ""
    echo "[OK] bootstrap 완료. Actions 실행 후 접속:"
    echo "    https://${slug%%/*}.github.io/${slug#*/}/"
}

cmd_prepare() {
    sync_files
    create_dashboard_workflow
    echo "[OK] prepare 완료: $DEPLOY_DIR (push 없음)"
}

cmd_init() {
    local repo_url
    repo_url="$(normalize_repo_url "$1")"
    local slug
    slug="$(repo_slug_from_url "$repo_url")"

    if [ -d "$DEPLOY_DIR/.git" ]; then
        echo "[INFO] 배포 디렉토리가 이미 존재합니다: $DEPLOY_DIR"
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
    git branch -M main

    if git push -u origin main 2>/dev/null; then
        echo "[OK] push 완료 (branch: main)"
    else
        echo "[ERROR] git push 실패. 저장소가 없으면 다음을 먼저 실행하세요:"
        echo "  ./tools/deploy_dashboard.sh create-repo $slug"
        echo "또는 GitHub 웹에서 Public 저장소를 만든 뒤 다시:"
        echo "  ./tools/deploy_dashboard.sh init $repo_url"
        exit 1
    fi

    echo ""
    echo "============================================"
    echo " 초기 배포 완료!"
    echo "============================================"
    echo ""
    echo "다음 단계 (한 번만):"
    echo "  ./tools/deploy_dashboard.sh enable-pages $slug"
    echo "  또는 https://github.com/${slug}/settings/pages → Source: GitHub Actions"
    echo ""
    echo "이후 업데이트:"
    echo "  ./tools/deploy_dashboard.sh sync"
    echo ""
}

cmd_sync() {
    if [ ! -d "$DEPLOY_DIR/.git" ]; then
        echo "[ERROR] 배포 디렉토리가 없습니다. 먼저 init을 실행해주세요."
        echo "  ./tools/deploy_dashboard.sh init <owner/repo 또는 URL>"
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
    local branch
    branch=$(git rev-parse --abbrev-ref HEAD)
    git push -u origin "$branch"

    echo ""
    echo "[OK] 대시보드가 업데이트되었습니다."
    echo "     GitHub Actions에서 자동 배포가 진행됩니다."
}

cmd_status() {
    echo "=== 대시보드 배포 상태 ==="
    echo ""

    if [ ! -d "$DEPLOY_DIR/.git" ]; then
        echo "[상태] 미설정 - init 또는 bootstrap을 실행하세요."
        echo "  ./tools/deploy_dashboard.sh bootstrap"
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
    git branch -vv
}

sync_files() {
    echo "[INFO] 대시보드 파일을 동기화합니다..."

    mkdir -p "$DEPLOY_DIR"

    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete \
            --exclude '.git' \
            --exclude '.github' \
            "$DASHBOARD_SRC/" "$DEPLOY_DIR/"
    else
        find "$DEPLOY_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' ! -name '.github' -exec rm -rf {} +
        cp -R "$DASHBOARD_SRC/"* "$DEPLOY_DIR/"
    fi

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
    cp "$PROJECT_ROOT/tools/templates/github-pages-deploy.yml" "$DEPLOY_DIR/.github/workflows/deploy.yml"
    echo "[OK] GitHub Actions 워크플로 생성 완료"
}

case "${1:-help}" in
    create-repo)
        cmd_create_repo "${2:-$DEFAULT_REPO_SLUG}"
        ;;
    enable-pages)
        cmd_enable_pages "${2:-$DEFAULT_REPO_SLUG}"
        ;;
    bootstrap)
        cmd_bootstrap "${2:-$DEFAULT_REPO_SLUG}"
        ;;
    prepare)
        cmd_prepare
        ;;
    init)
        if [ -z "${2:-}" ]; then
            echo "[ERROR] owner/repo 또는 URL을 지정해주세요."
            echo "  예: ./tools/deploy_dashboard.sh init speeno/delphi-dashboard"
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
