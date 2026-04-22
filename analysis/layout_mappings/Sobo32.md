# 레이아웃 매핑: Sobo32 (거래처원장) — 모던 ledger/customer 페이지

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다. **본 노트는 phase2 → phase1 승격 직전 산출물** (PLAN-LDG-CUSTOMER-2026-04-22 의 T5(a)).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu32/Sobo32.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu32/Sobo32.html) + `Sobo32.form.json` + `Sobo32.tree.json`
- **변형 폴더**: `Subu32_9/` 가 존재 — UI 분기 0건 (component count 만 31→21 차이, SQL/이벤트 동일). contract `customer_variants: ['UI 분기 0건']` 로 단언.
- 화면 카드: [`analysis/screen_cards/Sobo32.md`](../screen_cards/Sobo32.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu32.dfm`](../../legacy_delphi_source/legacy_source/Subu32.dfm) (대표) + `Subu32_9.dfm` (변형)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu32.pas`](../../legacy_delphi_source/legacy_source/Subu32.pas) — Button102Click L301, 분기 누적 L411~L506
- 모던 라우트: [`ledger/customer/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/ledger/customer/page.tsx)
- 계약: [`migration/contracts/customer_book_ledger_phase2.yaml`](../../migration/contracts/customer_book_ledger_phase2.yaml) v1.1.0 endpoints `customer_single`

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

레거시 `Sobo32` 는 **3 영역 화면** (top 검색, mid DBGrid101 시계열, bottom DBGrid301 도서별 분배). 모던 P2 → phase1 승격 1차 = **단일 시계열 그리드(mid 만)** 로 단순화 — DBGrid301 도서별 분배는 후속 P3 카드.

따라서 본 매핑은:

- **시계열 그리드(DBGrid101) + 검색 패널만** 의미 매핑 — `data-legacy-id` 부착.
- DBGrid301(도서별 분배), 본사/지사 토글, 진행 패널은 §6 out-of-scope.
- 모던 신설 컬럼 `<th>잔량</th>`(balance_qty) 는 §7 deltas — Subu31 의 nSqry 누적과 동일한 모던 잔량 표기.

## 2. dfm 영역 인벤토리 (Subu32.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
|---|---|---|---|---|
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | ≈18 (Label101/102, Panel101~103, Button101/201/700/701/702, Edit101~108, DateEdit1/2, dxButton1, CornerButton1/2/9) | `ledger/customer/page.tsx` 검색 영역 |
| 중단 시계열 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101, 11 컬럼) | `ledger/customer/page.tsx` DataGrid |
| 하단 도서별 분배 그리드 | `Panel003` (TFlatPanel) | 2 | 1 (DBGrid301 = TDBGridEh, ≈9 컬럼) | **out-of-scope** (P3 후속) |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | 3 | 5 (ProgressBar0/1, Panel008~010, StBar101/201) | **out-of-scope** — React `loading` 흡수 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/API 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
|---|---|---|---|---|---|---|
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 시작 (mask 'YYYY.MM.DD') | `<Input id="from" type="date">` | input(from) — `data-legacy-id="Sobo32.Edit101"` | ISO date ↔ legacy mask 정규화 |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 끝 | `<Input id="to" type="date">` | input(to) — `data-legacy-id="Sobo32.Edit102"` | |
| 2 | `Edit107` | TFlatEdit | 거래처 코드 (Hcode) | `<Input id="hcode">` | input(hcode) — `data-legacy-id="Sobo32.Edit107"` | **필수** (계약: required) |
| 3 | `Edit108` | TFlatEdit | 거래처명 (조회 후 표시) | `<span class="customer-name">` | label(customer-name) — `data-legacy-id="Sobo32.Edit108"` | read-only 표기 |
| 4 | `Edit103` | TFlatEdit | 도서코드 시작 (선택) | `<Input id="bcodeFrom">` | input(bcodeFrom) — `data-legacy-id="Sobo32.Edit103"` | 옵션 |
| 5 | `Edit105` | TFlatEdit (HIDDEN→노출) | 도서코드 끝 | `<Input id="bcodeTo">` | input(bcodeTo) — `data-legacy-id="Sobo32.Edit105"` | dfm HIDDEN 을 모던에서 노출 (Sobo31 와 동일 정책) |
| 6 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` | label(from) — `data-legacy-id="Sobo32.Panel101"` | |
| 7 | `Panel102` | TFlatPanel | 토글 ("도서명/본사도서/창고도서") | `<select id="scope">` (A/B/ALL) | select(scope) — `data-legacy-id="Sobo32.Panel102"` | Caption → enum 매핑 (legacy_pas L373~L375) |
| 8 | `Panel103` | TFlatPanel | "도서코드" 라벨 | `<Label htmlFor="bcodeFrom">도서코드</Label>` | label(bcodeFrom) — `data-legacy-id="Sobo32.Panel103"` | |
| 9 | `Button101` | TFlatButton (Visible=false, OnClick L291 → 102/103/104 분기) | 조회(분기) | (내부 분기) | — | 분기는 백엔드 흡수 |
| 10 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` | button(조회) — `data-legacy-id="Sobo32.dxButton1"` | Button101 과 동일 핸들러 |
| 11 | `Button700` | TFlatButton | 캘린더 트리거 1 | (HTML5 picker 내장) | — | §7 deltas |
| 12 | `Button701` | TFlatButton | 캘린더 트리거 2 | (HTML5 picker 내장) | — | §7 deltas |
| 13 | `Button702` | TFlatButton | (보조) | **out-of-scope** | — | |
| 14 | `Button201` | TFlatButton (HIDDEN) | 신규 | **out-of-scope** | — | 원장은 read-only |
| 15 | `DateEdit1` / `DateEdit2` | TDateEdit | 캘린더 시작/끝 | (HTML5 native picker) | — | §7 deltas |
| 16 | `CornerButton1/2/9` | TCornerButton | 인쇄/엑셀 (보조) | **out-of-scope** (DEC-017 후속) | — | |

> **TabOrder 보존**: 모던 검색 영역의 키보드 흐름은 from → to → hcode → bcodeFrom → bcodeTo → scope → 조회 순. dfm 의 TabOrder 0/1 (일자) → 2 (거래처) → 4/5 (도서코드 범위) 와 의미 흐름 일치.

## 4. 중단 그리드 매핑 (DBGrid101) — 시계열 컬럼 매핑

dfm `DBGrid101` 11 컬럼 (시계열 누적):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (ledger/customer/page.tsx) | data-legacy-id |
|---|---|---|---|---|---|
| 1 | `GDATE` | 거래일자 | 일자 | `<th>일자</th>` (key gdate) | th(일자) — `data-legacy-id="Sobo32.DBGrid101.GDATE"` |
| 2 | `GPSUM` | 이동 | 수량 | `<th>이동</th>` (**gsqut** — Subu31._accumulate_row SSOT) | th(이동) — `data-legacy-id="Sobo32.DBGrid101.GPSUM"` |
| 3 | `GISUM` | 반품(입고) | 수량 | `<th>반품</th>` (gisum) | th(반품) — `data-legacy-id="Sobo32.DBGrid101.GISUM"` |
| 4 | `GIQUT` | 입고 | 수량 | `<th>입고</th>` (giqut) | th(입고) — `data-legacy-id="Sobo32.DBGrid101.GIQUT"` |
| 5 | `GJQUT` | 증정 | 수량 | `<th>증정</th>` (gjqut) | th(증정) — `data-legacy-id="Sobo32.DBGrid101.GJQUT"` |
| 6 | `GOQUT` | 출고 | 수량 | `<th>출고</th>` (goqut) | th(출고) — `data-legacy-id="Sobo32.DBGrid101.GOQUT"` |
| 7 | `GPQUT` | 폐기 | 수량 | `<th>폐기</th>` (gpqut) | th(폐기) — `data-legacy-id="Sobo32.DBGrid101.GPQUT"` |
| 8 | `GBQUT` | 비품 | 수량 | `<th>비품</th>` (gbqut) | th(비품) — `data-legacy-id="Sobo32.DBGrid101.GBQUT"` |
| 9 | `GJSUM` | 비품금 | 금액 | `<th>비품금</th>` (gjsum) | th(비품금) — `data-legacy-id="Sobo32.DBGrid101.GJSUM"` |
| 10 | `GBSUM` | 폐기금 | 금액 | `<th>폐기금</th>` (gbsum) | th(폐기금) — `data-legacy-id="Sobo32.DBGrid101.GBSUM"` |
| 11 | `GBALANCE` (없음) | — | (모던 신설) | `<th>잔량</th>` (balance_qty) | th(잔량) — `data-legacy-id="Sobo32.DBGrid101.BALANCE"` (deltas) |

> **누적식 보존**: 11개 데이터 컬럼 모두 contract `branch_table` 의 가산식과 1:1. 백엔드 `_accumulate_row` (Subu31/32 공유) 가 본 표를 재현. balance_qty 는 모던 신설로 §7 deltas 표기.

## 5. (Sobo21 한정) 하단 입력·메모 패널

본 폼(Sobo32) 에 해당 없음 — 거래처원장은 read-only.

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
|---|---|---|
| 분배 그리드 | DBGrid301 (Panel003 내, ≈9 컬럼) | 도서별 분배 = P3 후속 카드 |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 / StBar101/201 | React `loading` 흡수 |
| 신규 | Button201 (HIDDEN) | 원장은 read-only |
| 보조 | CornerButton1/2/9 (인쇄/엑셀) | DEC-017 후속 |
| 변형 | Subu32_9.dfm 의 component count 차이 | UI 분기 0건 — `customer_variants` 단언 |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
|---|---|---|---|
| 모던 신규 | bcodeTo 입력 (Edit105 노출) | search 영역 | dfm 은 HIDDEN 이었음 — Sobo31 동일 정책 |
| 모던 신규 | scope `<select>` (A/B/ALL) | search 영역 | dfm Panel102 의 Caption 토글을 명시적 enum 으로 |
| 모던 신규 | "이월 기준일" 표시 | summary 상단 | `Sv_Ghng.Max(Gdate)` (legacy_pas L303) 를 응답 메타로 노출 |
| 모던 신규 | 잔량 컬럼 (balance_qty) | DataGrid columns | dfm 시계열은 일자별 가산만, 모던은 누적 잔량 표기 |
| 모던 신규 | summary block (opening_qty/total_in/total_out/closing_qty) | DataGrid 하단 | dfm 은 별도 표시 없음 — 자기일관성 검증(AC-LDG-1) 산출용 |
| dfm out-of-scope | DBGrid301 도서별 분배 | — | P3 후속 |
| dfm out-of-scope | 인쇄/엑셀 버튼 | — | DEC-017 |

## 8. 이벤트 매핑 (의미 일치 항목만)

| dfm 이벤트 | 모던 핸들러 | 비고 |
|---|---|---|
| `FormActivate` / `FormShow` | `useEffect` mount → setError(null) | 자동 호출 없음 (hcode 필수) |
| `Button101Click` (분기 L291) | `load()` (백엔드 분기 흡수) | 분기는 backend `customer_ledger_service.get_customer_ledger` 내부 |
| `Button102Click` (메인 L301) | `load()` 의 fetch 본체 | Subu32.pas L380~L660 ≡ 백엔드 Step 2~5 |
| `Button103Click` / `Button104Click` (분기) | (백엔드 흡수) | hcode 존재 검증은 백엔드 |
| `dxButton1.OnClick` | `load()` (조회) | Button101 과 동일 |
| `Edit101Change` / `Edit102Change` | `setDateFrom` / `setDateTo` | |
| `DateEdit1.OnAcceptDate` / `DateEdit2.OnAcceptDate` | (HTML5 native picker) | §7 deltas |
| `DBGrid101TitleClick` | (정렬은 모던 1차 미적용) | 후속 (DataGridPager 기본 정렬) |
| `DataSource1DataChange` | (자동 — React state 갱신) | |

## 9. 변형 차이 (`Subu32` 본 vs `Subu32_9`)

`legacy_source_root/Subu32_9/` 산출물: 동일 `TSobo32` 클래스명. component count 31→21 (TFlatPanel 5↔7, Edit 6=6, Button 5↔2, etc.). DBGrid 컬럼·SQL·이벤트 핸들러 명·분기 누적식 동일.

→ 본 매핑 노트 차원의 UI 차이 없음. contract `customer_variants` 섹션에 `["UI 분기 0건"]` 단언으로 기록.

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (≈22 개):
  - 검색 패널 8개: `input(from)`/Edit101, `input(to)`/Edit102, `input(hcode)`/Edit107, `input(bcodeFrom)`/Edit103, `input(bcodeTo)`/Edit105, `select(scope)`/Panel102, `label(from)`/Panel101, `label(bcodeFrom)`/Panel103, `button(조회)`/dxButton1
  - 그리드 헤더 11개: GDATE/GPSUM/GISUM/GIQUT/GJQUT/GOQUT/GPQUT/GBQUT/GJSUM/GBSUM/BALANCE
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (예: DBGrid301 도서별 분배, CornerButton 인쇄).
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: from → to → hcode → bcodeFrom → bcodeTo → scope → 조회 순.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 값) 가 코드에 없음.
- [ ] PLAN-LDG-CUSTOMER §3.2 회귀 가드 R1~R7 모두 적용 (백엔드 service 레이어).

## 11. 참조

- DEC-016/017/018: 권한키/인쇄/바코드 후속.
- DEC-019: customer_variants 통합 정책.
- DEC-024: 페이지네이션 표준.
- DEC-028: dfm→html 산출물 영구 입력 동결.
- DEC-033: mysql3 호환 — 페이저/JOIN 분리 (R1~R5).
- DEC-040: 신규 SQL 0건 정책.
- DEC-046: 권한 d_select (R7).
- DEC-055: useListSession.
- 화면 카드: [`analysis/screen_cards/Sobo32.md`](../screen_cards/Sobo32.md)
- contract: [`migration/contracts/customer_book_ledger_phase2.yaml`](../../migration/contracts/customer_book_ledger_phase2.yaml) v1.1.0 endpoints.customer_single
- 회귀 테스트: [`test/test_c6_customer_ledger_phase2.py`](../../test/test_c6_customer_ledger_phase2.py)
- T0 계획: [`docs/customer-ledger-implementation-plan.md`](../../docs/customer-ledger-implementation-plan.md)
