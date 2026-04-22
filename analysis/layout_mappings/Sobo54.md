# 레이아웃 매핑: Sobo54 (일별 입고내역서) — 모던 일별 리포트

DEC-028 의무 — DBGrid 컬럼·정렬·합계와 위젯 ID·TabOrder 를 1:1 보존.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu54/Sobo54.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu54/Sobo54.html) + `Sobo54.form.json` + `Sobo54.tree.json`
- 화면 카드: [`analysis/screen_cards/Sobo54.md`](../screen_cards/Sobo54.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu54.dfm`](../../legacy_delphi_source/legacy_source/Subu54.dfm) — 40 위젯, DBGrid 2개

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | (Panel001 류) | `<section data-legacy-id="Panel001">` | 거래일자(시작/종료) 단일일자 + 출판사/입고처 |
| 좌측 그리드 | `DBGrid101` | `<DataGrid data-legacy-id="DBGrid101">` | 출판사 단위 집계 (11 컬럼) |
| 우측 그리드 | `DBGrid201` | `<DataGrid data-legacy-id="DBGrid201">` | 입고처 단위 집계 (10 컬럼) |
| 액션 버튼 | (Button 류) | `<Toolbar>` | 조회 / 출력 (인쇄는 DEC-004 — 1차는 화면만) |

## 2. DBGrid101 (출판사 단위 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GDATE` | 거래일자 | `gdate` (date) | 좌, 그룹 키 |
| 2 | `HCODE` | 출판사코드 | `hcode` (string) | 좌, 그룹 키 |
| 3 | `HNAME` | 출판사명 | `hname` (string) | 좌 |
| 4 | `GCODE` | 코드 (입고처) | `gcode` | 좌 |
| 5 | `GNAME` | 입고처명 | `gname` | 좌 |
| 6 | `IDNUM` | No | `idnum` | 우 |
| 7 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 8 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 9 | `BNAME` | 도서명 | `bname` | 좌 |
| 10 | `GSQUT` | 수량 | `gsqut` (number) | 우, **합계** |
| 11 | `GDANG` | 단가 | `gdang` (number) | 우 |

## 3. DBGrid201 (입고처 단위 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GCODE` | 코드 | `gcode` | 좌, 그룹 키 |
| 2 | `GNAME` | 입고처명 | `gname` | 좌 |
| 3 | `IDNUM` | No | `idnum` | 우 |
| 4 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 5 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 6 | `BNAME` | 도서명 | `bname` | 좌 |
| 7 | `GSQUT` | 수량 | `gsqut` | 우, **합계** |
| 8 | `GDANG` | 단가 | `gdang` | 우 |
| 9 | `GRAT1` | 비율 | `grat1` | 우 |
| 10 | `GSSUM` | 금액 | `gssum` | 우, **합계** |

> **합계** = `gsqut`, `gssum` footer 합계. 컬럼 순서·라벨 dfm 그대로 보존.

## 4. 이벤트 매핑

| dfm | 모던 핸들러 | 역할 |
| --- | --- | --- |
| `FormActivate` | useEffect mount | 오늘 일자 디폴트 |
| 검색 일자 변경 | `onChange` | 그리드 양쪽 동기 새로 fetch |
| 조회 버튼 | `onClick` | GET `/api/v1/inbound/reports/daily?gdate=...` |
| 출력 버튼 | `onClick` (Phase 2) | DEC-004 인쇄 — 1차는 disabled 또는 브라우저 인쇄 |

## 5. 회귀 가드 체크리스트

- [x] DBGrid101 11 컬럼 + DBGrid201 10 컬럼 모두 모던 grid 정의에 존재 — `app/(app)/inbound/reports/daily/page.tsx` (C3 phase2).
- [x] 합계 행: `gsqut`/`gssum` footer 합계 표시 (그리드 직하 totals 영역).
- [x] `data-legacy-id="Sobo54.DBGrid101"`, `data-legacy-id="Sobo54.DBGrid201"` + 컬럼별 `Sobo54.DBGrid***.${FIELD}` 부착.
- [x] 검색 일자 변경 후 「조회」 클릭 시 두 그리드 동시 새로고침.
- [x] `DataGridPager` (DEC-033(g)) + `useListSession` (DEC-055) 적용 — 페이지/limit/일자가 sessionStorage 에 보존.
- [x] **합계 분리**: 화면 상단 「전체 합계」는 페이지 무관 전역 SUM (`totals`), 각 그리드 직하 「현재 페이지 합」은 페이지 행 SUM 으로 분리 표시.
- [x] **이중 그리드 동기 롤**: 두 그리드(by_publisher / by_vendor) 가 단일 페이저 1개로 동시 진행. `page.has_more = pub.has_more OR ven.has_more`. `page.total` 은 진척도 ceiling (정확한 그룹 수 아님) — `count_grouped` 대신 `LIMIT+1` has_more 패턴으로 30s 타임아웃 회피 (DEC-033(g) 대용량 변형).

## 6. 참조

- DEC-028 (dfm 영구 입력), DEC-004 (인쇄 1차 보류), DEC-033(g) (페이저 표준), DEC-055 (`useListSession`).
- contract: `migration/contracts/inbound_receipt.yaml`
  - 엔드포인트: `GET /api/v1/inbound/reports/daily` — `data_access` SQL-IN-10 (DAILY REPORT).
  - 회귀 팩: `migration/test-cases/_phase2_addendum.json` `endpoints.reports.daily_period` (TC-IN-RPT-001~003 / AC-IN-RPT-1~3).

## 7. Phase2 deltas (의도적 차이 — 레거시 대비)

| ID | 항목 | 레거시 | 모던 (phase2) | 사유 |
| --- | --- | --- | --- | --- |
| Δ-IN-RPT-1 | 행 적재 | 일자 매칭 전량 로드 | 서버 페이징 (limit/offset, 기본 100·최대 500) | 행 수 폭증 대비 (DEC-033(g)). |
| Δ-IN-RPT-2 | 합계 출처 | DBGrid 자체 footer (현재 표시 행 합) | `totals` 별도 SUM (전역) + 그리드 footer (페이지 합) 병행 | 페이지 변경 시 합계가 흔들리지 않도록 분리. |
| Δ-IN-RPT-3 | 페이저 단위 | 그리드별 분리 가능 | **두 그리드 동기 롤** (단일 페이저) | 레거시는 동일 조건 동시 갱신 — UI 단순화 + 재귀 버그 방지. |
