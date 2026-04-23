# 핵심 10 시나리오 — 화면 단위 포팅 계획·진행표

본 문서는 [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md) **C1~C10** 후보를 베타 라인까지 끌어가기 위한 **실행용 계획서**입니다.
- **목적**: 회의 합의를 기다리지 않고도 "다음에 뭘 만들지·어떤 델파이 폼을 봐야 하는지·어디까지 동등성을 맞춰야 하는지"를 한 표로 알 수 있게 한다.
- **연관 산출물**: [`migration/contracts/`](../migration/contracts/) · [`migration/test-cases/`](../migration/test-cases/) · [`analysis/screen_cards/`](../analysis/screen_cards/) · [`dashboard/data/porting-screens.json`](../dashboard/data/porting-screens.json) · **[`docs/delphi-form-screen-equivalence-matrix.md`](delphi-form-screen-equivalence-matrix.md)** (`python3 tools/delphi_form_screen_matrix.py` 로 갱신 — 레거시 DFM Caption ↔ `form-registry` 동등성 표, **DEC-061**)
- **베이스 라인**: [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) **DEC-003**(읽기→등록→수정/취소→배치/인쇄/장비→고객사 분기) · **DEC-004**(인쇄·바코드 1차 방향)
- **범위**: "**기능을 최대한 동일하게 유지**"가 원칙. 차이는 [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) DEC와 [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) OQ로 명시 추적.

> 본 계획서는 회의 확정 전이라도 **델파이 소스만으로** 도출 가능한 매핑·순서·절차를 동결합니다. C1~C10 채택이 변경되면 본 문서 §1·§3 표만 갱신해 후속 산출물 링크를 유지합니다.

### 포팅 파이프라인 훅 (레거시 제목 대조)

1. **폼 레지스트리·계약·라우트 수정 전후**: `python3 tools/delphi_form_screen_matrix.py` 실행 → [`delphi-form-screen-equivalence-matrix.md`](delphi-form-screen-equivalence-matrix.md) 및 `analysis/audit/delphi-form-screen-matrix.json` 갱신.
2. **품질 게이트**: `python3 tools/delphi_form_screen_matrix.py --check` — 등록된 `Subu*` 폴더에 대응 `*.dfm` 없으면 실패. 제목 문자열까지 엄격히 맞추려면 `--strict`(초기 코드베이스는 차이 행 다수 가능).
3. **회귀**: `pytest test/test_delphi_form_screen_matrix.py`.

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

## 7. C4 반품 처리 — 1차 포팅 완료 현황 (2026-04-19)

| 작업 | 완료물 | 비고 |
|------|--------|------|
| T1 DFM 매핑 | `analysis/layout_mappings/Sobo{23,23_1,24,25,51,55,40}.md` | chul_08 별도 namespace |
| T2 SQL 흐름 | `analysis/c4_returns_flow.md` (SQL-RT-1~27) | 3분기 재고 흐름 포함 |
| T3 계약 | `migration/contracts/return_receipt.yaml` v1.0.0 | 10 엔드포인트, 9 변형 |
| T4 테스트 | `test/test_c4_returns_phase1.py` (32 TC) | 32/32 pass |
| T5 백엔드 | `app/{models,services,routers}/returns.py` + `audit_service` | DEC-029 token gate |
| T6 프론트 | `/returns/{receipts,inventory,reports}` + 3 컴포넌트 | form-registry 5건 |
| T7 회귀 | pytest 47건 pass, tsc/eslint 0오류 | C3 회귀 없음 |

### C4 Phase 2 권고 (OQ-RT-7/8/9 — DEC-030 재번호)

> 참고: 이전 OQ-RT-1/2/3 번호는 `migration/contracts/return_receipt.yaml` 의 OQ-RT-1~6 과 충돌하여 **DEC-030 (2026-04-19)** 으로 OQ-RT-7/8/9 로 재번호함. 정본 카탈로그는 `legacy-analysis/decisions.md#DEC-030` 표 참조.

| ID | 항목 | 우선순위 |
|----|------|---------|
| OQ-RT-7 (구 core-1) | `D_Select` 기반 권한키 분기 구현 (DEC-009 해제 필요) — Phase 2 는 인터페이스만 노출, 실권한은 C10 | Phase 2 |
| OQ-RT-8 (구 core-2) | Sobo34_4 (기간별재고원장 상세-폐기) + Sobo58 (기간별반품내역서) 신규 화면 | Phase 2 |
| OQ-RT-9 (구 core-3) | DB 기반 audit 비밀번호 검증(bcrypt) + 실패 횟수 추적 (DEC-029 완전 구현 = OQ-RT-4 와 같이) | Phase 2 |

### C4 Phase 2 진행 현황 (2026-04-19, T1~T8 완료)

| Task | 결과 | 핵심 산출물 |
|------|------|------------|
| T1 정리 | ✅ | DEC-030 신규 + Sobo34_4/Sobo58 DFM 인벤토리 (`Subu34_4`, `Subu58`) |
| T2 매핑 노트 | ✅ | `analysis/layout_mappings/{Sobo34_4,Sobo58}.md` + `analysis/c4_returns_phase2_flow.md` (SQL-RT-28~40) + `analysis/sv_ghng_field_catalog.md` (Field1/2/3 ↔ 9종) |
| T3 contract | ✅ | `migration/contracts/return_receipt.yaml` v1.1.0 (OQ-RT-1~6 + 신규 endpoints) |
| T4 테스트 | ✅ | `test/test_c4_returns_phase2.py` 30 cases (27 pass / 3 의도 SKIP) |
| T5a 신규화면 BE | ✅ | `GET /returns/ledger`, `GET /returns/period-report` + 4개 SQL 상수 |
| T5b 라인 diff/롤백/부분 | ✅ | `PUT /returns/{key}` + `POST /returns/dispose/{regen,disassemble}/partial` + `POST /returns/{key}/rollback` |
| T5c bcrypt + DB audit | ✅ | `app/services/audit_password_service.py` + `migrations/2026_04_19_c4_phase2.sql` (`audit_password_attempts`, `audit_returns`, `application_settings.password_hash`) |
| T5d FOR UPDATE + D_Select | ✅ | `app/core/db.execute_transactional_block()` + `app/core/d_select.py` (인터페이스만, 항상 `1=1`) |
| T6 프론트엔드 | ✅ | `/returns/{ledger,period-report}` 신화면 + receipts 상세 라인편집/부분/롤백 + `AuditPasswordModal` 통합. Phase 2 신규 widget 89건 모두 `data-legacy-id` 부착 |
| T7 회귀 | ✅ | pytest 187 pass / 3 skip (의도) / dfm2html 2건은 사전 broken (무관). tsc/eslint 0오류. dfm-id grep: ledger 36 / period 33 / receipts 20 |
| T8 거버넌스 | ✅ | DEC-029 Phase 2 보강 + 본 §7 갱신 + dashboard 갱신 |

**Phase 2 정합성 핵심 변경**:
- `_user_context()` 헬퍼로 `Authorization-Context` 헤더 전달 (D_Select 호환).
- `process_change` 가 단일 트랜잭션 내 `SELECT ... FOR UPDATE` 후 UPSERT — race 조건 차단. mysql3_protocol 서버는 NotImplementedError 폴백으로 기존 경로 유지.
- `verify_audit_password` / `rotate_audit_password` 는 `audit_password_service` 로 위임 — Phase 1 평문 비교는 fallback 유지(이중 운영 호환).
- `audit_service.log_return_action` 이 `audit_password_service.persist_return_audit` 비동기 영속화 호출 — DB 실패 시 file 로깅은 항상 성공 (fail-safe).

### C5 정산 Phase 1 진행 현황 (2026-04-19, T1~T8 완료)

| Task | 결과 | 핵심 산출물 |
|------|------|------------|
| T1 매핑 노트 | ✅ | `analysis/layout_mappings/{Sobo45,Sobo45_1,Sobo47,Sobo41,Sobo42,Sobo42_1}_billing|cash.md` + `analysis/screen_cards/c5_settlement.md` (통합 카드, Sobo45.md 자동 생성본 보존) |
| T2 핸들러/i18n | ✅ | `analysis/handlers/c5_phase1.md` (Delphi 이벤트 ↔ FE/BE 1:1) + `i18n/messages/c5.ko.json` (마감/결재구분/audit 메시지 정본) |
| T3 contract | ✅ | `migration/contracts/settlement_billing.yaml` v1.0.0 + `migration/test-cases/settlement_billing.json` (26 케이스) |
| T4 백엔드 | ✅ | `app/routers/settlement.py` (10 endpoints) + `app/services/{settlement,cash}_service.py` + `app/models/settlement.py`. `audit_service.log_settlement_action` 신규. |
| T5 마이그레이션 | ✅ | `migrations/2026_05_01_c5_phase1.sql` — `application_settings` 정책 행(legacy_yesno) + `audit_password_attempts` 보장 + `audit_settlement` 신규 |
| T6 프론트엔드 | ✅ | `/settlement/{billing,period,cash,cash-status}` 4 페이지 + `lib/settlement-api.ts` + `form-registry.ts` (settlement 메뉴 그룹). variant 토글 단일화(DEC-019). 모든 위젯 `data-legacy-id`(DEC-028). |
| T7 회귀 | ✅ | `test/test_c5_settlement_phase1.py` 32 cases all pass + C4 phase1/2 회귀 (59 pass / 3 skip) 무영향. tsc/eslint 0오류. data-legacy-id grep: billing 22 / cash 20 / cash-status 11 / period 10. |
| T8 거버넌스 | ✅ | DEC-031/032 신규 + 본 §7 갱신 + dashboard 갱신 |

**Phase 1 정합성 핵심 결정**:
- **마감 정책 (DEC-031)**: `T2_Ssub.Yesno='1'` 단일 정본. 별도 `application_settings.settlement.close_until` 키 도입 금지 — `app/services/settlement_service.assert_period_open` 1곳에서만 판정.
- **Gpass 폐기 (DEC-032)**: `Sobo45.pas L372` InputBox 평문 비교 흐름 폐기. `POST /audit/gpass-rotate` (scope='gpass_change') + bcrypt 회전. C4 의 `/audit/password-rotate` (scope='audit') 와 **경로 분리** — 라우트 충돌·권한 혼동 차단.
- **변형 1단일화 (DEC-019)**: Sobo45_1/42_1 의 차이는 `?variant=takbae|sdate` 쿼리 파라미터 + service layer 분기로 흡수. 중복 컴포넌트/엔드포인트 0건.
- **audit 영속화**: `audit_settlement` 테이블에 `billing_*`/`cash_*`/`audit_password_rotated` 액션 best-effort INSERT. 파일 로그(`audit.settlement`)와 병행 — DB 실패 시 file 로깅은 항상 성공 (fail-safe).
- **Phase 2 미포함**: 청구서/세금계산서 인쇄(Sobo46/49), 재집계 배치, audit 회전 UI 는 Phase 2 로 이연.

### C5 정산 Phase 2 진행 현황 (2026-04-19, T1~T8 완료)

| Task | 결과 | 핵심 산출물 |
|------|------|------------|
| T1 매핑 노트 | ✅ | `analysis/layout_mappings/{Sobo46_billing, Sobo49_tax}.md` 신규 + `analysis/screen_cards/c5_settlement.md` Phase 2 섹션 갱신 (DEC-028 의무) |
| T2 핸들러/i18n | ✅ | `analysis/handlers/c5_phase2.md` (Sobo46/49/recalc/audit 회전 UI 이벤트 ↔ FE/BE 매핑, SQL-ST-13~23) + `i18n/messages/c5.ko.json` Phase 2 메시지 확장 |
| T3 contract | ✅ | `migration/contracts/settlement_billing.yaml` v1.1.0 — 8 신규 endpoints + customer_variants Sobo46/49 + DEC-034/035/036 |
| T4 백엔드 | ✅ | `app/services/settlement_print_service.py` (Sobo46) + `app/services/tax_invoice_service.py` (Sobo49, `_update_chek3` 단일 헬퍼) + `settlement_service.recalc_billing` + `audit_password_service.list_settlement_audit`. 라우터 누적 19 endpoints. |
| T5 마이그레이션 | (해당 없음) | Phase 2 는 신규 테이블/컬럼 없음. 기존 `audit_settlement` 활용 (액션 5종 신규 등록). |
| T6 프론트엔드 | ✅ | `/settlement/billing/[key]/print`, `/settlement/tax-invoice`, `/settlement/tax-invoice/[key]/print`, `/admin/audit-rotate` 신규. `AuditPasswordModal` → `components/shared` 공용화. `lib/audit-api.ts` 신규(verify/rotate/list 통합). `/settlement/billing` 재집계 버튼 + form-registry 갱신. 모든 위젯 `data-legacy-id`. |
| T7 회귀 | ✅ | `test/test_c5_settlement_phase2.py` 31 cases all pass + Phase 1 32 cases + C4 회귀 무영향. tsc/eslint 0오류. data-legacy-id grep 통과. `debug/probe_backend_all_servers.py` 매트릭스에 `settlement.tax_invoice` / `settlement.audit_settlement` 그룹 추가. |
| T8 거버넌스 | ✅ | DEC-034/035/036 신규 + OQ-ST-1/2/3/4 종결 + 본 §7 갱신 + dashboard 갱신 |

**Phase 2 정합성 핵심 결정**:
- **인쇄 정책 (DEC-034)**: Sobo46 청구서 + Sobo49 세금계산서 모두 **HTML 미리보기 + `window.print()`** 만 구현. PDF 생성/실제 인쇄 출력은 **C7 (라벨/송장 인쇄)** 에서 통합 — 회계용 영구 보관 PDF 와 라벨/QuickReport 가 같은 인쇄 인프라(WeasyPrint 등) 위에 올라가야 하므로 분산 구현 금지.
- **세금 외부 발행 (DEC-035)**: `POST /tax-invoice/{billing_key}/issue` 는 **`200 + status=NOT_INTEGRATED` stub** 으로만 응답하고 `audit_settlement.tax_issued_stub` 로그를 남긴다. 홈택스/이메일 등 실제 외부 채널 연동은 후속 시나리오 (외부 의존성·인증서·테스트 베드 분리). `Chek3` 토글은 별도 `/tax-invoice/chek3` 흐름으로 분리되어 외부 채널 stub 와 무관하게 동작.
- **Chek3 토글 단일 헬퍼 (DEC-036)**: 레거시 `Sobo49.pas` 의 "현재 값 반전" 토글 의미를 **백엔드 `_update_chek3(billing_keys: list)` 1곳**으로 흡수. 단건 토글과 월 일괄 토글이 동일 흐름 — 프론트는 키 배열만 전송. `assert_period_open` 가드 항상 적용.
- **마감 가드 재사용 (DEC-031 확장)**: `recalc_billing` / `update_chek3` / `update_sdate` 모두 동일 `assert_period_open` 호출 → HTTP 423. 마감 후 임의 수정 차단 일관성 유지.
- **Audit 회전 UI 통합 (OQ-ST-4 종결)**: `/admin/audit-rotate` 단일 페이지에서 `audit` (C4 패스워드, scope='audit') 와 `gpass` (C5 정산, scope='gpass_change') 회전 + 최근 `audit_settlement` / `audit_returns` 로그 열람을 통합 제공. `AuditPasswordModal` 공용화로 모달 로직 중복 제거.

## 7-C7. C7 라벨/송장 인쇄 — Phase 1 마감 (2026-04-20)

> **상태 (2026-04-20)**: T1~T10 모두 **완료**. C7 Phase 1 마감. Phase 2-α (거래처 변형 흡수) 는 별도 절로 분리.

- **범위 확정**: 5 양식 (P1-A 청구서/Sobo46, P1-B 세금계산서/Sobo49, P1-C 출고 거래명세서/Sobo27, P1-D 반품 영수증/Sobo23, P1-E 거래명세서/Sobo21) + 1 라벨 (P1-F Seep13 우편엽서). 6개 모던 미리보기 페이지에 **PDF 다운로드** 추가 + 4개 신규 미리보기 페이지 (outbound/returns/transactions/label) 신설.
- **PDF 엔진 단일화 (DEC-037)**: WeasyPrint(Python) 단일 엔진. `app.services.print_service.render_pdf` 가 HTML→PDF 변환을 책임지며, 미설치 시 `503 PR_ENGINE_UNAVAILABLE` graceful fallback. `NanumGothic` (SIL OFL) 을 `backend/static/fonts/` 에 번들.
- **신규 SQL 0건 (DEC-037 §7)**: `print_service.py` SELECT/INSERT/UPDATE/DELETE 0건. 라벨만 SQL-PR-6 (`Sg_Csum` 단건 LIMIT 1) 1건 신규. 5 양식의 detail SQL 은 모두 기존 (C2/C4/C5/C6 의 `get_*_detail`) 100% 재사용.
- **라벨 우편엽서 1종 (DEC-038)**: Seep13 의 `frReport00_01.LoadFromFile` 다중 양식 (5종) 중 우편엽서 (form=1, `Report_1_21.frf` 등가) 만 1차. `form` 파라미터는 호환성용 유지하되 `Query(1, ge=1, le=1)` 고정.
- **`.frf` 정본 = 참조용 (DEC-039)**: 98건 `.frf` (FastReport VCL 4.x 바이너리) 는 런타임 적재 0 / 자동 변환 0. HTML/CSS 는 정본을 수동 재현. T9 카탈로그 (별도 작업) + T10 OSS 파서 R&D (비차단) 로 분리.
- **OQ-002 부분 해소**: "라벨 = 서버 PDF" 분기 동결. 잔여 (라벨 직결 프린터 / Web Serial 스캐너) 는 OQ-002-R 로 분리 (Phase 2 이후).
- **회귀 매트릭스 (T7)**: `analysis/regression/c7_phase1.md` 5축 매트릭스 + DEC-028 grep + 신규 SQL 정적 검사. `debug/probe_backend_all_servers.py` 의 5 신규 그룹 (`print.outbound_statement_pdf` / `print.return_receipt_pdf` / `print.sales_statement_pdf` / `print.label_pdf` / `settlement.invoice_pdf`) 이 4 서버 전체에 라우팅 등록 검증.
- **테스트**: `test/test_c7_print_phase1.py` 22 케이스 PASS (PDF byte signature + 마감 워터마크 + 503 fallback + DEC-028 grep + 신규 SQL 0건 정적 검사 + i18n/매핑 노트/계약 정합성).

## 7-C7-α. C7 Phase 2-α — 거래처 양식 변형 + 라벨 5종 흡수 (2026-04-20)

> **상태 (2026-04-20)**: T1/T3/T5/T4/T7/T8 모두 **완료**. 18 변형 (Sobo27 v0..v9 + Sobo23 v1/v2/v3/v5 + 라벨 form 1..5) + base 3 = 총 21 양식 데이터 주도 분기. 신규 SQL 0건 + Phase 1 byte-identical 회귀 0.

- **단일 빌더 + 데이터 주도 분기 (DEC-019/028 패턴 재사용)**: `render_outbound_statement_html(detail, *, variant: str = "base")` (v0..v9), `render_return_receipt_html(detail, *, variant: str = "base")` (v1/v2/v3/v5), `label_service.render_label_html(row, *, form: int = 1)` (form 1..5). 코드 분기(if customer_id == ...) 0건 — 헤더 라벨 / `@page` CSS / `column-count` 만 차이.
- **신규 SQL 0건**: variant/form 별 데이터 동일 — Phase 1 의 `get_order_detail` / `get_return_detail` / `fetch_label_row` 100% 재사용. SELECT/INSERT/UPDATE/DELETE 추가 0건 (T4 정적 검사 TC-P2A-24d 로 보장).
- **base byte-identical 회귀**: `?variant=` 미지정 = `variant=base` = Phase 1 산출물 byte 동일 (TC-P2A-23a/b/c). `form` 미지정 = `form=1` = Phase 1 라벨 byte 동일.
- **422 가드 신설**: `PR_VARIANT_UNSUPPORTED` (Sobo27 미정의 vX, Sobo23 v4 결번), `PR_FORM_UNSUPPORTED` (라벨 form 6+, FastAPI Query `le=5` 1차 차단). 라우터 단계 차단 → 서비스 미진입.
- **Sobo23 v4 결번 처리**: `Report_2_13-4.frf` 부재 (거래처 4 폐업/공유 추정 — 운영 SME 확인 필요). `?variant=v4` → 422 + 결번 안내 메시지로 가시화. `customer_variants.Sobo23.pdf_variants` 에 명시.
- **회귀 매트릭스**: `debug/probe_backend_all_servers.py` 에 `print.outbound_statement_pdf_variant` (?variant=v0) + `print.return_receipt_pdf_variant_v4_must_422` (?variant=v4 → 422 단정) + `print.label_pdf_form2` (?form=2) 3 그룹 신규. 4 서버 전체 라우팅 등록 검증.
- **테스트**: `test/test_c7_print_phase2_alpha.py` 15 testcase + 19 subtest PASS. Phase 1 회귀 22 + Phase 2-α 15 = 총 37 PASS. Phase 1 의 `version: 1.0.0` 정확 매칭 단언은 `version: 1.x.y` 정규식으로 완화 (재귀 회귀 차단 — 사용자 룰 "수정 시 이전 케이스도 고려").
- **계약**: `migration/contracts/print_invoice.yaml` v1.1.0 (D-PR-5 + Sobo27.pdf_variants 11종 + Sobo23.pdf_variants 5종), `migration/contracts/print_label.yaml` v1.1.0 (D-LB-1 갱신 + label_forms 1..5).

## 7-C7-β. C7 Track B4 — `.frf → HTML` 자동 변환 PoC (1일 비차단, 2026-04-20)

> **상태 (2026-04-20)**: PoC 1일 **완료** — `analysis/research/c7_b4_poc_1day_report.md` 산출. **Phase 3 진입 보류** 결정. DEC-039 정책 유지 (운영 .frf 자동 변환 0).

- **PoC 결과 (3 가설)**: H1 `.frf → .frx` 변환기 = ⚠️ 부분 가능 (1일 미완, RDL 임포터 988 LOC 템플릿 검증). H2 `HTMLExport(Layers=true)` = ✅ 소스 분석 100% 검증 (`<div style="position:absolute">` 패턴 = WeasyPrint 100% 호환). H3 Jinja2 placeholder 주입 = ⚠️ marker patch 필요 (`OnObject` 이벤트 hook).
- **B4 작업 분해 갱신**: T10 §1.8 추정 4.5~8.5 인주 → PoC 후 5.5~9.5 인주 (+1 인주, H3 marker patch 부담 가시화). 자체 파서 B1 (6~13 인주) 대비 30~40% 절감 결론은 유효.
- **Phase 3 진입 조건**: ① 운영 SME 협의 (98 양식 디자인 변경 빈도 통계), ② 자체 파서 vs B4 비교 회의록, ③ R&D 1.5~2 사람-월 가용성. C9 이후 신규 시나리오 (C10/C11) 우선 진행 후 재평가.
- **운영 영향 0**: C7 Phase 1/Phase 2-α 운영 코드 변경 0줄. .NET 런타임 운영 도입 0. DEC-039 (운영 .frf 자동 변환 0) 유지.

## 7-C8. C8 바코드 스캔 → 출고/입고/반품 매칭 — Phase 1 마감 (2026-04-20)

> **상태 (2026-04-20)**: T1~T8 모두 **완료**. C8 Phase 1 마감. DEC-010 후속 작업 마감 (C2 D-OUT-2 흡수). Web Serial 직결만 OQ-002-R 잔류.

- **범위 확정**: 1 엔드포인트 (`POST /api/v1/scan/match`) + 1 공통 컴포넌트 (`components/shared/scan-input.tsx`) + 3 페이지 통합 (출고 `outbound/orders/[orderKey]`, 입고 `inbound/receipts/[receiptKey]`, 반품 `returns/receipts/[returnKey]`). 레거시 `Tong08.ComPortRxChar(#13) → Sobo*.FTong07.Button104Click → Tong07.Button100Click` 의 모던 등가.
- **서버/클라이언트 분리 (DEC-040)**: 서버는 G4_Book ISBN 매칭 + G1/G2_Ggeo 단가 폴백 (`Hcode='' 1순위 → 라인 Hcode 2순위`, 레거시 정합) → `resolved` 라인 객체만 반환. 라인 추가/저장은 클라이언트가 기존 `PUT /orders/{key}` (C2) / `PUT /inbound/receipts/{key}` (C3) / `PUT /returns/receipts/{key}` (C4) **desired-state diff** 흐름 그대로 사용 → **백엔드 회귀 0** 보장.
- **신규 SQL 0건 (DEC-040)**: G4_Book SELECT 1건 (ISBN 정확 매칭, 단건 LIMIT 1) + G1/G2_Ggeo SELECT 최대 2건 (Hcode 폴백). 모두 기존 마스터 테이블 재해석. INSERT/UPDATE/DELETE 0건. `pricing_service.resolve_grats(context, gcode, hcode, server_id)` 단일 헬퍼로 추출 (DRY + LSP — outbound/inbound/returns 향후 단가 조회도 본 헬퍼로 흡수 가능).
- **USB-HID 키보드 웨지 1차 (DEC-004)**: `lib/scanner.ts` 가 keydown 버퍼 + Enter(CR) 종결 + 50ms 무입력 디바운스 + 사람 입력 vs 웨지 구분 (키 간격 < 30ms). Web Serial 직결은 OQ-002-R 잔류 (Phase 2 이후).
- **단일 진입 컴포넌트 (DEC-028 룰 7)**: 모든 통합 페이지는 `ScanInput` 1 컴포넌트만 임포트. 입력 박스에 `data-legacy-id="FTong07.Edit101"` 부착 (레거시 Tong07.pas Edit101.Text 모던 등가). 토스트 영역에 `data-legacy-id="FTong07.Body_Data"` 부착 (레거시 nMsg.Body_Data 위치).
- **i18n (`c8.ko.json`) 8 키**: `scan.placeholder` / `scan.matched` / `scan.nodata` / `scan.duplicate` / `scan.error` / `scan.context.required` / `scan.no_grats` / `scan.input.disabled`.
- **회귀 매트릭스 (T7)**: `analysis/regression/c8_phase1.md` 5축 매트릭스. `debug/probe_backend_all_servers.py` 의 `scan.match` 1 그룹 신규 (POST 메서드 지원 추가) — 4 서버 전체에 라우팅 등록 검증. tsc/eslint 0 error.
- **테스트**: `test/test_c8_scan_phase1.py` 22 케이스 PASS (matched/nodata × 3 context + 단가 폴백 우선순위 + 4 server matrix + 신규 DML 0건 정적 검사 + ScanInput 통합 grep + i18n/handlers/contract 정합성).

## 7-C10. C10 권한 관리 Full — Phase 1 마감 (2026-04-20)

> **상태 (2026-04-20)**: T1~T8 모두 **완료**. C10 Phase 1 마감. Wave D 가드 강제(D-ADM-1) closed. Wave D 비번/audit(D-ADM-3) partial (Subu45 흡수). DEC-041/042/043 신규 동결. OQ-RT-7 (D_Select) **마감** — 헬퍼 인터페이스만이 아니라 실분기까지 도입.

- **범위 확정 (Full)**: (i) `app/core/deps.py::require_permission(code)/require_role(code)` 1 의존으로 RBAC 가드 통합. (ii) `Id_Logn` F11~F89 권한 매트릭스 — `/admin/id-logn` 단일 페이지 (사용자 CRUD + Fxx 매트릭스 + 비번 리셋). (iii) `d_select.py` 실분기 (admin = 1=1 / branch_manager·auditor = `Server_id` / operator = `Branch_id AND Hcode`). (iv) C13 (세션·권한 응답 코드 표준 + 글로벌 401/403 인터셉터 + 자동 refresh). (v) C15 (If-Match/ETag 낙관적 동시편집 — 428/409). (vi) Subu40 비번 모달 = 기존 `audit-password-modal.tsx` 100% 재사용 (DEC-029). (vii) DEC-043 IdP/SSO 인터페이스 (`auth_provider.py` — `LegacyIdLognProvider` 1구현체 + `Saml`/`Oidc` NotImplemented stub).
- **신규 SQL 0건 (DEC-040 룰 적용)**: `Id_Logn` 5 SQL 패턴 (Chul.pas L441 SELECT Hcode/Hname/Pdate, L1724 SELECT Server_id/Branch_id, L2451/L2452 Seek_Uses 권한 매트릭스, Subu45.pas L364 UPDATE Gpass) 100% 재사용. INSERT/DELETE/CREATE TABLE 0건 (`test_S_08_id_logn_service_no_new_dml` 정적 검사). C10 Phase 1 은 in-memory `_empty_seed` 시드로 운영 — Phase 2 에서 실 MySQL 연결 (회귀 면적 제로 분리).
- **F11~F89 카탈로그 30 정본 + 50 예약**: `legacy-analysis/permission-keys-catalog.md` — Chul.pas 80 `Seek_Uses(...)` 호출 지점 인덱싱 + 30 정본 매핑 (admin.user.read = F18r 신규). 매트릭스 셀 값 = `O`(read-write) / `R`(read-only) / `X`(deny) / 공백(미지정 = X). `test_G_05_unknown_permission_code_fails_fast` — 라우터에서 사용하는 모든 `permission_code` 가 카탈로그에 존재하는지 정적 검사.
- **C13 세션/권한 (DEC-041)**: 401 코드 = `AUTH_NO_TOKEN` / `AUTH_TOKEN_EXPIRED`, 403 코드 = `PERMISSION_DENIED` 표준화. `lib/api-client.ts` 가 `AUTH_TOKEN_EXPIRED` 수신 시 1회 `attemptRefresh` (`__noRefresh` flag 무한루프 차단), 실패 시 `/login?reason=expired` 이동. `middleware.ts` 가 `/admin/*` 경로의 `access_token` 쿠키 부재 시 client-side `PermissionGuard` 폴백.
- **C15 동시편집 (DEC-042)**: `app/core/concurrency.py` — `compute_etag(payload, revision)` (SHA-256 또는 revision) + `set_etag(response)` + `require_if_match()` Depends (헤더 부재 시 428 `PRECONDITION_REQUIRED`) + `check_etag(provided, expected)` (불일치 시 409 `STALE_VERSION`). `/admin/id-logn/{hcode}` PUT/permissions PUT 2 엔드포인트에 적용. 마스터/주문/정산 동일 정책으로 후속 라우터 점진 도입 가능.
- **DEC-043 IdP/SSO 분리**: `app/core/auth_provider.py` — `AuthProvider` 추상 (`authenticate` + `reset_password`) + `LegacyIdLognProvider` (Subu40 흡수) + `SamlProvider`/`OidcProvider` NotImplemented stub. `select_provider("legacy_id_logn")` 디폴트 — `saml`/`oidc` 는 향후 외부 IdP 연동 시 인터페이스 구현체 추가만으로 흡수 (OCP).
- **자기차단/슈퍼유저 가드 (422)**: `update_user_with_permissions` 가 `ID_LOGN_SELF_REVOKE` (자기 자신의 admin.user.write 권한 회수 시 422), `ID_LOGN_SUPER_USER_PROTECTED` (Hcode='0000' 시드 슈퍼유저 정보 수정 시 422) 가드. 자동화 회귀 (`test_R_09_self_revoke_blocked_422`, `test_R_10_super_user_protected_422`).
- **회귀 매트릭스 (T7)**: `analysis/regression/c10_phase1.md` 5축 + DEC trace + DEC-028 grep 검증. `debug/probe_backend_all_servers.py` 신규 4 그룹 (`admin.id_logn_list` / `admin.permission_matrix_stale_must_409` / `auth.expired_must_401` / `concurrency.precondition_required_must_428`) — 4 server × 4 = 16 행 (PUT 메서드 + extra headers 지원 추가).
- **테스트**: `test/test_c10_admin_phase1.py` 24 PASS (S 9 정적 + R 11 런타임 가드 매트릭스 + d_select 3 + G 2 회귀). axis_test_full = 333 PASS / 3 skip (사전 broken `dfm2html`/`res_string` 무관). tsc/eslint 0 error.
- **i18n (`c10.ko.json`)**: 세션 만료 / 권한 거부 / 동시편집 충돌 / Id_Logn 매트릭스 / 자기차단 / 슈퍼유저 보호 / 비번 자동 발급 메시지 정본.

### 7-C10 OQ-RT-7 마감

| 항목 | Phase 2 (C4) | C10 Phase 1 |
|---|---|---|
| `D_Select` 헬퍼 | 인터페이스만, 항상 `1=1` (DEC-009 잠금) | **실분기 도입** — `app/core/d_select.py::build_d_select_clause(table, user_context)` 가 admin/branch_manager/auditor/operator 4 분기 |
| `Authorization-Context` 헤더 | noop (선택적) | `app/core/deps.py::get_user_context` 가 JWT claim 우선 + 헤더 fallback |
| 슈퍼유저 (Hcode='0000') | 미정의 | `is_super_user` 정책 동결 + `admin.user.write` 자동 부여 |
| `legacy_permission_map` v1.x | seed v1.0 (7 키) | v1.1 (30 정본 + admin.user.read F18r 추가) |

OQ-RT-7 closure 조건 모두 충족 — 본 페이즈로 마감 (`legacy-analysis/open-questions.md` 후속 갱신 대상).

## 7-EXT. 확장 라인 v0.2 (C11/C13/C14/C15) — 진입 게이트 + 공수 추정 + 게이트 #6/#7 정의

> **상태 (2026-04-20)**: 4 시나리오 모두 v1.0 contract **frozen** + Phase 1 백엔드/스크립트/회귀 테스트 **완료**. 외부 시스템 연동 제외 (DEC-044 정합).

### 7-EXT.1 공수/일정 추정표 (sprint = 5 영업일 기준, 메인개발자 1인 기준)

| 시나리오 | 단계 | T1~T4 (분석/계약/스켈레톤) | T5 (백엔드/스크립트) | T6 (프론트) | T7 (회귀/통합) | T8 (DEC/문서/대시보드) | 합계 (인일) |
|---|---|---|---|---|---|---|---|
| **C11** Mobile UAT | Phase 1 (현 사이클) | 1.0 | 0.5 (ScanInput 모바일 보강) | 1.5 (5 디바이스 × 4 시나리오 정합 검증) | 1.0 (37 테스트) | 0.5 | **4.5** |
| **C13** Stats/Reports | Phase 1 (현 사이클) | 1.5 (Sobo50~55 인벤토리) | 1.5 (stats_service + 4 endpoint, 신규 SQL 0) | 2.5 (4 화면 + recharts) | 1.5 (12 테스트 + 수치 동등성) | 1.0 | **8.0** |
| **C14** Ops Monitoring | Phase 1 (현 사이클) | 1.0 (라벨 카디널리티 정책) | 2.0 (ops_service: ring+Prometheus+/health/full) | 1.5 (audit/alerts UI + 배너) | 1.5 (13 테스트) | 1.0 | **7.0** |
| **C15** Cut-over | Phase 1 (현 사이클) | 1.5 (테이블 인벤토리, validator 5종) | 2.0 (cutover_validator.py + InMemoryDataSource) | 0.5 (대시보드 진행 표기) | 1.5 (13 테스트) | 1.5 (OQ closure 표 + DEC-044) | **7.0** |
| **합계 (Phase 1)** |  | 5.0 | 6.0 | 6.0 | 5.5 | 4.0 | **26.5 인일 ≈ 5.3 sprint** |

> 본 추정은 *Phase 1 (정책 동결 + 정적/단위 회귀)* 기준. Phase 2 (실제 운영 DB 연결, recharts UI 풀 구현, MysqlDataSource 구현, 4 server cut-over 리허설) 는 본 표의 1.5~2× 추가 산정 권장.

### 7-EXT.2 신규 게이트 #6 / #7 정의

확장 라인 v0.2 의 종료를 위해 기존 게이트 #1~#5 와 별도로 다음 2 게이트를 신설한다.

#### 게이트 #6 — 운영 SLA (C14 종료 / 외부 시스템 연동 없이 self-hosted 모니터링 합격)

| 차단 조건 | 측정 방법 | 마감 행위자 |
|---|---|---|
| `/health/full` 의 DM-1~3 매핑이 운영 환경에서 5분 단위 health check 결과와 일치 | `test_c14_ops_phase1::test_R_01_health_full_dependency_split` + 운영 4 server probe | 운영팀 |
| `/metrics` 의 라벨 카디널리티가 정책 (≤ 50 unique value/metric) 을 위반 0건 | `test_R_06_metrics_no_forbidden_labels` + 운영 환경 1 시간 운영 후 unique label count grep | 메인개발자 |
| audit 통합 뷰가 admin/operator/branch_manager 3 role d_select 정합 | `test_R_05_audit_operator_dselect` 통과 + UAT 1 회 시연 | 메인개발자 + 사용자 |
| in-app 알림 배너가 critical 알림 수신 후 60s 내에 화면 노출 | UAT 시뮬레이션 (메인개발자가 push_alert + 사용자 확인) | 사용자 |

#### 게이트 #7 — Cut-over (C15 종료 / 4 server 운영 전환 + 24h 검증 + RTO ≤ 15분)

| 차단 조건 | 측정 방법 | 마감 행위자 |
|---|---|---|
| 4 server (138/153/154/155) 모두 cutover_validator 5 check 100% PASS | `python3 scripts/cutover_validator.py --legacy ... --modern ...` 4 회 모두 exit code 0 | 메인개발자 |
| OQ 차단 게이트 (OQ-IN-1, OQ-DBL-001/003) cutover_block:false 로 전환 (또는 우회 정책 동결) | `legacy-analysis/open-questions.md` §"Cut-over 진입 차단 게이트" 표 갱신 | 메인개발자 + 사용자 |
| 롤백 dry-run 1회 PASS (RTO ≤ 15분 측정) | 운영팀 리허설 (DNS 스위치 + read-only 전환 시간 측정) | 운영팀 |
| 24시간 운영 검증 (cut-over 후 0 critical 결함) | 운영 모니터링 (게이트 #6 자동화) + audit 큐 critical 0건 | 운영팀 + 사용자 |

본 두 게이트는 `dashboard/data/approvals.json` 의 #6 / #7 슬롯에 등록 (대시보드 sync 작업에서 진행).

## 8. 변경 이력

- 2026-04-20 — §7-EXT 신규 (확장 라인 v0.2 — C11/C13/C14/C15 Phase 1 마감). 공수 추정 26.5 인일. 게이트 #6 (운영 SLA) / #7 (Cut-over) 신규 정의. DEC-044 동결 (외부 시스템 연동 제외 + 신규 SQL 0건). C13 12 PASS / C14 13 PASS / C15 13 PASS / C11 37 PASS = 75 신규 회귀.
- 2026-04-20 — §7-C10 신규 (C10 Phase 1 Full: T1~T8 모두 완료, 24 PASS + axis_test_full 333 PASS). DEC-041/042/043 동결. OQ-RT-7 마감 (D_Select 실분기). Wave D D-ADM-1 closed / D-ADM-3 partial. 신규 SQL 0건.
- 2026-04-20 — §7-C7-β 신규 (Track B4 PoC 1일 비차단 완료, `analysis/research/c7_b4_poc_1day_report.md` 산출). 가설 3개 평가 (H1 부분, H2 ✅, H3 ⚠️). B4 작업 분해 5.5~9.5 인주로 갱신. **Phase 3 진입 보류** 결정 (운영 SME 협의 + ROI 비교 + R&D 가용성 3 조건 미충족). DEC-039 정책 유지 (운영 .frf 자동 변환 0).
- 2026-04-20 — §7-C7-α 신규 (C7 Phase 2-α: T1/T3/T5/T4/T7/T8 모두 완료, 15 testcase + 19 subtest PASS, 신규 SQL 0). DEC-019/028 패턴 재사용 (단일 빌더 + variant/form 인자 데이터 주도 분기). 18 변형 (Sobo27 v0..v9 + Sobo23 v1/v2/v3/v5 + 라벨 form 1..5) 흡수. 422 PR_VARIANT_UNSUPPORTED/PR_FORM_UNSUPPORTED 가드 신설. base byte-identical 회귀 0. Phase 1 회귀 1건 (version 정확 매칭) 정규식으로 완화 (재귀 회귀 차단).
- 2026-04-20 — §7-C8 신규 (C8 Phase 1: T1~T8 모두 완료, 22 pass + 신규 SQL 0). DEC-040 동결 (서버 매칭 + 클라이언트 라인 반영 분리). DEC-010 후속 마감 표시 (C2 D-OUT-2 흡수). OQ-002 → OQ-002-R 분리 (Web Serial 직결만 잔류).
- 2026-04-20 — §7-C7 마감 (T1~T10 완료). T8 거버넌스 + T9 frf_catalog (98건 인벤토리, 5+1 매핑, Phase 2 변형 정책) 동기화. frf_catalog §2 명명 가이드 부연 (「Sobo 번호 ≠ Report 번호」 혼동 차단).
- 2026-04-20 — §7-C7 신규 (C7 Phase 1: T1~T7 완료, T8 진행 중, T9/T10 PENDING/R&D). DEC-037/038/039 동결, OQ-002 부분 해소. DEC-004 보강 (라벨 = 서버 PDF 분기 = WeasyPrint 단일 엔진).
- 2026-04-19 — §C5 정산 Phase 2 진행 현황 추가 (T1~T8 모두 완료, 31 pass + Phase 1·C4 회귀 무영향). DEC-034/035/036 동결, OQ-ST-1/2/3/4 종결.
- 2026-04-19 — §C5 정산 Phase 1 진행 현황 추가 (T1~T8 모두 완료, 32 pass + C4 회귀 무영향). DEC-031/032 동결.
- 2026-04-19 — §C4 Phase 2 진행 현황 추가 (T1~T8 모두 완료, 27 pass/3 skip).
- 2026-04-19 — §C4 Phase 2 권고: DEC-030 에 따라 OQ-RT-1/2/3 → OQ-RT-7/8/9 로 재번호 (contract OQ-RT-1~6 정본).
- 2026-04-19 — §7 C4 반품 처리 1차 완료 현황 + Phase 2 권고 추가. DEC-029 동결.
- 2026-04-19 — §5 운영 룰 7 신규 (dfm→html 산출물 참조 의무, DEC-028 동결).
- 2026-04-18 — 최초 작성. C1~C10 매핑·DEC-003 단계 0~5·T1~T8 공통 절차 동결, hostingscreens.json 신설.

---

*관련: [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md), [`docs/screen-cards-generation-plan.md`](screen-cards-generation-plan.md), [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md), [`docs/decision-print-scanner-web.md`](decision-print-scanner-web.md), [`legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md`](../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md)*
