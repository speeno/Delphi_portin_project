# 화면 카드: Sobo96 (TSobo96)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu96.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu96.pas
- 컴포넌트 수: **20** / 이벤트 수: **25** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatButton×4, TFlatEdit×4, TFlatRadioButton×3, TSobo96×1, TmyLabel3d×1
- 핵심 SQL 수: **24** / 영향 테이블 수: **9** / 검증 규칙 수: **2**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo96 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu96.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TFlatRadioButton | 3 |
| TSobo96 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGridEh | 1 |
- component_count: 20, event_count: 25

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo96.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **25** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 7 | Button101 | Button101Click |
| OnKeyDown | 4 | Edit101 | Edit101KeyDown |
| OnKeyPress | 4 | Edit101 | Edit111KeyPress |
| OnChange | 3 | Edit101 | Edit101Change |
| OnActivate | 1 | Sobo96 | FormActivate |
| OnClose | 1 | Sobo96 | FormClose |
| OnShow | 1 | Sobo96 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnDblClick | 1 | DBGrid101 | DBGrid201DblClick |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **24**, 타입 분포: DELETE×2, INSERT×2, SELECT×16, UPDATE×4

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 8 |
| G5_Ggeo | 4 |
| S1_Memo | 4 |
| G4_Book | 2 |
| T1_Gbun | 2 |
| G7_Ggeo | 1 |
| H2_Gbun | 1 |
| T4_Ssub | 1 |
| Sg_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L526 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L560 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L566 **SELECT** `G5_Ggeo` — `Select Gname From G5_Ggeo Where`
- L580 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L667 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`
- L700 **SELECT** `G5_Ggeo` — `Select Gname,Gadd1,Gadd2,Gtel1,Gtel2 From G5_Ggeo Where`
- L749 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`
- L768 **UPDATE** `S1_Memo` — `UPDATE S1_Memo SET Gbigo=`
- L811 **INSERT** `S1_Memo` — `INSERT INTO S1_Memo`
- L878 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`
- L927 **SELECT** `T1_Gbun` — `Select Gname From T1_Gbun Where`
- L938 **SELECT** `T1_Gbun` — `Select Gname,Bebon From T1_Gbun Where`
- L982 **SELECT** `G5_Ggeo` — `Select Pubun From G5_Ggeo Where`
- L1003 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L1028 **SELECT** `G5_Ggeo` — `Select Gubun From G5_Ggeo Where`

_(상위 15건 표기, 전체 24건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **9**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| Sg_Csum | 3 | 4 | 5 | 6 | 18 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 1477 | empty_check |  |
| 1745 | message | 삭제 하시겠습니까? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo96` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
