# 레이아웃 매핑: Sobo27 (출고접수관리) — 모던 출고 페이지 3종

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 retrofit 산출물**(C2 phase1 동결 후 DEC-028 채택, HA-RET-01 첫 사례).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu27/Sobo27.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu27/Sobo27.html) + `Sobo27.form.json` + `Sobo27.tree.json`
- 변형 1: [`Subu27_1/Sobo27.*`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu27_1/) — **dfm 동일(diff 0행), `.pas` 22행 차이만 (1608 → 1586)** = 로직 변형, UI 변형 없음
- 화면 카드: [`analysis/screen_cards/Sobo27.md`](../screen_cards/Sobo27.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu27.dfm`](../../legacy_delphi_source/legacy_source/Subu27.dfm) (1273행, EUC-KR)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu27.pas`](../../legacy_delphi_source/legacy_source/Subu27.pas) (1608행)
- 모던 라우트: [`outbound/orders/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/outbound/orders/page.tsx), [`outbound/orders/new/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/outbound/orders/new/page.tsx), [`outbound/orders/[orderKey]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/outbound/orders/[orderKey]/page.tsx)
- 계약: [`migration/contracts/outbound_order.yaml`](../../migration/contracts/outbound_order.yaml)

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo27` 은 **"출판사 단위 출고접수 진행 모니터링 + 출고증 인쇄 트리거"** 화면 (T2_Sub71/T2_Sub72 join, 라디오 필터로 접수/완료/전체 보기, 출고증 인쇄 범위(전체/시내/지방) 선택). 모던 C2 phase1 은 contract [`outbound_order.yaml`](../../migration/contracts/outbound_order.yaml) 결정에 따라 **거래처 단위 주문 CRUD (목록·신규·상세/취소)** 로 UX 를 재설계함 (DEC-009 인쇄 후속, DEC-012 소프트 취소만, DEC-019 `customer_variants` 정책 그대로).

따라서 본 매핑은:

- **의미가 일치하는 dfm 위젯에만** 모던 컴포넌트의 `data-legacy-id` 부착 (예: 거래일자, 검색 버튼).
- **dfm 에 있으나 모던 1차 범위에서 빠진** 위젯(이미지 컬럼 4종, 자동알람, 출고증 라디오) 은 §6 "out-of-scope" 로 명시 — 부착 안 함, contract `out_of_scope` 와 동기.
- **모던에서 신설된** 위젯(거래처 자동완성 입력, 라인 인라인 그리드, 취소 다이얼로그) 은 §7 "deltas" 로 명시 — `data-legacy-id` 미부착(원본 없음).

## 2. dfm 영역 인벤토리 (Sobo27.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel, Color 14416873) | 0 | 13 (Label101, Panel101/102, Edit101~105, Button101/201/701/702, DateEdit1, dxButton1) | `outbound/orders/page.tsx` 필터 영역(line 119~166) |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | 2 (DBGrid101 10 컬럼, StBar101) | `outbound/orders/page.tsx` table(line 174~240) |
| 하단 진행 패널 | `Panel007` (TFlatPanel, Color clInfoBk) | 2 | 5 (ProgressBar0/1, Panel008/009/010) | **out-of-scope** — Phase 2 인쇄 진행 표시 |
| 우측 모드 라디오 1 | `Panel003` | 3 | 3 (RadioButton1/2/3 — 접수/완료/전체) | `outbound/orders/page.tsx` "취소 포함" 토글로 단순화(line 148~155) |
| 우측 라디오 2 | `Panel004` | 4 | 4 (RadioButton4~7 — 전체선택/해제/자동알람/자동해체) | **out-of-scope** — 그리드 다중선택은 1차 미사용 |
| 우측 라디오 3 | `Panel005` | 5 | 3 (RadioButton8~0 — 구간/신간/전체) | **out-of-scope** — 신간 필터 후속 |
| 우측 라디오 4 | `Panel011` | 6 | 3 (RadioButton11~13 — 출고증전체/시내/지방) | **out-of-scope** — 출고증 인쇄 후속 (DEC-009) |
| 데이터셋·이미지·타이머 | `DataSource1/2`, `ImageList1~4`, `Timer1` | n/a | 7 | 백엔드/API로 흡수 (`outbound_service.py`) |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (mask `!9999.!99.99;1; `) | `<Input id="from" type="date">` (line 122~127) | input(from) | dfm 단일 일자 → 모던 범위(from) 로 확장 |
| — | (모던 신규) | — | 종료일 | `<Input id="to" type="date">` (line 131~136) | input(to) | §7 deltas — dfm 미존재 |
| 1 | `Edit102` | TFlatEdit (Visible=false) | 출판사코드 | **out-of-scope** — 모던은 거래처 hcode 필드만 사용 | — | 의미 불일치(출판사 vs 거래처) |
| 2 | `Edit103` | TFlatEdit | 출판사명 표시 | **out-of-scope** | — | 의미 불일치 |
| 3 | `Edit104` | TFlatEdit (Visible=false) | (보조 코드) | **out-of-scope** | — | |
| 4 | `Edit105` | TFlatEdit | (보조 명칭) | **out-of-scope** | — | |
| 5 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` (line 121) | label(from) | 캡션 의미 매핑 |
| 6 | `Panel102` | TFlatPanel | "출판사명" 라벨 | **out-of-scope** | — | |
| 7 | `Button101` | TFlatButton (Visible=false, OnClick `Button101Click`) | 조회(보조) | `<Button onClick=load>` "조회" (line 156~165) | button(조회) | dxButton1 과 동일 핸들러로 묶임 |
| 8 | `Button201` | TFlatButton (Visible=false) | 신규 | `<Link href="/outbound/orders/new"><Button>신규 주문` (line 112~116) | button(신규) | 모던은 라우트 분리 |
| 9 | `DateEdit1` | TDateEdit | 캘린더 팝업 | (HTML5 date input 내장 — 별도 위젯 없음) | — | §7 deltas: HTML5 native picker |
| 10 | `Button701` | TFlatButton (Glyph) | 캘린더 트리거 1 | (HTML5 picker 내장) | — | |
| 11 | `Button702` | TFlatButton (Glyph) | 캘린더 트리거 2 | (HTML5 picker 내장) | — | |
| 12 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` (line 156~165) | button(조회) | Button101 과 동일 의미 — `data-legacy-id="dxButton1"` 1순위 부착 |

> **TabOrder 보존**: 모던 페이지는 검색 영역의 키보드 흐름이 시작일 → 종료일 → 거래처 → 취소포함 → 조회 순서로 자연 보장됨 (DOM 순서 = TabOrder). dfm 의 TabOrder 0/9 (Edit101 → DateEdit1) 는 HTML5 date input 단일 위젯으로 합쳐짐.

## 4. 중단 그리드 매핑 (DBGrid101) — 의미 변환

dfm `DBGrid101` 컬럼 10개 (출판사별 모니터링 모드):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (orders/page.tsx) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 1 | `GCODE` | 출판사코드 | hcode-like | (모던: `<th>거래처</th>` 의 sub-text — gcode/hcode) | th(거래처) — `data-legacy-id="DBGrid101.GCODE"` |
| 2 | `GNAME` | 출판사명 | 명칭 | `<th>거래처</th>` 본문 | th(거래처) — 동일 |
| 3 | `GTELS` | 전화번호 | tel | **out-of-scope** | — |
| 4 | `CODE5` | 선택 (체크박스) | 다중선택 | **out-of-scope** — 1차 단일 행 클릭만 | — |
| 5 | `GOQUT` | 접수건 | 카운트 | `<th>라인</th>` (count) | th(라인) — `data-legacy-id="DBGrid101.GOQUT"` |
| 6 | `GSQUT` | 완료건 | 카운트 | `<th>수량합</th>` (qty sum) | th(수량합) — `data-legacy-id="DBGrid101.GSQUT"` |
| 7 | `CODE1` | 미사용 (이미지) | 상태 마커 | **out-of-scope** | — |
| 8 | `CODE2` | 사용중 (이미지) | 상태 마커 | **out-of-scope** | — |
| 9 | `CODE3` | 접수 (이미지) | 상태 마커 | `<th>상태</th>` (배지: 정상) | th(상태) — `data-legacy-id="DBGrid101.CODE3"` (대표 1개만 부착, 나머지 3개 이미지는 deltas) |
| 10 | `CODE4` | 완료 (이미지) | 상태 마커 | (배지: 정상의 시각적 변형) | (CODE3 와 통합) |

모던 신규 컬럼 (§7 deltas):

- `<th>일자</th>` — 모던 신규 (dfm 그리드는 검색 패널의 거래일자 단일값을 사용)
- `<th>전표</th>` — 모던 신규 (dfm 은 status bar 에 표기)
- `<th>금액합</th>` — 모던 신규 (dfm 은 별도 합계 행 미사용)

> 컬럼 의미 차이의 본질: dfm 그리드 = "출판사별 진행 카운트", 모던 그리드 = "주문 단건 1행". 1:1 셀 매핑은 불가능하므로 **헤더 의미가 가장 가까운 1개에만 `data-legacy-id` 부착** + 나머지는 본 노트 §7 deltas 에 기록.

## 5. 신규 화면 (`outbound/orders/new/page.tsx`) 매핑

dfm Sobo27 에는 **"신규 주문 등록 폼" 자체가 없음** (Button201 클릭 → 외부 윈도우 호출, 본 dfm 외부). 모던에서는 라우트 분리하여 신규 등록 폼을 신설 — 본 페이지는 거의 전부 §7 deltas.

다만 의미 매핑 가능한 부분:

| 모던 위젯 | 의미 | 부착할 data-legacy-id | 근거 |
| --- | --- | --- | --- |
| `<Input id="gdate" type="date">` | 주문 일자 | `Sobo27.Edit101` | 거래일자 동일 의미 |
| `<CustomerSearchInput>` | 거래처 (hcode + 자동완성) | (없음 — deltas) | dfm 미존재, 모던 신설 |
| `<Input id="gjisa">` | 지사 | (없음 — deltas) | dfm 미존재 |
| `<OrderLineGrid>` | 라인 입력 | (없음 — deltas) | dfm 의 DBGrid101 과 의미 다름 (모니터링 vs 입력) |
| 헤더 "신규 출고 주문" 의 "저장" 버튼 | INSERT 트리거 | `Sobo27.Button201` | "신규" 의미 매핑 |
| 헤더 "목록" 링크 | 화면 닫기 | `Sobo27.FormClose` | OnClose 핸들러 의미 |

## 6. 상세/취소 화면 (`outbound/orders/[orderKey]/page.tsx`) 매핑

| 모던 위젯 | 의미 | 부착할 data-legacy-id | 근거 |
| --- | --- | --- | --- |
| 헤더 "주문 상세" + 상태 배지 | 단일 주문 보기 | (없음 — deltas) | dfm 은 그리드 행 선택으로 표시 |
| `<section>` 일자/거래처/전표 | 주문 키 표시 | `Sobo27.StBar101` | StatusBar 패널 의미 매핑 |
| `<OrderLineGrid readOnly={isCancelled}>` | 라인 표시·편집 | (없음 — deltas) | |
| "라인 저장" 버튼 | UPDATE diff 실행 | (없음 — deltas) | dfm 의 ApplyUpdates 호출과 의미 유사하나 별도 버튼 없음 |
| "주문 취소" 버튼 | 소프트 취소 | (없음 — deltas) | dfm 은 Yesno 컬럼 inline 토글로 처리 |
| `<CancelDialog>` | 취소 사유 확인 | (없음 — deltas) | |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 종료일 입력 | `outbound/orders/page.tsx` line 131 | 단일 일자 → 범위 검색 확장 (DEC-019 변형 통합 정책 재사용) |
| 모던 신규 | 거래처 코드 입력 | `outbound/orders/page.tsx` line 140 | C2 contract 가 거래처 단위 CRUD 로 재정의 |
| 모던 신규 | "취소 포함" 토글 | `outbound/orders/page.tsx` line 148 | dfm 의 Panel003 라디오(접수/완료/전체) 단순화 |
| 모던 신규 | DataGridPager | `outbound/orders/page.tsx` line 242 | dfm 은 모달리스 윈도우 — 모던 페이지네이션은 신규 |
| 모던 신규 | 신규 주문 폼 전체 | `outbound/orders/new/page.tsx` | dfm 외부 |
| 모던 신규 | 상세 페이지 / 취소 다이얼로그 | `outbound/orders/[orderKey]/page.tsx` | dfm 외부 |
| dfm out-of-scope | Panel004 자동알람·자동해체 | — | 1차 다중선택 미사용 |
| dfm out-of-scope | Panel005 신간 필터 | — | 후속 |
| dfm out-of-scope | Panel011 출고증 인쇄 라디오 | — | DEC-009 인쇄 후속 |
| dfm out-of-scope | Panel007 ProgressBar 진행 표시 | — | 인쇄 후속 |
| dfm out-of-scope | DBGrid 이미지 컬럼 CODE1/2/4 | — | 모니터링 표기 — 모던은 status 단일 배지 |
| dfm out-of-scope | Edit102~105 출판사 검색 | — | C2 모던 = 거래처 단위 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 위치 | 비고 |
| --- | --- | --- | --- |
| `FormActivate` | `useEffect` mount 후 자동 load | `orders/page.tsx` line 98 | 자동 페이지 사이즈 결정 후 첫 호출 |
| `FormShow` | (동일 useEffect) | | |
| `FormClose` | `<Link href="/outbound/orders">목록` | `new`, `[orderKey]` 헤더 | 의미: 화면 닫기 |
| `Button101Click` / `dxButton1.OnClick` | `load()` (조회) | `orders/page.tsx` line 71 | dfm 에서 두 버튼이 같은 핸들러 |
| `Edit101Change` | `setDateFrom` / `setGdate` | 각 페이지 | 거래일자 변경 |
| `DataSource2DataChange` | (자동 — React state 갱신) | | |
| `Timer1Timer` (Enabled=false) | (없음) | — | dfm 에서도 비활성 |

## 9. 변형 차이 (`Sobo27` 본 vs `Sobo27_1`)

`legacy_source/Subu27.dfm` vs `legacy_source/Subu27_1.dfm`: **diff 0행 (UI 동일).**  
`Subu27.pas` (1608행) vs `Subu27_1.pas` (1586행): **22행 차이 — 로직 분기.**

→ 본 매핑 노트 차원의 UI 차이는 없음. 로직 차이는 [`migration/contracts/outbound_order.yaml`](../../migration/contracts/outbound_order.yaml) `customer_variants` 섹션에 별도 기록 (T2 산출).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재.
  - 부착 대상: `Edit101`, `Panel101`, `Button101`/`dxButton1`(통합), `Button201`, `DBGrid101.GCODE`, `DBGrid101.GOQUT`, `DBGrid101.GSQUT`, `DBGrid101.CODE3`, `StBar101`, `FormClose` (총 ~10개)
- [ ] §6/§7 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (예: 자동알람 라디오) 리뷰.
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: 시작일 → 종료일 → 거래처 → 취소포함 → 조회 순.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 들어가지 않았는지 (픽셀 left/top/width/height 등) 리뷰.

## 11. 참조

- DEC-028: dfm→html 산출물 영구 입력 동결.
- DEC-019: customer_variants 통합 정책.
- DEC-009 / DEC-012: 인쇄 후속 / 소프트 취소만.
- HA-RET-01: retrofit 백로그 (본 노트가 첫 산출물).
- 화면 카드: [`analysis/screen_cards/Sobo27.md`](../screen_cards/Sobo27.md)
- contract: [`migration/contracts/outbound_order.yaml`](../../migration/contracts/outbound_order.yaml)
- 회귀 테스트: [`test/test_c2_outbound_phase1.py`](../../test/test_c2_outbound_phase1.py)
