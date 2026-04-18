# 레이아웃 매핑: Sobo61 (도서별 판매) — 모던 reports/book-sales 페이지

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 retrofit 산출물** (C6 phase1 동결 후 DEC-028 채택, HA-RET-01 두 번째 묶음).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu61/Sobo61.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu61/Sobo61.html) + `Sobo61.form.json` + `Sobo61.tree.json`
- **변형 폴더 부재** — `Subu61_*` 등 variant 디렉터리 0건.
- 화면 카드: [`analysis/screen_cards/Sobo61.md`](../screen_cards/Sobo61.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu61.dfm`](../../legacy_delphi_source/legacy_source/Subu61.dfm) (894행, EUC-KR)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu61.pas`](../../legacy_delphi_source/legacy_source/Subu61.pas) (Button101Click L288 — S1_Ssub GROUP BY + Sg_Csum 합계)
- 모던 라우트: [`reports/book-sales/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/reports/book-sales/page.tsx)
- 계약: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[4] BOOK_SALES

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo61` 은 **3 영역 화면** (top 검색, mid DBGrid101 도서별 합계, bottom DBGrid201 거래처별 분배 토글). 모던 C6 phase1 은 contract 결정에 따라 **단일 도서별 합계 그리드 (mid 만)** 로 단순화 — 거래처별 분배(bottom) 는 거래처판매(Sobo62) 라우트로 분리.

따라서 본 매핑은:

- **도서별 합계 그리드 + 검색 패널만** 의미 매핑 — `data-legacy-id` 부착.
- DBGrid201 (거래처별 분배), 본사출고제외 체크박스, 지점별검색 체크박스는 §6 out-of-scope (백엔드 scope 파라미터로 흡수).
- 모던 `<th>재고수/파지수/파지액</th>` 는 dfm 의 의미 변형 (Sg_Csum 보강) → §4 매핑 또는 §7 deltas.

## 2. dfm 영역 인벤토리 (Sobo61.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | 22 (Label101/102, Panel101~103, Button101/201/700/701/702, Edit101~108, CheckBox1/2, DateEdit1/2, dxButton1) | `book-sales/page.tsx` 검색 영역 (line 130~186) |
| 중단 도서별 합계 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101, 8 컬럼) | `book-sales/page.tsx` DataGrid (line 194~199) |
| 하단 거래처별 분배 그리드 | `Panel003` (TFlatPanel) | 2 | 1 (DBGrid201, 8 컬럼) | **out-of-scope** — 거래처별은 Sobo62 분리 |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | 3 | 5 (ProgressBar0/1, Panel008/009/010 — "레코드"/"검색진행") | **out-of-scope** — React `loading` 흡수 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/API 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 시작 | `<Input id="from" type="date">` (line 142~147) | input(from) — `data-legacy-id="Sobo61.Edit101"` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 끝 | `<Input id="to" type="date">` (line 149~155) | input(to) — `data-legacy-id="Sobo61.Edit102"` |
| 2 | `Edit107` | TFlatEdit (HIDDEN) | (보조) | **out-of-scope** | — | |
| 3 | `Edit108` | TFlatEdit | 출판사명 | **out-of-scope** | — | C6 1차 = hcode 단일 |
| 4 | `Edit103` | TFlatEdit (HIDDEN) | 도서코드 시작 | `<Input id="bcodeFrom">` (line 160~165) | input(bcodeFrom) — `data-legacy-id="Sobo61.Edit103"` |
| 5 | `Edit104` | TFlatEdit | 도서명 | **out-of-scope** | — | (1차는 코드 범위만) |
| 6 | `Edit105` | TFlatEdit (HIDDEN) | 도서코드 끝 | `<Input id="bcodeTo">` (line 167~173) | input(bcodeTo) — `data-legacy-id="Sobo61.Edit105"` |
| 7 | `Edit106` | TFlatEdit | (보조) | **out-of-scope** | — | |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` (line 141) | label(from) — `data-legacy-id="Sobo61.Panel101"` |
| 9 | `Panel103` | TFlatPanel | "출판사명" 라벨 | **out-of-scope** | — | |
| 10 | `Panel102` | TFlatPanel | "도 서 명" 라벨 | (모던: 도서명 라벨은 응답 그리드에 노출 — 검색 라벨은 bcode 위주) | — | §7 deltas |
| 11 | `Button101` | TFlatButton (HIDDEN, OnClick) | 조회(보조) | `<Button onClick=load>조회` (line 176~185) | button(조회) | dxButton1 동일 핸들러 |
| 12 | `Button201` | TFlatButton (HIDDEN) | 신규 | **out-of-scope** | — | 보고서는 read-only |
| 13 | `CheckBox1` | TFlatCheckBox ("지점별검색") | 지점 분배 | **out-of-scope** | — | scope 파라미터로 흡수 |
| 14 | `DateEdit1` | TDateEdit | 캘린더 시작 | (HTML5 date input) | — | §7 deltas |
| 15 | `DateEdit2` | TDateEdit | 캘린더 끝 | (HTML5 date input) | — | §7 deltas |
| 16 | `Button700` | TFlatButton | 캘린더 트리거 1 | (HTML5 picker) | — | |
| 17 | `Button701` | TFlatButton | 캘린더 트리거 2 | (HTML5 picker) | — | |
| 18 | `Button702` | TFlatButton | 캘린더 트리거 3 | (HTML5 picker) | — | |
| 19 | `CheckBox2` | TFlatCheckBox ("본사출고제외") | 필터 | **out-of-scope** | — | scope 파라미터로 흡수 |
| 20 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` (line 176~185) | button(조회) — `data-legacy-id="Sobo61.dxButton1"` (Button101 과 동일 핸들러) |
| (모던 신규) | — | — | hcode 입력 | `<Input id="hcode">` (line 133~138) | input(hcode) | dfm 은 본사 단일 가정 → 모던 명시 입력 |

> **TabOrder 보존**: 모던 검색 영역 키보드 흐름은 hcode → from → to → bcodeFrom → bcodeTo → 조회 순. dfm 의 일자 → 도서코드 흐름과 의미 일치.

## 4. 중단 그리드 매핑 (DBGrid101) — 도서별 GROUP BY

dfm `DBGrid101` 컬럼 8개 (도서별 GROUP BY 합계):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (book-sales/page.tsx) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 1 | `GNAME` | 도 서 명 | 명칭 | `<th>도서명</th>` (gname) | th(도서명) — `data-legacy-id="Sobo61.DBGrid101.GNAME"` |
| 2 | `GIQUT` | 입고수량 | SUM 입고 | `<th>입고수</th>` (giqut) | th(입고수) — `data-legacy-id="Sobo61.DBGrid101.GIQUT"` |
| 3 | `GOQUT` | 출고수량 | SUM 출고 | `<th>출고수</th>` (goqut) | th(출고수) — `data-legacy-id="Sobo61.DBGrid101.GOQUT"` |
| 4 | `GJQUT` | 증정수량 | SUM 증정 | `<th>재고수</th>` (gjqut) | th(재고수) — `data-legacy-id="Sobo61.DBGrid101.GJQUT"` |
| 5 | `GBQUT` | 반품수량 | SUM 반품 | `<th>반품수</th>` (gbqut) | th(반품수) — `data-legacy-id="Sobo61.DBGrid101.GBQUT"` |
| 6 | `GPQUT` | 폐기수량 | SUM 폐기 (Sg_Csum 보강) | `<th>파지수</th>` (gpqut) | th(파지수) — `data-legacy-id="Sobo61.DBGrid101.GPQUT"` |
| 7 | `GOSUM` | 출고금액 | SUM(Gssum) | `<th>출고액</th>` (gosum) | th(출고액) — `data-legacy-id="Sobo61.DBGrid101.GOSUM"` |
| 8 | `GBSUM` | 반품금액 | SUM 반품액 (Sg_Csum) | `<th>파지액</th>` (gpsum — 모던에서는 파지로 통칭) | th(파지액) — `data-legacy-id="Sobo61.DBGrid101.GBSUM"` |

모던 신규 컬럼 (§7 deltas):

- `<th>코드</th>` (gcode) — dfm 은 도서명만, 모던은 코드+명 둘 다 노출 (응답 row 의 gcode).

> 의미 차이: dfm = "도서별 단순 SUM 한 행", 모던 = "동일 + Sg_Csum 보강 (gpsum) + DataGridPager". 컬럼 매핑은 8개 중 7개 직접 매핑 가능.

## 5. (Sobo21 한정) 하단 입력·메모 패널

본 폼(Sobo61)에 해당 없음 — 보고서는 read-only. dfm Panel003(DBGrid201) 은 §6 out-of-scope.

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 검색 | Edit104/106/107/108, Panel102/103 | 도서명/출판사명 검색 후속 |
| 분배 그리드 | DBGrid201 (Panel003 내, 8 컬럼) | 거래처별 분배 = Sobo62 라우트 |
| 토글 | CheckBox1/2 (지점별검색/본사출고제외) | scope 파라미터로 흡수 |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` 흡수 |
| 신규 | Button201 (HIDDEN) | 보고서는 read-only |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | hcode 입력 | `book-sales/page.tsx` line 133 | dfm 은 본사 단일 가정 |
| 모던 신규 | bcodeFrom/bcodeTo 노출 | line 160, 167 | dfm Edit103/105 (HIDDEN) 를 노출 |
| 모던 신규 | DataGridPager | line 201~209 | DEC-024 페이지네이션 |
| 모던 신규 | gcode 컬럼 | columns line 110 | 도서코드 명시 노출 |
| dfm out-of-scope | DBGrid201 거래처 분배 8컬럼 | — | Sobo62 라우트로 분리 |
| dfm out-of-scope | 지점별검색/본사출고제외 체크박스 | — | scope 파라미터로 흡수 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 위치 | 비고 |
| --- | --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load()` (hcode 있을 때) | line 100~107 | |
| `Button101Click` | `load()` | line 66~98 | dfm 은 GROUP BY + Sg_Csum 합계 |
| `dxButton1.OnClick` | `load()` (조회) | line 176~185 | Button101 과 동일 |
| `Edit101Change` / `Edit102Change` | `setDateFrom` / `setDateTo` | line 145, 153 | |
| `DateEdit1.OnAcceptDate` | (HTML5 native picker) | — | §7 deltas |
| `CheckBox1.OnKeyDown` | (없음 — scope 흡수) | — | §6 out-of-scope |
| `DBGrid201.OnTitleClick` | (없음 — 분배 그리드 미사용) | — | §6 out-of-scope |
| `DataSource1DataChange` | (자동 — React state 갱신) | | |

## 9. 변형 차이 (`Sobo61` 본 vs variant)

`legacy_source_root/Subu61*` inventory: **`Subu61_*` 등 variant 폴더 0건 — UI/로직 variant 자체가 없음.**

→ 본 매핑 노트 차원의 UI 차이 없음. contract `customer_variants` 섹션에 단언으로 기록 (T2 산출).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재.
  - 부착 대상 (~12개): `input(from)` `Sobo61.Edit101`, `input(to)` `Sobo61.Edit102`, `input(bcodeFrom)` `Sobo61.Edit103`, `input(bcodeTo)` `Sobo61.Edit105`, `label(from)` `Sobo61.Panel101`, `button(조회)` `Sobo61.dxButton1`, `th(도서명)` `Sobo61.DBGrid101.GNAME`, `th(입고수)` `Sobo61.DBGrid101.GIQUT`, `th(출고수)` `Sobo61.DBGrid101.GOQUT`, `th(재고수)` `Sobo61.DBGrid101.GJQUT`, `th(반품수)` `Sobo61.DBGrid101.GBQUT`, `th(파지수)` `Sobo61.DBGrid101.GPQUT`, `th(출고액)` `Sobo61.DBGrid101.GOSUM`, `th(파지액)` `Sobo61.DBGrid101.GBSUM`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (지점별검색 체크박스 등).
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: hcode → from → to → bcodeFrom → bcodeTo → 조회 순.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 값) 가 코드에 없음.

## 11. 참조

- DEC-016/017/018: 권한키/인쇄/바코드 후속.
- DEC-019: customer_variants 통합 정책.
- DEC-024: 페이지네이션 표준.
- DEC-028: dfm→html 산출물 영구 입력 동결.
- HA-RET-01: retrofit 백로그 — C2 완료, **C6 묶음(본 노트 포함) 완료**, C1·C9 잔여.
- 화면 카드: [`analysis/screen_cards/Sobo61.md`](../screen_cards/Sobo61.md)
- contract: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[4]
- 회귀 테스트: [`test/test_c6_inquiry_phase1.py`](../../test/test_c6_inquiry_phase1.py)
