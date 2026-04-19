# 레이아웃 매핑: Sobo24 (반품재고-정품입고-재생) → 모던 `/returns/dispose/regen`

DEC-028 의무. C4 Phase 1 신규 매핑 — 반품 워크플로우의 **3분기 중 1: 정품 재생** (반품된 책을 정품 재고로 재입고).

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu24/Sobo24.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu24/Sobo24.html) + `Sobo24.form.json` + `Sobo24.tree.json` + `Sobo24.pas_analysis.json`
- 변형 부재 — `Subu24` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu24.dfm`](../../legacy_delphi_source/legacy_source/Subu24.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu24.pas`](../../legacy_delphi_source/legacy_source/Subu24.pas)
- 모던 라우트(예정 — T6): `/returns/dispose/regen/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/dispose/regen/*]` (T3)

## 1. 의미 분기 — 반품된 정품을 일반 재고로 환원

레거시 `Sobo24` 는 반품으로 들어온 책 중 **정품 상태가 양호한 것을 다시 정품 재고로 입고** 처리. 거래처/일자 범위로 후보 조회 → 행 선택 → 재고 환원 트랜잭션 (Sg_Csum 업데이트).

모던 Phase 1: **단일 라우트** `/returns/dispose/regen` — 검색 + 후보 그리드 + 행 선택 → "재생 처리" 버튼 → 백엔드 트랜잭션. 패스워드 게이트 (Sobo40) 통과 필수 (DEC-029).

## 2. dfm 영역 인벤토리 (tree.json)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자 from/to), Edit107/108 (출판사코드/명), Panel101 ("거래일자"), Panel104 ("출판사명"), DateEdit1/2 | `/returns/dispose/regen/page.tsx` 검색 영역 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 (7 컬럼) | `<DataGrid>` |
| 진행 패널 | `Panel007` (TFlatPanel) | 2 | ProgressBar0/1, Panel008/009/010 | React `loading` 흡수 |
| 액션 코너 | `Label301~309` + `CornerButton1~9` | n/a | "조회/검색자료/상태" | 헤더 버튼 (재생 처리, 새로고침) |
| 보조 액션 | Button700 (TO=10), dxButton1 ('검색', TO=11) | n/a | TFlatButton + TdxButton | `<Button>검색`, `<Button>재생 처리` (PRIMARY) |

## 3. 상단 검색 패널 위젯 매핑 (Panel001)

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo24.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo24.Edit102` |
| 4 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">기간</Label>` | `Sobo24.Panel101` |
| 5 | `Panel104` | TFlatPanel | "출판사명" 라벨 | `<Label htmlFor="hcode">출판사</Label>` | `Sobo24.Panel104` |
| 2 | `Edit107` | TFlatEdit (Visible=false) | 출판사코드 (보조) | (`<CustomerSearchInput type="publisher">` 통합) | `Sobo24.Edit107` |
| 3 | `Edit108` | TFlatEdit | 출판사명 | `<CustomerSearchInput id="hcode" type="publisher">` | `Sobo24.Edit108` |
| 8 | `DateEdit1` | TDateEdit | 캘린더 팝업 (from) | (HTML5 date input 내장) | — |
| 9 | `DateEdit2` | TDateEdit | 캘린더 팝업 (to) | (HTML5 date input 내장) | — |
| 6 | `Button101` (Visible=false) | TFlatButton | 조회 보조 | (`dxButton1` 통합) | — |
| 7 | `Button201` (Visible=false) | TFlatButton | 처리 보조 | (헤더 버튼 통합) | — |
| 10 | `Button700` | TFlatButton | 보조 액션 | **out-of-scope** | — |
| 11 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo24.dxButton1` |
| n/a | Label101 ("~") | TmyLabel3d | from~to 구분자 | (HTML "~" 텍스트) | — |

## 4. 중단 그리드 매핑 (DBGrid101) — 7 컬럼 후보 라인

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 거래일자 | 반품 라인의 일자 | `<th>일자</th>` | `Sobo24.DBGrid101.GDATE` |
| `BCODE` | 코드 | 도서코드 키 | `<th>도서코드</th>` | `Sobo24.DBGrid101.BCODE` |
| `BNAME` | 도서명 | 명칭 | `<th>도서명</th>` | `Sobo24.DBGrid101.BNAME` |
| `GSQUT` | 수량 | 재생 가능 수량 | `<th>수량</th>` (편집 가능 — 부분 재생) | `Sobo24.DBGrid101.GSQUT` |
| `GDANG` | 단가 | 단가 | `<th>단가</th>` | `Sobo24.DBGrid101.GDANG` |
| `GSSUM` | 금액 | 라인 금액 | `<th>금액</th>` (SUM) | `Sobo24.DBGrid101.GSSUM` |
| `GBIGO` | 적요 | 라인 메모 | `<th>적요</th>` (편집 가능) | `Sobo24.DBGrid101.GBIGO` |

> **수량/적요는 모던에서 inline edit 가능** (DEC-019 정책 — 부분 재생 허용). 행 선택 후 "재생 처리" 버튼으로 트랜잭션.

## 5. 액션 / 진행 위젯 매핑

| dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `Sobo24.Label301` | TmyLabel3d | "조\r\n회" | (모던: `<Button>조회` 흡수) | `Sobo24.Label301` |
| `Sobo24.Label302` | TmyLabel3d | "검\r\n색\r\n자\r\n료" | (모던: `<Button>재생 처리` PRIMARY) | `Sobo24.Label302` |
| `Sobo24.Label309` | TmyLabel3d | "상\r\n태" | (모던: 상단 진행 표시 텍스트) | `Sobo24.Label309` |
| `Sobo24.Panel007` | TFlatPanel | 진행 컨테이너 | (모던: React `loading` 흡수) | — (out-of-scope) |
| `Sobo24.Panel008/010` | TFlatPanel | "레코드"/"검색진행" | (모던: 상태 텍스트) | — |

## 6. out-of-scope (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` 흡수 |
| 코너 | CornerButton1/2/9 | 모던 흡수 |
| 보조 | Button700, Button101/201 (Visible=false) | 의미 흡수 |

## 7. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 패스워드 게이트 모달 | `<AuditPasswordModal>` (Sobo40) | 재고 변경 작업은 권한 인증 필수 (DEC-029) |
| 모던 신규 | "전체 선택 / 선택 행만 처리" 토글 | 그리드 헤더 | UX 개선 — 일괄 vs 부분 처리 |
| 모던 신규 | 처리 결과 토스트 | `useToast` | "N건 재생 처리 완료" |
| 모던 신규 | DataGridPager | 그리드 푸터 | dfm 모달리스 → 페이지네이션 (DEC-024) |
| dfm 흡수 | 진행률 바 | — | React `loading` boolean |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load()` |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.searchRegenerable({from, to, hcode})` |
| `DateEdit1.OnChange` / `Edit101.OnChange` | `setDateFrom` |
| `DateEdit2.OnChange` / `Edit102.OnChange` | `setDateTo` |
| `Edit107.OnChange` (출판사코드) | `setHcode` |
| (DBGrid 행 선택) | `setSelectedRows` |
| (헤더 "재생 처리" 버튼) | `<AuditPasswordModal>` 통과 → `returnsApi.regenerate({rows})` |

## 9. 변형 차이

`legacy_source_root/Subu24` 단일 폴더 — variant 0건. contract `customer_variants.Sobo24` 에 "variant 0건" 단언 (T3).

## 10. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~13개) 가 `/returns/dispose/regen/page.tsx` DOM 에 존재:
  - 검색: `Sobo24.Edit101/102/107/108`, `Sobo24.Panel101/104`, `Sobo24.dxButton1`
  - 그리드: `Sobo24.DBGrid101.{GDATE,BCODE,BNAME,GSQUT,GDANG,GSSUM,GBIGO}`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지
- [ ] DBGrid 헤더 의미가 §4 표와 일치
- [ ] **재생 처리 트랜잭션은 `<AuditPasswordModal>` (Sobo40) 통과 후에만 실행** (회귀 테스트 필수)
- [ ] DEC-028 §3 "버리는 정보" (픽셀 좌표) 가 코드에 없음

## 11. 참조

- DEC-024: 페이지네이션 표준
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029 (T8 신설): 재고 변경 작업의 패스워드 게이트 정책
- 본 폼 메인: [`Sobo23.md`](Sobo23.md)
- 자매 폼 (해체): [`Sobo25.md`](Sobo25.md)
- 패스워드 모달: [`Sobo40.md`](Sobo40.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4)
