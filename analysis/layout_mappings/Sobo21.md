# 레이아웃 매핑: Sobo21 (거래명세서) — 모던 거래명세서 페이지 2종

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 retrofit 산출물** (C6 phase1 동결 후 DEC-028 채택, HA-RET-01 두 번째 사례 묶음).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu21/Sobo21.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu21/Sobo21.html) + `Sobo21.form.json` + `Sobo21.tree.json`
- **변형 폴더 부재** — `Subu21_*` 등 variant 디렉터리가 generated 산출물에 0건 존재.
- 화면 카드: [`analysis/screen_cards/Sobo21.md`](../screen_cards/Sobo21.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu21.dfm`](../../legacy_delphi_source/legacy_source/Subu21.dfm) (1168행, EUC-KR)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu21.pas`](../../legacy_delphi_source/legacy_source/Subu21.pas) (Button101Click L460, S1_Memo UPSERT L1452)
- 모던 라우트:
  - [`transactions/sales-statement/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/transactions/sales-statement/page.tsx) (목록)
  - [`transactions/sales-statement/[orderKey]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/transactions/sales-statement/[orderKey]/page.tsx) (상세 + 메모 UPSERT)
- 계약: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[0..2]

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo21` 은 **단일 화면(top 검색 + mid 그리드 + bot 상세 입력 패널)** 에서 거래명세서 조회·라인 표시·메모(연락처·비고) 편집을 모달리스로 동시에 수행. 모던 C6 는 **목록 + 상세** 두 라우트이며, 2026-06 보강으로 목록 하단에 **참조·메모 패널** 을 복원했다:

- 검색·그리드·**하단 참조/메모** → `sales-statement/page.tsx` + `sales-statement-reference-panel.tsx` / `sales-statement-memo-panel.tsx`
- 행 선택 → 목록에서 메모 UPSERT; **상세 화면 열기** → `[orderKey]/page.tsx` (라인 그리드 + 동일 패널 컴포넌트 재사용)

따라서 본 매핑은:

- **의미가 일치하는 dfm 위젯에만** 모던 컴포넌트의 `data-legacy-id` 부착.
- dfm 의 출판사 검색·전표 인쇄·바코드 입력 등 **모던 1차 범위 외** 위젯은 §6/§7 deltas — 부착 안 함, contract `out_of_scope`/deltas 와 동기.
- 모던에서 신설된 페이지네이터·취소 포함 토글·DataGrid wrapper 는 §7 deltas — `data-legacy-id` 미부착.

## 2. dfm 영역 인벤토리 (Sobo21.dfm 직접 분석)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | 22 (Label100, Panel101~106, Button101/201/701/702/901, Edit101~109, DateEdit1, dxButton1) | `sales-statement/page.tsx` 검색 영역 (line 166~213) |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101 9 컬럼) | `sales-statement/page.tsx` DataGrid (line 221~233) |
| 하단 상세/메모 입력 | `Panel003` (TFlatPanel) | 2 | 24 (Label103/104, Panel201~204, Edit201~208, StaticText1~4, Button801~803) | `sales-statement/[orderKey]/page.tsx` 메모 카드 (line 181~243) |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | (separate) | 5 (ProgressBar0/1, Panel008/009/010 — "레코드"/"검색진행") | **out-of-scope** — 진행 표시는 React 의 `loading` boolean 으로 흡수 |
| 보조 패널 | `Panel401` | n/a | 0 | **out-of-scope** — 인쇄 후속 위젯 컨테이너 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/API 로 흡수 (`transactions_service`) |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (mask `!9999.!99.99;1;`) | `<Input id="from" type="date">` (line 179~184) | input(from) | dfm 단일 일자 → 모던 범위(from) |
| — | (모던 신규) | — | 종료일 | `<Input id="to" type="date">` (line 188~193) | input(to) | §7 deltas |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` (line 178) | label(from) | 캡션 의미 매핑 |
| 13 | `Panel104` | TFlatPanel | "거래처코드" 라벨 | `<Label htmlFor="gcode">` + `MasterLookupField(customer)` | `Sobo21.Edit104` | Subu21 L512 `@Gcode` = Edit104 |
| 12 | `Panel105` | TFlatPanel | "거래처명" 라벨 | `<Input id="customerName" readOnly>` | `Sobo21.Edit105` | lookup 선택명 표시 |
| 11 | `Panel102` | TFlatPanel | "출판사코드" 라벨 | **out-of-scope** | — | Edit107 출판사 |
| 10 | `Panel103` | TFlatPanel | "거래구분" 라벨 | `<select id="gubun">` 출고/반품/파지 | `Sobo21.Edit102` | Subu21 L510 `@Gubun` |
| (n/a) | `Edit103` | TFlatEdit | 전표번호 | `<Input id="jubun">` | `Sobo21.Edit103` | |
| (n/a) | `Edit104` | TFlatEdit | 거래처코드 | `MasterLookupField` value | `Sobo21.Edit104` | |
| (n/a) | `Edit105` | TFlatEdit | 거래처명 | readOnly 표시 | `Sobo21.Edit105` | |
| (n/a) | `Edit106` | TFlatComboBox | 지사(Gjisa) | `<select id="gjisa">` — `customerBranchList` 동적 로드, 0건 시 숨김 | `Sobo21.Edit106` | Subu21 L1048–1070 `H2_Gbun` |
| (n/a) | `Edit107/108` | TFlatEdit | 출판사코드/명 | **out-of-scope** | — | |
| (n/a) | `Edit109` | TFlatEdit | 보조 | **out-of-scope** | — | |
| (n/a) | `DateEdit1` | TDateEdit | 캘린더 팝업 | (HTML5 date input 내장) | — | §7 deltas |
| (n/a) | `Button701/702/901` | TFlatButton | 캘린더 트리거 / 인쇄 | (HTML5 picker 내장 / 인쇄 후속) | — | DEC-017 deferred |
| (n/a) | `Button101` | TFlatButton (Visible=false, OnClick `Button101Click`) | 조회(보조) | `<Button onClick=load>조회` (line 203~212) | button(조회) | dxButton1 과 동일 핸들러 |
| (n/a) | `Button201` | TFlatButton (Visible=false) | 신규 등록 | **out-of-scope** | — | 거래명세서 신규는 C2 outbound 와 분리 |
| (n/a) | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` (line 203~212) | button(조회) | Button101 과 동일 의미 — `data-legacy-id="dxButton1"` 1순위 부착 |

> **TabOrder 보존**: 모던 검색 영역의 키보드 흐름은 거래처 → 시작일 → 종료일 → 취소포함 → 조회 (DOM 순서). dfm 의 TabOrder 0 (Edit101) → 8 (Panel101 라벨) → 13 (Panel104 라벨) → ... 은 라벨이 input 의 `htmlFor` 로 묶이며 의미상 보존됨.

## 4. 중단 그리드 매핑 (DBGrid101) — 의미 변환

dfm `DBGrid101` 컬럼 9개 (라인 단위 표시):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (목록 page.tsx) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 1 | `PUBUN` | 구분 | 품목 구분 | 상세 `lineColumns.pubun` 헤더「구분」 | `Sobo21.DBGrid101.PUBUN` |
| 2 | `BCODE` | 도서코드 | 키 | 상세 `bcode` | `Sobo21.DBGrid101.BCODE` |
| 3 | `BNAME` | 도서명 | 명칭 | 상세 `product_name` | `Sobo21.DBGrid101.BNAME` |
| 4 | `GSQUT` | 수량 | 라인 수량 | 목록 `<th>수량합</th>` (SUM); 상세 `gsqut` | 목록 th — `DBGrid101.GSQUT`; 상세 동일 legacy-id |
| 5 | `GDANG` | 단가 | 단가 | 상세 `gdang` | `Sobo21.DBGrid101.GDANG` |
| 6 | `GRAT1` | 비율 | 할인율 | 상세 `grat1` (표시 `n%`) | `Sobo21.DBGrid101.GRAT1` |
| 7 | `GSSUM` | 금액 | 라인 금액 | 목록 금액합; 상세 `gssum` | `DBGrid101.GSSUM` |
| 8 | `GBIGO` | 비고 | 라인 메모 | 상세 `gbigo` | `Sobo21.DBGrid101.GBIGO` |
| 9 | `YESNO` | 배송(표제) | 라인 Yesno — dfm 표제는 배송, 필드는 동일 Yesno | 목록 집계행 `<th>상태</th>` (거래 취소 배지); **상세 라인** 컬럼「배송」은 라인 `yesno`(2=취소·그 외 완료 표시) | 목록 `DBGrid101.YESNO`; 상세 라인 `DBGrid101.YESNO` |

모던 신규 컬럼 (목록 page.tsx, §7 deltas):

- `<th>일자</th>` — 거래일자 (`order_key.gdate`) — 모던 그룹화 표현
- `<th>거래처</th>` — `customer_name + (hcode)` — dfm 은 검색 패널에서 입력만
- `<th>전표</th>` — `order_key.jubun` — dfm 은 라인 PUBUN 컬럼으로 추정
- `<th>라인</th>` — `row_count` 집계 — 모던 신규 (HOT-OUT-1 회피용 별칭)

> 그리드 의미 차이: dfm = "한 거래의 모든 라인 평면 표시", 모던 목록 = "거래 1건당 1행 (group by gdate/hcode/jubun/gjisa) + 상세 라우트로 라인 노출". 라인 수준 컬럼(PUBUN/BCODE/BNAME/GDANG/GRAT1/GBIGO) 은 상세 페이지의 `lineColumns` 로 이전 — `GBIGO` 만 의미가 명확하므로 `data-legacy-id` 부착.

## 5. 하단 입력·메모 패널 매핑 (Panel003) — 목록·상세 공통 컴포넌트

dfm Panel003 → `sales-statement-reference-panel.tsx` (참조) + `sales-statement-memo-panel.tsx` (S1_Memo UPSERT).

- **목록** `page.tsx`: 거래처·검색 조건으로 `GET .../customer-preview` (G1·`memo_preview`·재고); 그리드 행 선택 시 `detail` 로 메모 편집.
- **상세** `[orderKey]/page.tsx`: 동일 컴포넌트 재사용.

| dfm 위젯 ID | 클래스 | dfm 라벨/용도 | S1_Memo 컬럼 | 모던 위젯 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| `Panel201` | TFlatPanel | "전표번호" 라벨 | `order_key.jubun` | `<Input readOnly Edit201>` | `Sobo21.Edit201` |
| `Panel202` | TFlatPanel | "전화번호" 라벨 | G1_Ggeo 읽기전용 | `<Input readOnly Edit202>` | `Sobo21.Edit202` |
| `Panel204` | TFlatPanel | "주소" 라벨 | G1 `Gadd1` | 참조 패널 address | `Sobo21.Panel204` |
| `Panel203` | TFlatPanel | "추가 내용" | G1 `Memos`(RTF)+S1 `Gbigo` | 참조 패널 textarea | `Sobo21.Edit203` |
| `Edit203` | TFlatEdit | 비고1 | G1 `Gbigo`/`Email` | 참조 비고1 | `Sobo21.Edit203` (라벨 분리) |
| `Edit204` | TFlatEdit | 비고2 | G1 `Name1` | 참조 비고2 | `Sobo21.Edit204` |
| `Edit201` | TFlatEdit | 전표번호 표시 | — | readOnly `slip_no` | `Sobo21.Edit201` |
| `Edit202` | TFlatEdit | 전화번호(마스터) | G1 | readOnly phone | `Sobo21.Edit202` |
| `Edit203` | TFlatEdit | 비고1 / 업무 메모 | Gbigo (Button301) | 참조 패널 read-only textarea | `Sobo21.Edit203` |
| `Edit204` | TFlatEdit | 비고2 | Sbigo | `<textarea sbigo>` | `Sobo21.Edit204` |
| `Edit205` | TFlatEdit | 핸드폰 | Gtel1 | `<Input gtel1>` | `Sobo21.Edit205` |
| `Edit206` | TFlatEdit | 전화 | Gtel2 | `<Input gtel2>` | `Sobo21.Edit206` |
| `Edit207` | TFlatEdit | 받는사람 | Gname | `<Input gname>` | `Sobo21.Edit207` |
| `Edit208` | TFlatEdit | 우편번호 | Gpost | `<Input gpost>` | `Sobo21.Edit208` |
| `StaticText1~4` | TStaticText | 핸드폰/전화/받는사람/우편번호 | — | Label htmlFor | `Sobo21.StaticText1` … `4` |
| `Label103/104` | TmyLabel3d | 재고 | SUM(Gsqut) placeholder | `stock_qty` 표시 | `Sobo21.Label103` / `Label104` — Phase2 PrinJing |
| `Button801` | TFlatButton | 저장 | UPSERT | 메모 저장 | `Sobo21.Button801` |
| `Button802` | TFlatButton | 주소가져오기 | G1→메모 프리필 | 주소 가져오기 | `Sobo21.Button802` |
| `Button803` | TFlatButton | 우편조회 | **out-of-scope** | — | — |

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 검색 | Edit107/108 (출판사) | OOS-INQ-6 |
| 검색 | Edit107/108 (출판사코드/명) | 모던은 거래처 단위 |
| 검색 | Edit109 | 보조 |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` boolean 으로 흡수 |
| 인쇄 | Button701/702/901, Panel401 | DEC-017 — C7 인쇄 후속 |
| 라인 | Button803 (우편 팝업) | C8/우편 후속 |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 종료일 입력 | `sales-statement/page.tsx` line 188 | 단일 일자 → 범위 검색 확장 (DEC-019 정책) |
| 모던 신규 | "취소 포함" 토글 | `sales-statement/page.tsx` line 195~202 | dfm 의 검색 패널 미존재 — 백엔드 `include_cancelled` 와 짝 |
| 모던 신규 | DataGridPager | `sales-statement/page.tsx` line 235~243 | dfm 모달리스 → 모던 페이지네이션 |
| 모던 신규 | 상세 라우트 분리 | `sales-statement/[orderKey]/page.tsx` 전체 | dfm 은 단일 화면 — 모던은 list/detail 분리 |
| 모던 신규 | 라인 그리드 (`lineColumns`) | 상세 `[orderKey]/page.tsx` | dfm DBGrid 라인 컬럼 이전 — 단가·비율·배송(yesno)·합계 푸터(`FooterRow`) 포함 |
| 모던 신규 | 목록 필터 gcode·gubun·지사·전표 | `sales-statement/page.tsx` | `gcode`/`gubun`/`jubun`/`gjisa` + customer lookup |
| 모던 신규 | 상세 G1 참조 + 주소가져오기 | `[orderKey]/page.tsx` | `customer_profile` + Button802 |
| 모던 신규 | 당일만 토글 | 목록 | Edit101 단일일자 체감 |
| 모던 신규 | "메모 신규/수정" 안내 + UPSERT action 메시지 | 상세 line 94~98, 184 | PATCH 응답의 `action` 노출 (계약 추가 동작) |
| dfm out-of-scope | 출판사 검색 4종 | — | C6 1차 = 거래처 hcode 단일 |
| dfm out-of-scope | 인쇄/바코드 트리거 | — | DEC-017/018 후속 |
| 해소됨 (2026-04) | 라인 단가/할인 (GDANG/GRAT1) 상세 그리드 | 상세 페이지 | API·`SalesStatementLine` 모델 확장 후 노출 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 위치 | 비고 |
| --- | --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load(0, recommended)` | 목록 line 105~108 | 자동 페이지 사이즈 결정 후 첫 호출 |
| `FormClose` | `<Button variant="ghost" onClick=router.back>목록` | 상세 line 131~133 | 의미: 화면 닫기 |
| `Button101Click` / `dxButton1.OnClick` | `load()` (조회) | 목록 line 68~99 | dfm 에서 두 버튼이 같은 핸들러 |
| `Edit101Change` | `setDateFrom` | 목록 line 183 | 거래일자 변경 |
| `Button801Click` (메모 저장) | `onSaveMemo` → `transactionsApi.upsertMemo` | 상세 line 83~106 | UPDATE→INSERT 분기는 백엔드 UPSERT |
| `DataSource1DataChange` / `DataSource2DataChange` | (자동 — React state 갱신) | | |

## 9. 변형 차이 (`Sobo21` 본 vs variant)

`legacy_source_root/Subu21*` 디렉터리 inventory: **`Subu21_*` 등 variant 폴더 0건 — UI/로직 variant 자체가 없음.**

→ 본 매핑 노트 차원의 UI 차이 없음. contract `customer_variants` 섹션에는 "variant 0건 확인 — DEC-019/028 정책 그대로" 단언으로 기록 (T2 산출).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4·§5 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재.
  - 목록 `sales-statement/page.tsx` (~7개): `input(from)` `Sobo21.Edit101`, `label(from)` `Sobo21.Panel101`, `label(hcode)` `Sobo21.Panel104`, `input(hcode)` `Sobo21.Edit103`, `button(조회)` `Sobo21.dxButton1`, `th(수량합)` `Sobo21.DBGrid101.GSQUT`, `th(금액합)` `Sobo21.DBGrid101.GSSUM`, `th(상태)` `Sobo21.DBGrid101.YESNO`
  - 상세 `[orderKey]/page.tsx` (~10개): `header(jubun)` `Sobo21.Panel201`, `input(gname)` `Sobo21.Panel105`, `label(gtel1)` `Sobo21.Panel202`, `input(gtel1)` `Sobo21.Edit202`, `input(gtel2)` `Sobo21.Edit203`, `label(gpost)` `Sobo21.Panel204`, `input(gpost)` `Sobo21.Edit205`, `label(gbigo)` `Sobo21.Panel203`, `textarea(gbigo)` `Sobo21.Edit206`, `textarea(sbigo)` `Sobo21.Edit207`, `button(저장)` `Sobo21.Button801`, `th(비고@lines)` `Sobo21.DBGrid101.GBIGO`, `목록 링크` `Sobo21.FormClose`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (예: 출판사 검색 input).
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] 메모 저장 흐름이 PATCH UPSERT (action: inserted/updated) 의미 보존.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 left/top/width/height/Color) 가 코드에 없음.

## 11. PDF 절 (C7 Phase 1 보강 — 거래명세서)

DEC-017 의 종결 (2번째 — 본 노트가 거래명세서 본진).

| 항목 | 값 | 근거 |
| --- | --- | --- |
| 양식 코드 | `P1-E` (거래명세서) | `print_specs/c7_phase1.md` §1 |
| 용지/여백 | A4 세로 (`210mm 297mm`) / `12mm` | 동 §1 |
| 헤더 | 거래처명 + 출고일자 + 전표번호 + 지사 | §3 본 노트 (`Edit101`/`Panel101`/`Panel105`) |
| 본문 표 | 도서코드/도서명/구분/수량/금액/비고 (6컬럼) | DBGrid101 의 GCODE/GNAME/CODE3/GSQUT/GSSUM/GBIGO |
| 합계 | tfoot 2종 (수량합/금액합) | DBGrid101 footer (`GSQUT`/`GSSUM`) |
| 엔드포인트 | `GET /api/v1/print/sales-statement/{order_key}.pdf` (T5b — `routers/print.py`) | T5b |
| 빌더 | `transactions_service.render_sales_statement_html(order_key)` (기존 `get_sales_statement_detail` 재사용) | T5c — SRP, 신규 SQL 0 |
| 데이터 출처 | 기존 SQL-INQ-2~3 — 신규 SQL 없음 | C6 자산 재사용 |
| FE 진입점 | 신규 `/print/sales-statement/[orderKey]/page.tsx` (T6b) — 미리보기 + PDF 다운로드 | — |
| FE 트리거 | Sobo21 행 액션 "명세서" 버튼 → 신규 페이지 | T6b |
| 회귀 | `pytest -k test_sales_statement_pdf_signature/text/empty` 3 케이스 | T4 |

기본 PDF(`layout=default`)는 상·하 2단(공급자보관용 → 절취선 → 공급받는자보관용)을 유지하되, 2026-04-28 보강으로 삼련형 밀도에 맞춰 `6mm 8mm` 여백·소형 폰트·14행 기준을 사용한다. 기본 양식은 **흑백 인쇄 전용**이며 `section_border_colors` 는 `layout=legacy_triplicate` 에만 적용한다.

> **DEC-017 완전 종결**: C6 의 SQL/서비스는 그대로, 빌더 + 신규 페이지/엔드포인트만.

## 12. 레거시 삼련 인쇄 (P1-E `layout=legacy_triplicate`) — 2026-04-28

| 항목 | 값 / DOM | `data-legacy-id` (요지) |
| --- | --- | --- |
| API | `GET /api/v1/print/sales-statement/{order_key}.pdf?layout=legacy_triplicate` | — |
| 프로필 | [`migration/contracts/print_sales_statement.yaml`](../../migration/contracts/print_sales_statement.yaml) + `server_profile_map` | — |
| 3섹션 순서 | 공급자 보관용 → 공급받는자 보관용 → 인수증 (색 테두리만 구분) | `Sobo21.Print.Triplicate.supplier` 등 |
| 헤더 좌 | 거래처코드·발행일·거래처명 | `Sobo21.Triplicate.Hcode` / `Gdate` / `Gname` |
| 헤더 중 | 제목 + 괄호 라벨 | `Sobo21.Triplicate.Title` / `CopyLabel` |
| 헤더 우 | 공급자 법적 행(계약 YAML) | `Sobo21.Triplicate.Supplier.{n}` |
| 표 컬럼 | No., 서가번호, 도서명, 부수, 정가, 비율, 금액, 비고 | `Sobo21.Triplicate.LineNo` … `Gbigo` |
| 우측 세로 | 반품처 안내(계약 `vertical_return_note`) | `Sobo21.Triplicate.VerticalNote` |
| 푸터 | 은행(좌)·총부수(중)·합계(우) | `FooterBank` / `FooterQty` / `FooterSum` |
| 인수증 바코드 | 전표번호 Code128 | `Sobo21.Triplicate.SlipBarcode` |

기본 PDF(`layout` 생략·`default`)는 §11 의 2단 수동 빌더 유지 — 본 절은 **옵트인** 삼련만 적용.

## 12.1 2026-06 공통 검색창 보강

- 목록 필터 `hcode` 는 `MasterLookupField(lookupKind="publisher")` + `MasterLookupButton` 으로 보강했다.
- `data-legacy-id="Sobo21.Edit103"` 입력은 유지하고 버튼은 `Sobo21.LookupHcode` 로 추가했다.
- 조회 파라미터 계약은 기존 `hcode` 그대로 유지하며 API/SQL 변경은 없다.

## 13. 참조

- DEC-016: 권한키 분기 → C10 통합.
- DEC-017: 인쇄 트리거 → C7 (본 노트에서 종결).
- DEC-018: 바코드 결합 → C8.
- DEC-019: customer_variants 통합 정책 (variant 부재 단언에 그대로 적용).
- DEC-024: 페이지네이션 표준 (DataGridPager).
- DEC-028: dfm→html 산출물 영구 입력 동결 (본 노트 = 두 번째 retrofit 묶음).
- **DEC-037/038/039** (C7 T8): WeasyPrint / 라벨 1종 / .frf 참조용
- HA-RET-01: retrofit 백로그 — C2 완료, **C6 묶음(본 노트 포함) 완료**, C1·C9 잔여.
- 화면 카드: [`analysis/screen_cards/Sobo21.md`](../screen_cards/Sobo21.md)
- contract: [`migration/contracts/sales_inquiry.yaml`](../../migration/contracts/sales_inquiry.yaml) endpoints[0..2], [`migration/contracts/print_invoice.yaml`](../../migration/contracts/print_invoice.yaml) v1.0.0 (C7)
- 인쇄 사양: [`analysis/print_specs/c7_phase1.md`](../print_specs/c7_phase1.md) §P1-E
- 회귀 테스트: [`test/test_c6_inquiry_phase1.py`](../../test/test_c6_inquiry_phase1.py), [`test/test_c7_print_phase1.py`](../../test/test_c7_print_phase1.py)
