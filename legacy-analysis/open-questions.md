# 미해결 질문 (Open Questions)

## 형식
각 질문은 아래 형식으로 기록한다:
- **ID**: OQ-XXX
- **질문**: 구체적 질문 내용
- **발생 시점**: 어떤 분석 중 발생했는가
- **영향 범위**: 이 질문이 해결되지 않으면 어디에 영향을 주는가
- **상태**: 미해결 / 조사중 / 해결됨
- **해결 방법**: (해결 시 기록)

---

## 미해결 목록

### OQ-001: 고객사 목록 및 커스터마이징 범위
- **질문**: 현재 운영 중인 고객사 수와 각 고객사별 커스터마이징 분기 지점은 어디인가?
- **발생 시점**: Sprint 0 계획 수립
- **영향 범위**: Customer Variant Matrix(산출물 #6), 멀티테넌시 설계
- **상태**: 미해결

### OQ-002: 장비 연동 방식 상세
- **질문**: 현장에서 사용하는 스캐너/프린터/저울의 모델과 연동 방식(HID/시리얼/네트워크)은 무엇인가?
- **발생 시점**: Sprint 0 계획 수립
- **영향 범위**: 장비 브리지 설계, Capture Harness 캡처 범위
- **상태**: 미해결
- **코드베이스 1차 조사 (레거시 소스)**: [`docs/legacy-print-scanner-integration-survey.md`](../docs/legacy-print-scanner-integration-survey.md) — 프린터(VCL/QuickReport/캔버스), COM 바코드(`Tong08`), 리포트 바코드 객체(`Tong06.dfm`) 확인. TWAIN/WIA 스캐너 API는 미발견.

### OQ-003: DB 서버 구성
- **질문**: 운영 DB 서버가 몇 대이며, 서버 간 스키마 차이가 있는가?
- **발생 시점**: Sprint 0 계획 수립
- **영향 범위**: DB Impact Matrix, 마이그레이션 전략
- **상태**: 미해결

### OQ-DBL-001: 3.23 인스턴스 DB 내 로직 확정
- **질문**: MySQL 3.23 인스턴스(154/155)에 저장 루틴·트리거·뷰가 실제로 없는지 DBA/현장 확인이 필요한가? (3.23은 기능 자체가 미지원이나, 추가 확인 필요 여부)
- **발생 시점**: DB 비즈니스 로직 1차 자동 조사 (2026-04-21)
- **영향 범위**: DB 로직 인벤토리 확정, GAP-002
- **상태**: 조사중
- **해결 방법**: (확인 시 기록)

### OQ-DBL-002: FK·CHECK·DEFAULT 등 선언적 규칙의 포팅 재현
- **질문**: 운영 DB에 FK·UNIQUE·CHECK 제약이 없는 것은 정상인가? 델파이 코드 측에서 참조 무결성·중복 방지를 전부 처리하고 있는가?
- **발생 시점**: DB 비즈니스 로직 1차 자동 조사 (2026-04-21)
- **영향 범위**: 웹 포팅 시 DB 제약 추가 여부 결정, GAP-003
- **상태**: 미해결

### OQ-DBL-003: 런타임 전용 SQL 캡처 미실시
- **질문**: 델파이 실행 중에만 발생하는 동적 SQL·배치 SQL이 정적 분석에서 누락되었을 수 있는가? 운영 리허설을 통한 query_capture 실시가 필요한가?
- **발생 시점**: DB 비즈니스 로직 1차 자동 조사 (2026-04-21)
- **영향 범위**: 포팅 누락 위험, GAP-001
- **해결 방법(2026-04-22 동결)**:
  1. `tools/db/db_logic_cross_reference.py` 정적 1차 실행 (53 테이블 교차맵) — 완료.
  2. C1 시나리오 운영 캡처 1회 (일반 로그인 + 슈퍼유저 0000) — `docs/query-capture-rehearsal-tracker.md` §1 일정 협의 중.
  3. 캡처 도착 즉시 `python3 tools/db/db_logic_cross_reference.py --capture <file>` 재실행 → 신규 SQL 발견 시 `migration/contracts/<flow>.yaml.data_access` 즉시 패치.
- **상태**: **부분 완화** (정적 교차맵 완료, 캡처 1회 대기 — 외부 의존)

### OQ-LOGIN-1: 멀티테넌시 배포·매핑 모델
- **질문**: 현행 운영은 고객사별로 EXE/Config.Ini 가 분리된 단일테넌트 모델이 맞는가? 웹은 한 인스턴스에 여러 고객사를 수용할 때 사용자→테넌트 매핑을 어디(DB 컬럼 / JWT claim / 서브도메인)에 두는가?
- **발생 시점**: C1 로그인 T3 보강 (Chul.pas L376~L427 정밀 분석, 2026-04-22)
- **영향 범위**: D-LOGIN-4(웹 contract), Customer Variant Matrix(산출물 #6), 모든 후속 시나리오의 컨텍스트 주입 정책
- **코드 근거**:
  - `legacy_delphi_source/legacy_source/Chul.pas` L376~L393 — `Config.Ini[Client]` → `nBase/nUses/nPcip/nPort` 클라이언트 PC 단위 로드
  - `legacy_delphi_source/legacy_source/Chul.pas` L420~L427 — `Base10.Database.Host/Login/Password/Database` EXE 내 base64 하드코딩(`MimeDecodeString`), 주석에 `한국도서유통` 등 다른 고객사 흔적
  - `Subu32_1.pas` 등 다른 폼은 `nBase` 전역만 참조 (사용자→테넌트 매핑 코드 없음)
- **결정 게이트**: approvals.json id 4 (고객사별 차이 승인)
- **상태**: 미해결

---
*최종 업데이트: 2026-04-22 — OQ-LOGIN-1 추가 (C1 T3 보강). (이전: OQ-002에 인쇄·바코드 조사 링크 추가 2026-04-21)*
