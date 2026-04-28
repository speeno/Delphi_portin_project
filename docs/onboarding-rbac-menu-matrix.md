# 계정 유형별 메뉴·기능 노출 매트릭스 (`ACC-MENU-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 (2026-04-24 갱신: `source_builds` 컬럼 + ACC-T3 sub-type + 동일 테넌트 다중 빌드 정책) |
| 추적 ID | `ACC-MENU-*` (행 = 메뉴 노출 단위), `ACC-API-*` (행 = API 허용 단위) |
| 단일 원천 | 본 문서. 프론트 `PermissionGuard` 와 백엔드 라우터 가드는 본 표를 import 하여 동작. |
| 정합 | [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md) (`ACC-T1/T2-DIST/T2-PUB/T3`), [`docs/welove-ftp-tongpan-chulpan-chul-menu-diff.md`](welove-ftp-tongpan-chulpan-chul-menu-diff.md) (총판 vs 출판 표준 2 빌드), [`docs/welove-chul-build-menu-matrix.md`](welove-chul-build-menu-matrix.md) (7 빌드 합집합 매트릭스 — `source_builds` 컬럼 정본), [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md) (Seek_Uses Fxx 라이선스 키 메커니즘), [`docs/user-permission-management-plan.md`](user-permission-management-plan.md) (`Id_Logn` Fxx), `migration/contracts/admin_permissions.yaml` |
| Build ID 약칭 | `D-STD`=`BLD-DIST-STD` / `P-STD`=`BLD-PUB-STD` / `D-KBT`=`BLD-DIST-KBT` / `P-KBT`=`BLD-PUB-KBT` (≡P-STD) / `WH-WL`=`BLD-PUB-WAREHOUSE-WELOVE` / `WH-MS`=`BLD-PUB-WAREHOUSE-MS` / `WH-BB`=`BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW` |

---

## 1. 한 줄 요약

| 유형 | 1차 검증 출처 빌드 | 메뉴 출처 | 추가/제거 |
|---|---|---|---|
| **`ACC-T1` 수퍼관리자** | (전 빌드 합집합 + 운영 콘솔) | 전체 — 운영 콘솔 + 모든 도메인 | + admin 콘솔 / + 서버 라우팅 override |
| **`ACC-T2-DIST` 총판** | `D-STD` (1차) · `D-KBT` (확장 검증) | publisher 셸 + `출판사관리` | + 출판사관리 / + 소속 출판사 운영 보드 |
| **`ACC-T2-PUB` 소속 출판사** | `P-STD` ≡ `P-KBT` | `출판관리프로그램` 메뉴 셋 | + **년/월(통계)** / − 출판사관리 / `hcode` 격리 |
| **`ACC-T3` 독립 출판사** | `P-STD` (메뉴 셸) | publisher 셸 단독 운영 | + 본인 마스터 직접 등록 / 단독 DB |
| **`ACC-T3-WAREHOUSE-LITE` (가설)** | `WH-WL` (`chul_09` SKU = 위러브1·2·3 + 교문사) | 자체 물류 + publisher (메뉴 7개, 반품재고 통합) | + 출고/재고원장/반품재고관리/발송비/내역서 / − 거래·원장·회계·자료 (publisher 4 영역) |
| **`ACC-T3-WAREHOUSE-FULL` (가설)** | `WH-MS` (`book_21`) + `WH-BB` (`book_07` = 북앤북·유앤북) **2 빌드 일치** | 자체 물류 full (메뉴 8개, 재고/반품 분리) | + LITE 기능 + 재고관리·반품관리 분리 + (MS 한정) 라벨 SDK + (BB 한정) 신규 폼군 + 다중 DB 디렉토리 |

**가설 채택 근거** (`OQ-BLD-2`): WH-MS 와 WH-BB 가 **상단 메뉴 8개·재고/반품 분리·출판사관리 보유** 패턴이 일치 — 2 빌드 신뢰성으로 LITE/FULL 분리 권고.

> 기준: 본 매트릭스는 7 빌드 합집합을 단일 코드베이스에서 RBAC 분기로 운영. `source_builds` 컬럼 = 해당 메뉴가 발견된 빌드 ID 집합.

---

## 2. 최상위 메뉴 노출 (`ACC-MENU-NAV-*`)

| ID | 라우트(웹 대응) | 캡션 | T1 | T2-DIST | T2-PUB | T3 | T3-LITE | T3-FULL | source_builds |
|----|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `ACC-MENU-NAV-01` | `/(app)/masters` | 기초관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | D-STD, P-STD, D-KBT, P-KBT, WH-WL, WH-MS, WH-BB (전 빌드) |
| `ACC-MENU-NAV-02` | `/(app)/transactions` | 거래관리 | ✓ | ✓ | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT |
| `ACC-MENU-NAV-03` | `/(app)/ledger` | 원장관리 | ✓ | ✓ | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT |
| `ACC-MENU-NAV-04` | `/(app)/accounting` | 회계관리 | ✓ | ✓ | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT |
| `ACC-MENU-NAV-05` | `/(app)/data` | 자료관리 | ✓ | ✓ | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT |
| `ACC-MENU-NAV-06` | `/(app)/stats` | 통계관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 전 빌드 |
| `ACC-MENU-NAV-07` | `/(app)/year-month-stats` | 년/월(통계) | ✓ | — | ✓ | ✓ | — | — | P-STD, P-KBT (출판 전용) |
| `ACC-MENU-NAV-08` | `/(app)/admin` | 관리자 콘솔 | ✓ | — | — | — | — | — | 웹 신설 |
| `ACC-MENU-NAV-09` | `/(app)/shipping/orders` | 출고관리 | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB (자체 물류) |
| `ACC-MENU-NAV-10` | `/(app)/shipping/inventory-ledger` | 재고원장 | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB |
| `ACC-MENU-NAV-11` | `/(app)/shipping/inventory` | 재고관리 (분리) | ✓ | ✓ | — | — | — | ✓ | D-KBT, WH-MS, WH-BB |
| `ACC-MENU-NAV-12` | `/(app)/shipping/returns-inventory` | 반품재고관리 (통합) | ✓ | — | — | — | ✓ | — | WH-WL 단독 |
| `ACC-MENU-NAV-13` | `/(app)/shipping/returns` | 반품관리 (분리) | ✓ | ✓ | — | — | — | ✓ | D-KBT, WH-MS, WH-BB |
| `ACC-MENU-NAV-14` | `/(app)/billing` | 발송비/입금관리 | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB |
| `ACC-MENU-NAV-15` | `/(app)/billing/statements` | 내역서관리 | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB |
| `ACC-MENU-NAV-16` | `/(app)/shipping/courier` | 택배관리 | ✓ | ✓ | — | — | — | — | **D-KBT 단독** (한국도서유통 총판) |

**해석**: NAV-09~15 는 **자체 물류·distributor 셸** 의 메뉴군. publisher 셸 (NAV-02~05/07) 과는 정합되지 않음 — 같은 사용자가 두 셸을 동시에 보지 않는다. T2-DIST/T3-LITE/T3-FULL 는 자체 물류 셸을, T2-PUB/T3 는 publisher 셸을 본다.

→ 표 변경 시 [`backend/app/routers/admin.py`](../도서물류관리프로그램/backend/app/routers/admin.py) 의 nav 응답·`PermissionGuard` 의 라우트 화이트리스트가 자동 갱신되도록 **본 문서 → JSON export** 를 후속 단계에서 도입. `source_builds` 컬럼은 [`analysis/welove_chul_menu_matrix.json`](../analysis/welove_chul_menu_matrix.json) 에서 export.

---

## 3. 기초관리 하위 (`ACC-MENU-MASTERS-*`)

7 빌드 합집합 (정본은 [`analysis/welove_chul_menu_matrix.json`](../analysis/welove_chul_menu_matrix.json)). Fxx 는 [`analysis/welove_chul_menu_handlers.json`](../analysis/welove_chul_menu_handlers.json) 의 `Seek_Uses` 에서 추출 (예시값 — 핸들러별 정확한 키는 후속 사이클 `OQ-LICENSE-KEY-MAP` 에서 정본화).

| ID | 캡션 | 웹 라우트 | T1 | T2-DIST | T2-PUB | T3 | T3-LITE | T3-FULL | source_builds | Fxx |
|----|---|---|:-:|:-:|:-:|:-:|:-:|:-:|---|---|
| `ACC-MENU-MASTERS-01` | 거래처관리 (단일) | `/(app)/masters/customers` | ✓ | — | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT | F11 |
| `ACC-MENU-MASTERS-01a` | 거래처관리(개별) | `/(app)/masters/customers/individual` | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB | F11 |
| `ACC-MENU-MASTERS-01b` | 거래처관리(통합) | `/(app)/masters/customers/integrated` | ✓ | ✓ | — | — | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB | F11 |
| `ACC-MENU-MASTERS-02` | 입고처관리 | `/(app)/masters/inbound-vendors` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 전 빌드 | F12 |
| `ACC-MENU-MASTERS-03` | 기타거래처 | `/(app)/masters/etc-customers` | ✓ | — | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT | F13 |
| `ACC-MENU-MASTERS-04` | **출판사관리** | `/(app)/masters/publishers` | ✓ | ✓ | — | — | ✓ | ✓ | D-STD, D-KBT, WH-WL, WH-MS, WH-BB (publisher 빌드 부재) | F17 |
| `ACC-MENU-MASTERS-04a` | 출판사관리(설정) | `/(app)/masters/publishers/settings` | ✓ | ✓ | — | — | — | (MS) | D-KBT, WH-MS | (TBD) |
| `ACC-MENU-MASTERS-04b` | 출판사관리-택배 | `/(app)/masters/publishers/courier` | ✓ | ✓ | — | — | — | — | **D-KBT 단독** | (TBD) |
| `ACC-MENU-MASTERS-04c` | 출판사MMS(설정/조회) | `/(app)/masters/publishers/mms` | ✓ | ✓ | — | — | — | — | **D-KBT 단독** (Smms 폼군) | (TBD) |
| `ACC-MENU-MASTERS-05` | 도서관리 | `/(app)/masters/books` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 전 빌드 | F14 |
| `ACC-MENU-MASTERS-05a` | 도서관리(위치) | `/(app)/masters/books/locations` | ✓ | ✓ | — | — | — | (MS) | **WH-MS 단독** (창고 위치) | (TBD) |
| `ACC-MENU-MASTERS-06` | 저자관리 | `/(app)/masters/authors` | ✓ | — | ✓ | ✓ | — | — | D-STD, P-STD, P-KBT | F19 |
| `ACC-MENU-MASTERS-07` | 종당관리(도서) | `/(app)/masters/series` | ✓ | ✓ | — | — | — | ✓ | D-KBT, WH-MS, WH-BB | (TBD) |
| `ACC-MENU-MASTERS-08` | 지역분류 / (시내+지방) | `/(app)/masters/regions` | ✓ | ✓ | — | — | ✓ | ✓ | WH-WL(단순) · D-KBT/WH-MS/WH-BB(확장) | (TBD) |
| `ACC-MENU-MASTERS-09` | 출고증정렬 | `/(app)/masters/shipping-sort` | ✓ | ✓ | — | — | — | — | **D-KBT 단독** | (TBD) |
| `ACC-MENU-MASTERS-10` | 출고정지유무 | `/(app)/masters/shipping-block` | ✓ | — | — | — | — | (BB) | **WH-BB 단독** | (TBD) |
| `ACC-MENU-MASTERS-11` | 특별관리 | `/(app)/masters/special` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 전 빌드 | F18 |
| `ACC-MENU-MASTERS-12` | 환경설정 | `/(app)/masters/settings` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 전 빌드 | (TBD) |
| `ACC-MENU-MASTERS-13` | 메뉴보이기 / 메뉴감추기 | n/a — `(app)/profile/preferences::toolbar_visible` | — | — | — | — | — | — | P-STD, P-KBT (publisher 만 — 실제는 ToolBar 토글, [`menu-visibility-runtime-design.md::MENUVIS-DEC-02`](menu-visibility-runtime-design.md)) | F11 (스텁) |

> P-STD ≡ P-KBT 바이트 동일 (`BLD-PUB-KBT` 는 한국도서유통 패키지에 동봉된 표준 출판 빌드 — 별도 변형 아님). 매트릭스에서 항상 동일.

---

## 4. 거래·원장·회계·자료·통계 vs 출고·재고·발송비·내역서 (`ACC-MENU-OPS-*`)

레거시 두 셸 (publisher · distributor/warehouse) 의 동일 업무 매핑. 웹은 한 라우트 트리에서 RBAC 로 분기.

### 4.1 publisher 셸 (T2-PUB / T3 — `P-STD`/`P-KBT`)

| 카테고리 | 라우트 | T1 | T2-PUB | T3 | source_builds |
|---|---|:-:|:-:|:-:|---|
| 거래관리 (`/transactions/*`) | 출고·반품·입고·청구 | ✓ | ✓ | ✓ | P-STD, P-KBT (D-STD 도 동일 셸 보유) |
| 원장관리 (`/ledger/*`) | 거래처원장·도서원장 | ✓ | ✓ | ✓ | P-STD, P-KBT, D-STD |
| 회계관리 (`/settlement/*`) | 정산·마감 | ✓ | ✓ | ✓ | P-STD, P-KBT, D-STD |
| 자료관리 (`/reports/*`) | 자료·리포트 | ✓ | ✓ | ✓ | P-STD, P-KBT, D-STD |
| 통계관리 (`/stats/*`) | 일별·월별 통계 | ✓ | ✓ | ✓ | 전 빌드 |
| 년/월(통계) (`/year-month-stats/*`) | (§5) | ✓ | ✓ | ✓ | P-STD, P-KBT |

### 4.2 distributor / warehouse 셸 (T2-DIST / T3-LITE / T3-FULL — `D-KBT` · `WH-WL` · `WH-MS` · `WH-BB`)

| 레거시 캡션 | 웹 라우트 | T2-DIST | T3-LITE | T3-FULL | source_builds | 명칭 변형 |
|---|---|:-:|:-:|:-:|---|---|
| 출고관리/거래명세서 | `/(app)/shipping/sales-statement` | ✓ | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB | publisher 셸의 `거래관리/거래명세서` 와 동일 업무 |
| 출고관리/입고명세서 | `/(app)/shipping/inbound-statement` | ✓ | ✓ | ✓ | 동상 | publisher 셸의 `거래관리/입고명세서` 와 동일 |
| 출고관리/반품명세서 | `/(app)/shipping/returns-statement` | ✓ | ✓ | ✓ | 동상 | (publisher 셸은 거래관리/기타명세서로 표현) |
| 출고관리/신간발행 | `/(app)/shipping/new-release` | ✓ | ✓ | ✓ | 동상 | publisher 와 동일 캡션 |
| 출고관리/신간(가)입고 관리 | `/(app)/shipping/new-pre-inbound` | ✓ | — | ✓ | D-KBT, WH-MS, WH-BB | T3-LITE 부재 |
| 출고관리/출고접수관리·현황 | `/(app)/shipping/orders` | ✓ | ✓ | ✓ | 동상 | |
| 출고관리/출고검증관리(개별) | `/(app)/shipping/verification` | ✓ | — | (MS) | D-KBT, WH-MS | |
| 출고관리/출고택배관리 | `/(app)/shipping/courier-orders` | ✓ | ✓ | ✓ | 동상 | |
| 출고관리/전송자료받기(FTP) | `/(app)/shipping/import-ftp` | ✓ | ✓ | ✓ | 동상 | 외부 출판사 출고 데이터 인입 |
| 재고원장/도서별수불원장 | `/(app)/inventory/book-flow-ledger` | ✓ | ✓ | ✓ | 동상 | publisher 셸의 `원장관리/도서별수불원장` 과 동일 |
| 재고원장/기간별재고원장 | `/(app)/inventory/period-ledger` | ✓ | ✓ | ✓ | 동상 | publisher 셸의 `원장관리/기간별재고원장` 과 동일 |
| 재고관리/정품재고(변경/폐기) | `/(app)/inventory/regular` | ✓ | — | ✓ | D-KBT, WH-MS, WH-BB | T3-LITE 는 반품재고관리 통합본으로 처리 |
| 재고관리/반품재고(변경/폐기/입고) | `/(app)/inventory/returns` | ✓ | — | ✓ | 동상 | |
| 반품관리/반품명세서·반품재고원장·반품재고현황 | `/(app)/returns/*` | ✓ | — | ✓ | D-KBT, WH-MS, WH-BB | T3-LITE 는 §11 의 통합본 |
| 반품재고관리/* (통합) | `/(app)/returns-inventory/*` | — | ✓ | — | **WH-WL 단독** | T3-LITE 전용 통합 화면 |
| 발송비/입금관리/{발송비·청구서·입금·반품수거} | `/(app)/billing/*` | ✓ | ✓ | ✓ | D-KBT, WH-WL, WH-MS, WH-BB | publisher 셸 부재 — 자체물류 전용 |
| 내역서관리/{기간별·일별}{입고·출고·반품·택배}내역서 | `/(app)/billing/statements/*` | ✓ | ✓ | ✓ | 동상 | |
| 택배관리 | `/(app)/shipping/courier` | ✓ | — | — | **D-KBT 단독** | 한국도서유통 총판의 직접 택배 모듈 (Sobo28) |

### 4.3 publisher ↔ distributor/warehouse 동일 업무 명칭 매핑 표

| 의미 | publisher 캡션 | distributor/warehouse 캡션 | 표준화 (웹 표시) |
|---|---|---|---|
| 출고 1 건 발행 | 거래관리/거래명세서 | 출고관리/거래명세서 | "출고 명세서" |
| 입고 1 건 발행 | 거래관리/입고명세서 | 출고관리/입고명세서 | "입고 명세서" |
| 반품 1 건 발행 | 거래관리/기타명세서 | 출고관리/반품명세서 | "반품 명세서" |
| 도서 수불 원장 | 원장관리/도서별수불원장 | 재고원장/도서별수불원장 | "도서별 수불 원장" |
| 기간 재고 원장 | 원장관리/기간별재고원장 | 재고원장/기간별재고원장 | "기간별 재고 원장" |
| 반품·재고 처리 | (없음) | 반품관리 + 재고관리 (FULL) / 반품재고관리 (LITE) | "반품·재고" 메뉴 그룹 (UI 토글) |
| 발송비·청구·입금 | (없음) | 발송비/입금관리 | "정산·청구" 메뉴 그룹 |

> 가시 범위(읽기/쓰기) 차이는 **데이터 격리** 표(§6) 에서 다룬다 — 메뉴 표시 자체는 본 표.

---

## 5. 년/월(통계) 출판 전용 (`ACC-MENU-YM-*`)

| ID | 캡션 | 웹 라우트 | T1 | T2-DIST | T2-PUB | T3 |
|----|---|---|:-:|:-:|:-:|:-:|
| `ACC-MENU-YM-01` | 도서별/분류별판매 | `/year-month-stats/sales-by-book` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-02` | 거래처/구분별판매 | `/year-month-stats/sales-by-customer` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-03` | 도서별판매(년/월) | `/year-month-stats/sales-by-book-monthly` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-04` | 거래처판매(년/월) | `/year-month-stats/sales-by-customer-monthly` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-05` | 년/월판매(도서별) | `/year-month-stats/yearly-by-book` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-06` | 년/월판매(거래처) | `/year-month-stats/yearly-by-customer` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-07` | 거래처수금(년/월) | `/year-month-stats/collections-monthly` | ✓ | — | ✓ | ✓ |
| `ACC-MENU-YM-08` | 거래처수금(구분별) | `/year-month-stats/collections-by-class` | ✓ | — | ✓ | ✓ |

---

## 6. 데이터 가시성 / 격리 (`ACC-DATA-*`)

| ID | 정책 | T1 | T2-DIST | T2-PUB | T3 | T3-LITE | T3-FULL |
|----|---|---|---|---|---|---|---|
| `ACC-DATA-01` | 서버(`primary_server`) 가시 범위 | 모두 (admin override) | 본인 총판 1 서버 | 총판과 동일 서버 | 본인 단독 서버 | 본인 SKU 의 공유 서버 (chul_09 그룹) | 본인 SKU 의 단독/공유 서버 (book_07/book_21) |
| `ACC-DATA-02` | DB 가시 범위 | 모두 | 본인 총판 1 DB | 총판 DB (`hcode` 격리 컬럼 강제) | 본인 단독 DB | `chul_09_db` 공유 + `hcode` 격리 (위러브1·2·3+교문사) | `book_07_db` 또는 `book_21_db` (FULL-NEW=공유 + hcode / FULL-LABEL=단독) |
| `ACC-DATA-03` | `hcode` 행 격리 (M4 — 후속 결정) | 강제 안 함 | 강제 안 함 | **강제** | 강제 안 함 (1 hcode) | **강제** (chul_09 SKU 다중 테넌트) | (FULL-NEW) **강제** / (FULL-LABEL) 단독 → 강제 안 함 |
| `ACC-DATA-04` | 마스터 쓰기 권한 (출판사·총판 마스터) | ✓ | 본인 총판 + 소속 출판사 등록·승인 | — (본인 정보만) | 본인 정보만 | 본인 정보 + 본인 자체 물류 거래처 | 본인 정보 + 본인 자체 물류 거래처 + (MS) 라벨 프린터 설정 |

> M4 (`hcode` 행 강제) 는 `user-permission-management-plan.md` 의 보류 항목 — 본 매트릭스는 정책을 명시만 하고 강제 시점은 별 DEC. **T3-LITE 는 chul_09_db 공유로 확인되어 hcode 강제 필수** (`analysis/welove_db_route_matrix.json` 의 routes 4 건 = 위러브1·2·3 + 교문사).

---

## 7. 관리자 콘솔 (`ACC-MENU-ADMIN-*`)

| ID | 화면 | T1 | T2-DIST | T2-PUB | T3 |
|----|---|:-:|:-:|:-:|:-:|
| `ACC-MENU-ADMIN-01` | 사용자 관리 (`/admin/users`) | ✓ | ✓ (본인 소속 출판사 사용자만) | — | — |
| `ACC-MENU-ADMIN-02` | 가입 신청 큐 (`/admin/signup-requests`) | ✓ | ✓ (본인 총판 신청만) | — | — |
| `ACC-MENU-ADMIN-03` | 사용자별 서버 (`/admin/user-servers`) | ✓ | — | — | — |
| `ACC-MENU-ADMIN-04` | 권한 매트릭스 (`/admin/permissions`) | ✓ | — | — | — |
| `ACC-MENU-ADMIN-05` | 감사 로그 뷰 (`/admin/audit`) | ✓ | ✓ (본인 도메인 한정) | — | — |
| `ACC-MENU-ADMIN-06` | 본인 프로필·비번 (`/profile`) | ✓ | ✓ | ✓ | ✓ |

---

## 8. API 가드 (`ACC-API-*`) — 라우터 정합

| ID | 라우트 | 메서드 | 허용 유형 |
|----|---|---|---|
| `ACC-API-01` | `/api/v1/admin/users` | GET/POST/DELETE | T1, T2-DIST(본인 총판 hcode 필터) |
| `ACC-API-02` | `/api/v1/admin/signup-requests` | GET/POST(approve)/DELETE | T1, T2-DIST(본인 총판) |
| `ACC-API-03` | `/api/v1/admin/user-servers` | GET/POST/DELETE | T1 only |
| `ACC-API-04` | `/api/v1/admin/permissions` | GET/POST | T1 only |
| `ACC-API-05` | `/api/v1/public/signup-requests` | POST | 비로그인 (트랙 = T2-PUB / T3) |
| `ACC-API-06` | `/api/v1/profile/me/password` | POST | 본인(모든 유형) |
| `ACC-API-07` | `/api/v1/admin/users/{id}/password` | POST | T1, T2-DIST (본인 총판 사용자만) |
| `ACC-API-08` | 도메인 GET/POST/PUT (`/transactions/...`, `/ledger/...`, ...) | — | 모든 활성 유형 — `pool_for(jwt)` + (T2-PUB 의 경우) `hcode` 필터 자동 부착 |

---

## 9. 변경 절차

1. 본 문서의 표가 단일 원천이다.
2. 메뉴 추가/삭제 시 §2~§5 의 표에 1 행 추가/표시. 추적 ID 는 새로 부여.
3. 후속 단계에서 본 표를 `analysis/rbac_matrix.json` 으로 export — `PermissionGuard` 와 라우터 가드가 동일 JSON 에서 조회.
4. 변경 PR 은 본 문서 추적 ID(예: `ACC-MENU-NAV-08`)를 커밋 메시지에 명시.

---

## 10. 수용 기준

- ✅ 4 가지 유형 (+ 2 가설 sub-type T3-LITE/T3-FULL) × 표 §2~§5 의 모든 메뉴 항목이 ✓ / — 로 채워져 있음.
- ✅ 모든 `ACC-MENU-*` 행이 `source_builds` 컬럼 보유 (정본은 [`analysis/welove_chul_menu_matrix.json`](../analysis/welove_chul_menu_matrix.json)).
- ✅ §6 의 `ACC-DATA-03` 가 후속 DEC ID(M4 결정)와 1:1 링크.
- ✅ §7 의 admin 콘솔 5 항목이 현 [`backend/app/routers/admin.py`](../도서물류관리프로그램/backend/app/routers/admin.py) 와 라우트 정합.
- ✅ 본 문서가 `migration/contracts/admin_permissions.yaml` 의 `account_types[*].menus` 단락에서 인용.

---

## 11. 동일 테넌트 다중 빌드 / 동일 SKU 다중 테넌트 처리 정책 (`ACC-MULTI-*`)

`Uses=한국도서유통` 이 `D-KBT` + `WH-BB` 2 빌드에서 동시 사용되는 사례 (`OQ-BLD-5`) 와 `chul_09` SKU 가 위러브1·2·3 + 교문사 4 테넌트에 배포되는 사례 (`OQ-BLD-T3-LITE-MULTI`) 의 운영 규칙.

| ID | 정책 | 적용 시점 |
|---|---|---|
| `ACC-MULTI-01` | 로그인 라우팅 키 = `(tenant_id, account_family)` 또는 `(tenant_label, build_role)` 합성 키. `Uses` 라벨 단독 사용 금지. | DSN 라우팅 — [`docs/decision-login-db-routing.md::DSN-DEC-06`](decision-login-db-routing.md) |
| `ACC-MULTI-02` | 같은 운영 기관이 distributor 빌드 + warehouse 빌드를 동시에 운영하는 경우, 사용자별로 **단일 활성 빌드 셸**만 노출. `users.active_build_id` 컬럼으로 결정. | 메뉴 렌더 — `PermissionGuard` |
| `ACC-MULTI-03` | 같은 SKU (`chul_09`) 가 N 테넌트에 공유 배포된 경우, DB 컬럼 `hcode` 강제 필수 (행 격리). 모든 SELECT/UPDATE/DELETE 에 `WHERE hcode = :user.tenant_hcode` 자동 부착. | 데이터 — M4 결정에 합류 |
| `ACC-MULTI-04` | 같은 SKU 의 빌드 변형 (예: WH-FULL 의 `LABEL` vs `NEW` 변형) 은 `tenants.build_variant` 컬럼으로 식별. forced_hidden 메뉴와 추가 라이브러리 의존이 변형마다 다름. | 빌드 카탈로그 — [`analysis/welove_chul_builds.json`](../analysis/welove_chul_builds.json) |
| `ACC-MULTI-05` | `BLD-PUB-STD` ≡ `BLD-PUB-KBT` (바이트 동일) 같은 케이스는 카탈로그의 `binary_identical_groups` 에서 자동 검출 → RBAC 매트릭스의 source_builds 컬럼에서 두 ID 를 항상 같은 셋으로 취급. | 카탈로그 빌드 시점 |

**의사결정 트리 (운영자 입장)**:

```
사용자가 로그인하면
  ├─ JWT 클레임으로 (tenant_id, account_family, build_role) 결정
  ├─ tenant ↔ build_id 매핑 조회 (1:N 가능)
  │    ├─ 단일 빌드 → 그 빌드의 메뉴 셸 + forced_hidden + license_keys 적용
  │    └─ 다중 빌드 → users.active_build_id 가 결정한 빌드만 노출
  └─ ACC-T* 매트릭스 + license_keys 교집합으로 메뉴 가시성 산출
```
