# Wave B — UI placeholder·blocked 카드 스코핑 (세금·레거시 출력 계획)

**목적**: `incomplete-features-inventory.json` 과 동일 방법론(dfm→html 산출물, `analysis/layout_mappings/*.md`, `data-legacy-id`)으로 후속 착수 순서를 고정한다.
**원칙 (사용자 룰)**: 각 라우트별로 매핑 노트 4건을 미리 양산하지 않고, **착수 시점**에 `analysis/layout_mappings/<Form>.md` 를 작성하되, **dfm 산출물 후보·Subu*.pas 후보**는 본 인덱스에서 결정적으로 가리킨다 (= 재귀 오류·중복 방지).

## 1. UI placeholder 4경로 (우선순위 = 인벤토리 순)

| 순서 | 라우트 | 레지스트리 id | 매트릭스 ID | dfm/html 후보 폴더 (`tools/.../legacy_source_root/<X>/`) | 후속 layout_mapping 파일명 |
|------|--------|---------------|-------------|------------------------------------------------------|----------------------------|
| 1 | `/year-month-stats` | `MenuYearMonthStats` | `ACC-MENU-NAV-07` (8 sub: ACC-MENU-YM-01~08) | `Subu50/Sobo50.html` (매출통계), `Subu51/Sobo51.html` (거래처통계), `Subu52/Sobo52.html` (도서회전), `Subu53/Sobo53.html` (분기손익) | `analysis/layout_mappings/Sobo50_stats.md` 외 8건 |
| 2 | `/shipping/returns-inventory` | `MenuShippingReturnsInventory` | `ACC-MENU-NAV-12` (T1·T3-LITE) | `Subu23/Sobo23.html` (반품명세서), `Subu24/Sobo24.html` (반품재고-재생), `Subu25/Sobo25.html` (반품재고-해체), 변형 `Subu23_1`, `Subu23_1_chul05`, `Subu23_1_chul08` | `analysis/layout_mappings/Sobo23_returns.md` (통합) |
| 3 | `/billing/statements` | `MenuBillingStatements` | `ACC-MENU-NAV-15` (4종 × 2 그레인) | `Subu54/Sobo54.html` (일별입고), `Subu55/Sobo55.html`, `Subu57/Sobo57.html`, `Subu58/Sobo58.html` (기간 반품) | `analysis/layout_mappings/Sobo54_statement.md` 외 |
| 4 | `/master/discount/[type]` | (동적) `Sobo39_1/_2/_5` | C9 마스터 — variant 분기 | `Subu39/Sobo39.html` 본판만 존재. 변종(`Subu39_1/_2/_5`)은 dfm 산출 미생성 → `migration/contracts/master_data.yaml` `customer_variants` 로 흡수 | `analysis/layout_mappings/Sobo39.md` (variant 절 추가) |

각 라우트 루트에는 이미 `data-legacy-id="<MenuId>.Placeholder"` 가 부착되어 DOM 회귀 시 placeholder 세트를 식별 가능 (현 사이클 산출).

## 2. phase2-screen-cards blocked (인벤토리 vs 실제 라우트 — 라우트 드리프트)

| 인벤토리 id | 인벤토리 route | 실제 page.tsx | 정렬 결정 |
|-------------|----------------|---------------|-----------|
| `Sobo48_compare` | `/ledger/comparison` | **출판사 설정 (Sobo48 본판)** 이 점유 중 | 카드 `scenario.blockers` 에 라우트 드리프트 한 줄 추가 (본 사이클). 장부대조 진입 시 ① `/ledger/comparison?view=compare` 모드 분기 또는 ② `/ledger/audit-compare` 신규 라우트 분리 필요. |
| `Sobo29_other` | `/transactions/other` | **기타명세서 — 조회·메모 저장 구현 완료, `Sobo29.*` data-legacy-id 부착됨** | 카드의 stale 표기 사실을 `scenario.blockers` 한 줄로 명시 (본 사이클). 잔존 갭은 **인쇄 양식(T7)** 만이라 DEC-040 충돌 없이 후속 사이클에서 인쇄 모듈만 보강. |

> 위 두 변경은 `dashboard/data/phase2-screen-cards.json` 의 `scenario.blockers` 만 갱신했다. `tasks` 상태는 회귀 러너(`test_regression_phase2.py`) 가 503 허용 분기로 사용하는 단일 원천이라 본 사이클에서 변경하지 않는다 (사용자 룰: 임시방편 우선순위 변경 금지). 진짜 진입 시 카드의 `tasks.T7` 등을 갱신하면서 layout_mapping 도 같이 만든다.

## 3. 완료 판정 (Wave B — 본 사이클)

- [x] 4경로 placeholder 페이지에 `data-legacy-id="<MenuId>.Placeholder"` 부착.
- [x] 두 blocked 카드(`Sobo48_compare`, `Sobo29_other`) 의 라우트 드리프트 사실을 인벤토리 단일 원천(`phase2-screen-cards.json`) 에 영속.
- [ ] (다음 사이클) 진입 시 §1 의 후보 dfm 폴더 → `analysis/layout_mappings/<Form>.md` 1:1 작성, §2 의 라우트 분기 또는 신규 라우트 결정.
