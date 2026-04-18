# 화면 카드: Sobo45 (TSobo45)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45_1.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu45.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45_1.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu45.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45.pas
- 컴포넌트 수: **68** / 이벤트 수: **79** / form 등록 수: **4**
- 주요 컴포넌트: TFlatPanel×16, TFlatEdit×16, TFlatButton×13, TSobo45×4, TmyLabel3d×4, TFlatMaskEdit×4
- 핵심 SQL 수: **122** / 영향 테이블 수: **15** / 검증 규칙 수: **6**
- 매핑 시나리오: **C5 정산(일·월 마감)**

## 1. UI 구성
### TSobo45 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 2 |
| TSobo45 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDBGrid | 1 |
| TStatusBar | 1 |
- component_count: 15, event_count: 17

### TSobo45 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu45_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 2 |
| TSobo45 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDBGrid | 1 |
| TStatusBar | 1 |
- component_count: 15, event_count: 17

### TSobo45 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu45.dfm
| component_type | count |
| --- | --- |
| TFlatButton | 5 |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TSobo45 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGrid | 1 |
| TStatusBar | 1 |
- component_count: 19, event_count: 23

### TSobo45 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TSobo45 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TFlatComboBox | 1 |
| TdxButton | 1 |
| TStatusBar | 1 |
- component_count: 19, event_count: 22

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo45.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **79** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 16 | Edit101 | Edit101KeyDown |
| OnKeyPress | 16 | Edit101 | Edit111KeyPress |
| OnClick | 14 | Button101 | Button101Click |
| OnChange | 13 | Edit101 | Edit101Change |
| OnActivate | 4 | Sobo45 | FormActivate |
| OnClose | 4 | Sobo45 | FormClose |
| OnShow | 4 | Sobo45 | FormShow |
| OnTitleClick | 3 | DBGrid101 | DBGrid101TitleClick |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnDblClick | 1 | DBGrid101 | DBGrid101DblClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **122**, 타입 분포: INSERT×9, SELECT×102, UPDATE×11

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T2_Ssub | 25 |
| S1_Ssub | 14 |
| T3_Ssub | 12 |
| G7_Ggeo | 11 |
| G1_Ggeo | 11 |
| T1_Gbun | 6 |
| H2_Gbun | 6 |
| T1_Ssub | 5 |
| G4_Book | 5 |
| T4_Ssub | 5 |
| Sv_Ghng | 4 |
| Id_Logn | 2 |
| T6_Ssub | 2 |
| G5_Ggeo | 2 |
| T5_Ssub | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L346 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L351 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Order By Gcode`
- L361 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where Gcode=`
- L365 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where Gcode=`
- L374 **UPDATE** `Id_Logn` — `UPDATE Id_Logn SET Gpass=`
- L377 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where Gcode=`
- L377 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun`
- L385 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun`
- L393 **SELECT** `T4_Ssub` — `Select Hcode,Gcode,Gdate,Gjisa,Jubun,Gqut1,Gqut2,Gqut3 From T4_Ssub`
- L400 **SELECT** `T1_Ssub` — `Select * From T1_Ssub Where`
- L414 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2,Jumin,Giqut,Gisum,Gosum,Gssum From G7_Ggeo`
- L426 **UPDATE** `Id_Logn` — `UPDATE Id_Logn SET Gpass=`
- L462 **SELECT** `T2_Ssub` — `Select Gdate From T2_Ssub Where Gdate=`
- L466 **INSERT** `T2_Ssub` — `INSERT INTO T2_Ssub`
- L482 **SELECT** `S1_Ssub` — `Select Substring(Gdate,9,2),Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`

_(상위 15건 표기, 전체 122건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **15**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| T2_Ssub | 5 | 20 | 7 | 0 | 32 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| T3_Ssub | 7 | 5 | 7 | 0 | 19 | ✓ |
| T1_Ssub | 2 | 8 | 2 | 2 | 14 | ✓ |
| Id_Logn | 0 | 9 | 4 | 0 | 13 | ✓ |
| T5_Ssub | 1 | 5 | 1 | 1 | 8 | ✓ |
| T6_Ssub | 1 | 4 | 1 | 1 | 7 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **6**

| line | type | message |
| --- | --- | --- |
| 381 | message | 수정되었습니다. |
| 433 | message | 수정되었습니다. |
| 861 | message | 저장완료 |
| 1281 | message | 저장완료 |
| 2982 | message | 저장완료 |
| 3144 | message | 저장완료 |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo45` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C5 정산(일·월 마감))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
