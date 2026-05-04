# 구현되지 못한 기능 인벤토리 (저장소 자동 산출)

생성: `2026-05-04T09:14:55.754099+00:00` (`debug/generate_incomplete_features_inventory.py`)

## 판정 기준 (합집합)

본 인벤토리는 계획서 「구현되지 못한 기능 목록」에 따라 **원천별 합집합** 을 기록한다. 단일 정의가 아니라 (A) UI placeholder (B) T-파이프라인 비완료 (C) form-registry preview/STUB (D) 백엔드 범용 stub (E) crud-backlog §2.6 참조 를 모두 포함한다.

## 1. UI — `ScreenPlaceholder` 가 붙은 라우트

- `도서물류관리프로그램/frontend/src/app/(app)/billing/statements/page.tsx` → 라우트 추정 `/billing/statements`
- `도서물류관리프로그램/frontend/src/app/(app)/master/discount/[type]/page.tsx` → 라우트 추정 `/master/discount/[type]`
- `도서물류관리프로그램/frontend/src/app/(app)/shipping/returns-inventory/page.tsx` → 라우트 추정 `/shipping/returns-inventory`
- `도서물류관리프로그램/frontend/src/app/(app)/year-month-stats/page.tsx` → 라우트 추정 `/year-month-stats`

## 2. T1–T8 — `phase2-screen-cards.json` 에서 아직 done 아닌 task

> **드리프트 주의:** 카드의 레거시 ID·캡션과 해당 `route` 의 `page.tsx` 실구현 범위가 다를 수 있다. 판단은 API·화면 코드 우선.

- **Sobo48_compare** (장부대조) `/ledger/comparison` — {'T2': 'in_progress', 'T3': 'blocked', 'T4': 'pending', 'T5': 'pending', 'T6': 'in_progress', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['레거시 단일 SQL 미확정', '신규 SQL 0 정책(DEC-040)']
- **Sobo29_other** (기타명세서) `/transactions/other` — {'T2': 'in_progress', 'T3': 'blocked', 'T4': 'pending', 'T5': 'pending', 'T6': 'in_progress', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['레거시 폼 단순 출력기 — SQL 미확정']

## 3. `form-registry` — preview 또는 STUB

- `MenuBillingStatements` route `/billing/statements` — ['STUB', 'preview'] (line 1100)
- `MenuShippingReturnsInventory` route `/shipping/returns-inventory` — ['STUB', 'preview'] (line 1081)
- `MenuYearMonthStats` route `/year-month-stats` — ['STUB', 'preview'] (line 1062)

## 4. 백엔드 범용 stub

- 파일: `도서물류관리프로그램/backend/app/routers/_stub.py`
- 패턴: GET /api/v1/_stub/{name} -> 503 NOT_IMPLEMENTED
- 비고: 정산 세금 외부 발행 등 DEC-035 stub 은 settlement 라우터 주석 참고

## 5. `docs/crud-backlog.md` §2.6 참조 (문서 불릿)

- `Sobo29_other` (기타명세서)
- `Sobo48_compare` (장부대조)
- `Sobo43_stats_route` (출판사통계)
- (할인율 변형) `/master/discount/[type]` 라우트는 메뉴 미노출 — 별도 등록 없음.

## 갱신 방법

```bash
python3 debug/generate_incomplete_features_inventory.py
```

산출: `analysis/audit/incomplete-features-inventory.md` · `.json`

