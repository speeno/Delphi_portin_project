# 레이아웃 매핑: Sobo25 (반품재고-반품입고-해체) → 모던 `/returns/dispose/disassemble`

DEC-028 의무. C4 Phase 1 신규 매핑 — 반품 워크플로우의 **3분기 중 2: 해체/폐기** (반품된 책 중 손상·판매불가를 해체 처리).

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu25/Sobo25.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu25/Sobo25.html) + `Sobo25.form.json` + `Sobo25.tree.json` + `Sobo25.pas_analysis.json`
- 변형 부재 — `Subu25` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu25.dfm`](../../legacy_delphi_source/legacy_source/Subu25.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu25.pas`](../../legacy_delphi_source/legacy_source/Subu25.pas)
- 모던 라우트(예정 — T6): `/returns/dispose/disassemble/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/dispose/disassemble/*]` (T3)

## 1. 의미 분기 — 반품된 책의 해체/폐기 처리

레거시 `Sobo25` 는 반품으로 들어온 책 중 **손상·판매불가 상태인 것을 해체 처리** (= 폐기 재고로 분류, 정품 재고에서 차감). Sobo24 (재생) 와 **위젯 트리·필드 구조가 1:1 동일** — 차이는 백엔드 트랜잭션의 의미와 SQL 분기뿐.

모던 Phase 1: **단일 라우트** `/returns/dispose/disassemble` — Sobo24 와 동일 UI 패턴, 백엔드 분기만 다름. 패스워드 게이트 (Sobo40) 통과 필수 (DEC-029).

## 2. dfm 영역 인벤토리 (tree.json) — Sobo24 와 동일 구조

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자 from/to), Edit107/108 (출판사코드/명), Panel101 ("거래일자"), Panel104 ("출판사명"), DateEdit1/2 | `/returns/dispose/disassemble/page.tsx` 검색 영역 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 (7 컬럼 — Sobo24 와 동일) | `<DataGrid>` |
| 진행 패널 | `Panel007` (TFlatPanel) | 2 | ProgressBar0/1, Panel008/009/010 | React `loading` 흡수 |
| 액션 코너 | `Label301~309` + `CornerButton1~9` | n/a | "조회/검색자료/상태" | 헤더 버튼 (해체 처리, 새로고침) |
| 보조 액션 | Button700 (TO=10), dxButton1 ('검색', TO=11) | n/a | TFlatButton + TdxButton | `<Button>검색`, `<Button>해체 처리` (DESTRUCTIVE) |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — Sobo24 와 동일

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo25.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo25.Edit102` |
| 4 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">기간</Label>` | `Sobo25.Panel101` |
| 5 | `Panel104` | TFlatPanel | "출판사명" 라벨 | `<Label htmlFor="hcode">출판사</Label>` | `Sobo25.Panel104` |
| 2 | `Edit107` (Visible=false) | TFlatEdit | 출판사코드 (보조) | (`<CustomerSearchInput type="publisher">` 통합) | `Sobo25.Edit107` |
| 3 | `Edit108` | TFlatEdit | 출판사명 | `<CustomerSearchInput id="hcode" type="publisher">` | `Sobo25.Edit108` |
| 8 | `DateEdit1` | TDateEdit | 캘린더 (from) | (HTML5 내장) | — |
| 9 | `DateEdit2` | TDateEdit | 캘린더 (to) | (HTML5 내장) | — |
| 6 | `Button101` (Visible=false) | TFlatButton | 조회 보조 | (dxButton1 통합) | — |
| 7 | `Button201` (Visible=false) | TFlatButton | 처리 보조 | (헤더 버튼 통합) | — |
| 10 | `Button700` | TFlatButton | 보조 액션 | **out-of-scope** | — |
| 11 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo25.dxButton1` |

## 4. 중단 그리드 매핑 (DBGrid101) — 7 컬럼 (Sobo24 동일)

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 거래일자 | 반품 라인의 일자 | `<th>일자</th>` | `Sobo25.DBGrid101.GDATE` |
| `BCODE` | 코드 | 도서코드 키 | `<th>도서코드</th>` | `Sobo25.DBGrid101.BCODE` |
| `BNAME` | 도서명 | 명칭 | `<th>도서명</th>` | `Sobo25.DBGrid101.BNAME` |
| `GSQUT` | 수량 | 해체 가능 수량 | `<th>수량</th>` (편집 가능) | `Sobo25.DBGrid101.GSQUT` |
| `GDANG` | 단가 | 단가 | `<th>단가</th>` | `Sobo25.DBGrid101.GDANG` |
| `GSSUM` | 금액 | 라인 금액 | `<th>금액</th>` (SUM) | `Sobo25.DBGrid101.GSSUM` |
| `GBIGO` | 적요 | 라인 메모 | `<th>적요</th>` (편집 가능 — 해체 사유) | `Sobo25.DBGrid101.GBIGO` |

> **해체 처리는 DESTRUCTIVE 액션** — 모던은 처리 버튼을 빨강 (variant="destructive") + 패스워드 모달 + "확인하시겠습니까?" 한 번 더 게이트.

## 5. out-of-scope (Phase 1 미사용)

Sobo24 와 동일 — Panel007/ProgressBar0/1/Panel008~010, CornerButton1/2/9, Button700, Button101/201 (Visible=false).

## 6. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 패스워드 게이트 모달 | `<AuditPasswordModal>` (Sobo40) | DESTRUCTIVE 작업 권한 인증 필수 (DEC-029) |
| 모던 신규 | "확인 다이얼로그" 추가 | `<ConfirmDialog>` | "정말 해체 처리하시겠습니까?" — 패스워드 통과 후 추가 게이트 |
| 모던 신규 | 해체 사유 필수 입력 | GBIGO 컬럼 비어있으면 처리 불가 | 감사 로그용 |
| 모던 신규 | DataGridPager | 그리드 푸터 | DEC-024 |

## 7. 이벤트 매핑 — Sobo24 와 거의 동일

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load()` |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.searchDisassemblable({from, to, hcode})` |
| `DateEdit1/2.OnChange` / `Edit101/102.OnChange` | `setDateFrom/To` |
| `Edit107.OnChange` | `setHcode` |
| (DBGrid 행 선택) | `setSelectedRows` |
| (헤더 "해체 처리" 버튼) | `<ConfirmDialog>` → `<AuditPasswordModal>` → `returnsApi.disassemble({rows, reason})` |

## 8. 변형 차이

`legacy_source_root/Subu25` 단일 폴더 — variant 0건. contract `customer_variants.Sobo25` 에 "variant 0건" 단언 (T3).

## 9. Sobo24 와의 차이 요약 (코드 분기 의도)

| 항목 | Sobo24 (재생) | Sobo25 (해체) |
| --- | --- | --- |
| UI 위젯 트리 | 동일 | 동일 |
| DBGrid 컬럼 | 동일 (7개) | 동일 (7개) |
| 핵심 액션 | 정품 재고 +Sg_Csum | 폐기 재고 분류 + 정품 재고 차감 |
| 버튼 색상 | 기본 (PRIMARY) | DESTRUCTIVE (RED) |
| 추가 게이트 | 패스워드만 | 패스워드 + 확인 다이얼로그 |
| 사유 필수 | 선택 | **필수** (감사 로그) |

→ 모던에서는 **공통 컴포넌트 `DisposeGrid` 추출** + props 로 액션 종류만 분기 (LSP/DIP 준수). data-legacy-id 는 `Sobo24.*` / `Sobo25.*` 로 별도 부착.

## 10. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~13개) 가 `/returns/dispose/disassemble/page.tsx` DOM 에 존재 (Sobo24 와 동일 구조 — `Sobo25.*` namespace)
- [ ] §5 out-of-scope 항목이 코드에 없음
- [ ] **해체 처리 트랜잭션은 `<ConfirmDialog>` + `<AuditPasswordModal>` (Sobo40) 통과 후에만 실행**
- [ ] **GBIGO (해체 사유) 가 비어있으면 처리 버튼 비활성**
- [ ] 재생/해체 공통 컴포넌트 `DisposeGrid` 가 액션 종류에 따라 분기 (Sobo24 / Sobo25 두 라우트가 같은 컴포넌트 재사용)
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 없음

## 11. 참조

- DEC-024: 페이지네이션 표준
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029 (T8 신설): 재고 변경 작업의 패스워드 게이트 정책
- 본 폼 메인: [`Sobo23.md`](Sobo23.md)
- 자매 폼 (재생): [`Sobo24.md`](Sobo24.md)
- 패스워드 모달: [`Sobo40.md`](Sobo40.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4)
