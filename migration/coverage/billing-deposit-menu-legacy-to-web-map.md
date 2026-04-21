# 발송비/입금관리 메뉴 — 레거시 ↔ 웹 매핑 (BILLING IA 복원)

**ID**: BILLING-DEPOSIT-MENU-MAP
**일자**: 2026-04-21
**연관 문서**:
- 레거시 메뉴 정본: [`legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md`](../../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md) §「플로우: 발송비/입금관리」
- 화면 사양: [`legacy_delphi_source/legacy_source/docs/phase1-structure/12-screen-specification.md`](../../legacy_delphi_source/legacy_source/docs/phase1-structure/12-screen-specification.md)
- 웹 IA 단일 원천: [`도서물류관리프로그램/frontend/src/lib/form-registry.ts`](../../도서물류관리프로그램/frontend/src/lib/form-registry.ts)
- 시나리오 카드 인덱스: [`migration/coverage/phase2-32screens-t1-t2-index.md`](./phase2-32screens-t1-t2-index.md)
- C5 결정: DEC-031 / DEC-032 / DEC-034 / DEC-035 / DEC-036 / DEC-046

---

## 0. 목적

레거시 **「메인 메뉴 / 발송비/입금관리」** 트리에 등재된 14개 화면을 웹 `MENU_GROUPS` 의 `billing` 그룹과 1:1 매핑하고, 각 행의 매핑 유형(`alias` / `moved` / `gap` / `wrong_id`) 을 동결한다. 본 표는 [`dashboard/data/billing-c5-menu-porting.json`](../../dashboard/data/billing-c5-menu-porting.json) 의 `screens[]` 와 1:1 정합되며, [`form-registry.ts`](../../도서물류관리프로그램/frontend/src/lib/form-registry.ts) 의 `menuGroup: "billing"` 별칭 행과도 1:1 정합된다 (DEC-046 단일 원천 패턴).

---

## 1. 분류 정의

| 매핑 유형 | 정의 | 처리 |
|---|---|---|
| `alias` | 동일 기능이 이미 다른 `menuGroup` (대부분 `settlement`) 에 포팅되어 있음. `billing` 그룹에는 동일 `route` 를 가리키는 얇은 별칭 항목만 추가. | `form-registry.ts` 별칭 행 + 대시보드 `mappingType="alias"` |
| `moved` | 기능은 포팅되어 있으나 시나리오 분류상 다른 그룹(`statistics`/`returns`/`report`/`outbound`) 으로 이전 배치됨. `billing` 메뉴에 노출하지 않음 (중복 메뉴 방지). | 본 문서에만 기록, 대시보드 `mappingType="moved"` |
| `gap` | 레거시에 존재하나 웹 미구현. 별도 시나리오 카드 + 계약 + 라우트 신설 필요. | 백로그 등록 (단계 4 참조) |
| `wrong_id` | 웹 레지스트리에 동일 레거시 폴더(`Subu*`) 를 다른 기능으로 재사용한 항목 — 혼동 위험. | 본 문서 §3 에 경고 + (선택) ID/주석 정리 PR |

---

## 2. 발송비/입금관리 14행 매핑 표

레거시 메뉴 풀패스는 [`11-screen-business-flows.md`](../../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md) §「플로우: 발송비/입금관리」 행 순서를 따른다.

| # | 레거시 메뉴 풀패스 | 레거시 폼 / 유닛 | 웹 `FormMeta.id` | 웹 `route` | 현재 `menuGroup` | 매핑 유형 | C5 자산 / 비고 |
|---|---|---|---|---|---|---|---|
| 1 | / 메세지(팝업창) | `TSeok30` / `Seok03.pas` | — | — | — | `gap` (낮음) | 정보 모달 — Wave D 알림 통합으로 이관 후보 |
| 2 | / 명세서 발송건수 | `TSobo24_9` / `Subu24_9.pas` | — | — | — | `gap` (중) | 거래명세서 발행 카운트 — `transactions` 또는 `report` 후속 |
| 3 | / 반 품 수 거 / 반품수거내역 | `TSobo36` / `Subu36.pas` | `Sobo36_stats_route` | `/stats/customer` | `statistics` | `moved` | 웹은 거래처통계로 분기 (`phase2-32screens-t1-t2-index.md` §1.14) |
| 4 | / 반 품 수 거 / 반품수거현황 | `TSobo37` / `Subu37.pas` | `Sobo37_stats_route` | `/stats/book` | `statistics` | `moved` | 웹은 도서통계로 분기 (동 §1.15) |
| 5 | / **발송비관리** / 발송비내역 | `TSobo43` / `Subu43.pas` | — | — | — | `gap` ⚠ **P2** | 진짜 발송비 도메인 신설 필요. `Sobo43_stats_route` 와 혼동 금지 (§3) |
| 6 | / **발송비관리** / 발송비현황 | `TSobo44` / `Subu44.pas` | — | — | — | `gap` ⚠ **P2** | `Sobo44_inv` (재고현황) 과 혼동 금지 (§3) |
| 7 | / 세금계산서 | `TSobo49` / `Subu49.pas` | `Sobo49_tax` | `/settlement/tax-invoice` | `settlement` | `alias` | C5 Phase 2 (DEC-034) |
| 8 | / 운임관리-택배 | `TSobo38_1` / `Subu38_1.pas` | — | — | — | `gap` (중) | 택배 운임 단가 마스터 — C7 인쇄와 분리 트랙 |
| 9 | / **입금관리** / 입금내역 | `TSobo41` / `Subu41.pas` | `Sobo41_cash` | `/settlement/cash` | `settlement` | `alias` | C5 Phase 1 (DEC-031) |
| 10 | / **입금관리** / 입금현황(1) | `TSobo42` / `Subu42.pas` | `Sobo42_cash` | `/settlement/cash-status` (variant=hcode) | `settlement` | `alias` | layout: [Sobo42_cash.md](../../analysis/layout_mappings/Sobo42_cash.md) |
| 11 | / **입금관리** / 입금현황(2) | `TSobo42_1` / `Subu42_1.pas` | `Sobo42_cash` (variant) | `/settlement/cash-status?variant=sdate` | `settlement` | `alias` | 단일 화면 + variant 쿼리 (DEC-019) |
| 12 | / 청구금액(년월) | `TSobo47` / `Subu47.pas` | `Sobo47_billing` | `/settlement/period` | `settlement` | `alias` | C5 Phase 1 |
| 13 | / 청구서관리 | `TSobo45` / `Subu45.pas` | `Sobo45_billing` | `/settlement/billing` | `settlement` | `alias` | C5 Phase 1 (DEC-031/032) |
| 14 | / 청구서관리-택배 | `TSobo45_1` / `Subu45_1.pas` | `Sobo45_billing` (variant=takbae) | `/settlement/billing?variant=takbae` | `settlement` | `alias` | layout: [Sobo45_1_billing.md](../../analysis/layout_mappings/Sobo45_1_billing.md) |
| 15 | / 청구서출력 | `TSobo46` / `Subu46.pas` | `Sobo46_billing` | `/settlement/billing/{billingKey}/print` | `settlement` | `alias` | C5 Phase 2 (DEC-035) |
| 16 | / 출고내역서 | `TSobo39` / `Subu39.pas` | — | — | — | `moved` | 별도 추적 — `report`/`outbound` 그룹 후속 |

> **요약 카운트**: `alias` **8**, `moved` **3**, `gap` **5** (그 중 발송비 P2 = 2). 메뉴 노출 대상은 `alias` 8 항목.

---

## 3. wrong_id 경고 — 레거시 Subu43/44 와 웹 동명 ID 충돌

웹 [`form-registry.ts`](../../도서물류관리프로그램/frontend/src/lib/form-registry.ts) 에는 다음 두 항목이 레거시와 **다른 기능** 으로 등재되어 있다. **본 매핑표·대시보드·향후 신규 ID 명명 시 반드시 구분** 한다.

| 웹 `id` | 웹 `folder` | 웹 캡션 | 웹 `route` | 레거시 동명 | 충돌 위험 |
|---|---|---|---|---|---|
| `Sobo43_stats_route` | `Subu43` | 출판사통계 | `/stats/publisher` | `Subu43.pas` 발송비내역 | **HIGH** — 동일 폴더, 전혀 다른 도메인 |
| `Sobo44_inv` | `Subu44` | 재고현황 | `/inventory/status` | `Subu44.pas` 발송비현황 | **HIGH** — 동일 폴더, 전혀 다른 도메인 |

**조치 방침**:
1. 향후 진짜 발송비 도메인 포팅 시 신규 ID 는 **`Sobo43_shipping_ledger` / `Sobo44_shipping_status`** 등 의도가 드러나는 이름을 사용한다.
2. 본 매핑 표 + 대시보드 카드 + DEC-049 참조 주석을 코드에 1줄 추가하여 자동 식별 가능하게 한다.
3. 백로그 분리는 단계 4 (백로그 P2) 에서 별도 처리.

---

## 4. 백로그 우선순위 (P0~P3)

| Priority | 항목 | 산출물 |
|---|---|---|
| **P0** | `billing` 메뉴에 alias 8건 노출 → 사이드바 「준비 중...」 해소 | `form-registry.ts` 별칭 8행, [`billing-c5-menu-porting.json`](../../dashboard/data/billing-c5-menu-porting.json) |
| **P1** | wrong_id 차단 주석 + DEC-049 동결 | 본 문서 §3, [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md) |
| **P2** | 진짜 발송비 도메인(Subu43/44) — 시나리오 카드 + 계약 + 라우트 | [`migration/coverage/billing-subu43-44-shipping-backlog.md`](./billing-subu43-44-shipping-backlog.md), `analysis/screen_cards/Sobo43_shipping.md`, `migration/contracts/shipping_ledger.yaml` |
| **P3** | `Sobo24_9` 명세서 발송건수, `Sobo38_1` 운임관리-택배, `Seok30` 메세지, `Sobo39` 출고내역서 | C5 코어 이후 스프린트 |

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 1차 작성. alias 8 / moved 3 / gap 5 / wrong_id 2 동결. P0 = billing 별칭 노출, P2 = 진짜 발송비(Subu43/44) 신설. |
