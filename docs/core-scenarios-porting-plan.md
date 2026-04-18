# 핵심 10 시나리오 — 화면 단위 포팅 계획·진행표

본 문서는 [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md) **C1~C10** 후보를 베타 라인까지 끌어가기 위한 **실행용 계획서**입니다.
- **목적**: 회의 합의를 기다리지 않고도 "다음에 뭘 만들지·어떤 델파이 폼을 봐야 하는지·어디까지 동등성을 맞춰야 하는지"를 한 표로 알 수 있게 한다.
- **연관 산출물**: [`migration/contracts/`](../migration/contracts/) · [`migration/test-cases/`](../migration/test-cases/) · [`analysis/screen_cards/`](../analysis/screen_cards/) · [`dashboard/data/porting-screens.json`](../dashboard/data/porting-screens.json)
- **베이스 라인**: [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) **DEC-003**(읽기→등록→수정/취소→배치/인쇄/장비→고객사 분기) · **DEC-004**(인쇄·바코드 1차 방향)
- **범위**: "**기능을 최대한 동일하게 유지**"가 원칙. 차이는 [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) DEC와 [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) OQ로 명시 추적.

> 본 계획서는 회의 확정 전이라도 **델파이 소스만으로** 도출 가능한 매핑·순서·절차를 동결합니다. C1~C10 채택이 변경되면 본 문서 §1·§3 표만 갱신해 후속 산출물 링크를 유지합니다.

---

## 1. 시나리오 → 포팅 화면 매핑표 (델파이 → 웹)

`주 폼` / `유닛` / `Seek_Uses 권한키` 출처: [`legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md`](../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md)
`DB 영향` 출처: [`analysis/db_impact_matrix.json`](../analysis/db_impact_matrix.json)
`인쇄·스캐너` 출처: [`docs/legacy-print-scanner-integration-survey.md`](legacy-print-scanner-integration-survey.md)

| 순서 | 시나리오 | 델파이 폼·유닛 (주) | 함께 봐야 할 폼 | 권한키 | 용도 | 간략 내용 | 웹 라우트(제안) | 단계 |
|------|----------|--------------------|------------------|--------|------|------------|-----------------|------|
| 1 | **C1 로그인·세션 시작** | `TSubu00` (`Chul.dfm`/`Chul.pas`) | (로그인 다이얼로그는 `Chul.pas` `FormCreate` L441~) | — | 사용자 인증·세션 발급·헤더에 `Hcode/Hname` 노출 | 작업자명·아이디·비번 → `Id_Logn` 조회, `Hcode='0000'` 슈퍼유저 분기, JWT 발급 | `/(public)/login`, `POST /api/auth/login` | **0** |
| 2 | **C6 거래/잔액 조회 (읽기 전용)** | `TSobo21` 거래명세서 (`Subu21.pas`) | `TSobo61` 도서별판매·`TSobo62` 거래처판매·`TSobo31` 도서별수불원장 | F24, F61, F62, F31 | 거래·재고·잔액을 읽기만 하는 그리드 | 기간·거래처·도서 조건 그리드 조회. INSERT/UPDATE 없음 → 데이터 손상 위험 0 | `/transactions/sales-statement`, `/inventory/ledger` | **1 (읽기)** |
| 3 | **C9 상품·고객 마스터 등록** | `TSobo11` 거래처-통합 (`Subu11.pas`) | `TSobo15` 거래처-개별·`TSobo14` 도서·`TSobo17` 출판사·`TSobo12` 입고처·`TSobo16` 특별관리 | F11~F17 | 마스터 데이터 CRUD | `G6_Ggeo` 등 마스터 INSERT/UPDATE/DELETE. FK 영향 작은 등록 흐름부터 | `/master/customer`, `/master/book`, `/master/publisher` | **2 (등록)** |
| 4 | **C3 입고 접수** | `TSobo22` 입고명세서 (`Subu22.pas`) | `TSobo54` 일별 입고내역서·`TSobo57` 기간별 입고내역서·`TSobo38` 전송자료받기(FTP) | F25, F52, F56, F29 | 신규 입고 INSERT 위주 | 입고 본 테이블 INSERT, FTP/공유폴더 자료 수신 분기. `Tong08` 바코드 진입점 호출 가능 | `/inbound/receipts`, `/inbound/import`, `/inbound/reports/daily`, `/inbound/reports/period` | **2 (등록)** |
| 5 | **C2 출고 접수(주문 입력)** | `TSobo27` 출고접수관리 (`Subu27.pas`) | `TSobo26` 출고접수현황·`TSobo28` 출고택배관리·`TSobo23` 반품명세서 | F21, F22, F26 | 핵심 매출 흐름 (INSERT/UPDATE/DELETE) | `S1_Ssub`·`Sg_Csum` INSERT/UPDATE. `Tong08` 바코드와 결합. C11(수정/취소) 하위 시나리오 포함 | `/outbound/orders`, `/outbound/orders/[id]` | **3 (수정/취소)** |
| 6 | **C4 반품 처리** | `TSobo23` 반품명세서 (`Subu23.pas`) | `TSobo23_1`(반품과 변형)·`TSobo35` 반품재고(폐기)·`TSobo51` 반품재고(변경)·`TSobo55` 일별 반품내역서 | F26, F35~F37, F53 | 반품 + 재고 영향 + 정산 영향 | UPDATE/DELETE 동반, 정품/반품/폐기 재고 분기. 패스워드 모달 `Subu40` 의존 | `/returns`, `/returns/[id]` | **3 (수정/취소)** |
| 7 | **C5 정산(일·월 마감)** | `TSobo45` 청구서관리 (`Subu45.pas`) | `TSobo47` 청구금액(년월)·`TSobo46` 청구서출력·`TSobo49` 세금계산서·`TSobo41/42` 입금관리 | F43, F44, F45, F46, F47 | 일·월 집계·청구·세금계산서·입금 정산 | 집계 테이블 UPDATE. C12(마감 후 차단) 하위 시나리오 필수. 패스워드 모달 보호 | `/settlement/billing`, `/settlement/tax-invoice` | **3 (수정/취소)** |
| 8 | **C7 라벨/송장 인쇄** | `Tong04.pas`(`Print_*` 함수군) | `Seep13.pas`(라벨 캔버스), `Tong01.pas`(`TPrintDialog`) | — (호출 화면 권한 적용) | 거래명세·라벨·송장·세무 출력 | DEC-004: **HTML 인쇄 + 라벨 PDF 하이브리드**. `QuickReport`/`Printer.Canvas` → HTML/PDF 매핑 | `/print/preview/[type]/[id]` | **4 (배치·인쇄)** |
| 9 | **C8 바코드 스캔 → 출고 매칭** | `Tong08.pas`(시리얼 바코드 진입점) | `FTong07.Button104Click` → `Sobo21/22/23` (출고/입고/반품 매칭) | 호출 화면별 (F24·F25·F26) | 스캔 1건마다 매칭 SELECT/UPDATE | DEC-004: **USB-HID 키보드 웨지 1차**, Web Serial은 베타 후 재검토. C2/C3/C4와 결합 | (호출처 라우트에 통합) `keydown` 핸들러 | **4 (배치·인쇄)** |
| 10 | **C10 권한 관리(f11~f89)** | `TSubu10` 환경설정 (`Subu10.pas`) | `Id_Logn` 권한 컬럼 직접 편집 폼(현장 관행은 `Subu40` 패스워드 모달과 연계 확인 필요) | F18 + 슈퍼유저 0000 | 사용자·권한 매트릭스 관리 | `Id_Logn` UPDATE. C13(세션 만료·권한 부족) 하위 시나리오와 연계 E2E | `/admin/users`, `/admin/permissions` | **5 (관리)** |

> **순서 0**: C1(로그인)은 모든 시나리오의 전제 조건이라 별도 0번. 이미 [`migration/contracts/login.yaml`](../migration/contracts/login.yaml) · [`migration/test-cases/login.json`](../migration/test-cases/login.json) 골격이 동결된 상태이므로 본 계획서에서는 "베타 진입 검증 + 보안 결정 D-LOGIN-1·2·3 클로저"가 잔여 작업입니다.

### 1.1 하위 시나리오(C11~C15) 흡수 위치

[`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md) §1b 확장 후보를 **별도 화면 추가 없이** 위 흐름에 흡수합니다.

| 확장 ID | 흡수되는 곳 | 추가 검증 항목 |
|---------|-------------|----------------|
| C11 출고 수정/취소 | C2 (Sobo27/26) | 마감 전 UPDATE/DELETE, 재집계 일관성 |
| C12 마감 후 편집 차단 | C5 (Sobo45/47) | "마감됨" 분기 메시지 동등성 |
| C13 세션 만료·권한 부족 | C1 + C10 (Subu00/Subu10) | 토큰 만료 후 재진입, f권한 거부 시 UI |
| C14 핵심 보고서 동등성 | C6 (Sobo21/61/62) + C5 (Sobo45) | 숫자 대조 1~2건 |
| C15 델파이 병행 충돌 방지 | 모든 쓰기 흐름 (C2/C3/C4/C5/C9/C10) | 동일 건 동시 편집 시 정책 (last-write/경고) |

---

## 2. 포팅 순서(단계 0~5) — DEC-003 매핑

DEC-003 권장 위험도 순서를 **본 프로젝트의 베타 라인**에 맞춰 6단계로 재구성합니다.

| 단계 | 단계명 | 포함 시나리오 | DB 위험 | 게이트 | 목표 스프린트 |
|------|--------|----------------|---------|--------|----------------|
| 0 | 인증·세션 (전제) | C1 | SELECT + 단건 UPDATE | 베타 게이트 #1 | Sprint 0~1 (이미 골격 진행) |
| 1 | 읽기 전용 조회 | C6 | SELECT only | 분석 산출물 승인 #1 | Sprint 1 (5~14주차) |
| 2 | 신규 등록 (마스터·입고) | C9, C3 | INSERT 위주, UPDATE 일부 | DB 로직 게이트 #2 | Sprint 1~2 |
| 3 | 수정·취소·정산 | C2, C4, C5 (+ C11/C12) | INSERT/UPDATE/DELETE, 트랜잭션 경계 | API 계약 승인 #3 | Sprint 2~3 |
| 4 | 배치·인쇄·장비 | C7, C8 | SELECT + 마킹 UPDATE | 인쇄 결과 승인 #5 | Sprint 3~4 |
| 5 | 권한·고객사 분기 | C10 (+ C13/C15) | UPDATE | 고객사별 차이 승인 #4 | Sprint 4 |

### 2.1 베타 라인의 최소 셋

[`dashboard/data/release-milestones.json`](../dashboard/data/release-milestones.json) `beta.exitCriteria`는 **C1·C2·C7 포함**이 통상 라인입니다. 본 계획표 기준으로는 **단계 0 + 1 + (단계 3의 C2) + (단계 4의 C7)** = **베타 4종**으로 출발하고, 회의 결과에 따라 단계 4의 C8, 단계 1의 C6를 추가합니다.

---

## 3. 화면별 공통 단계별 절차 (T1 ~ T8)

각 화면은 **동일한 8단계**로 진행해 누락을 방지합니다. 단계 사이의 산출물 위치까지 고정해 둡니다 (DEC-001 8계층 하네스 원칙 반영).

| # | 단계명 | 입력 | 산출물 | 책임 | 통과 기준 |
|---|--------|------|--------|------|-----------|
| **T1** | 화면 카드 생성 | `analysis/*.json` 6종 | `analysis/screen_cards/<form>.md` | 메인개발자 | [`screen-cards-generation-plan.md`](screen-cards-generation-plan.md) §2 표준 구성 채워짐 |
| **T2** | 레거시 흐름 추출 | `<form>.pas`/`.dfm` 정독 | T1 카드의 §2 이벤트 흐름·§3 SQL 항목 | 메인개발자 + 델파이 담당자 | OnClick/OnShow 등 핵심 핸들러 코드 위치 + SQL 인용 완료 |
| **T3** | Migration Contract 작성 | T1·T2 결과 + OQ/DEC | `migration/contracts/<flow>.yaml` (`status: draft`) | 메인개발자 | `intent`/`inputs`/`outputs`/`data_access`/`endpoints`/`deltas`/`equivalence` 7섹션 채움 ([login.yaml](../migration/contracts/login.yaml) 형식) |
| **T4** | Regression Test Pack 골격 | T3 contract | `migration/test-cases/<flow>.json` | 메인개발자 + 기획자(QA) | `axes` 5축 명시, 정상 1건·실패 분기 1건·경계 1건 최소 (login.json 형식) |
| **T5** | 백엔드 API 구현 | T3 endpoints | `도서물류관리프로그램/backend/app/routers/<flow>.py` + `services/<flow>_service.py` | 메인개발자 | T4 정상 케이스 통과, EUC-KR 처리·파라미터 바인딩 적용 |
| **T6** | 프론트엔드 화면 구현 | T1 §1 UI + T3 inputs | `도서물류관리프로그램/frontend/src/app/(app)/<route>/page.tsx` | 메인개발자 | 핵심 입력·그리드·메시지가 레거시와 의미 보존 |
| **T7** | 5축 동등성 검증 | T4 + 캡처 데이터 | 계약의 `equivalence` 결과 + GAP 리포트 갱신 | 기획자(QA) | [`eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md) §1.1 "베타 임계값" 통과 |
| **T8** | 시나리오 DoD 충족 | T1~T7 전부 | contract `status: approved` + 본 진행표 체크 | 메인개발자 | [`eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md) §2.1 시나리오 DoD 6항 ✅ |

> **재귀적 오류 방지 가드**: T1·T2 단계에서 동일 화면을 열고 있는 다른 시나리오/하위 시나리오가 있는지 본 계획서 §1.1 표를 먼저 확인하고, 중복 폼이 있으면 같은 contract에 흡수(별도 contract 신설 금지)합니다.

---

## 4. 시나리오별 단계 체크리스트 (T1~T8)

각 시나리오의 진행 상태는 [`dashboard/data/porting-screens.json`](../dashboard/data/porting-screens.json)에 머신리더블로 동기화됩니다. 아래 표는 **주간 회의용 한 장 요약**입니다.

### 4.1 단계 0 — C1 로그인

| T# | 작업 | 상태 | 산출물·메모 |
|----|------|------|-------------|
| T1 | `analysis/screen_cards/Subu00.md` | ⏳ | screen_card_builder.py 구현 후 자동 생성 |
| T2 | `Chul.pas` FormCreate L441~/ToolButton18Click L1956~ 인용 | ✅ | login.yaml `data_access` 반영 완료 |
| T3 | `migration/contracts/login.yaml` | ✅ (draft) | D-LOGIN-1·2·3 결정 대기 |
| T4 | `migration/test-cases/login.json` | ✅ (draft) | 5축 골격 동결 |
| T5 | `backend/app/routers/auth.py` | ✅ | EUC-KR/3.x raw 경로·JWT 적용 |
| T6 | `frontend/src/app/(public)/login/` | ✅ | AppShell + 로그인 폼 |
| T7 | 5축 검증 (베타 임계값) | ⏳ | 캡처 1회 후 갭 리포트 갱신 |
| T8 | 시나리오 DoD | ⏳ | D-LOGIN-1·2·3 → DEC 등록 시 ✅ |

### 4.2 단계 1 — C6 거래/잔액 조회 (읽기 전용)

| T# | 작업 | 산출물·메모 |
|----|------|-------------|
| T1 | `analysis/screen_cards/Sobo21.md` (+ Sobo61/62/31) | 그리드 컬럼 구성, `query_catalog.json`의 SELECT 발췌 |
| T2 | `Subu21.pas` OnShow/조회 버튼 핸들러 추출 | 기간·거래처·도서 필터 SQL 인용 |
| T3 | `migration/contracts/sales_statement.yaml` | `data_access`는 SELECT only, `equivalence.data: "변경 없음"` |
| T4 | `migration/test-cases/sales_statement.json` | C14 동등성 1건 (집계 숫자 대조) 포함 |
| T5 | `backend/app/routers/transactions.py` | 페이지네이션·EUC-KR 헤더 |
| T6 | `frontend/.../transactions/sales-statement/page.tsx` | TStringGrid → 가상 스크롤 그리드 |
| T7 | 5축 — `data` 변경 0 검증 | 정적 SELECT diff 자동화 |
| T8 | DoD | 보고서 동등성 1건 통과 시 ✅ |

### 4.3 단계 2 — C9 마스터 등록 → C3 입고 접수

| T# | C9 (Sobo11/15/14/17) | C3 (Sobo22 + Sobo38 FTP) |
|----|----------------------|--------------------------|
| T1 | `screen_cards/Sobo11.md`+@ | `screen_cards/Sobo22.md`, `Sobo38.md` |
| T2 | INSERT/UPDATE/DELETE SQL 인용 | 입고 INSERT, FTP 파일 수신 흐름 |
| T3 | `contracts/master_customer.yaml`·`master_book.yaml`·`master_publisher.yaml` | `contracts/inbound_receipt.yaml` |
| T4 | 정상 등록·중복 키·삭제 보호 케이스 | 정상 입고·FTP 자료 부재 케이스·바코드 결합 케이스 |
| T5 | `routers/master.py` (CRUD) | `routers/inbound.py` + FTP 어댑터(또는 업로드) |
| T6 | `/master/customer` 등 | `/inbound/receipts` |
| T7 | `data` 축 INSERT delta 0 불일치 | 동일, 캡처 후 갭 리포트 갱신 |
| T8 | DoD | DoD |

### 4.4 단계 3 — C2 출고(+C11) → C4 반품 → C5 정산(+C12)

| T# | C2 (Sobo27/26/28) | C4 (Sobo23/23_1/35/51) | C5 (Sobo45/47/46/49 + Subu40 모달) |
|----|-------------------|------------------------|--------------------------------------|
| T1 | `screen_cards/Sobo27.md`+@ | `screen_cards/Sobo23.md`+@ | `screen_cards/Sobo45.md`+@ |
| T2 | 등록·수정·취소·바코드 호출 핸들러 | 반품·재고 분기 핸들러 | 일·월 마감 트리거·세금계산서 |
| T3 | `contracts/outbound_order.yaml` (C11 흡수) | `contracts/return_receipt.yaml` | `contracts/settlement_billing.yaml` (C12 흡수) |
| T4 | 정상·수정·삭제·마감 후 차단·바코드 매칭 | 정상 반품·재고 폐기·정산 영향 | 일/월 마감·재마감 차단·재집계 |
| T5 | `routers/outbound.py` + 트랜잭션 경계 | `routers/returns.py` | `routers/settlement.py` (배치 작업) |
| T6 | `/outbound/orders` (편집/삭제 가드 UI) | `/returns` (패스워드 모달) | `/settlement/billing` |
| T7 | `data` delta 100% 일치 (베타) | 동일 | C14 보고서 동등성 + 마감 후 차단 메시지 의미 보존 |
| T8 | DoD | DoD | DoD |

### 4.5 단계 4 — C7 인쇄 → C8 바코드

| T# | C7 (Tong04 Print_* / Seep13) | C8 (Tong08 → Sobo21/22/23) |
|----|------------------------------|-----------------------------|
| T1 | `screen_cards/Tong04.md`(인쇄 진입점 묶음) | `screen_cards/Tong08.md` + 호출처 표 |
| T2 | `Print_11_01` 등 함수별 데이터셋·폼 매핑 | `ComPortRxChar`·`#13` 종결·`Button104Click` 호출 체인 |
| T3 | `contracts/print_invoice.yaml`·`print_label.yaml` (DEC-004 1차: HTML+PDF) | `contracts/barcode_scan.yaml` (DEC-004 1차: USB-HID 웨지) |
| T4 | 거래명세·라벨 1매·세무 출력 비교 (PDF diff) | 정상 스캔·CR 누락·중복 스캔 |
| T5 | `routers/print.py` + WeasyPrint/Playwright PDF | (서버 라우트 불필요, 프론트 keydown 핸들러 + 기존 매칭 API 호출) |
| T6 | `/print/preview/<type>/<id>` | C2/C3/C4 화면 내 통합 (별도 화면 없음) |
| T7 | 출력 결과 승인 #5 (현업 사인) | 매칭 정확도·중복/누락 검증 |
| T8 | DoD + 인쇄 결과 승인 통과 | DoD |

### 4.6 단계 5 — C10 권한 관리 (+C13/C15)

| T# | 작업 | 메모 |
|----|------|------|
| T1 | `screen_cards/Subu10.md` + 사용자관리 폼(현장 확인 필요) | 메인 메뉴에 없는 숨은 화면 가능성 (체크리스트 §3.4) |
| T2 | `Id_Logn` UPDATE 경로·f11~f89 권한 검증 위치 | `Base10.Seek_Uses('Fxx')` 호출 지점 모두 인덱싱 |
| T3 | `contracts/admin_permissions.yaml` | C13(세션 만료·권한 부족) 하위 시나리오 명시 |
| T4 | 권한 부여·해제·자기 권한 박탈 차단·세션 만료 후 진입 | 슈퍼유저 0000 가드 케이스 |
| T5 | `routers/admin.py` + JWT 권한 미들웨어 | `frontend/src/middleware.ts` 와 정합 |
| T6 | `/admin/users`, `/admin/permissions` | 슈퍼유저만 표시 |
| T7 | `audit` 축 — 권한 변경 로그 100% 기록 | 베타 임계값 |
| T8 | DoD + 고객사별 차이 승인 #4 입력물 갱신 | C15 정책 반영 |

---

## 5. 운영 규칙 (포팅 중 유지)

1. **신규 화면 시작 전**: 본 §1 매핑표에서 기존 contract/카드가 있는지 먼저 확인 — **중복 신설 금지** (재귀 오류 방지).
2. **델파이 동작 차이가 발견되면**: 임시 방편으로 우선순위만 바꾸지 말고 [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md)에 DEC, [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md)에 OQ를 등록 → contract `deltas`에 인용.
3. **회귀 영향**: T7 5축 중 `data` 축 실패는 단계와 무관하게 **즉시 차단**( [`eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md) §3 ).
4. **고객사 분기(체크리스트 §1.1)**: 단계 5(C10)에서 일괄 처리하되, 단계 1~4에서 발견된 고객사 차이는 contract `customer_variants` 섹션에 **즉시 메모**.
5. **테스트 자산 위치**: 디버그 스크립트는 `debug/`, 자동화 테스트 코드는 `test/`에 신설 (사용자 규칙).
6. **인쇄·스캐너 결정**: DEC-004 1차 방향 유지. Web Serial / 라벨 직결은 **베타 후 OQ-002 결과로만 재검토**.
7. **dfm 레이아웃 산출물 참조 의무 (DEC-028)**: 신규 화면 포팅 시작 전 [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/<Subu*>/<Sobo*>.{html,form.json,tree.json}`](../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/) 의 변형 포함 모든 세트를 인벤토리하고, [`analysis/layout_mappings/<Sobo*>.md`](../analysis/layout_mappings/) 에 (영역 분할, 위젯 ID, **TabOrder**, DBGrid 컬럼·정렬·합계, 이벤트 매핑) 1:1 매핑표를 선행 작성한다. 모던 페이지의 모든 위젯에는 `data-legacy-id="<원본 ID>"` 부착 필수. 변형 차이는 코드 분기 금지·`customer_variants` 섹션에만 기록. 기존 done 시나리오는 회귀 발견 시 같은 룰로 retrofit.

---

## 6. 진행 추적 동기화

- 머신리더블 진행 상태: [`dashboard/data/porting-screens.json`](../dashboard/data/porting-screens.json) — 각 시나리오의 `tasks.T1~T8.status` 를 `not_started | in_progress | review | done | blocked` 로 갱신.
- 사람용 한 장 요약: 본 문서 §4 (주간 회의에서 ✅/⏳/⛔ 갱신)
- 대시보드 표시: [`dashboard/data/web-porting-progress.json`](../dashboard/data/web-porting-progress.json) → `docLinks` 에 본 문서 추가됨. 또한 트래커 JSON은 계획 대시보드의 `porting-screens-section`(웹 포팅 진행 블록 바로 아래)에 카드 그리드·라인 필터·KPI로 즉시 반영됨 (DEC-002 정적 사이트 원칙: JSON 편집 → push → 새로고침).
- **역할별 To-Do 동기화 규칙**: 시나리오 `C?` 의 `T8.status = done` 으로 바뀐 시점에 [`dashboard/data/todos.json`](../dashboard/data/todos.json) 의 `roles.M.tasks` 내 `M-S1-PORT-C?` 항목도 `done: true` 로 함께 갱신 (메인 개발자 역할 진척 누락 방지).
- **게이트 동기화**: 단계별 진입 게이트는 [`dashboard/data/todo-flow.json`](../dashboard/data/todo-flow.json) 의 `F-PORT` phase 와 [`dashboard/data/approvals.json`](../dashboard/data/approvals.json) #1~#7에 1:1 매핑 (단계 0·1 ↔ #1, 단계 2 ↔ #2, 단계 3 ↔ #3, 단계 4 ↔ #5, 단계 5 ↔ #4).

---

## 7. 변경 이력

- 2026-04-19 — §5 운영 룰 7 신규 (dfm→html 산출물 참조 의무, DEC-028 동결).
- 2026-04-18 — 최초 작성. C1~C10 매핑·DEC-003 단계 0~5·T1~T8 공통 절차 동결, hostingscreens.json 신설.

---

*관련: [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md), [`docs/screen-cards-generation-plan.md`](screen-cards-generation-plan.md), [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md), [`docs/decision-print-scanner-web.md`](decision-print-scanner-web.md), [`legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md`](../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md)*
