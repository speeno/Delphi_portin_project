# 레이아웃 매핑: Sobo22 (입고명세서) — 모던 입고 페이지

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑한다. 픽셀 좌표·폰트·색상은 가져오지 않는다.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22/Sobo22.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22/Sobo22.html) + `Sobo22.form.json` + `Sobo22.tree.json`
- 변형 1: [`Subu22_1/Sobo22_1.*`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_1/) — 사이즈/필드 구성 차이
- 변형 2: [`Subu22_2/Sobo22_2.*`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_2/) — 동일 구조, 컬럼 라벨 차이 가능
- 화면 카드: [`analysis/screen_cards/Sobo22.md`](../screen_cards/Sobo22.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu22.dfm`](../../legacy_delphi_source/legacy_source/Subu22.dfm) (1168행, EUC-KR)

## 1. 영역 분할 (모던 페이지 그리드 — 픽셀 모방 금지)

| 영역 | dfm 컨테이너 | 모던 컴포넌트 (제안) | 역할 |
| --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (8 자식) | `<section data-legacy-id="Panel001">` 검색 폼 | 거래일자/입고처/출판사/전표구분/조회 |
| 중단 라인 그리드 | `Panel002` + `DBGrid101` | `<DataGrid data-legacy-id="DBGrid101">` | 입고 상세 라인 (구분/도서코드/도서명/수량/단가/비율/금액/비고/배송) |
| 하단 입력·요약 패널 | `Panel003` (Panel201/202/203/204) | `<section data-legacy-id="Panel003">` 입력 폼 + 합계 | 전표번호/메모/주소/연락처/저장 |
| 진행 바·상태 | `Panel007` + `ProgressBar0` + `Panel008` | `<StatusBar data-legacy-id="Panel007">` | 진행 표시·상태 메시지 |
| 액션 버튼 (헤더) | `CornerButton1~3,9` | `<Toolbar>` 모던 버튼 그룹 | 조회/검색자료/참조/상태 (라벨 Label301~309 와 묶음) |

> 모던 페이지에서는 절대 픽셀 좌표 대신 CSS Grid `grid-template-rows: auto 1fr auto auto` 또는 Flex column 구성. 상단·하단 패널 폭은 100%, 그리드는 가용 높이 채우기.

## 2. 상단 검색 패널 (Panel001) 위젯 매핑 — TabOrder 보존 의무

| TabOrder | dfm 위젯 ID | 클래스 | 라벨 | 모던 컴포넌트 (제안) | 비고 |
| --- | --- | --- | --- | --- | --- |
| (라벨) | `Label100` | TmyLabel3d | 지점명 | `<Label data-legacy-id="Label100">` | 정적 표시 |
| 8 | `Panel101` | TFlatPanel | 거래일자 | `<DateInput data-legacy-id="Edit101">` (DateEdit1 와 분리, 마스크 입력) | 날짜 마스크 |
| 10 | `Panel103` | TFlatPanel | 전표구분 | `<Select data-legacy-id="Edit102">` | TFlatComboBox |
| 11 | `Panel102` | TFlatPanel | 출판사코드 | `<Input data-legacy-id="Edit103">` + 자동완성 | G7_Ggeo lookup |
| 12 | `Panel105` | TFlatPanel | 입고처명 | `<Input data-legacy-id="Edit105">` (read-only, 코드 선택 시 자동) | |
| 13 | `Panel104` | TFlatPanel | 입고처코드 | `<Input data-legacy-id="Edit104">` + 자동완성 | G1_Ggeo lookup |
| 14 | `Button101` | TFlatButton | 조회 | `<Button variant="primary" data-legacy-id="Button101">` | 클릭 → list_receipts |
| 15 | `Button201` | TFlatButton | 신규 | `<Button data-legacy-id="Button201">` | 새 행 추가 |

> **TabOrder 8→10→11→12→13→14→15 순서를 키보드 네비게이션에서 그대로 유지**. 모던 컴포넌트 `tabIndex` 속성에 동일 번호 부여 또는 DOM 순서로 자연 보장.

### 2.1 부가 위젯 (Panel001 내부, TabOrder 미할당 = mouse-only 가능)

| dfm ID | 모던 매핑 | 비고 |
| --- | --- | --- |
| `Edit106~109` | 부가 입력란 — `data-legacy-id` 부착 | 변형별 사용 여부 다름 |
| `DateEdit1` | `<DatePicker data-legacy-id="DateEdit1">` | Edit101 (마스크) 와 양방향 동기 |
| `Button701/702/801~803/901/dxButton1` | `<Button data-legacy-id="Button701">` 등 | 인쇄/저장/취소 — 1차는 일부만 활성, 나머지 disabled |

## 3. 중단 라인 그리드 (DBGrid101) 컬럼 매핑

dfm 정의(원본 EUC-KR 인용 + 디코딩):

| 순서 | FieldName (서버) | 한글 컬럼 | 모던 grid column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `PUBUN` | 구분 | `pubun` (string, lookup G1_Gbun) | 좌 정렬 |
| 2 | `BCODE` | 도서코드 | `bcode` (string, lookup G4_Book) | 좌 정렬, 자동완성 |
| 3 | `BNAME` | 도서명 | `bname` (string, read-only) | 좌 정렬 |
| 4 | `GSQUT` | 수량 | `gsqut` (number) | 우 정렬, **합계 행** |
| 5 | `GDANG` | 단가 | `gdang` (number) | 우 정렬 |
| 6 | `GRAT1` | 비율 | `grat1` (number, %) | 우 정렬 |
| 7 | `GSSUM` | 금액 | `gssum` (number) | 우 정렬, **합계 행** |
| 8 | `GBIGO` | 비고 | `gbigo` (string) | 좌 정렬 |
| 9 | `YESNO` | 배송 | `yesno` (enum '0'/'1'/'2') | 중앙 정렬, 색상 표시 |

> **합계 행** = `gsqut`, `gssum` 컬럼 footer 합계. 그리드 컴포넌트 footer prop 활성화. dfm 의 `SumList`/`Footers` 속성과 1:1.

> 컬럼 순서·라벨 모두 dfm 그대로. 변형(`Sobo22_1/_2`) 에서 컬럼 추가/제거 시 contract `customer_variants` 에 diff 로 기록(코드 분기 금지).

## 4. 하단 입력·요약 패널 (Panel003)

| dfm 위젯 | 라벨 | 모던 매핑 | 역할 |
| --- | --- | --- | --- |
| `Panel201` | (전표번호) | `<Input data-legacy-id="Panel201" readOnly>` | INSERT 시 채번 결과 표시 (Subu22.pas L760 `Max(Idnum)` 패턴) |
| `Panel202`/`Edit201~204` | 메모 1~4 | `<TextArea data-legacy-id="Edit201">` 등 | `S1_Memo` UPSERT (Subu22.pas L1216/1259) |
| `Panel203`/`Edit205~208` | 주소·연락처 | `<Input data-legacy-id="Edit205">` 등 | 매개 정보 |
| `Panel204` | (보조 패널) | (변형 차이 가능 — 1차 보존만) | |
| `Button801` | 저장 | `<Button variant="primary" data-legacy-id="Button801" type="submit">` | POST/PATCH `inbound/receipts` |
| `Button802` | 취소(폼) | `<Button data-legacy-id="Button802">` | 입력 클리어 (소프트 취소 X) |
| `Button803` | (행 삭제 → 소프트) | `<Button data-legacy-id="Button803">` | PATCH `cancel` (Yesno='2') |
| `StaticText1~4` | (합계/메시지) | `<Text data-legacy-id="StaticText1">` | 동적 합계/안내 |

## 5. 이벤트 매핑 (이벤트 → 모던 핸들러)

dfm `OnXxx` 와 모던 컴포넌트 핸들러를 1:1 로 매핑한다. 변형 폼도 동일 핸들러 이름 사용(코드 분기 금지).

| dfm 이벤트 | 모던 핸들러 | 역할 |
| --- | --- | --- |
| `FormActivate` | 페이지 mount 시 useEffect | 초기 데이터 로드 (마지막 거래일자 등) |
| `Edit101.OnExit` | `onBlur` (날짜 마스크) | 거래일자 정규화 → `_normalize_gdate` 호출 |
| `Edit104.OnChange` | `onChange` (입고처코드) | G1_Ggeo lookup → Edit105 자동 채움 |
| `Edit103.OnChange` | `onChange` (출판사코드) | G7_Ggeo lookup |
| `DBGrid101.OnEditButtonClick` (BCODE) | 도서 자동완성 모달 | G4_Book search |
| `DBGrid101.OnExit` (line) | 라인 수정 후 자동 합계 재계산 | gssum = gsqut * gdang * grat1 |
| `Button101.OnClick` (조회) | `onSubmit` of search form | GET `/api/v1/inbound/receipts` |
| `Button801.OnClick` (저장) | `onSubmit` of receipt form | POST/PATCH `/api/v1/inbound/receipts` |
| `Button803.OnClick` (취소) | `onClick` (확인 modal) | PATCH `cancel` |

## 6. 변형 차이 (`Sobo22` 본 vs `Sobo22_1` vs `Sobo22_2`)

| 항목 | Sobo22 | Sobo22_1 | Sobo22_2 | 처리 정책 |
| --- | --- | --- | --- | --- |
| 폼 크기 | 901×533 | (변형) | (변형) | 무시 (반응형) |
| `Edit106~109` 사용 여부 | 사용 | 일부 미사용 | 일부 미사용 | `customer_variants` 에 visible diff |
| DBGrid 컬럼 9개 | 9개 | (확인 필요) | (확인 필요) | T1 후속 — 변형 dfm 직접 비교 |
| 메모 슬롯 (`Edit201~204`) | 4개 | (변형) | (변형) | `customer_variants.memo_slot_count` |

> **코드 분기 금지**. 차이는 `migration/contracts/inbound_receipt.yaml` `customer_variants` 섹션에만 기록. 컴포넌트는 단일 — visible/required 만 prop 으로 분기.

## 7. 회귀 가드 체크리스트

모던 페이지 PR 머지 전 다음을 자동 검사한다.

- [ ] 본 매핑 노트의 모든 `data-legacy-id` 가 페이지 DOM 에 존재.
- [ ] DBGrid101 컬럼 9개의 FieldName 이 모두 grid 정의에 있음.
- [ ] TabOrder 8/10/11/12/13/14/15 가 키보드 Tab 순회로 동일 순서.
- [ ] 변형 차이는 `customer_variants` 에만 존재, 컴포넌트 코드에 if/switch 분기 0건.
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 들어가지 않았는지 (픽셀 left/top/width/height 등) 리뷰.

## 8. 참조

- DEC-028: dfm→html 산출물 영구 입력 동결.
- 화면 카드: [`analysis/screen_cards/Sobo22.md`](../screen_cards/Sobo22.md)
- contract: `migration/contracts/inbound_receipt.yaml` (T3 산출).
- 회귀 테스트: `test/test_c3_inbound_phase1.py` (T4 산출).
