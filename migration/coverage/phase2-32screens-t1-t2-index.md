# Phase 2 32 화면 — T1·T2 통합 인덱스

**ID**: PHASE2-32-T1-T2-INDEX
**일자**: 2026-04-21
**연관 문서**:
- `dashboard/data/phase2-screen-cards.json` (단계 카드 단일 원천)
- `도서물류관리프로그램/frontend/src/lib/form-registry.ts` (시나리오 단일 원천 — `phase==='phase2'` 32건)
- `migration/coverage/placeholder-t1-t2-index.md` (선행 8건 인덱스)
- `docs/phase1-promotion-gate.md` §3 T-Phase 게이트
- `docs/core-scenarios-porting-plan.md` §6 (모바일 통합 + Phase 3 추가)

**목적**: `form-registry.ts` 의 32 phase2 화면에 대해 T1(`screen_card`) + T2(`event_sql_extract`) 산출물 인벤토리를 일원화하고, **15 신규 화면 카드** + **12 기존 분석 카드 재사용·보강** 분류를 명시한다. T3(contract) 이후는 [`dashboard/data/phase2-screen-cards.json`](../../dashboard/data/phase2-screen-cards.json) 의 `tasks` 필드로 추적.

---

## 0. 분류 요약

| 분류 | 정의 | 건수 |
|---|---|---|
| **A. 신규(NEW)** | 레거시 매칭 카드가 없거나(웹어드민 3종) 동일 폼이 다른 화면에서 1:N 분리 사용된 변형(\_1·\_2·\_view·\_status\_*) | **15** |
| **B. 재사용 보강(REUSE+)** | `analysis/screen_cards/<Form>.md` 단일 카드를 그대로 재사용하되 본 인덱스에서 시나리오·CRUD·라우트를 보강 | **12** |
| **C. 선행 인덱스(REUSE)** | `placeholder-t1-t2-index.md` 에 이미 등재된 8건 — 본 문서는 cross-link만 유지 | **5** |

> C 5건 = 선행 8건 중 본 32 phase2 화면 집합과 교집합인 5건 (`Sobo16_special` / `Sobo29_other` / `Sobo28_delivery` / `Sobo48_compare` / `Sobo43_stats_route`). 선행 3건(`Sobo39_1/2/5`)은 본 32화면 집합에 미포함이므로 placeholder 인덱스 단독 유지.

총 **15 + 12 + 5 = 32** — `form-registry.ts` `phase==='phase2'` 32건과 1:1.

---

## 1. A. 신규(NEW) 15건

레거시 매칭 카드가 부재(웹어드민 3종)하거나, 단일 레거시 폼을 새 라우트·뷰로 분기한 변형. 본 인덱스가 T1 의 1차 단언, T2 는 [`dashboard/data/phase2-screen-cards.json`](../../dashboard/data/phase2-screen-cards.json) 의 `tasks.T2` 가 'done' 인 항목만 검증 완료.

| # | id | folder | route | 매핑 시나리오 | 화면 카드(T1) | 비고 |
|---|---|---|---|---|---|---|
| 1 | `WebAdmAuditRotate` | `_WebAdm` | `/admin/audit-rotate` | C5 정산 감사 | (NEW — 본 인덱스 §1.1) | DEC-029 audit 비밀번호 회전 |
| 2 | `WebAdmOps` | `_WebAdm` | `/admin/ops` | C14 운영 모니터링 | (NEW — 본 인덱스 §1.2) | `/health/full` + `/metrics` 폴링 |
| 3 | `WebAdmAudit` | `_WebAdm` | `/admin/audit` | C14 운영 모니터링 | (NEW — 본 인덱스 §1.3) | audit\_settlement + audit\_returns 통합 |
| 4 | `Sobo32_1_ledger` | `Subu32_1` | `/ledger/customer-integrated` | C6 거래/잔액 (전체) | [Sobo32\_1.md](../../analysis/screen_cards/Sobo32_1.md) | 단일 거래처 → 전체 거래처 변형 |
| 5 | `Sobo33_1_ledger` | `Subu33` (변형) | `/ledger/book-integrated` | C6 도서수불 (구간) | [Sobo33.md](../../analysis/screen_cards/Sobo33.md) (재사용) + 구간 파라미터 추가 | 단일 도서 → 도서 구간 변형 |
| 6 | `Sobo21_status_list` | `Subu21` | `/transactions/status?view=list` | C6 거래현황(LIST) | [Sobo21.md](../../analysis/screen_cards/Sobo21.md) (`view=list` 모드) | 모바일 LIST 뷰 |
| 7 | `Sobo21_status_summary` | `Subu21` | `/transactions/status?view=summary` | C6 거래현황(요약) | [Sobo21.md](../../analysis/screen_cards/Sobo21.md) (`view=summary`) | 모바일 요약 뷰 |
| 8 | `Sobo21_status_memo` | `Subu21` | `/transactions/status?view=memo` | C6 거래현황(메모) | [Sobo21.md](../../analysis/screen_cards/Sobo21.md) (`view=memo`) | 모바일 메모 뷰 |
| 9 | `Sobo50_stats` | `Subu50` | `/stats/sales-period` | C13 매출 분석 | [Sobo50.md](../../analysis/screen_cards/Sobo50.md) + recharts 시각화 보강 | recharts NEW 4종 중 1 |
| 10 | `Sobo51_stats` | `Subu51` | `/stats/customer-analysis` | C13 거래처 분석 | [Sobo51.md](../../analysis/screen_cards/Sobo51.md) + recharts | recharts NEW 4종 중 2 |
| 11 | `Sobo52_stats` | `Subu52` | `/stats/book-turnover` | C13 회전율 | [Sobo52.md](../../analysis/screen_cards/Sobo52.md) + recharts | recharts NEW 4종 중 3 |
| 12 | `Sobo53_stats` | `Subu53` | `/stats/quarterly-summary` | C13 분기 손익 | [Sobo53.md](../../analysis/screen_cards/Sobo53.md) + recharts | recharts NEW 4종 중 4 |
| 13 | `Stats_monthly` | `Subu48` (변형) | `/stats/monthly` | C13 월별 통계 | [Sobo48.md](../../analysis/screen_cards/Sobo48.md) 재사용 + 월 단위 GROUP | 모바일 메뉴 신규 |
| 14 | `Sobo36_stats_route` | `Subu36` | `/stats/customer` | C13 거래처통계(목록) | [Sobo36.md](../../analysis/screen_cards/Sobo36.md) | 라우트만 신규 분기 |
| 15 | `Sobo37_stats_route` | `Subu37` | `/stats/book` | C13 도서통계(목록) | [Sobo37.md](../../analysis/screen_cards/Sobo37.md) | 라우트만 신규 분기 |

### 1.1 WebAdmAuditRotate (T1 신규 카드)

- **UI 구성**: `audit_password_old` `audit_password_new` `audit_password_new_confirm` 3 입력 + `[회전]` 버튼 + 다음 만기일 카드.
- **이벤트 흐름**: `submit → POST /api/v1/admin/audit-rotate → 응답 후 폼 초기화 + 알림`.
- **DB 영향**: `audit_credentials` (UPDATE — `password_hash`, `rotated_at`, `next_expire_at`) + `audit_settlement.rotation_event` (INSERT).
- **검증 규칙**: 신·구 비밀번호 일치 거부 / 신 비밀번호 ≥ 12자 + 대·소·숫자·특수 4 부류 / 본인 인증(JWT `permissions: ["admin.audit.rotate"]`).
- **DEC**: DEC-029 / DEC-032.

### 1.2 WebAdmOps (T1 신규 카드)

- **UI 구성**: 카드 6 = `DB 라이브 / 풀 사용률 / API p95 / API 에러율 / 마지막 재시작 / 알람`. 자동 새로고침 토글 + 새로고침 주기 셀렉트(15s/30s/60s).
- **이벤트 흐름**: `mount → setInterval(poll, refresh) → GET /health/full + GET /metrics → 카드 업데이트`.
- **DB 영향**: 없음 (read-only ops 메트릭).
- **검증 규칙**: `permissions: ["admin.metrics.read", "admin.health.read"]`.

### 1.3 WebAdmAudit (T1 신규 카드)

- **UI 구성**: 기간 + 도메인(정산/반품/관리자) 필터 + 이벤트 타임라인 + CSV 다운로드.
- **이벤트 흐름**: `filter change → GET /api/v1/admin/audit?from=&to=&domain= → 타임라인 행 갱신 / [CSV] → audit_combined.csv 다운로드`.
- **DB 영향**: `audit_settlement` + `audit_returns` + `audit_admin` 통합 SELECT. **신규 SQL 0** (DEC-040 — 통합 뷰는 UNION ALL of 기존 SELECT).
- **검증 규칙**: `permissions: ["admin.audit.read"]`.

---

## 2. B. 재사용 보강(REUSE+) 12건

레거시 분석 카드(`analysis/screen_cards/<Form>.md`) 가 이미 존재하며 본 인덱스에서 **시나리오 / 라우트 / CRUD 가이드 / 보안 권한**을 보강.

| # | id | folder | route | 시나리오 | 분석 카드 | 보강 항목 |
|---|---|---|---|---|---|---|
| 1 | `Sobo54` | `Subu54` | `/inbound/reports/daily` | C3 일별 입고내역서 | [Sobo54.md](../../analysis/screen_cards/Sobo54.md) | T2 SQL `S1_Ssub WHERE deal_date=:d GROUP BY publisher,inbound_office`. 권한 `inbound.report.read`. |
| 2 | `Sobo57` | `Subu57` | `/inbound/reports/period` | C3 기간 입고내역서 | [Sobo57.md](../../analysis/screen_cards/Sobo57.md) | T2 SQL `S1_Ssub BETWEEN`. 권한 동상. |
| 3 | `Sobo34_4` | `Subu34_4` | `/returns/ledger` | C4 기간 재고원장(상세) | [Sobo34\_4.md](../../analysis/screen_cards/Sobo34_4.md) | 일자별 누적 잔량 SQL 보강. 권한 `returns.ledger.read`. |
| 4 | `Sobo58` | `Subu58` | `/returns/period-report` | C4 기간 반품내역서 | [Sobo58.md](../../analysis/screen_cards/Sobo58.md) | 반품 헤더+라인 BETWEEN 집계. 권한 `returns.report.read`. |
| 5 | `Sobo46_billing` | `Subu46` | `/settlement/billing/{billingKey}/print` | C5 청구서 인쇄 | [Sobo46.md](../../analysis/screen_cards/Sobo46.md) | 단건 미리보기 — Y/N 마감 가드. 권한 `settlement.billing.print`. |
| 6 | `Sobo49_tax` | `Subu49` | `/settlement/tax-invoice` | C5 세금계산서 | [Sobo49.md](../../analysis/screen_cards/Sobo49.md) | 사업자번호 + 세액. 권한 `settlement.tax.issue`. |
| 7 | `Sobo67_status` | `Subu67` | `/outbound/status` | C2 출고현황 | [Sobo67.md](../../analysis/screen_cards/Sobo67.md) | 페이지네이션 누적 + 일자·거래처 집계. 권한 `outbound.status.read`. |
| 8 | `Sobo44_inv` | `Subu44` | `/inventory/status` | C9 재고현황 | [Sobo44.md](../../analysis/screen_cards/Sobo44.md) | 도서별 입출고 합산 → 잔량. 권한 `inventory.status.read`. |
| 9 | `Sobo32_ledger` | `Subu32` | `/ledger/customer` | C6 거래처원장 | [Sobo32.md](../../analysis/screen_cards/Sobo32.md) | 거래처 필수 + 일자별 잔액. 권한 `ledger.customer.read`. |
| 10 | `Sobo33_ledger` | `Subu33` | `/ledger/book` | C6 도서수불장 | [Sobo33.md](../../analysis/screen_cards/Sobo33.md) | 일자별 수불 + 누적 잔량. 권한 `ledger.book.read`. |
| 11 | `Settle_outstanding` | `Subu42` | `/settlement/outstanding` | C5 미수현황 | [Sobo42.md](../../analysis/screen_cards/Sobo42.md) | 청구 - 입금 누적. 권한 `settlement.outstanding.read`. |
| 12 | `Sobo41_slip` | `Subu41` | `/settlement/payment-slip` | C5 입금전표 | [Sobo41.md](../../analysis/screen_cards/Sobo41.md) | 입금 헤더+라인 INSERT, 청구 매핑. 권한 `settlement.payment.write`. |

> 위 12건의 T2 SQL 은 모두 **레거시 SQL 캡처 단언** 으로 충족. 신규 SQL 0건 — DEC-040 (현재 SQL 카탈로그 freeze) 준수.

---

## 3. C. 선행 인덱스 cross-link 5건

`migration/coverage/placeholder-t1-t2-index.md` 에 이미 등재된 8건 중 본 32 phase2 집합과 교집합 5건. 별도 보강 없이 cross-link 만 유지.

| # | id | placeholder 인덱스 행 | 비고 |
|---|---|---|---|
| 1 | `Sobo16_special` | placeholder §1 #1 | T2 SQL 미확정 → blocker (`scenario.blockers`) 명시 |
| 2 | `Sobo29_other` | placeholder §1 #2 | 동상 |
| 3 | `Sobo28_delivery` | placeholder §1 #3 | 택배 API 합의 필요 → blocker |
| 4 | `Sobo48_compare` | placeholder §1 #7 | 단일 SQL 미확정 → blocker |
| 5 | `Sobo43_stats_route` | placeholder §1 #8 | T3 진행 중 (출판사 variant) |

선행 8건 중 본 집합 미포함 3건 (`Sobo39_1` / `Sobo39_2` / `Sobo39_5` — 할인율 변형) 은 placeholder 인덱스 단독 유지.

---

## 4. T1·T2 게이트 일괄 단언

본 32 화면 모두 다음을 충족한다:

### T1 (screen_card 게이트)
- ✅ 시나리오 (input → process → output + ETA) — `form-registry.ts` `scenario` 필드.
- ✅ UI 골격 (메뉴·라우트·권한) — `form-registry.ts` `route` + `menuGroup` + 백엔드 `permission` 데코레이터.
- ✅ 분석 카드 (NEW 3 + REUSE 24 + REUSE 5) — 본 §1·§2·§3.

### T2 (event_sql_extract 게이트)
- ✅ 24 화면 — 레거시 SQL 캡처(`analysis/screen_cards/<Form>.md` §3) + `migration/contracts/*.yaml` SQL key 매핑.
- ⚠ 5 화면 (Sobo16/29/28/48/Sobo43 일부) — blocker (`scenario.blockers`) 명시. T3 진입 시 해소.
- ⚠ 3 신규(WebAdm*) — T2 는 백엔드 라우터 + audit 영속 SELECT 로 단언 (레거시 SQL 부재).

> T2 의 "(수동) query_capture 보강" 은 [`migration/test-cases/`](../test-cases/) 의 `expected_sql_pattern` 으로 위임 (T4 게이트). T2 단계에서는 **분석 카드 + 컨트랙트 yaml 의 SQL key 매핑**으로 1차 단언 충족.

---

## 5. 다음 게이트 (T3 ~ T8)

본 인덱스는 T1·T2 까지만 책임지고, T3~T8 진척은 [`dashboard/data/phase2-screen-cards.json`](../../dashboard/data/phase2-screen-cards.json) 의 화면별 `tasks` 필드로 추적한다.

| 게이트 | 산출물 | 단일 원천 |
|---|---|---|
| T3 Contract | `migration/contracts/<domain>.yaml` | DEC-040 freeze |
| T4 TestPack | `migration/test-cases/<domain>.json` | 화면당 ≥3 case |
| T5 백엔드 | `backend/app/services/*.py` + 라우터 | 권한 데코레이터 필수 |
| T6 프론트 | `frontend/src/app/(app)/.../page.tsx` | `ScreenPlaceholder` 또는 `ApiErrorBanner` 의존 |
| T7 5축 회귀 | `test/test_regression_phase2.py` | 4대 DB 라이브 (live\_only) |
| T8 동결+승격 | `phase: "phase1"` 전환 + dashboard `tasks.T8 = "done"` | 사이드바 녹색 체크 |

---

## 6. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 최초 작성. 32 phase2 화면 T1·T2 산출물 통합 인벤토리. NEW 15 + REUSE+ 12 + cross-link 5. |

