# 분석 진행 상태

## 현재 단계: Sprint 1 - 분석 하네스

### 확보 완료
- [x] 델파이 소스 **1차** 확보 — 레포지토리 [`WeLove_FTP/`](../WeLove_FTP/) (도서유통-New·도서유통-출판 등, 고객사·빌드 변형 다수)
- [ ] 델파이 소스 **정리·단일 분석 루트** 확정 (`delphi-source/` 또는 `WeLove_FTP/` 내 대표 트리 선정, `.dcu`/`.~pas` 등 스캔 제외 정책)
- [x] DB 서버 접근 정보 확보 (MariaDB) — 후보 호스트 4대(115.68.3.153, 115.68.3.154, 115.68.3.155, 115.68.7.138). DB명·포트(기본 3306)·역할(마스터/슬레이브 등)은 합의 후 기록. **계정·비밀번호는 `.env`에만 저장**(Git 미추적).
- [x] MariaDB **호스트별 프로브·접속 검증** — `dashboard/data/db-status.json`. **4/4대** 접속·쿼리 테스트 성공. 153·138은 utf8 모던 클라이언트. 154·155는 MySQL 3.23.58 전용 호환(`pymysql_compat` 등, [`docs/mysql-3.23-legacy-connection-notes.md`](../docs/mysql-3.23-legacy-connection-notes.md)).
- [x] MariaDB **접속·쿼리 POC** — 4대 구현·연동 확인 완료(`db-status.json` pocStatus). 모던(153·138) + 3.23 전용(154·155, [문서](../docs/mysql-3.23-legacy-connection-notes.md)).
- [ ] MariaDB **스키마 추출·산출물 #4** — 모던 인스턴스는 `schema_extractor`(utf8). 3.23 인스턴스는 버전별 덤프/별도 도구 합의 후 진행.
- [x] DFM 텍스트 파일이 트리 내에 존재(백업 `.~dfm` 등 혼재)

### Sprint 0 진행 상황
- [x] 프로젝트 폴더 구조 생성
- [x] 상태 추적(L6) 파일 체계 구축
- [x] Git 저장소 초기화
- [x] 8계층 하네스 설계 문서 작성 (harness-architecture.md)
- [x] 가드레일(L5) 문서 확정 (guardrails.md)
- [x] AI 작업 지시 템플릿 + 기능 단위 입력 템플릿 확정 (templates/)
- [x] 대시보드 v1 구축 (dashboard/)
- [x] 대시보드 JSON 데이터 파일 생성 (9개)
- [ ] 델파이 소스 인벤토리 작성 (`WeLove_FTP/` 기준 스캔·대표 루트 합의 후)

### Sprint 1 진행 상황
- [x] 정적 분석(L2) 도구 구현 (tools/parsers/)
  - [x] DPR 파서 (dpr_parser.py) - 프로젝트 구조, uses 절, 의존 관계
  - [x] PAS 파서 (pas_parser.py) - SQL, 이벤트 핸들러, 검증 규칙, 고객사 분기
  - [x] DFM 파서 (dfm_parser.py) - 폼 인벤토리, 이벤트 바인딩
- [x] 실행 도구(L4) 구현
  - [x] DB 스키마 추출기 (tools/db/schema_extractor.py)
  - [x] DB 쿼리 캡처 파이프라인 (tools/db/query_capture.py)
  - [x] DB Impact Matrix 빌더 (tools/db/db_impact_builder.py)
- [x] Legacy Object Catalog 빌더 (tools/catalog_builder.py)
- [x] 전체 분석 파이프라인 실행기 (tools/run_analysis.py)
- [ ] 실제 소스에 대한 분석 실행 (소스코드 import 후)

### Sprint 2 진행 상황
- [x] Migration Contract 생성기 (tools/contracts/contract_generator.py)
- [x] Eval Case 생성기 (tools/contracts/eval_case_generator.py)
- [x] Golden Master / Test Harness (tools/harness/golden_master.py)
- [x] Characterization Test 생성기 (tools/harness/characterization_test.py)

### Sprint 3 진행 상황
- [x] Routing Harness 구현 (tools/harness/routing_harness.py)
- [x] Comparison Harness 구현 (tools/harness/comparison_harness.py)
- [x] 5축 평가 실행기 (tools/harness/eval_runner.py)
- [x] 라우팅 설정 파일 (tools/harness/routing_config.json)

### Sprint 4 진행 상황
- [x] 백엔드 API 보일러플레이트 (backend/app/)
  - [x] Health/Auth/Inbound/Outbound/Inventory API
  - [x] 하네스 미들웨어 (요청 추적, 시간 측정)
- [x] 프론트엔드 공통 컴포넌트 (frontend/src/)
  - [x] Layout, DataTable, ScannerInput
  - [x] API 클라이언트 (Routing Harness 연동)
- [x] 4계층 하네스 통합 파이프라인 (tools/harness/pipeline.py)

### Sprint 5 진행 상황
- [x] Go/No-Go 판단 자동화 (tools/harness/go_nogo.py)
- [x] 점진적 전환 관리자 (tools/harness/progressive_rollout.py)
- [x] 하네스 운영 런북 (docs/harness_runbook.md)

### Sprint 6 진행 상황
- [x] 하네스 → 운영 인프라 전환 (tools/harness/operationalize.py)
  - [x] Capture → Audit Log
  - [x] Comparison → CI 회귀 테스트
  - [x] Test → CI/CD 자동 테스트
  - [x] Routing → Canary 배포
- [x] 최종 완료 보고서 생성기 (tools/harness/final_report.py)

### 분석 대상 요약
- 소스 트리(1차): `WeLove_FTP/` (하위 다중 제품·변형 경로)
- 소스 유형: .dpr, .pas, .dfm (+ 컴파일 산출 .dcu 등, 분석 시 제외 권장)
- DB: MariaDB/MySQL — 호스트 4대 **접속·쿼리 POC 완료·연동 확인**(`db-status.json`). 스키마·#4는 버전별 전략.
- 빌드/구동: 환경별 확인 필요

---
*최종 업데이트: 4대 DB 접속·쿼리 검증 완료(154/155 MySQL 3.23 호환 메모 docs 반영)*
