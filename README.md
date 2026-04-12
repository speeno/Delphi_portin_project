# 델파이 도서 물류 시스템 - 무중단 웹 포팅

8계층 하네스 엔지니어링 기반 델파이 → 웹 포팅 프로젝트

---

## 빠른 시작

### 1. 대시보드 로컬 실행

```bash
cd dashboard
# Python 내장 HTTP 서버로 실행 (CORS 문제 방지)
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

### 2. 대시보드 GitHub Pages 배포

```bash
# 1) GitHub에 저장소 생성 후
git remote add origin https://github.com/<계정>/Delphi_porting.git
git push -u origin master

# 2) GitHub 저장소 → Settings → Pages
#    Source: "Deploy from a branch"
#    Branch: master, Folder: /dashboard
#    Save 클릭
#
# 3) 약 1~2분 후 https://<계정>.github.io/Delphi_porting/ 에서 접속 가능
```

> **참고**: GitHub Pages의 루트를 `/dashboard`로 지정해야 합니다. 또는 `docs/` 폴더로 심볼릭 링크를 만들어도 됩니다.

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
│       ├── todos.json
│       ├── harness.json
│       ├── deliverables.json
│       ├── approvals.json
│       ├── risks.json
│       ├── timeline.json
│       └── eval-summary.json
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
    └── harness_runbook.md             ← 하네스 운영 런북
```

---

## 델파이 소스코드 입수 후 실행 가이드

### Step 1: 소스코드 배치

델파이 소스코드를 프로젝트 내 `delphi-source/` 폴더에 배치합니다:

```bash
mkdir -p delphi-source
# 델파이 소스코드를 이 폴더에 복사
cp -r /path/to/delphi/source/* delphi-source/
```

### Step 2: 전체 분석 파이프라인 실행 (1회)

```bash
# 전체 분석을 한 번에 실행
# 산출물 #1~#6 + Legacy Object Catalog 자동 생성
python3 tools/run_analysis.py delphi-source/
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

```bash
# 예: 스프린트 상태 변경
# dashboard/data/sprints.json 에서 해당 스프린트의 status/progress 수정

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
