# 구현되지 못한 기능 인벤토리 (저장소 자동 산출)

생성: `2026-05-04T10:30:47.140004+00:00` (`debug/generate_incomplete_features_inventory.py`)

## 판정 기준 (합집합)

본 인벤토리는 계획서 「구현되지 못한 기능 목록」에 따라 **원천별 합집합** 을 기록한다. 단일 정의가 아니라 (A) UI placeholder (B) T-파이프라인 비완료 (C) form-registry preview/STUB (D) phase1 이지만 R/RU/STUB 인 부분 동등 (E) 백엔드 stub grep (F) crud-backlog §2.6 참조 를 모두 포함한다.

## 1. UI — `ScreenPlaceholder` 가 붙은 라우트

- `도서물류관리프로그램/frontend/src/app/(app)/billing/statements/page.tsx` → 라우트 추정 `/billing/statements`
- `도서물류관리프로그램/frontend/src/app/(app)/master/discount/[type]/page.tsx` → 라우트 추정 `/master/discount/[type]`
- `도서물류관리프로그램/frontend/src/app/(app)/shipping/returns-inventory/page.tsx` → 라우트 추정 `/shipping/returns-inventory`
- `도서물류관리프로그램/frontend/src/app/(app)/year-month-stats/page.tsx` → 라우트 추정 `/year-month-stats`

## 2. T1–T8 — `phase2-screen-cards.json` 에서 아직 done 아닌 task

> **드리프트 주의:** 카드의 레거시 ID·캡션과 해당 `route` 의 `page.tsx` 실구현 범위가 다를 수 있다. 판단은 API·화면 코드 우선.

- **Sobo48_compare** (장부대조) `/ledger/comparison` — {'T2': 'in_progress', 'T3': 'blocked', 'T4': 'pending', 'T5': 'pending', 'T6': 'in_progress', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['레거시 단일 SQL 미확정', '신규 SQL 0 정책(DEC-040)', '라우트 드리프트: /ledger/comparison 는 현재 Sobo48 본판(출판사 설정)이 임시 점유 중 — 장부대조 진입 시 별도 라우트 또는 view 모드 분리 필요 (analysis/audit/wave-b-placeholder-scoping.md §2)']
- **Sobo29_other** (기타명세서) `/transactions/other` — {'T2': 'in_progress', 'T3': 'blocked', 'T4': 'pending', 'T5': 'pending', 'T6': 'in_progress', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['레거시 폼 단순 출력기 — 인쇄 양식(T7) 미확정 (조회·메모 저장은 구현 완료, Sobo29.* data-legacy-id 부착 — analysis/audit/wave-b-placeholder-scoping.md §2)']

## 3. `form-registry` — preview 또는 STUB

- `MenuBillingStatements` (내역서관리) route `/billing/statements` — ['STUB', 'preview'] (line 1100)
  - notes: ACC-MENU-NAV-15 (T1·T2-DIST·T3-LITE·T3-FULL)
- `MenuShippingReturnsInventory` (반품재고관리(통합)) route `/shipping/returns-inventory` — ['STUB', 'preview'] (line 1081)
  - notes: ACC-MENU-NAV-12 (T1·T3_WAREHOUSE_LITE) — WH-WL 단독
- `MenuYearMonthStats` (년/월(통계)) route `/year-month-stats` — ['STUB', 'preview'] (line 1062)
  - notes: ACC-MENU-NAV-07 (T1·T2-PUB·T3) — 8 하위 화면 후속

## 4. `form-registry` — phase1 이지만 부분 동등 (R / RU / STUB)

> 레거시 화면은 풀 CRUD 였지만 모던 화면이 조회·부분쓰기에 머문 항목.

### R (21건)
- `Settle_outstanding` (미수현황) `/settlement/outstanding`
  - 조회 전용 — 미수 합계
- `Sobo17` (출판사·출고거래처(마스터)) `/master/publisher`
  - 1차 READ only — 신규/수정/삭제 후속 (page.tsx 주석)
- `Sobo32_1_ledger` (통합 거래처원장) `/ledger/customer-integrated`
  - 조회 전용 — DBGrid301 분해는 P3 (customer-ledger-implementation-plan §8)
- `Sobo32_ledger` (거래처원장) `/ledger/customer`
  - 조회 전용 — DBGrid301 분해는 P3 (customer-ledger-implementation-plan §8)
- `Sobo34_4` (기간별재고원장(상세)) `/returns/ledger`
  - 조회 전용 — 페이저 v1.2.0 (DEC-033 e/g 표준)
- `Sobo36_stats_route` (거래처통계(목록)) `/stats/customer`
  - 조회 전용 — statsApi.customerAnalysis → GET /api/v1/stats/customer-analysis (reports 재사용)
- `Sobo37_stats_route` (도서통계(목록)) `/stats/book`
  - 조회 전용 — reportsApi.bookSales → GET /api/v1/reports/book-sales (Sobo61 동등 경로)
- `Sobo38` (도서코드(마스터)) `/master/book-code`
  - READ only (단순 조회) — 수정 후속
- `Sobo39` (할인율(대표)) `/master/discount`
  - 1차 READ only — 수정 후속
- `Sobo41_slip` (입금전표) `/settlement/payment-slip`
  - 기존 입금 라인(settlementCashApi.list) 조회 + 전표 카드 인쇄(window.print) — 신규/수정 입금은 /settlement/cash
- `Sobo43_stats_route` (출판사통계) `/stats/publisher`
  - 조회 전용 — GET /api/v1/stats/publisher: book-sales 행을 출판사 축으로 재집계(stats_reports.yaml STAT-PUB, 신규 SQL 0건). 레거시 Subu43 전 지표·출력 1:1 복원은 비목표.
- `Sobo46_billing` (청구서 인쇄(미리보기)) ``
  - 인쇄 미리보기만 — 쓰기 없음 (DEC-035 외부 채널 후속)
- `Sobo46_billing_bill` (청구서출력) `/settlement/billing`
  - 인쇄 미리보기만 — 쓰기 없음 (DEC-035 후속)
- `Sobo50_stats` (기간별 매출 분석) `/stats/sales-period`
  - 차트 조회 전용
- `Sobo51_stats` (거래처별 판매 분석) `/stats/customer-analysis`
  - 차트 조회 전용
- `Sobo52_stats` (도서 회전율) `/stats/book-turnover`
  - 차트 조회 전용
- `Sobo53_stats` (분기/반기 손익) `/stats/quarterly-summary`
  - 차트 조회 전용
- `Sobo58` (기간별반품내역서) `/returns/period-report`
  - 조회 전용 — test_c4_returns_phase2 / test_returns_period_ledger_regression / DEC-028 data-legacy-id
- `Stats_monthly` (월별통계) `/stats/monthly`
  - 조회 전용 — statsApi.salesPeriod(groupBy=monthly) → GET /api/v1/stats/sales-period (DEC-040 재사용)
- `WebAdmAudit` (감사 통합 뷰) `/admin/audit`
  - 조회 전용 — C14 phase2 회귀 통과
- `WebAdmOps` (운영 모니터링) `/admin/ops`
  - 조회 전용 — C14 phase2 회귀 통과

### RU (9건)
- `Sobo11` (거래처관리(마스터)) `/master/customer`
  - 조회+수정만 — 신규(C)·삭제(D) 후속
- `Sobo14` (도서관리(마스터)) `/master/book`
  - 조회+수정만 — 신규(C)·삭제(D) 후속
- `Sobo16_special` (특별관리) `/master/special`
  - G6_Ggeo 목록 + Grat1/Gssum 부분 수정 — 신규/삭제·Gcode/Bcode 변경은 후속
- `Sobo28_delivery` (택배관리) `/shipping/courier`
  - 내부 S1_Ssub 라인 조회 + S1_Memo 조회/저장 완료 — 외부 택배사 API는 별도 후속
- `Sobo29_other` (기타명세서) `/transactions/other`
  - S1_Ssub 신간/기타 명세 조회 + S1_Memo 전체메모 저장
- `Sobo48_compare` (출판사관리(설정)) `/ledger/comparison`
  - G7_Ggeo 출판사 설정 조회 + Chek3/Scode 부분 저장
- `Sobo49_tax` (세금계산서 발행) `/settlement/tax-invoice`
  - DEC-035 외부 채널 발행 stub 배너 — 실제 발행은 후속
- `Sobo49_tax_bill` (세금계산서) `/settlement/tax-invoice`
  - DEC-035 외부 채널 발행 stub 배너 — 실제 발행은 후속
- `WebAdmAuditRotate` (감사 비밀번호 회전) `/admin/audit-rotate`
  - 회전(write) 동작 — C5 phase2 회귀 통과


## 5. 백엔드 stub grep (`app/routers/*.py`)

- `도서물류관리프로그램/backend/app/routers/_stub.py:10` — `503 + ``code=NOT_IMPLEMENTED`` 면 「준비 중」 으로 정확히 표시된다.`
- `도서물류관리프로그램/backend/app/routers/_stub.py:27` — `"""이름이 무엇이든 503 응답. 프론트는 NOT_IMPLEMENTED 로 인식."""`
- `도서물류관리프로그램/backend/app/routers/_stub.py:29` — `status_code=status.HTTP_503_SERVICE_UNAVAILABLE,`
- `도서물류관리프로그램/backend/app/routers/_stub.py:31` — `"code": "NOT_IMPLEMENTED",`
- `도서물류관리프로그램/backend/app/routers/returns.py:510` — `status_code=status.HTTP_501_NOT_IMPLEMENTED,`
- `도서물류관리프로그램/backend/app/routers/settlement.py:828` — `result = await tax_invoice_service.issue_external_stub(`

## 6. `docs/crud-backlog.md` §2.6 참조 (문서 불릿)

- `Sobo29_other` (기타명세서)
- `Sobo48_compare` (장부대조)
- `Sobo43_stats_route` (출판사통계)
- (할인율 변형) `/master/discount/[type]` 라우트는 메뉴 미노출 — 별도 등록 없음.

## 갱신·CI

```bash
python3 debug/generate_incomplete_features_inventory.py            # 갱신
python3 debug/generate_incomplete_features_inventory.py --check    # CI: 미갱신이면 exit 1
```

산출: `analysis/audit/incomplete-features-inventory.md` · `.json`

