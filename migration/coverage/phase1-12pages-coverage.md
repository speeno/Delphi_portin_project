# Phase1 12개 재사용 화면 — 동등성 커버리지 매트릭스

**ID**: COVERAGE-PHASE1-12P
**일자**: 2026-04-21
**연관 문서**: `docs/phase1-promotion-gate.md`, `legacy-analysis/decisions.md` DEC-NN
**목적**: 12개 재사용 화면(현재 `phase: "phase2"`) 의 T1~T7 산출물 매핑.
**상태**: draft (각 PR 단위로 PASS/FAIL 채움)

---

## 0. 표 범례

- **T1** screen_card / **T2** event_sql_extract → `analysis/screen_cards/<Form>.md`
- **T3** contract → `migration/contracts/<flow>.yaml`
- **T6** test_pack → `migration/test-cases/<flow>.json`
- **상태**: ✅ 보유 / 🟡 부분(작성 필요) / ❌ 부재

---

## 1. 12개 화면 매트릭스

| # | UI 경로 | 레거시 폼 | T1·T2 (screen_card) | T3 (contract) | T6 (test_pack) | 회귀 러너 그룹 | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | `outbound/status` | TSobo10/14/15 | ✅ Sobo10/14/14_1/15 | ✅ `outbound_order.yaml` | ✅ `outbound_order.json` | `outbound.list_orders` | C2 — 신규 contract 추가 0건 |
| 2 | `inventory/status` | TSobo44 | ✅ Sobo44 | 🟡 (Sobo31 ledger 재사용 — 동등성 항목 추가 필요) | 🟡 `sales_inquiry.json` 의 `TC-INQ-LEDGER-*` 재사용 | `inventory.ledger` | 본 매트릭스 §2.1 patch 항목 참조 |
| 3 | `settlement/outstanding` | TSobo67/68/69 | ✅ Sobo67/68/69 + c5_settlement | ✅ `settlement_billing.yaml` | ✅ `settlement_billing.json` | `settlement.outstanding` | 본 매트릭스 §2.2 patch 항목 참조 |
| 4 | `settlement/payment-slip` | TSobo71/Subu70 | ✅ Sobo71 + c5_settlement | ✅ `settlement_billing.yaml` (cash_list) | ✅ `settlement_billing.json` | `settlement.cash_list` | (동일 contract) |
| 5 | `transactions/status` | TSobo21 | ✅ Sobo21 | ✅ `sales_inquiry.yaml` | ✅ `sales_inquiry.json` | `sales.statement_list` | C6 |
| 6 | `ledger/customer` | TSobo32 | ✅ Sobo32 | 🟡 `sales_inquiry.yaml` 의 endpoints 에 `/inventory/ledger?scope=customer` 명시 필요 | 🟡 신규 케이스 `TC-INQ-LEDGER-CUST-001~003` | `inventory.ledger?scope=customer` | §2.3 patch |
| 7 | `ledger/customer-integrated` | TSobo32_1 | ✅ Sobo32_1 | 🟡 `sales_inquiry.yaml` 에 통합 집계 변형 추가 | 🟡 신규 케이스 `TC-INQ-LEDGER-CUST-INT-001` | `transactions.statement_list_grouped` | §2.3 patch — 클라이언트 집계 1차 |
| 8 | `ledger/book` | TSobo31 | ✅ Sobo31 | ✅ `sales_inquiry.yaml` (SQL-INQ-5/6) | ✅ `sales_inquiry.json` 의 `TC-INQ-LEDGER-BOOK-*` | `inventory.ledger?scope=book` | C6 |
| 9 | `ledger/book-integrated` | TSobo31_1(가상) | 🟡 신규 screen_card 작성 필요 | 🟡 `sales_inquiry.yaml` 통합 집계 추가 | 🟡 신규 케이스 `TC-INQ-LEDGER-BOOK-INT-001` | `inventory.ledger_grouped` | §2.3 patch — 클라이언트 집계 1차 |
| 10 | `stats/monthly` | TSobo60 | ✅ Sobo60 | ✅ `stats_reports.yaml` (sales_period) | 🟡 `stats_reports` 전용 test_pack 부재 → §2.4 신설 | `stats.sales_period` | C13/C14 |
| 11 | `stats/customer` | TSobo62 | ✅ Sobo62 | ✅ `sales_inquiry.yaml` (SQL-INQ-9 customer-sales) | ✅ `sales_inquiry.json` 의 `TC-INQ-CUST-*` | `reports.customer_sales` | C6 — stats 메뉴는 동일 라우트 재사용 |
| 12 | `stats/book` | TSobo61 | ✅ Sobo61 | ✅ `sales_inquiry.yaml` (SQL-INQ-7/8 book-sales) | ✅ `sales_inquiry.json` 의 `TC-INQ-BOOK-*` | `reports.book_sales` | C6 — stats 메뉴는 동일 라우트 재사용 |

---

## 2. Patch 작업 항목 (gap 채우기)

### 2.1 inventory/status — `inventory.ledger` 동등성 노트 (신규 contract 불필요)

본 화면은 백엔드 라우트 `/api/v1/inventory/ledger` (sales_inquiry.yaml SQL-INQ-5/6) 를 그대로 호출.
sales_inquiry.yaml 의 `equivalence:` 섹션에 다음 항목 추가가 필요(차후 contract PR):

```yaml
equivalence:
  data:
    additional_threshold: |
      Sobo44 재고현황 호출 시 (scope='B', bcode='%') 응답 row 가
      Sobo31 도서별 수불원장과 1:1 일치 (단순 SELECT alias 차이만 허용).
```

### 2.2 settlement/outstanding & payment-slip — settlement_billing.yaml 보강

- `settlement_billing.yaml` 의 `endpoints` 에 `/api/v1/settlement/outstanding` 와 `/api/v1/settlement/cash-list` 가 모두 정의되어 있는지 확인.
- 미정의 시 후속 PR 에서 SQL-BILL-N (Sobo71 매입현황 SELECT) 추가.

### 2.3 ledger/customer / ledger/book / 통합 뷰 — sales_inquiry.yaml endpoints 보강

`sales_inquiry.yaml` 의 endpoints 섹션에 다음을 추가(후속 contract PR):

```yaml
- method: GET
  path: /api/v1/inventory/ledger
  description: "도서·거래처 단위 수불원장 (Sobo31/Sobo32 동등 + Sobo44 재고스냅샷 흡수)."
  request:
    query:
      scope: "string ('book'|'customer', default 'book')"
      # ... 기존 ledger query 유지
```

> 통합 뷰(`*_integrated/page.tsx`) 는 1차 클라이언트 집계로 흡수 — 백엔드 신규 SQL 추가 불필요.
> Phase2 에서 서버측 GROUP BY 로 이전.

### 2.4 stats_reports.yaml — 전용 test_pack 신설

| 케이스 | scope | 검증 |
|---|---|---|
| TC-STATS-MONTHLY-001 | hcode='%', period=12개월 | 월별 합계 12행, 합계행 1행 |
| TC-STATS-MONTHLY-002 | hcode='C001', period=3개월 | 거래처 단일 필터 |
| TC-STATS-MONTHLY-003 | 빈 데이터 기간 | 200 + rows=[] |
| TC-STATS-MONTHLY-004 | 4대 DB probe (data axis) | mysql3/5/8/maria 모두 동일 합계 |

→ `migration/test-cases/stats_reports.json` 신규 파일.

---

## 3. 회귀 러너 그룹 (regression_phase1.py 입력)

`test/regression_phase1.py` 가 본 매트릭스의 **회귀 러너 그룹** 컬럼을 읽어
4대 DB(mysql3/5/8/maria) 에 차례로 호출하고 5축 결과를 리포트한다.

| 그룹 ID | 호출 라우트 | contract |
|---|---|---|
| `outbound.list_orders` | `GET /api/v1/outbound/orders` | outbound_order |
| `inventory.ledger` | `GET /api/v1/inventory/ledger` | sales_inquiry |
| `settlement.outstanding` | `GET /api/v1/settlement/outstanding` | settlement_billing |
| `settlement.cash_list` | `GET /api/v1/settlement/cash-list` | settlement_billing |
| `sales.statement_list` | `GET /api/v1/transactions/sales-statement` | sales_inquiry |
| `transactions.statement_list_grouped` | `GET /api/v1/transactions/sales-statement` (client-aggregate) | sales_inquiry |
| `inventory.ledger_grouped` | `GET /api/v1/inventory/ledger` (client-aggregate) | sales_inquiry |
| `stats.sales_period` | `GET /api/v1/stats/sales-period` | stats_reports |
| `reports.book_sales` | `GET /api/v1/reports/book-sales` | sales_inquiry |
| `reports.customer_sales` | `GET /api/v1/reports/customer-sales` | sales_inquiry |

---

## 4. 승격 체크리스트 (PR 단위)

각 화면 PR 본문에 다음 5축 결과를 표로 첨부:

```
| 축 | 결과 | 증빙 링크 |
|---|---|---|
| functional | PASS | test/regression_phase1.py::test_<group>__functional |
| data       | PASS | reports/regression-<date>.json#<group>.data |
| ui         | PASS | analysis/screen_cards/<Form>.md §UI checklist |
| audit      | N/A (read-only) | - |
| performance| PASS (P95=<ms>) | reports/regression-<date>.json#<group>.timing |
```

5축 모두 PASS 시 `frontend/src/lib/form-registry.ts` 에서 `phase: "phase2" → "phase1"` 1-line patch + 본 매트릭스의 해당 행을 ✅ 로 갱신.

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 최초 draft. 12개 매트릭스 + gap patch 4건 + 회귀 러너 그룹 10개 정의. |
