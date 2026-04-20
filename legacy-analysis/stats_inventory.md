# 통계/리포트 인벤토리 (Sobo50~55, C13 진입 선행)

_생성: 2026-04-20 — 확장 라인 v0.2 — C13 통계 진입 게이트 자료_

> 본 인벤토리는 C13 통계 확장 진입 전 **레거시 통계 폼(Sobo50~55)** 의 SQL 패턴/집계 호출 지점을 분류하고, 모던 신규 endpoint 가 **신규 SQL 0건 정책(DEC-040)** 을 충족할 수 있는지를 검증하는 단일 정본이다.

## 0. 목적
- (a) Sobo50~55 의 레거시 SQL 5종 패턴 매핑 (재사용 가능 여부 확정)
- (b) 신규 4 endpoint 가 어떤 기존 service 함수를 재해석할 수 있는지 1:1 매핑
- (c) 누락 SQL 발견 시 DEC 신규 등록 후 진입 (지금은 0건 가정)

## 1. 레거시 폼 인벤토리

| 폼 | 명칭 | Phase 1 포팅 여부 | 주요 SQL 패턴 | 모던 등가 |
|---|---|---|---|---|
| Sobo50 | (예약/미사용) | ❌ | (없음) | (없음) |
| Sobo51 | KPI 리포트 (Sobo51.pas L?) | ❌ (Phase 1 미포팅) | `SELECT ... FROM S1_Ssub WHERE Gdate BETWEEN ... GROUP BY YYYYMM` | `reports_service.get_book_sales` 의 GROUP BY 재해석 |
| Sobo52 | KPI 보강 (Sobo52.pas L?) | ❌ | `SELECT SUM(Gssum) FROM S1_Ssub WHERE Hcode=...` | `outbound_service.list_outbound_orders` SUM 재구성 |
| Sobo53 | 배송 리포트 | ❌ | `SELECT ... FROM S2_Stra WHERE ...` | `transactions_service` SELECT 재해석 |
| Sobo54 | 일별 입고 (이미 C3 phase2 활용) | ✅ (C3 phase2) | `SELECT ... FROM S1_Ssub WHERE Gdate=... AND Ocode='I'` | 이미 `inbound_service.list_daily_receipts` 로 흡수 |
| Sobo55 | 반품 분석 (Sobo55.pas L?) | ❌ | `SELECT ... FROM R1_Rsub WHERE ...` | `returns_service` SELECT 재해석 |

> Phase 1 미포팅 폼(Sobo51/52/53/55) 은 **소스 인벤토리만 진행**, 본 사이클의 모던 endpoint 는 4종 신규(STAT-1~4) 정의를 따른다 (계약 `migration/contracts/stats_reports.yaml`).

## 2. 신규 4 endpoint vs 기존 SELECT 재사용 매핑

| 신규 endpoint | 신규 화면 | 기존 SELECT 재사용 | 신규 SQL? | 비고 |
|---|---|---|---|---|
| `GET /api/v1/stats/sales-period` | 기간별 매출 분석 | `reports_service.get_book_sales` (Subu61.pas SQL-INQ-7/8 재해석) + 응답 후처리 (groupBy daily/weekly/monthly) | **0건** | C6 자산 100% 재사용 (DEC-040 정합) |
| `GET /api/v1/stats/customer-analysis` | 거래처별 판매 분석 | `reports_service.get_customer_sales` (Subu62.pas SQL-INQ-9 재해석) + Hcode 필터 | **0건** | C6 자산 100% 재사용 |
| `GET /api/v1/stats/book-turnover` | 도서 회전율 | `reports_service.get_book_sales` 결과를 (입고-출고) ratio 로 재계산 | **0건** | 응답 후처리 (서비스 layer 산술만) |
| `GET /api/v1/stats/quarterly-summary` | 분기·반기·연간 손익 | `settlement_service.list_billing_period` (월합계 Sobo47) + `cash_service.list_cash_status` (월별 입금) 합산 | **0건** | C5 자산 100% 재사용 (DEC-031 마감 가드 정합) |

**결론**: 4 신규 endpoint 모두 **신규 SQL 0건** 으로 구현 가능. 기존 service SELECT 호출 + 응답 후처리(집계/포맷팅) 로 충분.

## 3. C5 마감 정책 정합 (DEC-031 연동)

C13 통계 endpoint 가 받는 `dateFrom/dateTo/year/quarter` 의 기간이 마감된 월(YYYYMM) 을 포함할 수 있으므로 다음 정책을 강제한다:

- (a) **마감된 월 데이터 = 변경 불가**: 통계는 SELECT only 이므로 마감 가드 영향 없음 (R/O).
- (b) **기간 경계 검증**: `dateFrom > dateTo` 또는 분기 외 값(quarter ∉ [1,4]) 은 422 `STAT_INVALID_RANGE` 반환.
- (c) **마감되지 않은 미래 기간**: 응답 `metadata.partial=true` 플래그로 마감 미완 표시 (사용자 가시성).
- (d) **C5 의 `assert_period_open`** 는 통계 endpoint 가 **호출하지 않음** (R/O 이므로 불필요). 단, 검증 케이스(`test_c13_stats_phase1.py::test_period_boundary_partial_marker`) 로 마감 미완 응답 정합성을 회귀 가드.

## 4. 신규 SQL 0건 정적 가드 명령

C13 진입 후 axis_data 검증 시:

```bash
# stats_service.py / stats_router 에 신규 INSERT/UPDATE/DELETE/CREATE 0 건
rg -n "(INSERT\s+INTO|UPDATE\s+\w+|DELETE\s+FROM|CREATE\s+TABLE)" \
   도서물류관리프로그램/backend/app/services/stats_service.py \
   도서물류관리프로그램/backend/app/routers/stats.py \
   | grep -v -E "^\s*#" | wc -l
# 기대값: 0
```

본 가드는 `analysis/regression/c13_phase1.md` §axis_data 에 명시.

## 5. 변경 이력

- 2026-04-20 — 초판 (C13 진입 게이트 — Sobo50~55 인벤토리 + 4 endpoint 재사용 매핑 + 신규 SQL 0건 가드 명령).
