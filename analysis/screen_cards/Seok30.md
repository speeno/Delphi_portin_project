# 화면 카드: Seok30 (TSeok30)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03_1.pas
- 컴포넌트 수: **73** / 이벤트 수: **43** / form 등록 수: **2**
- 주요 컴포넌트: TToolButton×26, TFlatPanel×12, TFlatMaskEdit×6, TDateEdit×6, TDBGrid×4, TSeok30×2
- 핵심 SQL 수: **17** / 영향 테이블 수: **2** / 검증 규칙 수: **4**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeok30 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03.dfm
| component_type | count |
| --- | --- |
| TToolButton | 13 |
| TFlatPanel | 6 |
| TFlatMaskEdit | 3 |
| TDateEdit | 3 |
| TDBGrid | 2 |
| TSeok30 | 1 |
| TmyLabel3d | 1 |
| TRichEdit | 1 |
| TRxRichEdit | 1 |
| TToolBar | 1 |
| TComboBox | 1 |
| TEdit | 1 |
| TUpDown | 1 |
| TBitBtn | 1 |
| TFlatCheckBox | 1 |
| TFlatButton | 1 |
- component_count: 38, event_count: 22

### TSeok30 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok03_1.dfm
| component_type | count |
| --- | --- |
| TToolButton | 13 |
| TFlatPanel | 6 |
| TFlatMaskEdit | 3 |
| TDateEdit | 3 |
| TDBGrid | 2 |
| TSeok30 | 1 |
| TmyLabel3d | 1 |
| TRichEdit | 1 |
| TToolBar | 1 |
| TComboBox | 1 |
| TEdit | 1 |
| TUpDown | 1 |
| TBitBtn | 1 |
- component_count: 35, event_count: 21

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seok30.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **43** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 19 | UndoButton | UndoButtonClick |
| OnAcceptDate | 6 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 6 | DateEdit1 | DateEdit1ButtonClick |
| OnChange | 4 | FontName | FontNameChange |
| OnActivate | 2 | Seok30 | FormActivate |
| OnClose | 2 | Seok30 | FormClose |
| OnPaint | 2 | Seok30 | FormPaint |
| OnShow | 2 | Seok30 | FormShow |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **17**, 타입 분포: DELETE×2, INSERT×2, SELECT×11, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Me_Sage | 15 |
| G7_Ggeo | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L338 **SELECT** `G7_Ggeo` — `Select Gcode,Gname From G7_Ggeo Order By Gcode`
- L347 **SELECT** `G7_Ggeo` — `Select Gcode,Gname From G7_Ggeo Where`
- L347 **SELECT** `Me_Sage` — `Select Hcode,Count(*) From Me_Sage Group by Hcode`
- L357 **SELECT** `Me_Sage` — `Select Hcode,Count(*) From Me_Sage`
- L359 **SELECT** `Me_Sage` — `Select Hcode,Count(*) From Me_Sage Where`
- L383 **SELECT** `Me_Sage` — `Select Gdate From Me_Sage Where Hcode=`
- L396 **SELECT** `Me_Sage` — `Select Gdate From Me_Sage Where`
- L406 **SELECT** `Me_Sage` — `Select Date1,Date2,Gbigo From Me_Sage`
- L421 **SELECT** `Me_Sage` — `Select Date1,Date2,Gbigo From Me_Sage`
- L421 **SELECT** `Me_Sage` — `Select Date1,Date2,Gbigo From Me_Sage Where Hcode=`
- L436 **SELECT** `Me_Sage` — `Select Date1,Date2,Gbigo From Me_Sage Where`
- L452 **UPDATE** `Me_Sage` — `UPDATE Me_Sage SET`
- L473 **UPDATE** `Me_Sage` — `UPDATE Me_Sage SET`
- L488 **INSERT** `Me_Sage` — `INSERT INTO Me_Sage`
- L497 **INSERT** `Me_Sage` — `INSERT INTO Me_Sage`

_(상위 15건 표기, 전체 17건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Me_Sage | 2 | 13 | 2 | 2 | 19 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 193 | empty_check |  |
| 197 | empty_check |  |
| 534 | message | 삭제 하시겠습니까? |
| 587 | message | 삭제 하시겠습니까? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Seok30` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
