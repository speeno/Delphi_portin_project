# 레이아웃 매핑: Sobo58 (기간별반품내역서) → 모던 `/returns/period-report`

DEC-028 의무. C4 Phase 2 신규 매핑 — OQ-RT-8.

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu58/Sobo58.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu58/Sobo58.html) + `Sobo58.form.json` + `Sobo58.tree.json` + `Sobo58.pas_analysis.json`
- 변형 부재 — `Subu58` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu58.dfm`](../../legacy_delphi_source/legacy_source/Subu58.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu58.pas`](../../legacy_delphi_source/legacy_source/Subu58.pas)
- 모던 라우트(예정 — T6): `frontend/src/app/(app)/returns/period-report/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/period-report]` (T3)

## 1. 의미 분기 — 기간별 반품 내역서

레거시 `Sobo58` 은 기간 + 출판사 단위로 반품 라인을 출판사별 누계(마스터 그리드) + 라인 디테일(디테일 그리드) 로 표시. SQL 은 두 단계:
1. 마스터: `SELECT Hcode, Count(Hcode), Sum(Gsqut), Sum(Gssum) FROM S1_Ssub WHERE ... GROUP BY Hcode`
2. 디테일: `SELECT * FROM S1_Ssub WHERE ... AND Hcode=...` (선택된 출판사)

Sobo55 (일별) 와 같은 데이터 소스 (`S1_Ssub Gubun='반품'`) 이지만 집계 차원만 다름 — 일자 → 기간.

## 2. dfm 영역 인벤토리 (form.json)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자), Edit105/106 (출판사 코드/명), dxButton1 ('검색') | 검색 영역 |
| 마스터 그리드 | `Panel002` + `DBGrid101` | 1 | HCODE/HNAME (출판사별 누계 — 4 컬럼) | `<DataGrid>` 마스터 |
| 디테일 그리드 | `Panel003` + `DBGrid201` | 2 | GDATE/GCODE/GNAME/IDNUM/PUBUN/BCODE/BNAME/GSQUT/GDANG/GRAT1/GSSUM (11 컬럼 — 라인) | `<DataGrid>` 디테일 |
| 진행 패널 | `Panel007` | 3 | ProgressBar | React `loading` |
| KPI 패널 | `Panel200` | 4 | Edit201/202/203/204 (총 출판사수/총 건수/총 권수/총 금액) | `<KpiCards>` |

## 3. 상단 검색 패널 위젯 매핑 (Panel001)

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo58.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo58.Edit102` |
| 2 | `Edit103` (V=false) | TFlatEdit | 출판사코드 보조 | (CustomerSearchInput 통합) | `Sobo58.Edit103` |
| 3 | `Edit104` | TFlatEdit | 출판사명 1 | `<CustomerSearchInput type="publisher">` | `Sobo58.Edit104` |
| 4 | `Edit105` (V=false) | TFlatEdit | 출판사코드 보조2 | (선택 — Phase 2 미사용) | `Sobo58.Edit105` |
| 5 | `Edit106` | TFlatEdit | 출판사명 2 | (선택 — Phase 2 미사용) | `Sobo58.Edit106` |
| 6 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label>기간</Label>` | `Sobo58.Panel101` |
| 7 | `Panel105` | TFlatPanel | "출판사명" 라벨 | `<Label>출판사</Label>` | `Sobo58.Panel105` |
| 10/11 | `DateEdit1/2` | TDateEdit | 캘린더 | (HTML5 내장) | — |
| 12/13 | `Button701/702` | TFlatButton | 보조 | **out-of-scope** | — |
| 14 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo58.dxButton1` |
| 15 | `Panel106` | TFlatPanel | "거래처명" 라벨 | (선택 — Phase 2 미사용) | `Sobo58.Panel106` |
| 8/9 | `Button101/201` (V=false) | TFlatButton | 보조 (dxButton1 통합) | — | — |

## 4. 마스터 그리드 매핑 (DBGrid101) — 출판사별 누계

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `HCODE` | 출판사코드 | (G1_Ggeo.Gcode where Hcode='') | `<th>출판사코드</th>` | `Sobo58.DBGrid101.HCODE` |
| `HNAME` | 출판사명 | (G1_Ggeo.Gname) | `<th>출판사명</th>` | `Sobo58.DBGrid101.HNAME` |
| `Count(Hcode)` | 건수 | 라인 건수 | `<th>건수</th>` | `Sobo58.DBGrid101.COUNT` |
| `Sum(Gsqut)` | 권수 | 수량 누계 | `<th>권수</th>` | `Sobo58.DBGrid101.SUM_GSQUT` |
| `Sum(Gssum)` | 금액 | 금액 누계 | `<th>금액</th>` | `Sobo58.DBGrid101.SUM_GSSUM` |

## 5. 디테일 그리드 매핑 (DBGrid201) — 라인

| dfm FieldName | 한글 컬럼 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- |
| `GDATE` | 거래일자 | `<th>일자</th>` | `Sobo58.DBGrid201.GDATE` |
| `GCODE` | 코드 | `<th>거래처코드</th>` | `Sobo58.DBGrid201.GCODE` |
| `GNAME` | 거래처명 | `<th>거래처명</th>` | `Sobo58.DBGrid201.GNAME` |
| `IDNUM` | No | `<th>No</th>` | `Sobo58.DBGrid201.IDNUM` |
| `PUBUN` | 구분 | `<th>구분</th>` | `Sobo58.DBGrid201.PUBUN` |
| `BCODE` | 도서코드 | `<th>도서코드</th>` | `Sobo58.DBGrid201.BCODE` |
| `BNAME` | 도서명 | `<th>도서명</th>` | `Sobo58.DBGrid201.BNAME` |
| `GSQUT` | 수량 | `<th>수량</th>` | `Sobo58.DBGrid201.GSQUT` |
| `GDANG` | 단가 | `<th>단가</th>` | `Sobo58.DBGrid201.GDANG` |
| `GRAT1` | 정율 | `<th>정율</th>` | `Sobo58.DBGrid201.GRAT1` |
| `GSSUM` | 금액 | `<th>금액</th>` | `Sobo58.DBGrid201.GSSUM` |

## 6. KPI 패널 매핑 (Panel200) — Phase 2 신규

| dfm Edit | 라벨 | 모던 KPI | data-legacy-id |
| --- | --- | --- | --- |
| `Edit201` | 총 출판사수 | `<KpiCard label="출판사수">` | `Sobo58.Edit201` |
| `Edit202` | 총 건수 | `<KpiCard label="건수">` | `Sobo58.Edit202` |
| `Edit203` | 총 권수 | `<KpiCard label="권수">` | `Sobo58.Edit203` |
| `Edit204` | 총 금액 | `<KpiCard label="금액">` | `Sobo58.Edit204` |

## 7. out-of-scope (Phase 2 미사용)

- Edit105/106 (출판사명 2 — 두 번째 검색)
- Panel106 (거래처명 — 출판사 모드에서는 미사용)
- Button701/702 (보조 액션 — 운영팀 확인 후속)
- CornerButton1~9 + Label301~309 (장식 코너 액션)

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `setDefaults()` |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.periodReportQuery({from,to,hcode})` |
| `Edit101/102.OnChange` | `setDateFrom/To` |
| `Edit103/104.OnChange` | `setHcode` |
| 마스터 행 선택 | `setSelectedHcode` → 디테일 자동 로드 |

## 9. 변형 차이

`legacy_source_root/Subu58` 단일 — variant 0건. contract `customer_variants.Sobo58` 에 "variant 0건" 단언.

## 10. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~22개) 가 `/returns/period-report/page.tsx` DOM 에 존재:
  - 검색: `Sobo58.Edit101/102/103/104`, `Sobo58.Panel101/105`, `Sobo58.dxButton1`
  - 마스터: `Sobo58.DBGrid101.{HCODE,HNAME,COUNT,SUM_GSQUT,SUM_GSSUM}`
  - 디테일: `Sobo58.DBGrid201.{GDATE,GCODE,GNAME,IDNUM,PUBUN,BCODE,BNAME,GSQUT,GDANG,GRAT1,GSSUM}`
  - KPI: `Sobo58.Edit201/202/203/204`
- [ ] §7 out-of-scope 항목이 코드에 없음
- [ ] Sobo55 와 데이터 소스가 동일하므로 `daily_report` 와 `period_report_query` 가 동일 핵심 SQL 사용 — 코드 중복 금지 (공통 헬퍼)

## 11. 참조

- DEC-028, DEC-030
- OQ-RT-8 (Phase 2 신화면)
- 자매 폼: [`Sobo34_4.md`](Sobo34_4.md), [`Sobo55.md`](Sobo55.md) (일별 → 기간 확장)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml)
- 회귀 테스트: [`test/test_c4_returns_phase2.py`](../../test/test_c4_returns_phase2.py)
