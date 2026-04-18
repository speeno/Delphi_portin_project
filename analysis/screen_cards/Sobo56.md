# 화면 카드: Sobo56 (TSobo56)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu56.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu56.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu56.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu56.pas
- 컴포넌트 수: **44** / 이벤트 수: **54** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×9, TFlatButton×9, TFlatEdit×8, TmyLabel3d×4, TFlatMaskEdit×4, TDateEdit×4
- 핵심 SQL 수: **10** / 영향 테이블 수: **4** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo56 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu56.dfm
| component_type | count |
| --- | --- |
| TFlatButton | 5 |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TmyLabel3d | 2 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo56 | 1 |
| TDBGrid | 1 |
| TStatusBar | 1 |
- component_count: 22, event_count: 27

### TSobo56 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu56.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 5 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TmyLabel3d | 2 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo56 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 22, event_count: 27

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo56.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **54** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 10 | Edit101 | Edit101KeyDown |
| OnKeyPress | 10 | Edit101 | Edit111KeyPress |
| OnClick | 10 | Button101 | Button101Click |
| OnChange | 8 | Edit101 | Edit101Change |
| OnAcceptDate | 4 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 4 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 2 | Sobo56 | FormActivate |
| OnClose | 2 | Sobo56 | FormClose |
| OnShow | 2 | Sobo56 | FormShow |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **10**, 타입 분포: SELECT×10

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 2 |
| G7_Ggeo | 2 |
| G1_Ggeo | 2 |
| G4_Book | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L317 **SELECT** `` — `Select Hcode,Count(Hcode),Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L343 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L344 **SELECT** `` — `Select Hcode,Count(Hcode),Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L370 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L378 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where Gcode=`
- L384 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where Gcode=`
- L398 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where Gcode=`
- L405 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L411 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L425 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- (validation_rules 매칭 0건)

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo56` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
