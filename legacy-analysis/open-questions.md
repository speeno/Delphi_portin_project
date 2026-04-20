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
- **상태**: **추가 해소 (2026-04-20, C8 Phase 1)** — 바코드 스캐너 분기는 DEC-004 + DEC-040 으로 동결 (USB-HID 키보드 웨지 1차, `lib/scanner.ts` keydown+CR+디바운스). 라벨 프린터 직결 + Web Serial 직결 + 저울만 잔여 → **OQ-002-R** 로 분리 (Phase 2 이후).
- **코드베이스 1차 조사 (레거시 소스)**: [`docs/legacy-print-scanner-integration-survey.md`](../docs/legacy-print-scanner-integration-survey.md) — 프린터(VCL/QuickReport/캔버스), COM 바코드(`Tong08`), 리포트 바코드 객체(`Tong06.dfm`) 확인. TWAIN/WIA 스캐너 API는 미발견.
- **C7 Phase 1 결과 (2026-04-20)**: PDF 다운로드 = WeasyPrint(Python) 단일 엔진 (DEC-037), 라벨 = 우편엽서 1종 (DEC-038), `.frf` 정본 = 참조용 (DEC-039 / T9 카탈로그). 직결 프린터·라벨 프린터 드라이버 연동은 본 페이즈 out-of-scope.
- **C8 Phase 1 결과 (2026-04-20)**: USB-HID 키보드 웨지 채택 (DEC-004 = 1차 정책). `POST /api/v1/scan/match` 1 엔드포인트로 G4_Book 매칭 + G1/G2_Ggeo 단가 폴백 (DEC-040). 출고/입고/반품 3 화면에 단일 `ScanInput` 공통 컴포넌트 통합 (DEC-028 룰 7). Web Serial 직결은 **OQ-002-R 잔류**.

### OQ-002-R: 라벨 프린터 직결 + Web Serial 스캐너 직결 + 저울 통합 (잔여)
- **분리 일자**: 2026-04-20 (C8 Phase 1 마감 시점)
- **잔여 항목**: (a) 라벨 프린터 직결 (Zebra/Brother 등 ZPL/DPL 스트림 직접 송신), (b) Web Serial API (Chromium 89+) 로 USB 시리얼 스캐너 직결, (c) 저울 (시리얼/USB 로 무게 자동 입력) 의 모던 포팅 방식.
- **현재 우회**: (a) 모든 라벨/송장 = WeasyPrint PDF 다운로드 후 OS 인쇄 (DEC-037), (b) 모든 스캐너 = USB-HID 키보드 웨지 (DEC-004 / `lib/scanner.ts`), (c) 저울 = 수기 입력.
- **Phase 2 트리거**: 라벨 프린터 직결 1건 이상 운영 요구 발생, 또는 Web Serial 호환 브라우저 시장 점유 90%+ 달성, 또는 저울 자동 입력 누락 비용 > 도입 비용.
- **참조**: DEC-004, DEC-040, `analysis/regression/c8_phase1.md` §6 운영 배포 체크.

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
- **상태**: **후속 이관 (1차 포팅 범위 외)**
- **결정(2026-04-22)**: **DEC-008** — 1차 포팅은 단일 테넌트 운영(레거시와 동일한 고객사별 별도 인스턴스 모델 유지). 1차 합격선 "기존 사용자가 기존 ID/PW 로 그대로 로그인" 단순화 우선. 멀티테넌시(옵션 A/B/C 합의) 는 후속 사이클에서 별도 결정 DEC-XXX 로 동결 후 도입.
- **후속 작업**: 멀티테넌시 합의 사이클이 시작될 때 (1) 옵션 A/B/C 비교 (2) Id_Logn 스키마 변경 또는 user_tenant 매핑 테이블 (3) 모든 후속 API 의 RLS 필터 패치 (4) TC-LOGIN-010/012 phase1_in_scope=true 로 전환.

### OQ-OUT-1: Yesno enum 운영 분기
- **질문**: `S1_Ssub.Yesno` 의 '0'(미처리)/'1'(처리완료)/'2'(취소) 중 '1' 처리완료 흐름이 실 운영에 사용되는가? (별도 화면 또는 배치 트리거?)
- **발생 시점**: C2 출고 접수 1차 포팅 (2026-04-25, `analysis/c2_outbound_flow.md` §6)
- **영향 범위**: SQL-OUT-5 CANCEL 의 WHERE 에 `Yesno='1'` 제한 복원 여부 (Subu27.pas L655 `@Yesoo='1'`)
- **상태**: **후속 이관** — 1차는 단순화 ('2' = cancelled, 그 외 active). 운영 검증 후 OQ-OUT-1 closure → SQL-OUT-5 패치.

### OQ-OUT-2: Sg_Csum 트리거 존재 여부
- **질문**: Sobo67(출고현황) 에서만 보이는 `Sg_Csum` 집계 테이블이 `S1_Ssub` INSERT/UPDATE 시 트리거로 자동 갱신되는가? 아니면 배치/별도 화면에서 갱신되는가?
- **발생 시점**: C2 1차 포팅 (`query_catalog.json` 정적 분석에서 TSobo27 의 Sg_Csum 미접근 확인)
- **영향 범위**: 1차에서는 Sg_Csum 미접근으로 충분하지만, 트리거가 있다면 데이터 무결성 의존이 운영 DB 에 잠재. 후속 Sobo67 사이클에서 명시적 동기화 필요 여부.
- **상태**: **후속 이관** — Sobo67 분석 사이클에서 closure.

### OQ-OUT-3: 합성키 동시성
- **질문**: 동일 `(Gdate, Hcode)` 에 1초 내 동시 신규 등록 시 자동 채번 `jubun` 충돌이 운영에서 발생할 가능성이 있는가?
- **발생 시점**: C2 1차 포팅 (analysis/c2_outbound_flow.md §4.1)
- **영향 범위**: SQL-OUT-1 INSERT 충돌 → 500 OUT_TX_FAILED. 1차는 마이크로초 자동 채번으로 회피, 2차에서 UNIQUE + retry 패턴 검토.
- **상태**: **부분 완화** (마이크로초 채번으로 1차 운영 안정), **후속 이관** (UNIQUE 제약 + retry 패턴 정식화).

### OQ-OUT-4: Gjisa 합성키 승격
- **질문**: `Gjisa` (지사 코드) 가 합성키의 일부로 승격되어야 하는가? (Subu27 SELECT GROUP BY 에 포함되어 있음)
- **발생 시점**: C2 1차 포팅 (Subu27.pas L464 GROUP BY)
- **영향 범위**: 1차는 메타로 처리하여 URL key 미포함. 운영 데이터 분포 (한 hcode 가 여러 gjisa 를 갖는지) 확인 후 합성키 추가 결정.
- **상태**: **후속 이관** — 운영 데이터 분포 분석 사이클 후 closure.

### OQ-RT-7: D_Select 권한키 분기 (DEC-009 해제 + C10 마감)
- **질문**: `D_Select` 헬퍼가 Phase 2 (C4) 시점에는 인터페이스만 노출 (`1=1` 폴백) — 실권한 분기는 C10 (권한 관리) 로 이관. C10 Phase 1 시점에서 admin / branch_manager / auditor / operator 4 분기를 도입할 수 있는가?
- **발생 시점**: C4 Phase 2 (2026-04-19) — DEC-030 으로 OQ-RT-1 → OQ-RT-7 재번호.
- **영향 범위**: 모든 도메인 라우터 (마스터/주문/입고/반품/정산/리포트) 의 d_select 호출 정합. C10 의 Id_Logn F11~F89 매트릭스와 1:1 의존.
- **상태**: **마감 (2026-04-20, C10 Phase 1)** — DEC-009 해제 (1차 포팅 단순화 종료). `app/core/d_select.py::build_d_select_clause(table, user_context)` 가 4 분기 도입.
- **마감 근거**:
  - admin (Hcode='0000' 또는 role='admin') → `1=1` (전 데이터)
  - branch_manager / auditor → `Server_id = '<server_id>'` (본 지점 + 산하 / R/O 강제)
  - operator (그 외) → `Branch_id = '<branch_id>' AND Hcode = '<hcode>'` (본 사용자 데이터만)
  - `app/core/deps.py::get_user_context` 가 JWT claim 우선 + `Authorization-Context` 헤더 fallback 으로 user_context 조립
  - `test/test_c10_admin_phase1.py::DSelectBranching` 3 케이스 PASS (admin/branch/operator).
  - `analysis/handlers/c10_phase1.md` §5 d_select 매트릭스 동결.
- **후속 작업**: 마스터/주문/정산 라우터에 d_select 점진 도입 (별도 리팩토링 사이클) — 회귀 면적 제어를 위해 라우터별 분리.
- **참조**: DEC-030, `app/core/d_select.py`, `app/core/deps.py`, `test/test_c10_admin_phase1.py`, `analysis/regression/c10_phase1.md`

### OQ-IN-1: FTP 자동 수신 — 자격증명·스케줄러 인프라 합의
- **질문**: 레거시 TSobo38(전송자료받기) 가 사용하던 외부 FTP 서버의 호스트/계정/스케줄과 파일 포맷(EUC-KR 고정폭? CSV?) 은 무엇인가? 모던 환경에서 FTP 폴링/SFTP/오브젝트 스토리지 중 어느 채널을 채택할 것인가?
- **발생 시점**: C3 입고 접수 1차 포팅 (2026-04-19, `analysis/screen_cards/Sobo38.md`)
- **영향 범위**: C3 Phase 2 — 자동 수신 기능 활성화 시점. Phase 2 UI 보강(2026-04-19, HOT-INB-3) 에서도 사용자 직접 업로드(`/inbound/import`) 흐름 유지. 1차는 사용자 파일 업로드 우회(DEC-027) 로 핵심 기능 보존.
- **상태**: **후속 이관** — 운영 인프라/계정 합의 후 별도 결정으로 채널/스케줄 동결.
- **후속 작업 (스파이크 단계, C3 phase2 완료 시점 기준)**:
    1. 운영 FTP 호스트/계정 인계 또는 SFTP 전환 합의 (보안팀 + 인프라팀 별행).
    2. 파일 포맷 sample 1건 수집 (실제 운영 환경의 EUC-KR CSV/고정폭 인코딩 확인).
    3. `inbound_service.import_from_file` 가 받는 입력 포맷과 동일하게 정규화 → 어댑터 1개로 자동/수동 두 채널 통일 (SOLID DIP — 스토리지 추상화).
    4. 스케줄러(APScheduler 등 또는 외부 cron) 정의 — 1차는 dry-run 만, 안정화 후 자동 INSERT.
    5. 합의 결과는 신규 DEC-IN-FTP-* 로 동결 후 본 OQ closure.
- **선행 차단 요소**: 운영팀과의 외부 FTP 자격증명 공유 합의(보안 정책) — 본 작업은 코드 우선이 아니라 합의가 우선.

---
### Cut-over 진입 차단 게이트 (C15 — 확장 라인 v0.2)

다음 OQ 들은 C15 Cut-over (`migration/contracts/cutover.yaml` v1.0) 진입 시 *각각의 cutover_block 플래그* 에 따라 진행 가능 여부를 결정한다 (DEC-044 정합).

| OQ | cutover_block | 차단 사유 | 마감/우회 조건 |
|---|---|---|---|
| OQ-IN-1 (FTP 자동 수신 채널 합의) | **true** | "예약입고" 인스턴스 마감/cancel 정책이 결정되지 않으면 cut-over 후 회복 불가. 1차 우회(DEC-027) 가 활성화 되어 있는 동안만 cut-over 진행 시도 가능. | (a) 운영팀 FTP 자격 합의 + DEC-IN-FTP-* 동결 → block 해제, (b) "수동 업로드 only 운영" 정책으로 동결 (DEC 신규) → block 해제. |
| OQ-DBL-001 (3.23 인스턴스 DB 내 로직) | **true** | cut-over 시 평문 password / 레거시 SQL 트리거의 동작이 신규 환경에 부재하면 보안/정합 사고. | (a) Id_Logn 평문 → bcrypt 일괄 전환 정책 동결 + 마이그레이션 스크립트 1회 dry-run PASS, (b) 3.23 트리거 인벤토리 0건 확인. |
| OQ-DBL-002 (FK/CHECK/DEFAULT 선언적 규칙) | **false** | cut-over 후 운영 SLA #6 게이트와 함께 후속 보강 가능. 데이터 손실/정합 위험 없음 (단, 신규 컬럼 추가 시 default 값 미정 risk 는 schema_diff (VC-5) 에서 차단). | post-cutover Phase 2 작업 — 본 OQ 자체는 cut-over 진행을 막지 않음. |
| OQ-DBL-003 (동일 hcode 다중 server 분산) | **true** | 4 server 단계 cut-over 시 동일 hcode 가 두 환경 사이에 분산되면 DEC-033 의 server_id 라우팅이 충돌. | (a) hcode→server_id 1:1 매핑 동결 (DEC 신규), (b) "동일 server 동시 cut-over (138/153/154/155 모두 동일 윈도우)" 운영팀 합의. |

본 표는 `cutover.yaml` §scope.open_questions_handling 과 1:1 정합 (`test/test_c15_cutover_phase1.py::test_S_08_oq_block_gate` 가 최소 3건의 cutover_block:true 등록 확인).

---
*최종 업데이트: 2026-04-20 — C15 Cut-over 진입 차단 게이트 표 신설 (OQ-IN-1, OQ-DBL-001/003 = block:true / OQ-DBL-002 = block:false). DEC-044 정합 (외부 시스템 연동 제외 + 마감 정책).*
*이전: 2026-04-20 — OQ-RT-7 마감 (C10 Phase 1: D_Select 실분기 4 분기 도입, DEC-009 해제). 후속 OQ-IDP-* (외부 IdP/SSO 합의) 미등록 — 외부 합의 트리거 시 신규 (DEC-043 인터페이스 동결로 후속 도입 시 회귀 0).*
*이전: 2026-04-19 — OQ-IN-1 후속 작업 5단계 스파이크 계획 명시 (C3 phase2 UI 보강 완료 시점, HOT-INB-3).*
*이전: 2026-04-19 — OQ-IN-1 신규 (C3 입고 1차 FTP 우회 결정 후속).*
*이전: 2026-04-25 — OQ-OUT-1~4 신규 (C2 출고 접수 1차 포팅 동결 반영). (이전: 2026-04-22 OQ-LOGIN-1 "후속 이관" 표기)*
