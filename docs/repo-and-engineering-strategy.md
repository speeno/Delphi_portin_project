# 저장소·브랜치·CI/CD 및 레거시 분석·웹 플랫폼 전략

이 문서는 **GitHub 저장소 골격**, **브랜치·CI 운영**, **레거시(델파이) 분석 방향**, **웹 제품 구현 방향**을 한곳에서 맞추기 위한 상위 기준입니다. 세부 절차는 링크된 문서를 따릅니다.

## 1. 저장소 3층 구조 (역할 분리)

| 저장소 | 역할 | 주요 내용 |
|--------|------|-----------|
| **Delphi_porting (본 허브)** | 분석·하네스·계약·도구·진행 대시보드 **소스** | `tools/`, `migration/`, `legacy-analysis/`, `docs/`, `dashboard/`(동기 소스), `harness-architecture.md`, `guardrails.md` |
| **도서물류관리프로그램 (제품 웹)** | 실서비스에 가까운 **웹 앱** 형상·CI·릴리즈 | `backend/`(FastAPI), `frontend/`(Vanilla JS). 원격은 **별도 GitHub 저장소** 권장(아래「중복 정책」). |
| **delphi-dashboard (Public)** | **진행·지표** GitHub Pages | 메인 허브의 `dashboard/**`를 [deploy-dashboard 워크플로](../.github/workflows/deploy-dashboard.yml)로 동기화. 앱 배포와 무관. |

**이슈·PR 규칙(권장)**

- 레거시 파서·산출물·하네스·대시보드 JSON: **허브** 저장소.
- API·UI·배포·런타임 버그: **제품 웹** 저장소.
- Pages 배포·대시보드 UI만: 허브에서 `dashboard/` 수정 → sync.

## 2. 브랜치 전략 (허브·제품 공통 권장)

- 기본 브랜치: **`main`** (GitHub **Branch protection**: PR 필수, 필수 status check 이름은 CI job `name`과 일치).
- 일상 개발: **`feature/<주제>`** → PR → squash merge(팀 합의).
- 릴리즈 태그: 제품 레포에서 `v0.1.0` 형식 권장.

## 3. CI/CD 골격

### 3.1 제품 웹 (`도서물류관리프로그램/`)

- [`.github/workflows/ci.yml`](../도서물류관리프로그램/.github/workflows/ci.yml): `push`/`pull_request` on `main`.
- 단계: Python 의존성 설치 → `compileall` 또는 `ruff`(도입 시) → (테스트 추가 시 `pytest`).
- 프론트: 추후 `eslint`/빌드 스텝 추가 가능.

### 3.2 허브 (Delphi_porting)

- [`.github/workflows/tools-smoke.yml`](../.github/workflows/tools-smoke.yml): `tools/parsers` 등 **경량 스모크**(문법·import 수준). DB·대용량 소스 없이 동작.
- 기존 [deploy-dashboard.yml](../.github/workflows/deploy-dashboard.yml): `dashboard/**` 변경 시 Public 저장소 sync 유지.

### 3.3 배포(운영)

- k8s·VM·컨테이너 레지스트리 등 **운영 배포 파이프라인**은 별도 설계(본 문서 범위 밖). 제품 레포에 `deploy-*.yml` 추가 시 Environments·Secrets 분리.

## 4. 웹 플랫폼 구현 방향

- **현재 스택**: FastAPI + Vanilla JS, Routing/Comparison 하네스와 API 클라이언트 연동([`frontend/src/utils/api.js`](../frontend/src/utils/api.js)).
- **동등성**: 화면·API는 **Migration Contract·Eval Case·회귀 하네스**로 검증([harness-architecture.md](../harness-architecture.md), [harness_runbook.md](harness_runbook.md)).
- **선택적 진화**(후속): 프론트 프레임워크 도입, 컨테이너 이미지, `staging` 환경 — 결정 시 본 절에 한 줄 추가.

## 5. 레거시 코드 분석 — 방향·방법·전략

### 5.1 범위·입력

- 소스 트리: [`WeLove_FTP/`](../WeLove_FTP/) 1차 반입(다중 변형). **대표 분석 루트** 선정·`.dcu`/`.~pas` 등 제외 정책: [delphi-source-analysis-procedure.md](delphi-source-analysis-procedure.md) §1.

### 5.2 정적 분석 (L2)

- [`tools/run_analysis.py`](../tools/run_analysis.py) → `inventory/`, `analysis/` 산출물 #1~#6 및 카탈로그. 절차: [delphi-source-analysis-procedure.md](delphi-source-analysis-procedure.md) §2~3.

### 5.3 DB

- 호스트 4대: 모던 클라이언트 vs **MySQL 3.23.58** — POC·`pocStatus`는 [db-status.json](../dashboard/data/db-status.json), 상세는 [mysql-3.23-legacy-connection-notes.md](mysql-3.23-legacy-connection-notes.md).
- **스키마·산출물 #4**: `schema_extractor`는 모던 프로토콜 전제; 3.23은 **서버측 덤프 또는 전용 클라이언트** 분기(문서「후속 작업」).

### 5.4 하네스·포팅 순서

- 8계층 L1~L7과 산출물 매핑: [harness-architecture.md](../harness-architecture.md), 운영 절차: [harness_runbook.md](harness_runbook.md).

## 6. 제품 레포 로컬 정리 (Git)

`도서물류관리프로그램/` 디렉터리는 상위 `.gitignore`로 **허브 저장소에 커밋되지 않으며**, 내부에 **독립 `.git`**이 있습니다.

```bash
cd 도서물류관리프로그램
git status
git branch   # main 권장
git remote add origin https://github.com/<org>/<product-repo>.git
git push -u origin main
```

초기 커밋이 없으면: `git add -A && git commit -m "chore: initial product repo"`.  
샌드박스·권한 문제 시 로컬 터미널에서 동일 명령 실행.

## 7. 문서 유지

브랜치 규칙·저장소 URL·CI job 이름이 바뀌면 본 문서와 [README.md](../README.md)의 링크를 함께 수정합니다.
