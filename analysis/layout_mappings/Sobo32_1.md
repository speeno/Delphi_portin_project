# 레이아웃 매핑: Sobo32_1 (통합 거래처원장) — 모던 ledger/customer-integrated 페이지

DEC-028 의무. **본 노트는 phase2 → phase1 승격 직전 산출물** (PLAN-LDG-CUSTOMER-2026-04-22 의 T5(a)).

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu32_1/Sobo32_1.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu32_1/Sobo32_1.html) + `Sobo32_1.form.json` + `Sobo32_1.tree.json`
- **변형 폴더 부재** — `Subu32_1*` variant 디렉터리 0건.
- 화면 카드: [`analysis/screen_cards/Sobo32_1.md`](../screen_cards/Sobo32_1.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu32_1.dfm`](../../legacy_delphi_source/legacy_source/Subu32_1.dfm)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu32_1.pas`](../../legacy_delphi_source/legacy_source/Subu32_1.pas) — 4 SQL (G7_Ggeo×2, Sv_Ghng, G4_Book)
- 모던 라우트: [`ledger/customer-integrated/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/ledger/customer-integrated/page.tsx)
- 계약: [`migration/contracts/customer_book_ledger_phase2.yaml`](../../migration/contracts/customer_book_ledger_phase2.yaml) v1.1.0 endpoints `customer_integrated`

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유 (필수 선언)

`Sobo32_1` 은 Sobo32 와 동일 분기/누적식이지만 **그룹 단위가 거래처 (Hcode)** 로 변경된 통합 뷰. 모던 P2 → phase1 승격 1차 = **거래처 단위 합산 그리드만**.

따라서 본 매핑은:

- **거래처 단위 합산 그리드(DBGrid101) + 검색 패널만** 의미 매핑.
- 일자/도서 단위 분배는 §6 out-of-scope (단일 거래처는 `Sobo32` 사용 안내).
- 모던 신설 컬럼 `closing_qty` 는 §7 deltas.

## 2. dfm 영역 인벤토리 (Sobo32_1.tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수) | 모던 매핑 위치 |
|---|---|---|---|---|
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | ≈14 (Label 4, Panel 4, Edit 4, Button 4, CornerButton 3, dxButton1, DateEdit1, FlatMaskEdit) | `ledger/customer-integrated/page.tsx` 검색 영역 |
| 중단 거래처 그리드 | `Panel002` (TFlatPanel) | 1 | 1 (DBGrid101 = TDBGridEh, 6 컬럼) | `ledger/customer-integrated/page.tsx` DataGrid |
| 진행/상태 패널 | `Panel007` (있을 시) | n/a | n/a | **out-of-scope** — React `loading` |
| 데이터셋 | `DataSource1` | n/a | 1 | 백엔드/API 흡수 |

## 3. 상단 검색 패널 위젯 매핑 — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (page.tsx) | data-legacy-id 부착 위치 | 비고 |
|---|---|---|---|---|---|---|
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 시작 | `<Input id="from" type="date">` | input(from) — `data-legacy-id="Sobo32_1.Edit101"` | |
| 1 | `Edit102` | TFlatEdit | 거래일자 끝 | `<Input id="to" type="date">` | input(to) — `data-legacy-id="Sobo32_1.Edit102"` | |
| 2 | `Edit107` | TFlatEdit | 거래처 패턴 (선택) | `<Input id="customerPattern">` | input(customerPattern) — `data-legacy-id="Sobo32_1.Edit107"` | LIKE prefix |
| 3 | `Edit108` | TFlatEdit | (보조 — 거래처명 표시) | (응답 행에 표시) | — | 모던 = 그리드 hname 컬럼 |
| 4 | `Edit114` | TFlatEdit | (예약) | **out-of-scope** | — | |
| 5 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` | label(from) — `data-legacy-id="Sobo32_1.Panel101"` | |
| 6 | `Panel102` | TFlatPanel | (mode 토글 — 본 폼은 거래처 prefix) | `<select id="scope">` (A/B/ALL) | select(scope) — `data-legacy-id="Sobo32_1.Panel102"` | Sobo32 와 동일 정책 |
| 7 | `Button101` | TFlatButton (HIDDEN, 분기) | 조회(분기) | (내부 분기) | — | 분기는 백엔드 흡수 |
| 8 | `dxButton1` | TdxButton ("검색") | 검색 실행 | `<Button onClick=load>조회` | button(조회) — `data-legacy-id="Sobo32_1.dxButton1"` | Button101 과 동일 |
| 9 | `Button700`/`Button701` | TFlatButton | 캘린더 트리거 | (HTML5 picker 내장) | — | §7 deltas |
| 10 | `Button201` | TFlatButton (HIDDEN) | 신규 | **out-of-scope** | — | 원장은 read-only |
| 11 | `DateEdit1` | TDateEdit | 캘린더 | (HTML5 native picker) | — | §7 deltas |
| 12 | `CornerButton1/2/3` | TCornerButton | 인쇄/엑셀 (보조) | **out-of-scope** (DEC-017) | — | |

> **TabOrder 보존**: from → to → customerPattern → scope → 조회 순.

## 4. 중단 그리드 매핑 (DBGrid101) — 거래처 컬럼 매핑

dfm `DBGrid101` 6 컬럼 (거래처 합산):

| dfm 순서 | dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (ledger/customer-integrated/page.tsx) | data-legacy-id |
|---|---|---|---|---|---|
| 1 | `HCODE` | 거래처코드 | 키 | `<th>거래처</th>` (key hcode) | th(거래처) — `data-legacy-id="Sobo32_1.DBGrid101.HCODE"` |
| 2 | `HNAME` | 거래처명 | 표시 | `<th>거래처명</th>` (hname) | th(거래처명) — `data-legacy-id="Sobo32_1.DBGrid101.HNAME"` |
| 3 | `OPEN` | 이월잔량 | 수량 | `<th>이월</th>` (opening_qty) | th(이월) — `data-legacy-id="Sobo32_1.DBGrid101.OPEN"` |
| 4 | `IN_QTY` | 입고합 | 수량 | `<th>입고</th>` (period_in) | th(입고) — `data-legacy-id="Sobo32_1.DBGrid101.IN_QTY"` |
| 5 | `OUT_QTY` | 출고합 | 수량 | `<th>출고</th>` (period_out) | th(출고) — `data-legacy-id="Sobo32_1.DBGrid101.OUT_QTY"` |
| 6 | `CLOSE` (모던 신설) | 잔량 | 수량 | `<th>잔량</th>` (closing_qty) | th(잔량) — `data-legacy-id="Sobo32_1.DBGrid101.CLOSE"` (deltas) |

> **AC-LDG-3 등가성**: `closing_qty` = `opening_qty + period_in - period_out` 자기일관. AC-LDG-3 은 본 응답의 hcode 별 closing_qty 가 `Sobo32` 단일 호출의 summary.closing_qty 와 일치.

## 5. (Sobo21 한정) 하단 입력·메모 패널

본 폼(Sobo32_1) 에 해당 없음.

## 6. out-of-scope 위젯 (1차 미사용)

| 분류 | dfm 위젯 | 사유 |
|---|---|---|
| 진행 | Panel007 / ProgressBar | React `loading` 흡수 |
| 신규 | Button201 (HIDDEN) | 원장은 read-only |
| 보조 | CornerButton1/2/3 (인쇄/엑셀) | DEC-017 후속 |
| 보조 | Edit114 (예약) | 미사용 |

## 7. Deltas — 모던에 신설되었거나 dfm 에서 빠진 위젯

| 분류 | 항목 | 위치 | 사유 |
|---|---|---|---|
| 모던 신규 | scope `<select>` (A/B/ALL) | search 영역 | 일관성 — Sobo32 와 동일 |
| 모던 신규 | closing_qty 컬럼 | DataGrid columns | 자기일관성 검증(AC-LDG-3) |
| dfm out-of-scope | 인쇄/엑셀 버튼 | — | DEC-017 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
|---|---|---|
| `FormActivate` / `FormShow` | `useEffect` mount | 자동 호출 X (date 필수) |
| `Button101Click` (HIDDEN, 분기) | `load()` | 분기는 백엔드 |
| `dxButton1.OnClick` | `load()` (조회) | |
| `DBGrid101Enter` / `DBGrid101Exit` | (모던 1차 미적용) | 후속 (focus highlight) |
| `DBGrid101TitleClick` | (정렬은 1차 미적용) | DataGridPager 기본 |

## 9. 변형 차이

`Subu32_1*` variant 폴더 0건. UI/SQL variant 자체가 없음.

→ `customer_variants: ['variant 0건']` 단언.

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (≈12 개):
  - 검색 패널 6개: `input(from)`/Edit101, `input(to)`/Edit102, `input(customerPattern)`/Edit107, `select(scope)`/Panel102, `label(from)`/Panel101, `button(조회)`/dxButton1
  - 그리드 헤더 6개: HCODE/HNAME/OPEN/IN_QTY/OUT_QTY/CLOSE
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지.
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신).
- [ ] TabOrder 키보드 순회: from → to → customerPattern → scope → 조회 순.
- [ ] DEC-028 §3 "버리는 정보" (픽셀 값) 가 코드에 없음.
- [ ] PLAN-LDG-CUSTOMER §3.2 회귀 가드 R1~R7 모두 적용.

## 11. 참조

- DEC-016/017/018, DEC-019, DEC-024, DEC-028, DEC-033, DEC-040, DEC-046, DEC-055.
- 화면 카드: [`analysis/screen_cards/Sobo32_1.md`](../screen_cards/Sobo32_1.md)
- contract: [`migration/contracts/customer_book_ledger_phase2.yaml`](../../migration/contracts/customer_book_ledger_phase2.yaml) v1.1.0 endpoints.customer_integrated
- 회귀 테스트: [`test/test_c6_customer_ledger_phase2.py`](../../test/test_c6_customer_ledger_phase2.py)
- T0 계획: [`docs/customer-ledger-implementation-plan.md`](../../docs/customer-ledger-implementation-plan.md)
