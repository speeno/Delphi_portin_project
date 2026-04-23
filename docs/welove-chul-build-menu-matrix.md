# WeLove Chul 7-빌드 메뉴 합집합 매트릭스 (`MainMenu1`)

| 항목 | 내용 |
|------|------|
| 분석 일자 | 2026-04-24 |
| 근거 | [`analysis/welove_chul_builds.json`](../analysis/welove_chul_builds.json), [`analysis/welove_chul_menu_trees.json`](../analysis/welove_chul_menu_trees.json), [`analysis/welove_chul_menu_matrix.json`](../analysis/welove_chul_menu_matrix.json), [`analysis/welove_chul_menu_handlers.json`](../analysis/welove_chul_menu_handlers.json) |
| 추출 도구 | [`tools/build_chul_catalog.py`](../tools/build_chul_catalog.py), [`tools/extract_chul_menus.py`](../tools/extract_chul_menus.py) (CP949 강제 디코드 · 자격증명 미수집) |
| 인코딩 | DFM/PAS 내 한글 문자열은 **CP949** — 모든 read 는 `errors="replace"` |
| 비밀 정책 | [`docs/secrets-policy.md`](secrets-policy.md) `SEC-POL-CITE-01`. PAS 본문에 평문 DB 자격증명이 발견되었으나(`book_21_pw` 등 — `OQ-BLD-4` 참고) 본 문서·JSON 어디에도 인용하지 않음. |
| 선행 문서 | [`docs/welove-ftp-tongpan-chulpan-chul-menu-diff.md`](welove-ftp-tongpan-chulpan-chul-menu-diff.md) (표준 2 빌드 비교 — 본 매트릭스가 상위 문서로 합류) |

---

## 1. 빌드 7 종 한눈에

| 빌드 ID | 약칭 | App Caption | Config Uses | DFM/PAS MD5 동일군 | 상단 메뉴 | 출판사관리 | 메뉴보이기/감추기 | 추가 라이브러리 | 메모 |
|---|---|---|---|---|:-:|:-:|:-:|---|---|
| `BLD-DIST-STD` | D-STD | 총판관리프로그램 | Client02 | — | 6 | O | × | — | 표준 총판 템플릿 |
| `BLD-PUB-STD` | P-STD | 출판관리프로그램 | 홍길동 | **=P-KBT** | 7 | × | O | — | 표준 출판 템플릿 |
| `BLD-DIST-KBT` | D-KBT | 도서물류관리프로그램 | 한국도서유통 | — | 9 | O | × | `libmysql.dll` `midas.dll` | KBT 총판 — `택배관리` 단독 보유 |
| `BLD-PUB-KBT` | P-KBT | 출판관리프로그램 | 홍길동 | **=P-STD** | 7 | × | O | — | KBT 패키지 동봉 출판 — P-STD 와 바이트 동일 |
| `BLD-PUB-WAREHOUSE-WELOVE` | WH-WL | 도서물류관리프로그램 | 위러브 | — | 7 | O | × | `libmysql.dll` | 자체 물류 lite — `반품재고관리` 통합 |
| `BLD-PUB-WAREHOUSE-MS` | WH-MS | **도서관리프로그램** | MS북스 | — | 8 | O | × | `TSCLIB.dll` `libmysql.dll` | 자체 물류 full + 라벨 SDK |
| `BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW` | WH-BB | 도서물류관리프로그램 | 한국도서유통 | — | 8 | O | × | `libmysql.dll` | 자체 물류 full + 신규 폼군 + 다중 DB 디렉토리 |

**중복 검출** (`analysis/welove_chul_builds.json::binary_identical_groups`):
- `BLD-PUB-STD` ≡ `BLD-PUB-KBT` (`Chul.dfm`/`Chul.pas` MD5 일치) → **별도 변형 아님**. KBT 패키지가 표준 출판 빌드를 그대로 동봉. 본 매트릭스에서 두 컬럼은 항상 일치.

**동일 테넌트 다중 빌드** (`tenant_label_groups`):
- `Uses=한국도서유통` → `BLD-DIST-KBT` + `BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW` (총판 + 자체물류 출판 2 빌드 동시 존재) — 자세히는 §7
- `Uses=홍길동` → `BLD-PUB-STD` + `BLD-PUB-KBT` (sample placeholder)

---

## 2. 최상위 메뉴 막대 7 빌드 비교

전 빌드의 합집합 (✓ = 보유, 빈칸 = 없음):

| 캡션 | D-STD | P-STD | D-KBT | P-KBT | WH-WL | WH-MS | WH-BB |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 기초관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 통계관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 거래관리 | ✓ | ✓ |  | ✓ |  |  |  |
| 원장관리 | ✓ | ✓ |  | ✓ |  |  |  |
| 회계관리 | ✓ | ✓ |  | ✓ |  |  |  |
| 자료관리 | ✓ | ✓ |  | ✓ |  |  |  |
| 년/월(통계) |  | ✓ |  | ✓ |  |  |  |
| 출고관리 |  |  | ✓ |  | ✓ | ✓ | ✓ |
| 재고원장 |  |  | ✓ |  | ✓ | ✓ | ✓ |
| 발송비/입금관리 |  |  | ✓ |  | ✓ | ✓ | ✓ |
| 내역서관리 |  |  | ✓ |  | ✓ | ✓ | ✓ |
| 재고관리 |  |  | ✓ |  |  | ✓ | ✓ |
| 반품관리 |  |  | ✓ |  |  | ✓ | ✓ |
| 반품재고관리 |  |  |  |  | ✓ |  |  |
| 택배관리 |  |  | ✓ |  |  |  |  |

**3 가지 명확한 패턴군**:

1. **publisher 패턴 (P-STD/P-KBT)**: `기초/거래/원장/회계/자료/통계 (+년/월(통계))` 7 항목 — 출판사 자기 거래 관점.
2. **distributor + warehouse 패턴 (D-KBT/WH-WL/WH-MS/WH-BB)**: `출고/재고원장/(재고관리)/발송비/내역서/통계/(반품)/기초` 7~9 항목 — 물류 운영 관점.
3. **standard distributor (D-STD)**: 메뉴는 publisher 와 동일 6 항목이지만 `기초관리` 안에 출판사관리 포함 — 표준 총판 템플릿이 publisher 와 메뉴 셸을 공유하는 레거시.

**빌드 단독 메뉴 항목**:
- `D-KBT 단독`: `택배관리` (전체 6 하위 항목)
- `WH-WL 단독`: `반품재고관리` (전체 6 하위 항목, `반품관리` + `재고관리` 의 통합본)
- 그 외 모든 단독 항목은 §3~§7 에서 상세히.

---

## 3. 기초관리 하위 비교 (`기초관리/*`)

| 캡션 | D-STD | P-STD | D-KBT | P-KBT | WH-WL | WH-MS | WH-BB | 비고 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| 도서관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 공통 |
| 입고처관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 공통 |
| 특별관리 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 공통 |
| 환경설정 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 공통 |
| E&xit | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 공통 (종료) |
| 거래처관리 | ✓ | ✓ |  | ✓ |  |  |  | publisher 형 |
| 거래처관리-개별 |  |  | ✓ |  | ✓ | ✓ | ✓ | 자체물류·KBT-D 형 (분리) |
| 거래처관리-통합 |  |  | ✓ |  | ✓ | ✓ | ✓ | 자체물류·KBT-D 형 (분리) |
| 기타거래처 | ✓ | ✓ |  | ✓ |  |  |  | publisher 형 |
| 저자관리 | ✓ | ✓ |  | ✓ |  |  |  | publisher 형 |
| 출판사관리 | ✓ |  | ✓ |  | ✓ | ✓ | ✓ | distributor + warehouse 만 |
| 출판사관리(설정) |  |  | ✓ |  |  | ✓ |  | KBT-D + WH-MS |
| 출판사관리-택배 |  |  | ✓ |  |  |  |  | D-KBT 단독 |
| 출판사MMS(설정) |  |  | ✓ |  |  |  |  | D-KBT 단독 (MMS 발송 SaaS) |
| 출판사MMS(조회) |  |  | ✓ |  |  |  |  | D-KBT 단독 |
| 종당관리(도서) |  |  | ✓ |  |  | ✓ | ✓ | KBT-D + WH-MS/BB |
| 지역분류 |  |  |  |  | ✓ |  |  | WH-WL 단독 |
| 지역분류(시내+지방) |  |  | ✓ |  |  | ✓ | ✓ | KBT-D + WH-MS/BB (확장) |
| 도서관리(위치) |  |  |  |  |  | ✓ |  | WH-MS 단독 (창고 위치 추가) |
| 출고증정렬 |  |  | ✓ |  |  |  |  | D-KBT 단독 |
| 출고정지유무 |  |  |  |  |  |  | ✓ | WH-BB 단독 |
| 메뉴보이기 |  | ✓ |  | ✓ |  |  |  | publisher 만 — **실제 동작은 ToolBar 토글 (§5)** |
| 메뉴감추기 |  | ✓ |  | ✓ |  |  |  | publisher 만 — 동상 |

**해석**:
- "거래처관리" 의 **개별/통합 분리**는 `D-KBT + 모든 WH-*` 빌드 공통 → 다중 거래처(소속 출판사 또는 다중 매입처) 운영 모델의 시그니처.
- `출판사관리(설정)/(택배)/MMS` 는 **D-KBT 단독 또는 D-KBT + WH-MS** → 한국도서유통 총판 운영의 추가 SKU. 일반 warehouse 출판사 (WH-WL/WH-BB) 에는 부재.
- `메뉴보이기/감추기` 는 publisher (P-STD/KBT) 에만 존재하지만 §5 분석대로 **실제는 메뉴 권한 토글이 아니라 ToolBar 토글**.

---

## 4. 거래·원장·회계·자료·통계 vs 출고·재고·발송비·내역서 매핑

레거시 두 모델은 **동일 업무를 다른 메뉴 셸로 표현**:

| 업무 영역 | publisher 셸 (P-STD/P-KBT) | distributor·warehouse 셸 (D-KBT/WH-WL/WH-MS/WH-BB) |
|---|---|---|
| 입출고 거래 | `거래관리/{거래·기타·신간·원천징수·입고·제작}명세서/현황` | `출고관리/{거래·반품}명세서` + `출고관리/{출고접수·출고검증·출고택배·전송자료받기}` |
| 거래 원장 | `원장관리/{거래처·도서별}원장총괄·거래원장·기간별재고원장·기간별미수원장·도서별수불원장·담당자판매실적` | `재고원장/{도서별수불원장·기간별재고원장·기간별평균재고·출판사재고현황·재고및재고금액·기간별재고(세분)}` |
| 자료 (마감·회계) | `회계관리/*`, `자료관리/{원장변경·자료백업·자료삭제·재고변경·초기계정·초기미수·초기재고·코드변경·회계정리}` | publisher-only (warehouse 빌드는 없음 — 회계는 본사 책임) |
| 발송비 / 청구 | (없음) | `발송비/입금관리/{발송비·청구서·세금계산서·반품수거·입금관리·청구금액(년월)}` |
| 내역서 | (없음) | `내역서관리/{기간별·일별} {입고·출고·반품·택배}내역서` |
| 통계·수금 분석 | `통계관리/{거래처년말집계·거래처집계·...}` + `년/월(통계)/{거래처판매·도서별판매·년/월판매·...}` | `통계관리/{거래처년말집계·...}` |

**자체 물류 3 종 (WH-WL · WH-MS · WH-BB) 의 반품·재고 명칭 변형**:

| 분류 | WH-WL (lite) | WH-MS (full) | WH-BB (full + new) |
|---|---|---|---|
| 상단 메뉴 | `반품재고관리` 통합 1개 | `재고관리` + `반품관리` 2개 분리 | `재고관리` + `반품관리` 2개 분리 |
| 반품재고관리 (WL) → MS/BB | 6 하위 (`반품재고(입고)/(폐기)`, `반품재고입력-자체운영`, `반품재고현황-자체운영`, `재고변경(반품/정품재고)`) | `재고관리` 안으로 분산 | `재고관리` 안으로 분산 |
| 재고관리 / 반품관리 | 부재 | 10 + 5 항목 | 10 + 5 항목 |

→ ACC-T3-WAREHOUSE 의 sub-type 구분 결정 근거. 자세히 §6.

---

## 5. 폼 파일 존재 여부 (`*.pas` 폼군)

| 폼군 prefix | D-STD | P-STD | D-KBT | P-KBT | WH-WL | WH-MS | WH-BB | 의미 (잠정) |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `Subu*` | 61 | 77 | 89 | 77 | 3 | 1 | 71 | MDI 자식 폼 (메뉴→Subu) |
| `Tong*` | 8 | 12 | 8 | 12 |  |  | 9 | 통신·통계 보조 |
| `Seak*` | 9 | 10 | 11 | 10 |  |  | 10 | 검색 매스터 (잠정) |
| `Seek*` | 9 | 9 | 9 | 9 |  |  | 9 | 검색 보조 |
| `Seok*` |  | 3 | 7 | 4 |  |  | 6 | 분류·세부 |
| `Seep*` | 2 | 2 | 2 | 2 |  |  | 2 | 환경 페이지 |
| `Base*` | 1 | 1 | 1 | 1 |  |  | 1 | 공통 데이터 모듈 |
| `Smms*` |  |  | 4 |  |  |  |  | **D-KBT 단독** — MMS 발송 모듈 |
| `Exls*` |  |  | 2 |  |  |  |  | **D-KBT 단독** — 엑셀 변환 |

→ `analysis/welove_chul_builds.json::form_families` 카운트.

**관찰**:
- `WH-WL` 과 `WH-MS` 폴더는 `Subu*.pas` 가 매우 적음(3, 1) — 다른 폼은 동봉되지 않은 **빌드 산출물 디렉토리** (DCU 만 포함되거나, 외부 의존 컴포넌트로 동적 로드). `OQ-BLD-3` 의 SME 검증 대상.
- `WH-BB` 는 `Seak/Seek/Seok/Seep/Base` 28 폼을 보유 — `D-KBT` 와 유사한 풀 폼 셸 + 신규 모듈 가능성 (`OQ-BLD-6`).
- `Smms*`/`Exls*` 는 `D-KBT` 단독 → 한국도서유통 총판 운영 전용 모듈.

---

## 6. 자체 물류 3 종 정밀 비교 (WH-WL vs WH-MS vs WH-BB)

`ACC-T3-WAREHOUSE` 의 sub-type 분리 결정 근거.

| 차원 | WH-WL (위러브) | WH-MS (MS북스) | WH-BB (북앤북NEW) |
|---|---|---|---|
| 빌드 SKU (account_family) | `chul_09` (위러브1·2·3 + 교문사 4 테넌트 공유) | `book_21` (MS북스 단일) | `book_07` (북앤북·유앤북 2 테넌트 공유) |
| App Caption | 도서물류관리프로그램 | **도서관리프로그램** | 도서물류관리프로그램 |
| 상단 메뉴 수 | 7 | 8 | 8 |
| `재고관리` / `반품관리` 분리 | × (반품재고관리 통합 1개) | ✓ | ✓ |
| 추가 라이브러리 | `libmysql.dll` | `libmysql.dll` + **`TSCLIB.dll`** (TSC 라벨 프린터 SDK) | `libmysql.dll` |
| DB 백엔드 디렉토리 | `Remote/` | (없음) | **`Interbase/`, `Mysql/`, `Remote/`** |
| 폼 파일 갯수 | 3 (Subu26/27/30) | 1 (Subu30) | 108 (Subu71+ 신규 폼군 28) |
| 출판사관리 | ✓ | ✓ | ✓ |
| FormShow Menu hide | 없음 | **8 항목** (Menu300/400/500/600/700/800/208/308) | 없음 |

**제안 sub-type 매핑**:
- `ACC-T3-WAREHOUSE-LITE` ← `WH-WL` (반품재고 통합, 메뉴 7개)
- `ACC-T3-WAREHOUSE-FULL` ← `WH-MS` + `WH-BB` (재고/반품 분리, 메뉴 8개)
  - `FULL-LABEL` 변형 ← `WH-MS` 한정 (라벨 프린터 SDK)
  - `FULL-NEW` 변형 ← `WH-BB` 한정 (신규 폼군 + 다중 DB 디렉토리)

**WH-MS FormShow 의 startup-conditional menu hide** (8 항목):
`Menu300, Menu400, Menu500, Menu600, Menu700, Menu800, Menu208, Menu308 := False`

→ DFM 상으로는 8 메뉴 모두 정의되지만 런타임에 일부가 가려짐. 실제 노출 메뉴는 더 적을 가능성 — 이는 §7.2 `OQ-BLD-MS-1` 로 추적.

---

## 7. 동일 테넌트 다중 빌드 분석 (`Uses=한국도서유통`)

3 빌드가 한국도서유통 라벨을 공유:

| 빌드 | build_role | account_family | 관계 가설 |
|---|---|---|---|
| `BLD-DIST-KBT` | distributor | `book_kb` | 한국도서유통 본사 운영 (총판) |
| `BLD-PUB-KBT` | publisher | (placeholder) | KBT 패키지 동봉 표준 출판본 (P-STD 와 바이트 동일) — 운영 정본이 아닐 가능성 |
| `BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW` | warehouse_publisher | `book_07` | 북앤북NEW (자체 물류 출판사) — KBT 와 어떤 관계인지 `OQ-BLD-5` |

**DSN 라우팅 시사점**:
- `Uses` 라벨 단독으로는 **빌드/계정 SKU 를 결정할 수 없다** → DSN 라우팅 키는 `(tenant_label, account_family)` 또는 `(tenant_label, build_role)` 합성 키여야 함.
- DB 사용자 prefix (`book_kb`, `book_07`) 가 실 라우팅 키 → [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) 보강 (`DSN-DEC-06` 신설).

**`OQ-BLD-5` 핵심 질문**:
- 북앤북이 KBT 의 소속 출판사라면 → 1:N 출판사 등록·승인 흐름이 KBT-총판 의 책임 (ACC-T2-DIST 의 ONB-T2-PUB 트랙).
- 북앤북이 KBT 와 무관한 독립 출판사라면 → 자체 ONB-T3 트랙 + Config.Ini Uses 가 단순 잘못된 placeholder.
- DB 루트 매트릭스 ([`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json)) 상 `book_07` 은 **북앤북 + 유앤북** 2 테넌트 → KBT(book_kb) 와 별 DB → 후자(독립) 가설이 우세하지만 SME 확인 필요.

---

## 8. 합집합 매트릭스 본문

`analysis/welove_chul_menu_matrix.json::matrix.rows` 가 정본. 본 문서에는 §3·§4 에 발췌만 게재. 합계:

| 통계 | 값 |
|---|---|
| 합집합 메뉴 경로 (depth ≥ 1) | 180 |
| 빌드별 경로 수 | D-STD=57 / P-STD=67 / D-KBT=101 / P-KBT=67 / WH-WL=53 / WH-MS=83 / WH-BB=72 |
| 라이선스 키 (Seek_Uses) UNION | 62 (`F11`~`F78`) |
| FormShow startup menu hide | D-KBT=3 / WH-MS=8 / 그 외=0 |

라이선스 키 → 메뉴 매핑은 별도 사이클 (`OQ-LICENSE-KEY-MAP`) — 본 사이클 비커버.

---

## 9. 후속 액션 (`OQ-BLD-*` / 별 사이클)

- `OQ-BLD-1` — `Uses=홍길동` 가 P-STD/P-KBT 의 운영 정본인지 sample 인지
- `OQ-BLD-2` — ACC-T3-WAREHOUSE-LITE / -FULL sub-type 분리 채택 여부 (§6 기반 분리 권고)
- `OQ-BLD-3` — D-KBT 추가 폼 (Subu13_1, Subu59_3 등) 의 업무 모듈 SME 검증
- `OQ-BLD-4` — `WH-MS` 의 `TSCLIB.dll` 운영 필수성 + 웹 라벨 출력 대안 + "도서관리프로그램" 캡션 정체성
- `OQ-BLD-5` — `WH-BB` Uses=한국도서유통 의 의미 (북앤북-KBT 관계)
- `OQ-BLD-6` — `WH-BB` 신규 폼군 (`Seak/Seek/Seok/Seep/Base` 28폼) 업무 매핑
- `OQ-BLD-7` — `WH-BB` `Interbase/Mysql/Remote` 디렉토리 의미 (마이그레이션? 병행운영?)
- `OQ-LICENSE-KEY-MAP` (별 사이클) — `Seek_Uses('F##')` 62 키 → 메뉴/기능 매핑 표 작성. RBAC 권한 단위와 1:1 정합 검증.
- `OQ-BLD-MS-1` (신규) — WH-MS FormShow 의 `Menu300~800/208/308 := False` startup hide 의 실효 노출 메뉴 정정.

추적 ID 합류: [`docs/welove-tracking-ids-backlog.md`](welove-tracking-ids-backlog.md).
