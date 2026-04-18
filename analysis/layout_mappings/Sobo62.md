# 레이아웃 매핑: Sobo62 (거래처별 판매) — 모던 reports/customer-sales 페이지

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 retrofit 산출물** (C6 phase1 동결 후 DEC-028 채택, HA-RET-01 두 번째 묶음).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu62/Sobo62.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu62/Sobo62.html) + `Sobo62.form.json` + `Sobo62.tree.json`
- **변형 폴더 부재** — `Subu62_*` 등 variant 디렉터리 0건.
- 화면 카드: [`analysis/screen_cards/Sobo62.md`](../screen_cards/Sobo62.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu62.dfm`](../../legacy_delphi_source/legacy_source/Subu62.dfm) (903행, EUC-KR)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu62.pas`](../../legacy_delphi_source/legacy_source/Subu62.pas) (Button101Click L288 — S1_Ssub GROUP BY 거래처+지사)
- 모던 라우트: [`reports/customer-sales/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/reports/customer-sales/page.tsx)
- 계약: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[5] CUSTOMER_SALES

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo62` 는 **3 영역 화면** (top 검색, mid DBGrid101 거래처×도서 GROUP BY, bottom DBGrid201 도서 토글). 모던 C6 phase1 은 contract 결정에 따라 **단일 거래처×도서 그리드 (mid 만)** 로 단순화 — Sobo62 의 H1_Ssub 입출금 sub-query 결합은 D-INQ-4 → C5 정산 후속.

따라서 본 매핑은:

- **거래처×도서 GROUP BY 그리드 + 검색 패널만** 의미 매핑 — `data-legacy-id` 부착.
- DBGrid201 (도서 토글), 본사출고제외 / 지점별검색 체크박스, 출판사 검색은 §6 out-of-scope.
- 모던 `<th>수수/금액</th>` 등 합산 컬럼은 dfm DBGrid101 의 `GSUSU/GSSUM` 과 직접 매핑.

## 2. dfm 영역 인벤토리 (Sobo62.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | 22 (Label101/102, Panel101~103, Button101/201/700/701/702, Edit101~108, CheckBox1/2, DateEdit1/2, dxButton1) | `customer-sales/page.tsx` 검색 영역 (line 128~185) |
| 중단 거래처×도서 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101, 9 컬럼) | `customer-sales/page.tsx` DataGrid (line 193~198) |
| 하단 도서 토글 그리드 | `Panel003` (TFlatPanel) | 2 | 1 (DBGrid201, 8 컬럼) | **out-of-scope** — 도서별은 Sobo61 라우트로 분리 |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | 3 | 5 (ProgressBar0/1, Panel008/009/010 — "레코드"/"검색진행") | **out-of-scope** — React `loading` 흡수 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/API 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 시작 | `<Input id="from" type="date">` (line 140~145) | input(from) — `data-legacy-id="Sobo62.Edit101"` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 끝 | `<Input id="to" type="date">` (line 147~153) | input(to) — `data-legacy-id="Sobo62.Edit102"` |
| 2 | `Edit107` | TFlatEdit (HIDDEN) | (보조) | **out-of-scope** | — | |
| 3 | `Edit108` | TFlatEdit | 출판사명 | **out-of-scope** | — | C6 1차 = hcode 단일 |
| 4 | `Edit103` | TFlatEdit (HIDDEN) | 도서코드 시작 | `<Input id="gcodeFrom">` (line 158~163) | input(gcodeFrom) — `data-legacy-id="Sobo62.Edit103"` |
| 5 | `Edit105` | TFlatEdit (HIDDEN) | 도서코드 끝 | `<Input id="gcodeTo">` (line 165~171) | input(gcodeTo) — `data-legacy-id="Sobo62.Edit105"` |
| 6 | `Edit104` | TFlatEdit | 거래처명 | **out-of-scope** | — | (1차는 hcode 단위) |
| 7 | `Edit106` | TFlatEdit | (보조) | **out-of-scope** | — | |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` (line 139) | label(from) — `data-legacy-id="Sobo62.Panel101"` |
| 9 | `Panel103` | TFlatPanel | "출판사명" 라벨 | **out-of-scope** | — | |
| 10 | `Panel102` | TFlatPanel | "거래처명" 라벨 | `<Label htmlFor="hcode">거래처 hcode (선택)</Label>` (line 130) | label(hcode) — `data-legacy-id="Sobo62.Panel102"` |
| 11 | `Button101` | TFlatButton (HIDDEN, OnClick) | 조회(보조) | `<Button onClick=load>조회` (line 175~184) | button(조회) | dxButton1 동일 핸들러 |
| 12 | `Button201` | TFlatButton (HIDDEN) | 신규 | **out-of-scope** | — | 보고서는 read-only |
| 13 | `CheckBox1` | TFlatCheckBox ("지점별검색") | 지점 분배 | **out-of-scope** | — | scope 파라미터로 흡수 |
| 14 | `DateEdit1` | TDateEdit | 캘린더 시작 | (HTML5 date input) | — | §7 deltas |
| 15 | `DateEdit2` | TDateEdit | 캘린더 끝 | (HTML5 date input) | — | §7 deltas |
| 16 | `Button700` | TFlatButton | 캘린더 트리거 1 | (HTML5 picker) | — | |
| 17 | `Button701` | TFlatButton | 캘린더 트리거 2 | (HTML5 picker) | — | |
| 18 | `Button702` | TFlatButton | 캘린더 트리거 3 | (HTML5 picker) | — | |
| 19 | `CheckBox2` | TFlatCheckBox ("본사출고제외") | 필터 | **out-of-scope** | — | scope 파라미터로 흡수 |
| 20 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` (line 175~184) | button(조회) — `data-legacy-id="Sobo62.dxButton1"` (Button101 과 동일 핸들러) |
| (모던 신규) | — | — | hcode 입력 (선택) | `<Input id="hcode">` (line 131~138) | input(hcode) | dfm 은 거래처명으로 검색 — 모던은 hcode 명시 |

> **TabOrder 보존**: 모던 검색 영역 키보드 흐름은 hcode → from → to → gcodeFrom → gcodeTo → 조회 순. dfm 의 일자 → 도서코드 → 거래처명 흐름과 의미 일치 (모던은 거래처명 입력 미사용).

## 4. 중단 그리드 매핑 (DBGrid101) — 거래처×도서 GROUP BY

dfm `DBGrid101` 컬럼 9개 (거래처×도서 GROUP BY):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (customer-sales/page.tsx) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 1 | `HCODE` | 출판사 (Width=0 숨김) | 출판사 코드 | (모던 응답 `hcode` — 거래처코드) | th(거래처코드) — `data-legacy-id="Sobo62.DBGrid101.HCODE"` (의미 매핑: dfm 의 출판사 자리에 모던은 거래처) |
| 2 | `GNAME` | 거래처명 | 명칭 | (모던 1차 응답 hcode/gjisa/gcode/gname 노출 — gname 은 도서명) | — (deltas — dfm 의 거래처명은 모던에서 hcode 표시로 단순화) |
| 3 | `GOQUT` | 출고수량 | SUM 출고 | `<th>출고수</th>` (goqut) | th(출고수) — `data-legacy-id="Sobo62.DBGrid101.GOQUT"` |
| 4 | `GOSUM` | 출고금액 | SUM 출고액 | `<th>출고액</th>` (gosum) | th(출고액) — `data-legacy-id="Sobo62.DBGrid101.GOSUM"` |
| 5 | `GJQUT` | 증정수량 | SUM 증정 | `<th>재고수</th>` (gjqut) | th(재고수) — `data-legacy-id="Sobo62.DBGrid101.GJQUT"` |
| 6 | `GBQUT` | 반품수량 | SUM 반품 | `<th>반품수</th>` (gbqut) | th(반품수) — `data-legacy-id="Sobo62.DBGrid101.GBQUT"` |
| 7 | `GBSUM` | 반품금액 | SUM 반품액 | `<th>반품액</th>` (gbsum) | th(반품액) — `data-legacy-id="Sobo62.DBGrid101.GBSUM"` |
| 8 | `GSUSU` | 판매수량 | SUM 수수 (판매=출고-반품) | `<th>수수</th>` (gsusu) | th(수수) — `data-legacy-id="Sobo62.DBGrid101.GSUSU"` |
| 9 | `GSSUM` | 판매금액 | SUM 수수액 | `<th>금액</th>` (gssum) | th(금액) — `data-legacy-id="Sobo62.DBGrid101.GSSUM"` |

모던 신규 컬럼 (§7 deltas):

- `<th>지사</th>` (gjisa) — dfm GROUP BY 에 Gjisa 포함되나 별도 컬럼 미노출 → 모던은 명시 노출.
- `<th>도서코드</th>` (gcode) / `<th>도서명</th>` (gname) — dfm 은 거래처명 단일 노출 → 모던은 거래처×도서 행 단위.
- `<th>재고액</th>` (gjsum) — dfm 미노출.

> 의미 차이: dfm = "거래처별 합계 한 행 (Gname=거래처)", 모던 = "거래처×도서 단위 한 행 (gname=도서명)". `GNAME` 컬럼의 의미가 변경 (거래처명→도서명) 되었으므로 deltas 처리, 그 외 8개 합계 컬럼은 1:1 매핑.

## 5. (Sobo21 한정) 하단 입력·메모 패널

본 폼(Sobo62)에 해당 없음 — 보고서는 read-only. dfm Panel003(DBGrid201) 은 §6 out-of-scope.

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 검색 | Edit104/106/107/108, Panel103 | 거래처명/출판사명 검색 후속 |
| 토글 그리드 | DBGrid201 (Panel003 내, 8 컬럼) | 도서 토글 = Sobo61 라우트로 분리 |
| 토글 | CheckBox1/2 (지점별검색/본사출고제외) | scope 파라미터로 흡수 |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` 흡수 |
| 정산 sub-query | H1_Ssub 입출금 결합 | D-INQ-4 → C5 정산 후속 |
| 신규 | Button201 (HIDDEN) | 보고서는 read-only |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | hcode 입력 (선택) | `customer-sales/page.tsx` line 131 | dfm 은 거래처명 검색 — 모던은 hcode 명시 |
| 모던 신규 | gcodeFrom/gcodeTo 노출 | line 158, 165 | dfm Edit103/105 (HIDDEN) 를 노출 |
| 모던 신규 | DataGridPager | line 200~208 | DEC-024 페이지네이션 |
| 모던 신규 | 지사 컬럼 (gjisa) | columns line 106 | dfm GROUP BY 에 포함되나 미노출 → 명시 노출 |
| 모던 신규 | 도서코드/도서명 컬럼 | columns line 107~108 | dfm 은 거래처 단위 한 행 → 모던은 거래처×도서 |
| 모던 신규 | 재고액 컬럼 (gjsum) | columns line 114 | dfm 미노출 |
| dfm out-of-scope | DBGrid201 도서 토글 8컬럼 | — | Sobo61 라우트로 분리 |
| dfm out-of-scope | 지점별검색/본사출고제외 체크박스 | — | scope 파라미터로 흡수 |
| dfm out-of-scope | H1_Ssub 입출금 sub-query | — | C5 정산 (D-INQ-4) |
| dfm 의미변형 | GNAME (거래처명 → 도서명) | columns line 108 | 모던 GROUP BY 단위가 거래처×도서 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 위치 | 비고 |
| --- | --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load()` | line 99~102 | hcode 선택 시 빈 hcode 도 동작 (전체) |
| `Button101Click` | `load()` | line 67~93 | dfm 은 GROUP BY 거래처+도서 |
| `dxButton1.OnClick` | `load()` (조회) | line 175~184 | Button101 과 동일 |
| `Edit101Change` / `Edit102Change` | `setDateFrom` / `setDateTo` | line 143, 151 | |
| `DateEdit1.OnAcceptDate` | (HTML5 native picker) | — | §7 deltas |
| `CheckBox1.OnKeyDown` | (없음 — scope 흡수) | — | §6 out-of-scope |
| `DBGrid201.OnTitleClick` | (없음 — 도서 토글 미사용) | — | §6 out-of-scope |
| `DataSource1DataChange` | (자동 — React state 갱신) | | |

## 9. 변형 차이 (`Sobo62` 본 vs variant)

`legacy_source_root/Subu62*` inventory: **`Subu62_*` 등 variant 폴더 0건 — UI/로직 variant 자체가 없음.**

→ 본 매핑 노트 차원의 UI 차이 없음. contract `customer_variants` 섹션에 단언으로 기록 (T2 산출).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재.
  - 부착 대상 (~13개): `input(from)` `Sobo62.Edit101`, `input(to)` `Sobo62.Edit102`, `input(gcodeFrom)` `Sobo62.Edit103`, `input(gcodeTo)` `Sobo62.Edit105`, `label(from)` `Sobo62.Panel101`, `label(hcode)` `Sobo62.Panel102`, `button(조회)` `Sobo62.dxButton1`, `th(거래처코드)` `Sobo62.DBGrid101.HCODE`, `th(출고수)` `Sobo62.DBGrid101.GOQUT`, `th(출고액)` `Sobo62.DBGrid101.GOSUM`, `th(재고수)` `Sobo62.DBGrid101.GJQUT`, `th(반품수)` `Sobo62.DBGrid101.GBQUT`, `th(반품액)` `Sobo62.DBGrid101.GBSUM`, `th(수수)` `Sobo62.DBGrid101.GSUSU`, `th(금액)` `Sobo62.DBGrid101.GSSUM`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (지점별검색 체크박스, H1_Ssub 정산 등).
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: hcode → from → to → gcodeFrom → gcodeTo → 조회 순.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 값) 가 코드에 없음.

## 11. 참조

- DEC-016/017/018: 권한키/인쇄/바코드 후속.
- DEC-019: customer_variants 통합 정책.
- DEC-024: 페이지네이션 표준.
- DEC-028: dfm→html 산출물 영구 입력 동결.
- HA-RET-01: retrofit 백로그 — C2 완료, **C6 묶음(본 노트 포함) 완료**, C1·C9 잔여.
- 화면 카드: [`analysis/screen_cards/Sobo62.md`](../screen_cards/Sobo62.md)
- contract: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[5]
- 회귀 테스트: [`test/test_c6_inquiry_phase1.py`](../../test/test_c6_inquiry_phase1.py)
