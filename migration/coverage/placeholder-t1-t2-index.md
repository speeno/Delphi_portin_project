# Placeholder 8 화면 — T1·T2 인덱스 (Phase2 유지)

**ID**: PLACEHOLDER-T1-T2-INDEX
**일자**: 2026-04-21
**연관 문서**: `docs/phase1-promotion-gate.md` §3 T-Phase, `migration/coverage/phase1-12pages-coverage.md`
**목적**: 6개(실제 8개) placeholder 화면의 T1(screen_card) + T2(이벤트·SQL 추출) 산출물 인덱싱 + Phase 1 승격 비대상 명시.

---

## 0. 결론

8개 placeholder 화면 모두 T1·T2 산출물(`analysis/screen_cards/<Form>.md`) 이 이미 존재한다.
본 인덱스는 다음을 명문화한다:

1. **승격 비대상**: 8개 화면은 사용자 합의에 따라 Phase 1 승격 대상이 아니다 (`form-registry.ts` 의 `phase: "phase2"` 유지).
2. **Phase 2 진입 조건**: 본 인덱스에서 ✅ 표시된 T1·T2 산출물 외에 T3(contract.yaml) ~ T6(test_pack.json) 까지 추가 작성 필요.
3. **현재 사용자 노출**: `screen-placeholder.tsx` 가 "준비 중 (Phase 2)" 안내 + 백엔드 라우트는 `/api/v1/_stub/<name>` 503 응답으로 통일.

---

## 1. 8개 화면 인덱스

| # | id | folder | route | screen_card (T1·T2) | 매핑 시나리오 | DB 영향 (write 테이블) | 후속 |
|---|---|---|---|---|---|---|---|
| 1 | Sobo16_special | Subu16 | `/master/special` | [Sobo16.md](../../analysis/screen_cards/Sobo16.md) | C9 상품·고객 마스터 | G4_Book / G1_Ggeo / G6_Ggeo | T3 — `master_data.yaml` 변형 추가 |
| 2 | Sobo29_other   | Subu29 | `/transactions/other` | [Sobo29.md](../../analysis/screen_cards/Sobo29.md) | C6 거래/잔액 조회 (변형) | S1_Ssub / S1_Memo | T3 — `sales_inquiry.yaml` 변형 추가 |
| 3 | Sobo28_delivery | Subu28 | `/delivery/management` | [Sobo28.md](../../analysis/screen_cards/Sobo28.md) | (신규 — 택배 관리) | S1_Ssub (택배 컬럼) | T3 — `delivery_dispatch.yaml` 신설 |
| 4 | Sobo39_1 (할인율2) | Subu39_1 | (메뉴만) | [Sobo39_1.md](../../analysis/screen_cards/Sobo39_1.md) | C9 마스터 (할인율 변형) | (Sobo39 와 공유) | T3 — `master_data.yaml` discount variant |
| 5 | Sobo39_2 (할인율 기타) | Subu39_2 | (메뉴만) | [Sobo39_2.md](../../analysis/screen_cards/Sobo39_2.md) | C9 마스터 (할인율 변형) | (Sobo39 와 공유) | T3 — 동상 |
| 6 | Sobo39_5 (할인율 물류) | Subu39_5 | (메뉴만) | [Sobo39_5.md](../../analysis/screen_cards/Sobo39_5.md) | C9 마스터 (할인율 변형) | (Sobo39 와 공유) | T3 — 동상 |
| 7 | Sobo48_compare | Subu48 | `/ledger/comparison` | [Sobo48.md](../../analysis/screen_cards/Sobo48.md) | C6 원장 (장부대조) | (read-only, S1_Ssub vs Sg_Csum) | T3 — `sales_inquiry.yaml` audit_compare |
| 8 | Sobo43_stats_route | Subu43 | `/stats/publisher` | [Sobo43.md](../../analysis/screen_cards/Sobo43.md) | C13 통계 (출판사 변형) | (read-only) | T3 — `stats_reports.yaml` publisher variant |

> 사용자 메모의 "6개 placeholder" 는 **메뉴 기준 6 카드** 이고, 화면 카드 단위로는 위 8개 (할인율 3종 분리). 본 인덱스는 분석 단위 8개 모두를 다룬다.

---

## 2. T1·T2 산출물 검증 체크

각 screen_card 가 T1·T2 게이트를 충족하는지 일괄 확인 (자동 생성: `tools/analysis/screen_card_builder.py`).

### T1 (screen_card 게이트)
- ✅ `## 1. UI 구성` — 컴포넌트 인벤토리 + 카운트 표
- ✅ `## 2. 이벤트 흐름` — 이벤트 종류 분포 + 핸들러 카운트
- ✅ `## 4. DB 영향` — 영향 테이블 CRUD 매트릭스
- ✅ `## 5. 검증 규칙` — empty_check 등 검증 위치
- ✅ `## 6. 고객사 분기` — variant 부재 단언 (또는 매칭 결과)

### T2 (event_sql_extract 게이트)
- ✅ `## 3. 데이터 액세스 (SQL)` — 주요 SQL line + 타입 + 테이블
- ⚠ "(수동) query_capture 보강" 권고 — 라이브 캡처는 후속 (Phase 2 입력)

8개 모두 위 6항목 자동 생성 완료. T2 의 query_capture 보강은 **Phase 2 진입 시점에 작성**하는 것이 비용 효율적.

---

## 3. Placeholder 표시 정책

**프론트엔드** (`screen-placeholder.tsx`):
- 본 8개 화면의 page.tsx 는 `<ScreenPlaceholder formId="..." caption="..." />` 만 렌더.
- 사용자에게 "준비 중 (Phase 2 — 화면카드 작성 완료, 백엔드 SQL 미구현)" 메시지 노출.

**백엔드** (`routers/_stub.py`):
- 본 8개 화면이 호출할 가능성이 있는 라우트는 명시적으로 503 + `code=NOT_IMPLEMENTED` 응답.
- 프론트의 `api.getOptional()` 헬퍼가 503/NOT_IMPLEMENTED 를 흡수하여 사용자에게 placeholder 만 노출.

**사이드바** (`components/layout/sidebar.tsx`):
- `phase: "phase2"` → 회색 dot 표시 (녹색 체크 아님).
- 정상 동작 — 별도 변경 불필요.

---

## 4. Phase 2 승격 시나리오

본 8개 화면이 Phase 2 (정상 동작) 로 승격되려면 다음 추가 작업 필요:

1. **T3 contract**: 위 표의 "후속" 컬럼에 명시된 contract.yaml 변형 추가.
2. **T4 api**: 백엔드 `services/<domain>_service.py` + 라우터 추가.
3. **T5 ui**: 모던 화면 page.tsx 신설 (placeholder 대체).
4. **T6 test_pack**: contract 와 1:1 회귀 케이스.

> Phase 1 승격(녹색 체크) 까지 가려면 추가로 T7 (회귀) + T8 (PR 승급).
> 본 인덱스는 T1·T2 만 명시하고 T3~T8 은 화면별 별도 PR 단위로 진행.

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 최초 작성. 8개 placeholder 화면 T1·T2 산출물 일괄 인덱싱 + Phase 1 승격 비대상 명시. |
