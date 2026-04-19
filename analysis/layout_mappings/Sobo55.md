# 레이아웃 매핑: Sobo55 (일별 반품내역서) → 모던 `/returns/reports/daily`

DEC-028 의무. C4 Phase 1 신규 매핑 — 반품 일일 보고서. **Sobo54 (일별 입고)** + **Sobo57 (기간별 입고)** 패턴의 반품 버전.

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu55/Sobo55.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu55/Sobo55.html) + `Sobo55.form.json` + `Sobo55.tree.json` + `Sobo55.pas_analysis.json`
- 변형 부재 — `Subu55` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu55.dfm`](../../legacy_delphi_source/legacy_source/Subu55.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu55.pas`](../../legacy_delphi_source/legacy_source/Subu55.pas)
- 모던 라우트(예정 — T6): `/returns/reports/daily/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/reports/daily]` (T3)
- 자매 보고서 (Phase 2): `Subu58/Sobo58` (기간별 반품내역서)

## 1. 의미 분기 — 일별 반품 보고서 (출판사 → 라인 2단 그리드)

레거시 `Sobo55` 는 **2단 그리드 보고서**:
- DBGrid101 (상단) = 일자별 출판사 단위 집계 (3 컬럼)
- DBGrid201 (하단) = 선택된 행의 라인 상세 (10 컬럼)
- Panel200 (하단) = 총합 KPI (총 출판사수 / 총 건수 / 총 권수 / 총 금액)

모던 Phase 1: 단일 라우트 `/returns/reports/daily` — 상단 그리드 행 클릭 시 하단 라인 그리드 갱신 (master-detail 패턴, Sobo54 와 동일).

## 2. dfm 영역 인벤토리 (tree.json)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자), Edit103/104/105/106 (거래처/출판사 코드/명), Panel101/105 (라벨), DateEdit1/2 | `/returns/reports/daily/page.tsx` 검색 영역 |
| 상단 그리드 (마스터) | `Panel002` (TFlatPanel) | 1 | DBGrid101 (3 컬럼: 일자/출판사) | `<DataGrid>` 마스터 |
| 하단 그리드 (디테일) | `Panel003` (TFlatPanel) | 2 | DBGrid201 (10 컬럼: 라인 상세) | `<DataGrid>` 디테일 |
| 진행 패널 | `Panel007` (TFlatPanel) | 3 | ProgressBar0/1, Panel008~010 | React `loading` 흡수 |
| KPI 푸터 | `Panel200` (TFlatPanel) | 4 | Panel201/202/203/204 (라벨), Edit201/202/203/204 (값) | KPI 카드 / 푸터 텍스트 |
| 액션 | dxButton1 ('검색', TO=14), Button701/702 (인쇄 — TO=12/13) | n/a | TdxButton + TFlatButton | `<Button>조회`, (인쇄 = out-of-scope C7) |

## 3. 상단 검색 패널 위젯 매핑 (Panel001)

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo55.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo55.Edit102` |
| 6 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">기간</Label>` | `Sobo55.Panel101` |
| 7 | `Panel105` | TFlatPanel | "출판사명" 라벨 | `<Label htmlFor="hcode">출판사</Label>` | `Sobo55.Panel105` |
| 2 | `Edit103` (Visible=false) | TFlatEdit | 거래처코드 (보조) | (CustomerSearchInput 통합) | `Sobo55.Edit103` |
| 3 | `Edit104` | TFlatEdit | 거래처명 | `<CustomerSearchInput id="gcode">` | `Sobo55.Edit104` |
| 4 | `Edit105` (Visible=false) | TFlatEdit | 출판사코드 (보조) | (CustomerSearchInput 통합) | `Sobo55.Edit105` |
| 5 | `Edit106` | TFlatEdit | 출판사명 | `<CustomerSearchInput id="hcode" type="publisher">` | `Sobo55.Edit106` |
| 10/11 | `DateEdit1/2` | TDateEdit | 캘린더 | (HTML5 내장) | — |
| 12/13 | `Button701/702` | TFlatButton | 인쇄/미리보기 | **out-of-scope** (DEC-017 → C7) | — |
| 14 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo55.dxButton1` |
| 8 | `Button101` (Visible=false) | TFlatButton | 조회 보조 | (dxButton1 통합) | — |
| 9 | `Button201` (Visible=false) | TFlatButton | 처리 보조 | **out-of-scope** | — |
| n/a | Label101/102 ("~") | TmyLabel3d | from~to 구분자 | (HTML "~" 텍스트) | — |

## 4. 상단 그리드 (DBGrid101) — 마스터 (3 컬럼)

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 거래일자 | 일자 | `<th>일자</th>` | `Sobo55.DBGrid101.GDATE` |
| `HCODE` | 출판사코드 | 출판사 키 | `<th>출판사코드</th>` | `Sobo55.DBGrid101.HCODE` |
| `HNAME` | 출판사명 | 출판사명 | `<th>출판사</th>` | `Sobo55.DBGrid101.HNAME` |

> 행 클릭 시 하단 그리드 (DBGrid201) 가 해당 일자/출판사의 라인 상세로 갱신 (master-detail).

## 5. 하단 그리드 (DBGrid201) — 디테일 (10 컬럼)

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GCODE` | 코드 | 거래처코드 | `<th>거래처코드</th>` | `Sobo55.DBGrid201.GCODE` |
| `GNAME` | 거래처명 | 거래처명 | `<th>거래처</th>` | `Sobo55.DBGrid201.GNAME` |
| `IDNUM` | No | 라인 번호 | `<th>No</th>` | `Sobo55.DBGrid201.IDNUM` |
| `PUBUN` | 구분 | 품목 구분 | `<th>구분</th>` | `Sobo55.DBGrid201.PUBUN` |
| `BCODE` | 도서코드 | 도서 키 | `<th>도서코드</th>` | `Sobo55.DBGrid201.BCODE` |
| `BNAME` | 도서명 | 도서명 | `<th>도서명</th>` | `Sobo55.DBGrid201.BNAME` |
| `GSQUT` | 수량 | 라인 수량 | `<th>수량</th>` (SUM) | `Sobo55.DBGrid201.GSQUT` |
| `GDANG` | 단가 | 단가 | `<th>단가</th>` | `Sobo55.DBGrid201.GDANG` |
| `GRAT1` | 비율 | 할인율 | `<th>할인</th>` | `Sobo55.DBGrid201.GRAT1` |
| `GSSUM` | 금액 | 라인 금액 | `<th>금액</th>` (SUM) | `Sobo55.DBGrid201.GSSUM` |

## 6. KPI 푸터 (Panel200) — 총합 4종

| dfm 위젯 ID | 클래스 | 라벨 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `Panel201` | TFlatPanel | "총 출판사수" 라벨 | `<Card>총 출판사수</Card>` | `Sobo55.Panel201` |
| `Edit201` | TFlatEdit | (출판사수 값) | (Panel201 카드 값) | `Sobo55.Edit201` |
| `Panel202` | TFlatPanel | "총 건수" 라벨 | `<Card>총 건수</Card>` | `Sobo55.Panel202` |
| `Edit202` | TFlatEdit | (건수 값) | (Panel202 카드 값) | `Sobo55.Edit202` |
| `Panel203` | TFlatPanel | "총 권수" 라벨 | `<Card>총 권수</Card>` | `Sobo55.Panel203` |
| `Edit203` | TFlatEdit | (권수 값) | (Panel203 카드 값) | `Sobo55.Edit203` |
| `Panel204` | TFlatPanel | "총 금액" 라벨 | `<Card>총 금액</Card>` | `Sobo55.Panel204` |
| `Edit204` | TFlatEdit | (금액 값) | (Panel204 카드 값) | `Sobo55.Edit204` |

## 7. out-of-scope (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 진행 | Panel007/ProgressBar0/1/Panel008~010 | React `loading` 흡수 |
| 인쇄 | Button701/702 | DEC-017 → C7 |
| 보조 | Button101/201 (Visible=false) | 의미 흡수 |

## 8. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | DataGridPager (마스터) | 상단 그리드 푸터 | DEC-024 |
| 모던 신규 | "라인 상세" 토글 | 마스터 그리드 행 클릭 | dfm 자동 갱신 → 모던 명시적 표시 |
| 모던 신규 | KPI 카드 형태 | Panel200 흡수 | UX 개선 — 정렬·강조 |
| 모던 신규 | CSV/Excel 다운로드 버튼 | 헤더 (Phase 2) | 인쇄 대체 (DEC-017 후속) |
| dfm out-of-scope | 인쇄 트리거 | — | C7 |

## 9. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `load(today, today)` |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.dailyReport({from, to, gcode, hcode})` |
| `DateEdit1/2.OnChange` / `Edit101/102.OnChange` | `setDateFrom/To` |
| `Edit103.OnChange` (거래처코드) | `setGcode` |
| `Edit105.OnChange` (출판사코드) | `setHcode` |
| `DBGrid101.OnRowSelect` | `setSelectedMasterRow` → 디테일 그리드 갱신 |
| `Button701Click` (인쇄) | (out-of-scope C7) |

## 10. 변형 차이

`legacy_source_root/Subu55` 단일 — variant 0건. contract `customer_variants.Sobo55` 에 "variant 0건" 단언 (T3).

## 11. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~26개) 가 `/returns/reports/daily/page.tsx` DOM 에 존재:
  - 검색: `Sobo55.Edit101/102/103/104/105/106`, `Sobo55.Panel101/105`, `Sobo55.dxButton1`
  - 마스터 그리드: `Sobo55.DBGrid101.{GDATE,HCODE,HNAME}`
  - 디테일 그리드: `Sobo55.DBGrid201.{GCODE,GNAME,IDNUM,PUBUN,BCODE,BNAME,GSQUT,GDANG,GRAT1,GSSUM}`
  - KPI: `Sobo55.Panel201/202/203/204`, `Sobo55.Edit201/202/203/204`
- [ ] §7 out-of-scope 항목이 코드에 없음
- [ ] DBGrid 헤더 의미가 §4·§5 표와 일치 (라벨 변경 시 본 노트 동시 갱신)
- [ ] master-detail 동작: 상단 그리드 행 클릭 → 하단 그리드 갱신
- [ ] KPI 4종이 모두 표시 (출판사수/건수/권수/금액)
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 없음
- [ ] 보고서이므로 패스워드 게이트 **불필요** (Sobo24/25/51 과 다름)

## 12. 참조

- DEC-017: 인쇄 트리거 → C7
- DEC-024: 페이지네이션 표준
- DEC-028: dfm→html 산출물 영구 입력 동결
- 본 폼 메인: [`Sobo23.md`](Sobo23.md)
- 자매 보고서 (입고): [`Sobo54.md`](Sobo54.md), [`Sobo57.md`](Sobo57.md)
- 자매 보고서 (Phase 2): Subu58 (기간별 반품내역서)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4)
