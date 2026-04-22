# 레이아웃 매핑: Sobo57 (기간별 입고내역서) — 모던 기간 리포트

DEC-028 의무 — DBGrid 컬럼·정렬·합계와 위젯 ID 를 1:1 보존.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu57/Sobo57.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu57/Sobo57.html) + `Sobo57.form.json` + `Sobo57.tree.json`
- 화면 카드: [`analysis/screen_cards/Sobo57.md`](../screen_cards/Sobo57.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu57.dfm`](../../legacy_delphi_source/legacy_source/Subu57.dfm) — 41 위젯, DBGrid 2개

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | (Panel001 류) | `<section data-legacy-id="Panel001">` | **시작일~종료일** + 출판사·입고처 필터 |
| 좌측 그리드 | `DBGrid101` | `<DataGrid data-legacy-id="DBGrid101">` | 출판사 단위 기간 집계 (11 컬럼) |
| 우측 그리드 | `DBGrid201` | `<DataGrid data-legacy-id="DBGrid201">` | 입고처 단위 기간 집계 (10 컬럼) |
| 액션 버튼 | (Button 류) | `<Toolbar>` | 조회 / 출력 (DEC-004 — 1차는 화면만) |

## 2. DBGrid101 (출판사 단위 기간 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `HCODE` | 출판사코드 | `hcode` | 좌, 그룹 키 |
| 2 | `HNAME` | 출판사명 | `hname` | 좌 |
| 3 | `GDATE` | 거래일자 | `gdate` (date) | 좌 |
| 4 | `GCODE` | 코드 | `gcode` | 좌 |
| 5 | `GNAME` | 입고처명 | `gname` | 좌 |
| 6 | `IDNUM` | No | `idnum` | 우 |
| 7 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 8 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 9 | `BNAME` | 도서명 | `bname` | 좌 |
| 10 | `GSQUT` | 수량 | `gsqut` (number) | 우, **합계** |
| 11 | `GDANG` | 단가 | `gdang` (number) | 우 |

## 3. DBGrid201 (입고처 단위 기간 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GDATE` | 거래일자 | `gdate` | 좌, 그룹 키 |
| 2 | `GCODE` | 코드 | `gcode` | 좌 |
| 3 | `GNAME` | 입고처명 | `gname` | 좌 |
| 4 | `IDNUM` | No | `idnum` | 우 |
| 5 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 6 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 7 | `BNAME` | 도서명 | `bname` | 좌 |
| 8 | `GSQUT` | 수량 | `gsqut` | 우, **합계** |
| 9 | `GDANG` | 단가 | `gdang` | 우 |
| 10 | `GRAT1` | 비율 | `grat1` | 우 |
| 11 | `GSSUM` | 금액 | `gssum` | 우, **합계** |

> Sobo54 와 동일 컬럼 패턴이지만 그룹 키가 출판사(HCODE)+거래일자(GDATE) 또는 거래일자(GDATE) — Sobo54 (일별) 와 차이는 **검색 시작일~종료일 범위** 뿐. SQL 은 BETWEEN 으로 변경.

## 4. 이벤트 매핑

| dfm | 모던 핸들러 | 역할 |
| --- | --- | --- |
| `FormActivate` | useEffect mount | 시작일=이번달1일, 종료일=오늘 디폴트 |
| 시작/종료 일자 변경 | `onChange` | 그리드 양쪽 동기 새로 fetch |
| 조회 버튼 | `onClick` | GET `/api/v1/inbound/reports/period?from=...&to=...` |

## 5. 회귀 가드 체크리스트

- [x] DBGrid101 11 컬럼 + DBGrid201 11 컬럼(합계 포함) 모두 모던 grid 정의 — `app/(app)/inbound/reports/period/page.tsx` (C3 phase2).
- [x] 합계 행: `gsqut`/`gssum` 두 그리드 모두 표시.
- [x] `data-legacy-id="Sobo57.DBGrid101"`, `data-legacy-id="Sobo57.DBGrid201"` + 컬럼별 `Sobo57.DBGrid***.${FIELD}` 부착.
- [x] 시작/종료 일자 양방향 검증 (시작 ≤ 종료) — 클라이언트 가드.
- [x] `DataGridPager` (DEC-033(g)) + `useListSession` (DEC-055) 적용 — 페이지/limit/시작/종료 일자가 sessionStorage 에 보존.
- [x] **합계 분리**: 화면 상단 「전체 합계」는 페이지 무관 전역 SUM (`totals`), 각 그리드 직하 「현재 페이지 합」은 페이지 행 SUM 으로 분리 표시.
- [x] **이중 그리드 동기 롤**: 두 그리드(by_publisher / by_vendor) 가 단일 페이저 1개로 동시 진행. `page.has_more = pub.has_more OR ven.has_more` (한 그리드라도 다음 페이지가 있으면 True). `page.total` 은 진척도 ceiling — 정확한 그룹 수가 아닌 `offset + visible (+1 if has_more)`.
- [x] 빈 집합 (기간 내 입고 없음) → 200 + 빈 배열 + `totals={qty:0,amount:0}` (DEC-033 mysql3 빈집합 정합).

## 6. 참조

- DEC-028, DEC-004, DEC-033 (mysql3 호환 + 페이저 표준), DEC-055 (`useListSession`).
- contract: `migration/contracts/inbound_receipt.yaml`
  - 엔드포인트: `GET /api/v1/inbound/reports/period` — `data_access` SQL-IN-11 (PERIOD REPORT).
  - 회귀 팩: `migration/test-cases/_phase2_addendum.json` `endpoints.reports.daily_period` (TC-IN-RPT-004~006 / AC-IN-RPT-4~6).

## 7. Phase2 deltas (의도적 차이 — 레거시 대비)

| ID | 항목 | 레거시 | 모던 (phase2) | 사유 |
| --- | --- | --- | --- | --- |
| Δ-IN-RPT-1 | 행 적재 | 기간 매칭 전량 로드 | 서버 페이징 (limit/offset, 기본 100·최대 500) | 기간 길이에 비례한 행 수 폭증 대비 (DEC-033(g)). |
| Δ-IN-RPT-2 | 합계 출처 | DBGrid 자체 footer (현재 표시 행 합) | `totals` 별도 SUM (전역) + 그리드 footer (페이지 합) 병행 | 페이지 변경 시 합계가 흔들리지 않도록 분리. |
| Δ-IN-RPT-3 | 페이저 단위 | 그리드별 분리 가능 | **두 그리드 동기 롤** (단일 페이저) | UI 단순화 + 재귀 버그 방지. Sobo54 와 동일. |
| Δ-IN-RPT-4 | mysql3 LIMIT 문법 | 단일 LIMIT 절 | `apply_limit_offset_syntax` + `limit_offset_bind` (3.23 호환) | 4대 DB SKIP 환경에서도 200 보장 — 500 회귀 근본 제거. |
