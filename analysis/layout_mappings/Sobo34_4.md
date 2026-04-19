# 레이아웃 매핑: Sobo34_4 (기간별재고원장 상세-폐기) → 모던 `/returns/ledger`

DEC-028 의무. C4 Phase 2 신규 매핑 — OQ-RT-8.

> **중요**: 폼 캡션은 **"기간별재고원장(상세)-폐기"** 이며 "반품 원장" 이 아님. 반품(`Gubun='반품'`) 외에 폐기/재생/해체/변경 다축 회계 검증 보고서. 모던 라우트는 `/returns/ledger` (반품 모듈 내 통합 보고서) 로 배치.

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu34_4/Sobo34_4.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu34_4/Sobo34_4.html) + `Sobo34_4.form.json` + `Sobo34_4.tree.json` + `Sobo34_4.pas_analysis.json`
- 변형 부재 — `Subu34_4` 단일 (`Subu34/34_1/34_2/34_3` 는 다른 화면)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu34_4.dfm`](../../legacy_delphi_source/legacy_source/Subu34_4.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu34_4.pas`](../../legacy_delphi_source/legacy_source/Subu34_4.pas)
- 모던 라우트(예정 — T6): `frontend/src/app/(app)/returns/ledger/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/ledger]` (T3)

## 1. 의미 분기

레거시 `Sobo34_4` 는 **기간 + 출판사 + 도서** 단위로 재고 흐름(입고/출고/조정/판매/폐기/재생/해체) 을 누계 집계하는 회계 검증 화면. SQL 은 `S1_Ssub` 와 `Sb_Csum` (집계) 와 `Sv_Ghng` (변경 이력) 를 동시 조회. Phase 2 는 1차로 **반품·폐기 축** (`Gubun IN ('반품','재생','해체','변경')`) 만 노출 — 입출고 축은 C5/C6 후속.

## 2. dfm 영역 인벤토리 (form.json)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자), Edit107/108 (출판사), Edit104/106 (도서), Panel101/102/103, dxButton1 ('검색') | 검색 영역 |
| 마스터 그리드 | `Panel002` + `DBGrid101` | 1 | GNAME/GSUSU/aPQUT/bPQUT/bPSUM/xSQUT*4/GSSUM (10 컬럼 — 도서별 누계) | `<DataGrid>` 마스터 |
| 디테일 그리드 | `Panel003` + `DBGrid201` | 2 | GDATE/GUBUN/GCODE/GNAME/GIQUT/GISUM/GOQUT/GOSUM/GJQUT/GJSUM/GBQUT/GBSUM/GPQUT/GPSUM/GSUSU/GSQUT/GSSUM/GSUMX/GSUMY/aBQUT/aPQUT/aPSUM/bBQUT/bPQUT/bPSUM/xSQUT (26 컬럼) | `<DataGrid>` 디테일 (확장 펼침) |
| 진행 패널 | `Panel007` + Panel008/009/010 | 3 | ProgressBar, "레코드/검색진행" 라벨 | React `loading` 흡수 |
| 액션 코너 | `CornerButton1~9` + `Label301~309` | n/a | "조회/검색자료/상태" | 헤더 버튼 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001)

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo34_4.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo34_4.Edit102` |
| 2 | `Edit107` (Visible=false) | TFlatEdit | 출판사코드 보조 | (CustomerSearchInput 통합) | `Sobo34_4.Edit107` |
| 3 | `Edit108` | TFlatEdit | 출판사명 | `<CustomerSearchInput type="publisher">` | `Sobo34_4.Edit108` |
| 4 | `Edit103` (Visible=false) | TFlatEdit | 도서코드 보조 | (BookSearchInput 통합) | `Sobo34_4.Edit103` |
| 5 | `Edit104` | TFlatEdit | 도서명 1 | `<BookSearchInput>` | `Sobo34_4.Edit104` |
| 6 | `Edit105` (Visible=false) | TFlatEdit | 도서코드 보조2 | (선택 — Phase 2 미사용) | `Sobo34_4.Edit105` |
| 7 | `Edit106` | TFlatEdit | 도서명 2 | (선택 — Phase 2 미사용) | `Sobo34_4.Edit106` |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label>기간</Label>` | `Sobo34_4.Panel101` |
| 9 | `Panel102` | TFlatPanel | "도서명" 라벨 | `<Label>도서</Label>` | `Sobo34_4.Panel102` |
| 18 | `Panel103` | TFlatPanel | "출판사명" 라벨 | `<Label>출판사</Label>` | `Sobo34_4.Panel103` |
| 13/14 | `DateEdit1/2` | TDateEdit | 캘린더 (from/to) | (HTML5 내장) | — |
| 15/16 | `Button701/702` | TFlatButton | 보조 액션 | **out-of-scope** | — |
| 17 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo34_4.dxButton1` |
| 10/11 | `Button101/201` (V=false) | TFlatButton | 보조 (dxButton1 통합) | — | — |
| 19 | `Button700` | TFlatButton | 보조 | **out-of-scope** | — |

## 4. 마스터 그리드 매핑 (DBGrid101) — 도서별 누계

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GNAME` | 도서명 | 도서명 (G4_Book.Gname) | `<th>도서</th>` | `Sobo34_4.DBGrid101.GNAME` |
| `GSUSU` | 입고수 | 입고 누계 수량 | `<th>입고</th>` | `Sobo34_4.DBGrid101.GSUSU` |
| `aPQUT` | 매(정품) | 정품 매출 수량 | `<th>매(정품)</th>` | `Sobo34_4.DBGrid101.aPQUT` |
| `bPQUT` | 매(상품) | 상품 매출 수량 | `<th>매(상품)</th>` | `Sobo34_4.DBGrid101.bPQUT` |
| `bPSUM` | 파기 | 파기 누계 | `<th>파기</th>` | `Sobo34_4.DBGrid101.bPSUM` |
| `xSQUT`(×4) | 기타 | 기타 (4 분류 — Sv_Ghng Field 9종 중 일부) | `<th>기타</th>`×4 | `Sobo34_4.DBGrid101.xSQUT_{1..4}` |
| `GSSUM` | 재고합계 | 회계 검증 합계 | `<th>재고</th>` | `Sobo34_4.DBGrid101.GSSUM` |

## 5. 디테일 그리드 매핑 (DBGrid201) — 일자별 트랜잭션 (26 컬럼 → Phase 2 핵심 12종만)

| dfm FieldName | Phase 2 노출 | 한글 라벨 | 비고 |
| --- | --- | --- | --- |
| `GDATE` | O | 일자 | |
| `GUBUN` | O | 구분 | 입고/출고/반품/재생/해체/변경 |
| `GCODE` | O | 거래처코드 | |
| `GNAME` | O | 거래처명 | |
| `GIQUT/GISUM` | O | 입고수/금 | |
| `GOQUT/GOSUM` | O | 출고수/금 | |
| `GJQUT/GJSUM` | O | 조정수/금 | |
| `GBQUT/GBSUM` | O | 변경수/금 | |
| `GSQUT/GSSUM` | O | 매출수/금 | |
| `GPQUT/GPSUM` | △ | 폐기수/금 | OQ-RT-3 의 9종 카탈로그 확정 후 |
| `GSUSU/GSUMX/GSUMY/aBQUT/aPQUT/aPSUM/bBQUT/bPQUT/bPSUM/xSQUT` | × | (보류) | Phase 3 후속 |

## 6. out-of-scope (Phase 2 미사용)

- Edit105/106 (도서명 2 — 두 번째 도서 검색)
- Button701/702/700 (보조 액션 — 의미 미상, 운영팀 확인 필요)
- DBGrid201 의 14종 보류 컬럼 (xSQUT/aBQUT/bBQUT 등 — OQ-RT-3 확정 후 Phase 3)
- 입고/출고/판매 축 마스터 그리드 (C5/C6 전용)

## 7. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `setDefaults()` (오늘 날짜) |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.ledgerQuery({from,to,hcode,bcode})` |
| `DateEdit1/2.OnChange` / `Edit101/102.OnChange` | `setDateFrom/To` |
| `Edit107/108.OnChange` | `setHcode` |
| `Edit103/104.OnChange` | `setBcode` |
| 마스터 행 선택 (DBGrid101 OnCellClick) | `setSelectedBcode` → 디테일 자동 로드 |
| `Button101/102/103/201/202/203Click` | (대부분 마스터/디테일 갱신 핸들러 — 모던은 단일 search 액션으로 통합) |

## 8. 변형 차이

`legacy_source_root/Subu34_4` 단일 — variant 0건. contract `customer_variants.Sobo34_4` 에 "variant 0건" 단언 (T3).

## 9. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~22개) 가 `/returns/ledger/page.tsx` DOM 에 존재
  - 검색: `Sobo34_4.Edit101/102/103/104/107/108`, `Sobo34_4.Panel101/102/103`, `Sobo34_4.dxButton1`
  - 마스터: `Sobo34_4.DBGrid101.{GNAME,GSUSU,aPQUT,bPQUT,bPSUM,xSQUT_1..4,GSSUM}`
  - 디테일: `Sobo34_4.DBGrid201.{GDATE,GUBUN,GCODE,GNAME,GIQUT,GISUM,GOQUT,GOSUM,GJQUT,GJSUM,GBQUT,GBSUM,GSQUT,GSSUM}`
- [ ] §6 out-of-scope 항목이 코드에 없음
- [ ] DBGrid201 의 보류 14종은 Phase 3 메모로 contract `deferrals` 에 명시
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 없음

## 10. 참조

- DEC-028 (dfm 영구 입력)
- DEC-030 (OQ-RT 정본 통일)
- OQ-RT-3 (Sv_Ghng Field 9종 카탈로그 — `analysis/sv_ghng_field_catalog.md`)
- OQ-RT-8 (Phase 2 신화면)
- 자매 폼: [`Sobo58.md`](Sobo58.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml)
- 회귀 테스트: [`test/test_c4_returns_phase2.py`](../../test/test_c4_returns_phase2.py)
