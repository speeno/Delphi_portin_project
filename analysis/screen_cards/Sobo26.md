# 화면 카드: Sobo26 (TSobo26)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu26.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/version/Subu26.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu26.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/version/Subu26.pas
- 컴포넌트 수: **40** / 이벤트 수: **50** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×8, TFlatButton×8, TFlatEdit×8, TFlatRadioButton×6, TSobo26×2, TmyLabel3d×2
- 핵심 SQL 수: **38** / 영향 테이블 수: **8** / 검증 규칙 수: **2**
- 매핑 시나리오: **C2 출고 접수(주문 입력)**

## 1. UI 구성
### TSobo26 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu26.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TFlatRadioButton | 3 |
| TSobo26 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGridEh | 1 |
- component_count: 20, event_count: 25

### TSobo26 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/version/Subu26.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TFlatRadioButton | 3 |
| TSobo26 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGridEh | 1 |
- component_count: 20, event_count: 25

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo26.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **50** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 14 | Button101 | Button101Click |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnChange | 6 | Edit101 | Edit101Change |
| OnActivate | 2 | Sobo26 | FormActivate |
| OnClose | 2 | Sobo26 | FormClose |
| OnShow | 2 | Sobo26 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnDblClick | 2 | DBGrid101 | DBGrid201DblClick |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **38**, 타입 분포: INSERT×2, SELECT×32, UPDATE×4

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 8 |
| G1_Ggeo | 8 |
| S1_Memo | 8 |
| G4_Book | 4 |
| T1_Gbun | 4 |
| G7_Ggeo | 2 |
| H2_Gbun | 2 |
| T4_Ssub | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L438 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L472 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L478 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L483 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L492 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L517 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L523 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L537 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L601 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`
- L634 **SELECT** `G1_Ggeo` — `Select Gname,Gadd1,Gadd2,Gtel1,Gtel2 From G1_Ggeo Where`
- L646 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`
- L679 **SELECT** `G1_Ggeo` — `Select Gname,Gadd1,Gadd2,Gtel1,Gtel2 From G1_Ggeo Where`
- L683 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`
- L702 **UPDATE** `S1_Memo` — `UPDATE S1_Memo SET Gbigo=`
- L728 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`

_(상위 15건 표기, 전체 38건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **8**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 1412 | empty_check |  |
| 1457 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo26` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C2 출고 접수(주문 입력))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
