# 델파이 도서 물류 시스템 - 무중단 웹 포팅

8계층 하네스 엔지니어링 기반 델파이 → 웹 포팅 프로젝트

---

## 저장소 역할 및 CI·분석 전략

**한 문서로 정리**: [docs/repo-and-engineering-strategy.md](docs/repo-and-engineering-strategy.md) — GitHub **3저장소**(본 허브·제품 웹 `도서물류관리프로그램`·Public 대시보드), **브랜치·CI**, **레거시 분석**, **웹 플랫폼 방향**.

### 루트 `backend/`·`frontend/` vs `도서물류관리프로그램/`

허브 루트의 `backend/`·`frontend/`와 `도서물류관리프로그램/` 아래 동명 디렉터리는 **같은 제품 형상**을 두 군데에서 편집할 수 있는 구조입니다. 상위 [.gitignore](.gitignore)에 **`도서물류관리프로그램/`** 이 있어 **허브 Git에는 제품 폴더가 포함되지 않습니다**; 제품은 폴더 내부 **별도 `.git`**으로 관리합니다.

- **릴리즈·앱 전용 CI·PR**: [도서물류관리프로그램/README.md](도서물류관리프로그램/README.md) 기준 **제품 레포**에서 수행하는 것을 권장합니다.
- **허브**: 문서·하네스·`dashboard/`·`tools/` 중심. 웹 코드를 루트에서 수정했다면 제품 쪽과 **수동 동기**하거나, 팀 합의로 **서브모듈**·단일 소스만 유지하는 방식을 택합니다.
- 로컬 실행 경로는 제품 README의 `cd backend` / `cd frontend/public` 을 기준으로 맞춥니다.

---

## 빠른 시작

### 1. 대시보드 로컬 실행

```bash
cd dashboard
# Python 내장 HTTP 서버로 실행 (CORS 문제 방지)
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

### 2. 대시보드 GitHub Pages 무료 배포

메인 저장소(Private)와 대시보드 저장소(Public)를 분리하여 무료로 배포합니다.

**방법 A: 스크립트로 배포 (권장)**

저장소가 **아직 없으면** GraphQL/404 오류가 납니다. 아래 **bootstrap** 한 줄이 저장소 생성 → push → Pages(API) 활성화까지 순서대로 시도합니다 (`gh` 로그인 필요).

```bash
# 한 번에 (저장소 없을 때)
./tools/deploy_dashboard.sh bootstrap speeno/delphi-dashboard

# 또는 단계별
./tools/deploy_dashboard.sh create-repo speeno/delphi-dashboard
./tools/deploy_dashboard.sh init speeno/delphi-dashboard
./tools/deploy_dashboard.sh enable-pages speeno/delphi-dashboard

# 이후 대시보드(JSON·js·css 등) 수정 후 — 메인 저장소만 커밋하면 Pages는 갱신되지 않음
./tools/deploy_dashboard.sh sync

# 접속: https://speeno.github.io/delphi-dashboard/
```

Pages API가 거부되면: 해당 저장소 **Settings → Pages → Source: GitHub Actions** 를 수동으로 한 번 선택합니다.

로컬에만 복사(pull 없음): `./tools/deploy_dashboard.sh prepare`

#### push 후 대시보드 자동 반영 (택일)

| 방식 | 설명 |
|------|------|
| **GitHub Actions** | 메인 저장소에 `dashboard/**` (또는 Pages 템플릿) 변경을 **push**하면, CI가 Public `delphi-dashboard`에 rsync 후 push. **Secrets**에 `DASHBOARD_DEPLOY_TOKEN`(classic PAT, `repo` 권한) 등록 필요. 선택: **Variables** `DASHBOARD_REPO`(기본 `speeno/delphi-dashboard`). 워크플로: [.github/workflows/deploy-dashboard.yml](.github/workflows/deploy-dashboard.yml). 토큰이 없으면 워크플로는 경고만 내고 종료합니다. |
| **로컬 한 줄** | `git push` 직후 같은 머신에서 `sync`까지 실행: `./tools/push_with_dashboard_sync.sh` (인자는 `git push`와 동일, 예: `origin main`). **선행**: `./tools/deploy_dashboard.sh init …`로 `../delphi-dashboard` 클론·remote가 이미 있어야 합니다. |

**방법 B: 수동 배포**

```bash
# 1) 대시보드 파일만 별도 디렉토리로 복사
mkdir -p ../delphi-dashboard
cp -r dashboard/* ../delphi-dashboard/

# 2) Git 초기화 + Public 저장소로 push
cd ../delphi-dashboard
git init && git add -A
git commit -m "Dashboard deploy"
git remote add origin https://github.com/<계정>/delphi-dashboard.git
git push -u origin master

# 3) GitHub → Settings → Pages → Source: "GitHub Actions" → Save
```

> **참고**: 무료 계정에서 GitHub Pages는 Public 저장소에서만 사용 가능합니다. 대시보드에는 민감한 코드가 포함되지 않으므로 Public으로 공개해도 안전합니다.

#### Actions 배포가 404로 실패할 때 (`Failed to create deployment`)

워크플로는 정상인데 **`deploy-pages` 단계만 404**이면, 거의 항상 **해당 Public 저장소에서 Pages가 아직 “GitHub Actions”로 켜지지 않은 상태**입니다.

1. 브라우저에서 열기: `https://github.com/<계정>/delphi-dashboard/settings/pages`
2. **Build and deployment** → **Source**를 **Deploy from a branch**가 아니라 **GitHub Actions**로 변경
3. **Save**
4. 저장소 **Actions** 탭 → 실패한 워크플로 → **Re-run all jobs**

CLI로 시도(저장소 관리 권한·`gh` 로그인 필요):

```bash
gh api -X POST repos/speeno/delphi-dashboard/pages -f build_type=workflow
```

처음 실행 시 **Actions**에서 `github-pages` 환경 배포 승인을 요청하면 **Review deployments**에서 승인해야 할 수 있습니다.

---

## 프로젝트 구조

```
Delphi_porting/
│
├── README.md                          ← 이 파일 (사용 가이드)
├── harness-architecture.md            ← 8계층 하네스 설계 문서
├── guardrails.md                      ← 가드레일(L5) - 금지 사항 목록
│
├── legacy-analysis/                   ← 상태 추적(L6) 파일
│   ├── progress.md                    ← 분석 진행 상태
│   ├── open-questions.md              ← 미해결 질문
│   ├── decisions.md                   ← 의사결정 기록
│   └── known-risks.md                 ← 알려진 위험
│
├── WeLove_FTP/                      ← 델파이 소스 1차 확보 트리 (.pas/.dfm/.dpr 등, 다중 고객·변형 경로)
│
├── templates/                         ← AI 작업 지시 템플릿
│   ├── feature_input_template.yaml    ← 기능 단위 입력 템플릿
│   └── ai_task_template.md            ← AI 작업 지시 템플릿
│
├── migration/                         ← 마이그레이션 산출물
│   ├── contracts/                     ← API 계약서 (YAML)
│   └── test-cases/                    ← 평가 케이스 (JSON)
│
├── inventory/                         ← 자산 인벤토리 (분석 결과)
├── analysis/                          ← 정적 분석 결과
│
├── tools/                             ← 분석/하네스 도구
│   ├── parsers/                       ← 델파이 소스 파서
│   │   ├── dpr_parser.py              ← .dpr 파일 파서
│   │   ├── pas_parser.py              ← .pas 파일 파서
│   │   └── dfm_parser.py              ← .dfm 파일 파서
│   ├── db/                            ← DB 분석 도구
│   │   ├── schema_extractor.py        ← MariaDB 스키마 추출기
│   │   ├── query_capture.py           ← 쿼리 캡처 파이프라인
│   │   └── db_impact_builder.py       ← DB Impact Matrix 빌더
│   ├── contracts/                     ← 계약/평가 생성기
│   │   ├── contract_generator.py      ← Migration Contract 생성기
│   │   └── eval_case_generator.py     ← Eval Case 생성기
│   ├── harness/                       ← 하네스 코어
│   │   ├── routing_harness.py         ← Routing Harness (프록시)
│   │   ├── comparison_harness.py      ← Comparison Harness (비교)
│   │   ├── golden_master.py           ← Golden Master (스냅샷)
│   │   ├── characterization_test.py   ← Characterization Test 생성
│   │   ├── eval_runner.py             ← 5축 평가 실행기
│   │   ├── pipeline.py                ← 통합 파이프라인
│   │   ├── go_nogo.py                 ← Go/No-Go 자동 판단
│   │   ├── progressive_rollout.py     ← 점진적 전환 관리
│   │   ├── operationalize.py          ← 운영 인프라 전환
│   │   ├── final_report.py            ← 최종 보고서 생성
│   │   └── routing_config.json        ← 라우팅 설정
│   ├── catalog_builder.py             ← Legacy Object Catalog 빌더
│   └── run_analysis.py                ← 전체 분석 파이프라인
│
├── dashboard/                         ← 프로젝트 관리 대시보드
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   └── data/                          ← JSON 데이터 (상태 관리)
│       ├── project.json
│       ├── sprints.json
│       ├── release-milestones.json   ← 오픈 단계 마일스톤(베타·내부·공식); 일정은 sprintIds→sprints.json과 동기화
│       ├── todos.json
│       ├── harness.json
│       ├── deliverables.json
│       ├── approvals.json
│       ├── risks.json
│       ├── timeline.json
│       ├── eval-summary.json
│       └── db-status.json              ← MariaDB 호스트별 연결 프로브 결과(비밀 없음); 갱신: debug/db_connect_probe.py
│
├── backend/                           ← 웹 API 서버 (FastAPI)
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── api/                       ← 입고/출고/재고/인증 API
│       ├── middleware/                 ← 하네스 미들웨어
│       ├── services/
│       └── models/
│
├── frontend/                          ← 프론트엔드 (Vanilla JS)
│   ├── public/index.html
│   └── src/
│       ├── components/                ← Layout, DataTable, ScannerInput
│       └── utils/api.js               ← API 클라이언트
│
└── docs/                              ← 운영 문서
    ├── harness_runbook.md             ← 하네스 운영 런북
    ├── delphi-source-analysis-procedure.md
    └── mysql-3.23-legacy-connection-notes.md  ← 154/155 MySQL 3.23 접속 호환 테스트 메모
```

---

## 델파이 소스코드 입수 후 실행 가이드

**현재(1차)**: 레거시 소스는 저장소 루트 [`WeLove_FTP/`](WeLove_FTP/) 에 확보된 상태입니다(도서유통-New·도서유통-출판 등 복수 트리). 대시보드 상단 **레거시 소스 위치**·**확보 현황**·달력 타임라인(2026-04-13 자산 이벤트)과 [`legacy-analysis/progress.md`](legacy-analysis/progress.md)에 동일 내용이 반영됩니다. 분석 파이프라인에 넣기 전에 대표 경로 선정·백업 파일(`.~pas`, `.dcu` 등) 제외 정책을 잡는 것을 권장합니다.

### Step 1: 소스코드 배치

권장: 분석 전용으로 `delphi-source/` 에 **대표 소스만** 복사하거나, 1차 트리를 그대로 쓸 경우 경로만 바꿉니다.

```bash
mkdir -p delphi-source
# 예: 1차 확보 트리에서 대표만 복사
# cp -r WeLove_FTP/도서유통-New/일부경로/* delphi-source/
# 또는 전체 스캔(용량·중복 많음 — 정책 수립 후)
# cp -r /path/to/delphi/source/* delphi-source/
```

### Step 2: 전체 분석 파이프라인 실행 (1회)

```bash
# 전체 분석을 한 번에 실행
# 산출물 #1~#6 + Legacy Object Catalog 자동 생성
python3 tools/run_analysis.py delphi-source/
# 1차 트리 직접 지정 시(용량·중복 주의): python3 tools/run_analysis.py WeLove_FTP/
```

실행 결과:
- `inventory/dpr_files.json` - 프로젝트 파일 목록
- `analysis/form_inventory.json` - **산출물 #1** 폼 인벤토리
- `analysis/event_flow.json` - **산출물 #2** 이벤트 흐름 맵
- `analysis/query_catalog.json` - **산출물 #3** SQL 카탈로그
- `analysis/validation_rules.json` - **산출물 #5** 검증 규칙
- `analysis/customer_variants.json` - **산출물 #6** 고객사 분기
- `analysis/legacy_object_catalog.json` - Legacy Object Catalog
- `analysis/unit_dependency_graph.json` - 유닛 의존 관계 그래프

### Step 3: 개별 파서 실행 (필요 시)

```bash
# .dpr 파서만 실행
python3 tools/parsers/dpr_parser.py delphi-source/ inventory/dpr_files.json

# .pas 파서만 실행 (SQL, 이벤트, 검증, 고객사 분기 추출)
python3 tools/parsers/pas_parser.py delphi-source/ analysis/

# .dfm 파서만 실행 (폼 인벤토리, 이벤트 바인딩)
python3 tools/parsers/dfm_parser.py delphi-source/ analysis/
```

### Step 4: Legacy Object Catalog 빌더

```bash
# 분석 결과를 통합하여 Legacy Object Catalog 생성
python3 tools/catalog_builder.py analysis/ analysis/legacy_object_catalog.json
```

---

## DB 정보 입수 후 실행 가이드

접속 호스트·계정·비밀번호는 **저장소에 커밋하지 말고** 로컬 `.env`에만 두세요. 변수 예시는 루트 [`.env.example`](.env.example)를 참고합니다.

### Step 1: DB 스키마 추출

```bash
pip install mysql-connector-python

python3 tools/db/schema_extractor.py \
  --host <DB호스트> \
  --port 3306 \
  --user <사용자> \
  --password <비밀번호> \
  --database <데이터베이스명> \
  --output analysis/
```

실행 결과:
- `analysis/tables.json` - 테이블 목록
- `analysis/columns.json` - 컬럼 정보
- `analysis/keys.json` - PK/FK 관계
- `analysis/indexes.json` - 인덱스
- `analysis/routines.json` - 프로시저/함수
- `analysis/triggers.json` - 트리거
- `analysis/views.json` - 뷰
- `analysis/db_impact_matrix.json` - **산출물 #4** DB 영향도 매트릭스

### Step 2: DB Impact Matrix 빌드

```bash
# SQL 카탈로그 + DB 스키마를 결합하여 DB 영향도 매트릭스 생성
python3 tools/db/db_impact_builder.py analysis/ analysis/db_impact_matrix_full.json
```

### Step 3: 쿼리 캡처 (Capture Harness)

```bash
# 방법 1: General Log 파일 모니터링
python3 tools/db/query_capture.py \
  --mode file \
  --log-path /var/log/mysql/general.log \
  --output captured/queries.json

# 방법 2: General Log 테이블에서 읽기
python3 tools/db/query_capture.py \
  --mode table \
  --host <DB호스트> \
  --user <사용자> \
  --password <비밀번호> \
  --output captured/queries.json
```

> **주의**: 쿼리 캡처 전에 MariaDB에서 `SET GLOBAL general_log = 'ON';`을 실행해야 합니다.

---

## Migration Contract & Eval Case 생성

### Step 1: Migration Contract 생성

```bash
# Legacy Object Catalog를 기반으로 API 계약 자동 생성
python3 tools/contracts/contract_generator.py \
  analysis/legacy_object_catalog.json \
  migration/contracts/
```

### Step 2: Eval Case 생성

```bash
# 계약과 카탈로그를 기반으로 5축 평가 케이스 자동 생성
python3 tools/contracts/eval_case_generator.py \
  analysis/legacy_object_catalog.json \
  migration/contracts/ \
  migration/test-cases/
```

### Step 3: Characterization Test 생성

```bash
# 캡처된 쿼리에서 현재 동작을 기록하는 테스트 자동 생성
python3 tools/harness/characterization_test.py \
  captured/queries.json \
  migration/test-cases/
```

---

## 백엔드 API 서버 실행

```bash
cd backend
pip install -r requirements.txt

# 개발 모드 실행
uvicorn app.main:app --reload --port 8082

# API 문서 확인: http://localhost:8082/docs
```

---

## 하네스 도구 사용법

### Routing Harness (트래픽 분기)

```bash
# 기본 설정 생성
python3 tools/harness/routing_harness.py init

# 설정 파일 편집: tools/harness/routing_config.json
# mode: "legacy_only" | "percent" | "feature_toggle" | "mirror" | "new_only"
```

### Comparison Harness (신/구 비교)

```bash
# 비교 테스트 실행 (스크립트 내 테스트)
python3 tools/harness/comparison_harness.py
```

### Golden Master (DB 스냅샷 비교)

```bash
# 스냅샷 캡처
python3 tools/harness/golden_master.py capture \
  --config capture_config.json \
  --output snapshots/before.json

# 스냅샷 비교
python3 tools/harness/golden_master.py compare \
  --before snapshots/before.json \
  --after snapshots/after.json \
  --output reports/comparison.json
```

### 5축 평가 실행

```bash
python3 tools/harness/eval_runner.py \
  migration/test-cases/ \
  http://localhost:8082 \
  --output reports/eval_report.json
```

### 통합 파이프라인

```bash
python3 tools/harness/pipeline.py \
  --capture-dir captured/ \
  --eval-dir migration/test-cases/ \
  --comparison-dir comparison_results/ \
  --routing-config tools/harness/routing_config.json \
  --output reports/pipeline_report.json \
  --dashboard-output dashboard/data/pipeline.json
```

### Go/No-Go 판단

```bash
python3 tools/harness/go_nogo.py \
  --comparison-dir comparison_results/ \
  --eval-report reports/eval_report.json \
  --routing-config tools/harness/routing_config.json \
  --approvals dashboard/data/approvals.json \
  --output reports/go_nogo.json
```

### 점진적 전환 관리

```bash
# 현재 상태 확인
python3 tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --comparison-dir comparison_results/ \
  --action status

# 다음 단계로 전환 (10% → 30% → 50% → 80% → 100%)
python3 tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --comparison-dir comparison_results/ \
  --action next

# 긴급 롤백
python3 tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --action rollback \
  --reason "긴급 롤백 사유"
```

---

## 대시보드 데이터 업데이트

대시보드는 `dashboard/data/` 폴더의 JSON 파일을 수정하면 반영됩니다.

**일정·진행 달력**: `dashboard/data/sprints.json`의 각 스프린트 `startDate`·`endDate`, `approvals.json`의 `plannedDate`, `timeline.json`의 `date`가 달력에 반영됩니다. 기간을 바꿀 때는 위 필드를 함께 수정하세요.

**오픈 단계 마일스톤**: `dashboard/data/release-milestones.json`의 각 단계(`beta` / `internal_open` / `official_open`)는 `sprintIds`로 스프린트를 가리킵니다. 대시보드에 표시되는 **계획 완료일**은 해당 id들의 `sprints.json` **`endDate` 중 가장 늦은 날**로 자동 계산되며, 달력의 오픈 마일스톤 점·날짜 상세에도 같은 값이 쓰입니다. 스프린트 일정만 `sprints.json`에서 바꾸면 마일스톤 표시 일정이 다음 로드 시 함께 갱신되므로, 별도 목표 날짜 필드를 이중으로 맞출 필요가 없습니다. 단계별 문구·상태·`sprintIds` 매핑은 `release-milestones.json`에서 편집합니다.

```bash
# 예: 스프린트 상태 변경
# dashboard/data/sprints.json 에서 해당 스프린트의 status/progress 및 startDate/endDate 수정

# 예: 체크리스트 항목 완료
# dashboard/data/todos.json 에서 해당 task의 done: true로 변경

# 변경 후 배포
git add dashboard/data/
git commit -m "Update dashboard: Sprint 1 진행률 반영"
git push
# → GitHub Pages 자동 갱신 (1~2분 소요)
```

---

## 의존성

### Python (3.10+)
```bash
pip install mysql-connector-python  # DB 연동 시
pip install fastapi uvicorn httpx   # 백엔드 API 서버 실행 시
```

### 대시보드
- 의존성 없음 (순수 HTML/CSS/JS)
- Python 3 내장 HTTP 서버로 로컬 실행 가능

---

## 주요 워크플로우 요약

```
[소스코드 입수] → run_analysis.py → 10대 산출물 생성
                                         ↓
[DB 정보 입수] → schema_extractor.py → DB 스키마 추출
                → query_capture.py   → 쿼리 캡처
                                         ↓
             contract_generator.py → Migration Contract 생성
             eval_case_generator.py → Eval Case 생성
                                         ↓
             백엔드 API 구현 (backend/)
             프론트엔드 구현 (frontend/)
                                         ↓
             pipeline.py → Capture → Test → Compare → Route
             go_nogo.py  → 전환 가능 여부 자동 판단
             progressive_rollout.py → 점진적 전환 (0% → 100%)
                                         ↓
             operationalize.py → 하네스 → 운영 인프라 전환
             final_report.py   → 최종 보고서 생성
```
