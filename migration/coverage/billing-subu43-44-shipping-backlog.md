# 진짜 발송비 도메인 — Subu43/44 백로그 분리 (P2)

**ID**: BILLING-SUBU43-44-SHIPPING-BACKLOG
**일자**: 2026-04-21
**우선순위**: P2 (C5 정산 코어 안정 이후)
**연관 결정**: DEC-049 (billing 메뉴 IA 복원), DEC-040 (신규 SQL 0), DEC-031/032 (C5 정산 마감 가드), DEC-046 (단일 원천)
**상위 추적**: [`migration/coverage/billing-deposit-menu-legacy-to-web-map.md`](./billing-deposit-menu-legacy-to-web-map.md) §3·§4, [`dashboard/data/billing-c5-menu-porting.json`](../../dashboard/data/billing-c5-menu-porting.json) `Bill_gap_shipping_ledger` / `Bill_gap_shipping_status`

---

## 0. 분리 이유 (혼동 방지)

웹 [`form-registry.ts`](../../도서물류관리프로그램/frontend/src/lib/form-registry.ts) 에 **레거시와 동일 폴더 명** 을 **다른 도메인** 에 이미 사용 중.

| 웹 ID | 웹 folder | 웹 캡션 | 웹 라우트 | 레거시 동명 | 도메인 |
|---|---|---|---|---|---|
| `Sobo43_stats_route` | `Subu43` | 출판사통계 | `/stats/publisher` | `Subu43.pas` | **발송비내역** (전혀 다름) |
| `Sobo44_inv` | `Subu44` | 재고현황 | `/inventory/status` | `Subu44.pas` | **발송비현황** (전혀 다름) |

→ **본 백로그를 청구·입금 별칭(DEC-049 별칭 8 행) 과 같은 PR/스프린트에 포함하지 않는다.** 이름·라우트가 충돌하면 사용자·AI 모두 잘못된 화면을 가리키게 되어 회귀가 어렵다.

---

## 1. 신규 식별자 (확정)

| 도메인 | 신규 ID | 신규 라우트 | 신규 계약 파일(예정) | T1 카드(예정) |
|---|---|---|---|---|
| 발송비내역 (CRUD) | `Sobo43_shipping_ledger` | `/settlement/shipping-ledger` | `migration/contracts/shipping_ledger.yaml` | `analysis/screen_cards/Sobo43_shipping.md` |
| 발송비현황 (집계) | `Sobo44_shipping_status` | `/settlement/shipping-status` | (`shipping_ledger.yaml` 의 `status` 섹션 재사용 권장) | `analysis/screen_cards/Sobo44_shipping.md` |

신규 ID 는 **반드시** `_shipping_ledger` / `_shipping_status` 접미를 유지하여 접두 `Sobo43_` 와의 통계 라우트(혼동 케이스) 를 정적으로 grep 분리할 수 있게 한다.

---

## 2. 단계별 백로그 (T1 ~ T8)

| 단계 | 산출물 | 의존 | 비고 |
|---|---|---|---|
| **T1** | `analysis/screen_cards/Sobo43_shipping.md`, `Sobo44_shipping.md` (UI/이벤트/검증/DEC) | 레거시 [`Subu43.pas`](../../legacy_delphi_source/legacy_source/Source/Subu43.pas) [`Subu44.pas`](../../legacy_delphi_source/legacy_source/Source/Subu44.pas) 분석 | T3_Ssub.NAME1/NAME2/GSSUM 등 도메인 컬럼 정리 |
| **T2** | `analysis/screen_cards/Sobo43_shipping.md::events` + SQL 추출 | DEC-040 정합 — **신규 SQL 0** 원칙 검토 (기존 헬퍼 재사용 가능 여부) | 헬퍼 부족 시 **T2 에서 먼저 차단 신호** |
| **T3** | `migration/contracts/shipping_ledger.yaml` v0.1.0 | T2 SQL 추출 + DEC-031 마감 가드 | `equivalence` 5축 정의 의무 |
| **T4** | `migration/test-cases/shipping_ledger.json` (≥ 5 케이스) | T3 contract | empty / single hcode / cross hcode / 마감일 가드 / 권한 거부 |
| **T5** | `app/services/shipping_ledger_service.py` + `app/api/v1/settlement/shipping_ledger.py` | T3+T4 + 멀티 DB 헬퍼 (`apply_limit_offset_syntax`, `t3_ssub_adapt.py` 신설 가능성) | 라우트 4건: list / create / update / delete |
| **T6** | Next.js 페이지 `/settlement/shipping-ledger`, `/settlement/shipping-status` | T5 + `form-registry.ts` 신규 ID 2건 등록 (`menuGroup: "billing"`) | 별칭이 아닌 **정본** — `phase: "phase2"` 시작 |
| **T7** | `test/test_regression_phase2.py` 에 신규 그룹 추가 + 4대 DB 회귀 PASS | T5+T6 + DB 환경(DEC-047) | 5축 모두 PASS 시 phase1 승격 후보 |
| **T8** | `phase: "phase2" → "phase1"` PR + 카드 동결 | T7 4대 DB PASS + DEC-045 게이트 | DEC-049 (b) 단일 원천 갱신 |

---

## 3. 차단/주의 사항

1. **DEC-040 신규 SQL 0 정책 충돌**: 발송비 라인은 `T3_Ssub.NAME1/NAME2/GSSUM` 도메인을 사용. 기존 settlement 헬퍼 (`Sobo45_billing` 청구) 와 **컬럼 의미가 다름** (NAME1/NAME2 = 발송비 항목명, GSSUM = 발송비 합계). T2 단계에서 헬퍼 재사용 가능성 우선 검토 후, 불가하면 DEC-049 (e) 보강 결정 필요.
2. **멀티 DB 호환 (DEC-033)**: `T3_Ssub` 컬럼 변이는 `t3_ssub_adapt.py` (신규) 로 흡수. `if server_id` 분기 금지.
3. **마감 가드 (DEC-031)**: 발송비 라인의 INSERT/UPDATE/DELETE 도 `Y/N` 마감 플래그를 따른다. 청구 마감 가드 헬퍼 재사용.
4. **권한 (DEC-029/032)**: 쓰기 경로는 `permissions: ["settlement.write"]` 로 게이트 (audit_settlement 기록 의무).
5. **wrong_id 영구 가드**: 본 백로그 진행 중에도 `Sobo43_stats_route`/`Sobo44_inv` 의 캡션·라우트는 **변경 금지** — 두 도메인을 명확히 분리한 채 신규 ID 만 추가한다.

---

## 4. Definition of Done (백로그 → 정식 진입 전환)

본 백로그가 **정식 스프린트 항목** 으로 전환되려면 아래 4 조건을 모두 만족해야 한다.

- [ ] C5 정산 코어 (DEC-031/032/034/035/036) 4대 DB 회귀 PASS — 즉, `dashboard/data/billing-c5-menu-porting.json` alias 8 행이 T7 'done' 으로 진입.
- [ ] T2 SQL 추출 결과 + DEC-040 정합 검토서 (`analysis/research/shipping_ledger_sql_reuse_review.md`) 작성.
- [ ] 신규 SQL 가 필요하면 DEC-049 (e) 보강 결정 (PR + 사용자 합의).
- [ ] R&D/SME 가용성 확인 (Phase 3 트랙과 자원 경쟁 회피).

위 4 조건이 갖춰지기 전에는 본 백로그는 **`dashboard/data/billing-c5-menu-porting.json::screens` 에 `mappingType="gap" + priority="P2"`** 로만 노출 (현재 상태 유지).

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 1차 작성 — DEC-049 분리 결정 + wrong_id 2건 영구 가드 + 신규 ID/라우트 확정 + T1~T8 단계 + DoD 4 조건. |
