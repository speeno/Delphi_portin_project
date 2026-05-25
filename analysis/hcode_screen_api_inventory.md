# Hcode 격리 화면·API 인벤토리

작성: 2026-05-25 — 「Hcode 격리 전면 적용」 Phase 0 산출물.

본 문서는 hcode 검색 UI 가 있는 레거시 화면, 모던 라우터, 프론트 페이지를 1:1 로 매핑하고
각 엔드포인트의 **빈 hcode 처리 정책**(`hcode_query_policy`)을 단일 정본으로 고정한다.

## 1. 정책 태그

| 태그 | 정의 | 적용 계정 (ACC-DATA-03) |
|------|------|------------------------|
| `coalesce_jwt` | 쿼리 `hcode` 가 비면 **JWT scope hcode** 자동 주입. | T2_PUB · T3 공유 DB(chul_09) → 강제 / T1·T2_DIST·super → `None` 반환 → 전체 |
| `optional_wide` | 빈 `hcode` = 전체 조회. coalesce 호출은 하되, 헬퍼가 정책상 `None` 을 돌려줘 결과적으로 무필터. | T1·T2_DIST 가 주 사용 — 동일 코드 경로로 통일 (DEC-033 f) |
| `implicit_scope` | 쿼리 `hcode` 자체가 없음. 라우터가 항상 `resolve_scope_hcode(ctx)` 적용. | 마스터·자동완성 (이미 적용) |
| `key_identity` | `hcode` 가 식별자(합성키)라 격리 의미 없음. coalesce 불필요. | 단건 메모/상세 PATCH 등 |
| `range_filter` | `hcodeFrom/hcodeTo` 범위 검색. coalesce 적용 안 함 (총판 운영 화면). | NAV-16 택배 |
| `n_a` | hcode 파라미터 없음. | (대다수 비대상) |

## 2. 엔드포인트 매트릭스 (P0 → P1 → 비대상)

상태 컬럼: `OK` = 이미 coalesce/resolve 적용 / `GAP` = 본 계획 대상 / `KEEP` = 변경 없음.

### 2.1 P0 — 데이터 노출 위험 큼

| 라우터 파일 | Method · Path | 정책 | 상태 | 레거시 | 모던 라우트 |
|---|---|---|---|---|---|
| [`transactions.py`](../도서물류관리프로그램/backend/app/routers/transactions.py) | GET `/api/v1/transactions/sales-statement` | `coalesce_jwt` | GAP | Sobo21 | `/(app)/transactions/sales-statement` |
| 〃 | GET `/api/v1/transactions/status` | `coalesce_jwt` | GAP | Sobo21_status | 위 페이지 내 탭 |
| 〃 | GET `/api/v1/transactions/other` | `coalesce_jwt` | OK | Sobo29 | `/(app)/transactions/other` |
| [`outbound.py`](../도서물류관리프로그램/backend/app/routers/outbound.py) | GET `/api/v1/outbound/orders` | `coalesce_jwt` | GAP | Subu27/Sobo27 | `/(app)/outbound/orders` |
| 〃 | GET `/api/v1/outbound/shipment-status` | `coalesce_jwt` | GAP | Sobo67 | `/(app)/outbound/status` |
| [`inbound.py`](../도서물류관리프로그램/backend/app/routers/inbound.py) | GET `/api/v1/inbound/receipts` | `coalesce_jwt` | GAP | Sobo38 | `/(app)/inbound/receipts` |
| [`returns.py`](../도서물류관리프로그램/backend/app/routers/returns.py) | GET `/api/v1/returns` | `coalesce_jwt` | GAP | Sobo23/22 | `/(app)/returns/receipts` |
| 〃 | GET `/api/v1/returns/reports/daily` | `coalesce_jwt` | GAP | Sobo55 | `/(app)/returns/reports` |
| 〃 | GET `/api/v1/returns/ledger` | `coalesce_jwt` | GAP | Sobo32_1/Sobo34_4 | `/(app)/returns/ledger` |
| 〃 | GET `/api/v1/returns/period-report` | `coalesce_jwt` | GAP | Sobo58 | `/(app)/returns/period-report` |

### 2.2 P1 — 정산·통계·기타 GET

| 라우터 파일 | Method · Path | 정책 | 상태 | 레거시 |
|---|---|---|---|---|
| [`settlement.py`](../도서물류관리프로그램/backend/app/routers/settlement.py) | GET `/api/v1/settlement/billing` | `coalesce_jwt` | GAP | Sobo45_billing |
| 〃 | GET `/api/v1/settlement/billing/period` | `coalesce_jwt` | GAP | Sobo47_billing |
| 〃 | GET `/api/v1/settlement/outstanding` | `coalesce_jwt` | OK | Sobo48 |
| 〃 | GET `/api/v1/settlement/cash` | `coalesce_jwt` | GAP | Sobo41_cash/Sobo42 |
| 〃 | GET `/api/v1/settlement/cash-status` | `coalesce_jwt` | OK | Sobo42_cash |
| 〃 | GET `/api/v1/settlement/tax-invoice` | `coalesce_jwt` | GAP | Sobo49_tax |
| [`stats.py`](../도서물류관리프로그램/backend/app/routers/stats.py) | GET `/api/v1/stats/sales-period` | `coalesce_jwt` | GAP | (C13 신규) |
| 〃 | GET `/api/v1/stats/customer-analysis` | `coalesce_jwt` | GAP | (C13 신규) |
| 〃 | GET `/api/v1/stats/book-turnover` | `coalesce_jwt` | GAP | (C13 신규) |
| 〃 | GET `/api/v1/stats/publisher` | `coalesce_jwt` | GAP | (C13 신규) |
| 〃 | GET `/api/v1/stats/quarterly-summary` | `coalesce_jwt` | GAP | Sobo62 류 |
| 〃 | GET `/api/v1/stats/dashboard/*` (7건) | `coalesce_jwt` | GAP (KPI 전용 헬퍼만 존재) | 대시보드 |
| [`inventory.py`](../도서물류관리프로그램/backend/app/routers/inventory.py) | GET `/api/v1/inventory/ledger` | `coalesce_jwt` | OK | Sobo31 |
| [`reports.py`](../도서물류관리프로그램/backend/app/routers/reports.py) | GET `/api/v1/reports/book-sales` | `coalesce_jwt` | OK | Sobo61 |
| 〃 | GET `/api/v1/reports/customer-sales` | `coalesce_jwt` | OK | Sobo62 |
| 〃 | GET `/api/v1/reports/year-end-book` | `coalesce_jwt` | OK | Sobo67_yearbook |
| [`masters.py`](../도서물류관리프로그램/backend/app/routers/masters.py) | GET `/api/v1/masters/special` | `coalesce_jwt` | OK | Sobo16 |
| 〃 | 기타 28엔드포인트 | `implicit_scope` | OK | C2/C9 마스터 |

### 2.3 비대상 (변경 없음)

| 라우터 파일 | 엔드포인트 | 정책 | 사유 |
|---|---|---|---|
| [`courier.py`](../도서물류관리프로그램/backend/app/routers/courier.py) | GET `/lines` | `range_filter` | `hcodeFrom/hcodeTo` 범위 (NAV-16 D-KBT 단독 — 총판 운영) |
| 〃 | GET/PATCH `/memo` | `key_identity` | `hcode` 가 합성키의 일부 |
| [`dashboard_external.py`](../도서물류관리프로그램/backend/app/routers/dashboard_external.py) | GET `/weather-risk` 등 3건 | `coalesce_jwt` (선택) | 외부 API 라우팅 키. 빈 hcode 시 경고 단순화 — 정합 위해 P1 끝에 흡수 |
| [`transactions.py`](../도서물류관리프로그램/backend/app/routers/transactions.py) | PATCH `/other/memo`, `/sales-statement/{key}/memo`, GET `/sales-statement/{order_key}` | `key_identity` | path/body 의 hcode 가 키 식별자 |
| [`outbound.py`](../도서물류관리프로그램/backend/app/routers/outbound.py) | POST/PUT/PATCH `/orders/...` | `key_identity` | order_key 합성키 |
| [`inbound.py`](../도서물류관리프로그램/backend/app/routers/inbound.py) | GET `/reports/daily`, `/reports/period` | `n_a` | hcode 파라미터 없음 |
| [`returns.py`](../도서물류관리프로그램/backend/app/routers/returns.py) | 단건/처리 엔드포인트 | `key_identity` | return_key 합성키 |
| [`settlement.py`](../도서물류관리프로그램/backend/app/routers/settlement.py) | billing/{key}/* PATCH/POST, tax-invoice/{key}/issue 등 | `key_identity` | billing_key 합성키 |

## 3. 화면 ↔ API 매핑 (검색 UI에 hcode 입력 있음)

레거시 폼 38건([`analysis/layout_mappings`](layout_mappings/) 기준).

| 레거시 폼 | 화면 | 모던 페이지 | 백엔드 API | 상태 |
|---|---|---|---|---|
| Sobo21 | 거래명세서 목록 | `/(app)/transactions/sales-statement` | `transactions.list_sales_statements` | GAP → P0 |
| Sobo29 | 기타/신간 명세서 | `/(app)/transactions/other` | `transactions.list_other_statements` | OK |
| Sobo27 | 출고 목록 | `/(app)/outbound/orders` | `outbound.list_orders` | GAP → P0 |
| Sobo67 | 출고현황 집계 | `/(app)/outbound/status` | `outbound.list_shipment_status` | GAP → P0 |
| Sobo38 / Sobo38_inbound | 입고 목록 | `/(app)/inbound/receipts` | `inbound.list_receipts` | GAP → P0 |
| Sobo23 / Sobo22 | 반품 목록 | `/(app)/returns/receipts` | `returns.list_returns` | GAP → P0 |
| Sobo24 / Sobo25 / Sobo51 | 반품 처리 | (각 페이지) | `returns.process_*` | KEEP (key_identity) |
| Sobo32 / Sobo32_1 / Sobo34_4 | 반품 재고원장 | `/(app)/returns/inventory`, `/(app)/returns/ledger` | `returns.get_returns_ledger` | GAP → P0 |
| Sobo55 | 반품 일별 보고서 | `/(app)/returns/reports` | `returns.daily_report` | GAP → P0 |
| Sobo58 | 반품 기간 보고서 | `/(app)/returns/period-report` | `returns.get_returns_period_report` | GAP → P0 |
| Sobo31 | 도서별 수불원장 | `/(app)/inventory/ledger` | `inventory.get_inventory_ledger` | OK |
| Sobo61 | 도서별 판매 | `/(app)/reports/book-sales` | `reports.get_book_sales` | OK |
| Sobo62 | 거래처별 판매 | `/(app)/reports/customer-sales` | `reports.get_customer_sales` | OK |
| Sobo16 | 특별관리 | `/(app)/master/special` | `masters.list_special_master` | OK |
| Sobo41_cash / Sobo42_cash / Sobo42_1_cash | 입금/현금 | `/(app)/settlement/cash`, `/cash-status` | `settlement.list_cash`, `settlement.cash_status` | cash_status OK / cash GAP → P1 |
| Sobo45_billing / Sobo45_1_billing / Sobo46_billing | 청구서 | `/(app)/settlement/billing` | `settlement.list_billing`, `aggregate_billing`, `confirm_billing`, `cancel_billing`, `get_billing_detail`, `recalc_billing`, `get_billing_print_*` | list/period GAP → P1 / 단건은 key_identity |
| Sobo47_billing | 청구 기간 | `/(app)/settlement/period` | `settlement.list_period_summary` | GAP → P1 |
| Sobo48 | 미수금 | `/(app)/settlement/outstanding` | `settlement.list_outstanding` | OK |
| Sobo49_tax | 세금계산서 | `/(app)/settlement/tax-invoice` | `settlement.list_tax_invoices`, `toggle_tax_chek3`, `update_tax_sdate`, `issue_tax_invoice` | list GAP → P1 / 처리는 key_identity |
| Sobo54 / Sobo57 | 일별·기간 입고내역서 | `/(app)/inbound/reports/*` | `inbound.daily_report`, `period_report` | n_a |
| Sobo28 | 택배 | `/(app)/shipping/courier` | `courier.*` | range_filter / key_identity |
| Sobo11 / Sobo14 / Sobo17 / Sobo38 / Sobo39 | 마스터 | `/(app)/master/*` | `masters.*` | implicit_scope OK |
| Sobo25 | 반품 분해 검색 | `/(app)/returns/inventory` | (returns ledger 재사용) | (포함) |
| Subu40 | 패스워드 검증 | (모달) | `audit/password-verify` | n_a |
| Id_Logn | 로그인 | `/login` | `auth.*` | n_a |
| c8_scan_match | 스캔 매칭 | `/(app)/scan` | `scan.*` | n_a |

## 4. 4대 DB 영향

| 서버 | 격리 강제 계정 예 | 본 계획 적용 후 |
|---|---|---|
| `remote_138` | T2_PUB / T3 공유 | 동일 코드 경로 (분기 없음) |
| `remote_153` | 위러브1·2·3 + 교문사 (chul_09 SKU) | 동일 |
| `remote_154` | (차단 해소 후) 동일 | 동일 |
| `remote_155` | T2_PUB | 동일 |

DB 별 분기 금지 — 정책 스위치는 [`get_user_context`](../도서물류관리프로그램/backend/app/core/deps.py) 의 `account_type`/`account_family` 만.

## 5. 후속 산출물

- Phase 1: P0 4 라우터 → P1 settlement/stats/dashboard 일괄 패치.
- Phase 2: [`tools/audit_router_hcode_coalesce.py`](../tools/audit_router_hcode_coalesce.py) 신규.
- Phase 3: [`migration/contracts/*.yaml`](../migration/contracts/) 의 각 GET 에 `hcode_query_policy` 키 추가, [`docs/onboarding-rbac-menu-matrix.md`](../docs/onboarding-rbac-menu-matrix.md) `ACC-DATA-03` 표 보강.
