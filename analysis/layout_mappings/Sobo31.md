# 레이아웃 매핑: Sobo31 (도서별 수불원장) — 모던 inventory/ledger 페이지

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 retrofit 산출물** (C6 phase1 동결 후 DEC-028 채택, HA-RET-01 두 번째 묶음).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu31/Sobo31.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu31/Sobo31.html) + `Sobo31.form.json` + `Sobo31.tree.json`
- **변형 폴더 부재** — `Subu31_*` 등 variant 디렉터리 0건.
- 화면 카드: [`analysis/screen_cards/Sobo31.md`](../screen_cards/Sobo31.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu31.dfm`](../../legacy_delphi_source/legacy_source/Subu31.dfm) (882행, EUC-KR)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu31.pas`](../../legacy_delphi_source/legacy_source/Subu31.pas) (Button101Click L280 → Button102Click L290 일반 / Button103Click 변형)
- 모던 라우트: [`inventory/ledger/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/inventory/ledger/page.tsx)
- 계약: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[3] LEDGER

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo31` 은 **3 영역 화면** (top 검색, mid DBGrid101 시계열, bottom DBGrid201 거래처별 분배). 모던 C6 phase1 은 contract 결정에 따라 **단일 시계열 그리드 (mid 만)** 로 단순화 — 거래처별 분배(bottom) 는 C5 정산 후속.

따라서 본 매핑은:

- **시계열 그리드 + 검색 패널만** 의미 매핑 — `data-legacy-id` 부착.
- DBGrid201 (거래처별 분배), 본사/지점 토글, 신간 라디오 등은 §6 out-of-scope.
- 모던 `<th>입고액/출고액/재고액</th>` 등 금액 컬럼은 dfm 시계열 그리드에 없음 → §7 deltas.

## 2. dfm 영역 인벤토리 (Sobo31.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | 21 (Label101/102, Panel101~105, Button101/201/700/701, Edit101~108, DateEdit1/2, dxButton1) | `inventory/ledger/page.tsx` 검색 영역 (line 125~177) |
| 중단 시계열 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101, 10 컬럼) | `inventory/ledger/page.tsx` DataGrid (line 191~197) |
| 하단 거래처별 분배 그리드 | `Panel003` (TFlatPanel) | 2 | 1 (DBGrid201, 9 컬럼) | **out-of-scope** — 거래처 분배는 C5 정산 |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | 3 | 5 (ProgressBar0/1, Panel008/009/010 — "레코드"/"검색진행") | **out-of-scope** — React `loading` 으로 흡수 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/API 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 시작 (mask) | `<Input id="from" type="date">` (line 156~161) | input(from) | 의미 일치 |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 끝 | `<Input id="to" type="date">` (line 163~169) | input(to) | dfm 단일 → 모던도 범위 직접 매핑 |
| 2 | `Edit107` | TFlatEdit (HIDDEN) | (보조 코드) | **out-of-scope** | — | |
| 3 | `Edit108` | TFlatEdit | 출판사명 | **out-of-scope** | — | C6 1차 = hcode 단일 |
| 4 | `Edit106` | TFlatEdit | 도서명/검색어 | (모던 hcode/bcode 와 의미 다름) | — | §7 deltas — 1차 미사용 |
| 5 | `Edit104` | TFlatEdit | 도 서 명 | **out-of-scope** | — | 도서명 검색은 후속 (1차는 bcode 직접) |
| 6 | `Edit103` | TFlatEdit | 도서코드 | `<Input id="bcode">` (line 137~142) | input(bcode) — `data-legacy-id="Sobo31.Edit103"` |
| 7 | `Edit105` | TFlatEdit (HIDDEN) | 도서코드 끝 | `<Input id="bcodeTo">` (line 146~151) | input(bcodeTo) — `data-legacy-id="Sobo31.Edit105"` |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` (line 155) | label(from) — `data-legacy-id="Sobo31.Panel101"` |
| 9 | `Panel105` | TFlatPanel | "출판사명" 라벨 | **out-of-scope** | — | |
| 10 | `Panel104` | TFlatPanel | "정     가" 라벨 | **out-of-scope** | — | |
| 11 | `Panel103` | TFlatPanel | "도 서 명" 라벨 | **out-of-scope** | — | (1차는 bcode 단위) |
| 12 | `Panel102` | TFlatPanel | "도서코드" 라벨 | `<Label htmlFor="bcode">도서코드 시작 *</Label>` (line 136) | label(bcode) — `data-legacy-id="Sobo31.Panel102"` |
| 13 | `Button101` | TFlatButton (Visible=false, OnClick `Button101Click` → 102/103 분기) | 조회(분기) | `<Button onClick=load>조회` (line 171~176) | button(조회) | 분기는 백엔드 흡수 |
| 14 | `Button201` | TFlatButton (HIDDEN) | 신규 | **out-of-scope** | — | 수불원장은 read-only |
| 15 | `DateEdit1` | TDateEdit | 캘린더 시작 | (HTML5 date input 내장) | — | §7 deltas |
| 16 | `DateEdit2` | TDateEdit | 캘린더 끝 | (HTML5 date input 내장) | — | §7 deltas |
| 17 | `Button700` | TFlatButton | 캘린더 트리거 1 | (HTML5 picker 내장) | — | |
| 18 | `Button701` | TFlatButton | 캘린더 트리거 2 | (HTML5 picker 내장) | — | |
| 19 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` (line 171~176) | button(조회) — `data-legacy-id="Sobo31.dxButton1"` (Button101 과 동일 핸들러) |
| (모던 신규) | — | — | hcode 입력 | `<Input id="hcode">` (line 128~133) | input(hcode) | dfm 은 거래처 hcode 를 본사 단일로 가정 — 모던은 명시 입력 |

> **TabOrder 보존**: 모던 검색 영역의 키보드 흐름은 hcode → bcode → bcodeTo → from → to → 조회 순. dfm 의 TabOrder 0/1 (일자) → 6/7 (도서코드) 와 의미 흐름 일치.

## 4. 중단 그리드 매핑 (DBGrid101) — 시계열 컬럼 매핑

dfm `DBGrid101` 컬럼 10개 (시계열 입출고 단순 누적):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (ledger/page.tsx) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 1 | `GDATE` | 거래일자 | 일자 | `<th>일자</th>` (key gdate) | th(일자) — `data-legacy-id="Sobo31.DBGrid101.GDATE"` |
| 2 | `GIQUT` | 입고 | 수량 | `<th>입고수</th>` (giqut) | th(입고수) — `data-legacy-id="Sobo31.DBGrid101.GIQUT"` |
| 3 | `GISUM` | 반입 | (반입 별도 — 모던에서는 입고에 통합) | (없음 — 입고수에 흡수) | — (deltas) |
| 4 | `GOQUT` | 출고 | 수량 | `<th>출고수</th>` (goqut) | th(출고수) — `data-legacy-id="Sobo31.DBGrid101.GOQUT"` |
| 5 | `GJQUT` | 증정 | 수량 | `<th>재고수</th>` (gjqut) | th(재고수) — `data-legacy-id="Sobo31.DBGrid101.GJQUT"` |
| 6 | `GBQUT` | 반품 | 수량 | `<th>반품수</th>` (gbqut) | th(반품수) — `data-legacy-id="Sobo31.DBGrid101.GBQUT"` |
| 7 | `GPQUT` | 폐기 | 수량 | `<th>파지수</th>` (gpqut) | th(파지수) — `data-legacy-id="Sobo31.DBGrid101.GPQUT"` |
| 8 | `GSQUT` | 변경 | (조정) | (없음 — 1차 deltas) | — |
| 9 | `GSUMY` | 현재고 | 잔고 | (모던 응답 `gjqut` 누적) | — (deltas — 의미 통합) |
| 10 | `GSSUM` | 재고(반) | 잔고(반품 분리) | (없음) | — |

모던 신규 컬럼 (§7 deltas):

- `<th>코드</th>` (gcode), `<th>도서명</th>` (gname) — dfm 은 검색 패널의 도서코드 단일 → 모던은 응답 행에 노출.
- `<th>입고액</th>` (gisum), `<th>출고액</th>` (gosum), `<th>재고액</th>` (gjsum) — dfm DBGrid101 은 수량만, 모던은 금액 노출.

> 의미 차이: dfm DBGrid101 = "단일 도서의 시계열 수량 흐름". 모던 = "동일 + 금액 + 다중 도서(범위) 행 표시". 수량 컬럼만 1:1 의미 매핑 → 부착, 금액·코드/명은 deltas.

## 5. (Sobo21 한정) 하단 입력·메모 패널

본 폼(Sobo31)에 해당 없음 — 수불원장은 read-only. dfm Panel003(DBGrid201) 은 §6 out-of-scope.

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 검색 | Edit104/106/108, Panel103/104/105 | 도서명/출판사명/정가 검색은 후속 |
| 분배 그리드 | DBGrid201 (Panel003 내, 9 컬럼) | 거래처별 분배 = C5 정산 후속 (D-INQ-4) |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` 흡수 |
| 신규 | Button201 (HIDDEN) | 수불원장은 read-only |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | hcode 입력 | `ledger/page.tsx` line 128 | dfm 은 본사 단일 가정 — 모던은 거래처/지사 명시 |
| 모던 신규 | 도서코드 끝 (bcodeTo) input | line 146 | dfm 의 Edit105 (HIDDEN) 를 노출 — 의미 매핑 가능 |
| 모던 신규 | "이월 기준일" 표시 | line 185~189 | dfm 은 별도 표시 없음 (백엔드 opening_date 응답) |
| 모던 신규 | 금액 컬럼 3종 (입고/출고/재고액) | DataGrid columns line 109~111 | dfm 은 수량만 |
| dfm out-of-scope | DBGrid201 거래처별 분배 9컬럼 | — | C5 정산 |
| dfm out-of-scope | 출판사명/정가 검색 | — | 후속 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 위치 | 비고 |
| --- | --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → setError(null) | line 92~94 | 자동 호출 없음 (hcode/bcode 필수) |
| `Button101Click` (분기) | `load()` | line 61~90 | 분기는 백엔드 SQL 분기로 흡수 |
| `dxButton1.OnClick` | `load()` (조회) | line 171~176 | Button101 과 동일 |
| `Edit101Change` / `Edit102Change` | `setDateFrom` / `setDateTo` | line 159, 167 | |
| `DateEdit1.OnAcceptDate` | (HTML5 native picker) | — | §7 deltas |
| `DataSource1DataChange` | (자동 — React state 갱신) | | |

## 9. 변형 차이 (`Sobo31` 본 vs variant)

`legacy_source_root/Subu31*` inventory: **`Subu31_*` 등 variant 폴더 0건 — UI/로직 variant 자체가 없음.**

→ 본 매핑 노트 차원의 UI 차이 없음. contract `customer_variants` 섹션에 단언으로 기록 (T2 산출).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재.
  - 부착 대상 (~12개): `input(from)` `Sobo31.Edit101`, `input(to)` `Sobo31.Edit102`, `input(bcode)` `Sobo31.Edit103`, `input(bcodeTo)` `Sobo31.Edit105`, `label(from)` `Sobo31.Panel101`, `label(bcode)` `Sobo31.Panel102`, `button(조회)` `Sobo31.dxButton1`, `th(일자)` `Sobo31.DBGrid101.GDATE`, `th(입고수)` `Sobo31.DBGrid101.GIQUT`, `th(출고수)` `Sobo31.DBGrid101.GOQUT`, `th(재고수)` `Sobo31.DBGrid101.GJQUT`, `th(반품수)` `Sobo31.DBGrid101.GBQUT`, `th(파지수)` `Sobo31.DBGrid101.GPQUT`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (예: DBGrid201 거래처 분배 컬럼).
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: hcode → bcode → bcodeTo → from → to → 조회 순.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 값) 가 코드에 없음.

## 11. 참조

- DEC-016/017/018: 권한키/인쇄/바코드 후속.
- DEC-019: customer_variants 통합 정책.
- DEC-024: 페이지네이션 표준.
- DEC-028: dfm→html 산출물 영구 입력 동결.
- HA-RET-01: retrofit 백로그 — C2 완료, **C6 묶음(본 노트 포함) 완료**, C1·C9 잔여.
- 화면 카드: [`analysis/screen_cards/Sobo31.md`](../screen_cards/Sobo31.md)
- contract: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[3]
- 회귀 테스트: [`test/test_c6_inquiry_phase1.py`](../../test/test_c6_inquiry_phase1.py)
