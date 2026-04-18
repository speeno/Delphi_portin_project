# 화면 카드: Sobo21 (TSobo21)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu21.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu21.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu21.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu21.pas
- 컴포넌트 수: **56** / 이벤트 수: **72** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×16, TFlatEdit×11, TFlatButton×7, TmyLabel3d×6, TFlatComboBox×4, TCornerButton×4
- 핵심 SQL 수: **45** / 영향 테이블 수: **9** / 검증 규칙 수: **13**
- 매핑 시나리오: **C6 거래/잔액 조회 (읽기 전용)**

## 1. UI 구성
### TSobo21 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu21.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 8 |
| TFlatEdit | 5 |
| TFlatButton | 2 |
| TFlatComboBox | 2 |
| TSobo21 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDBGrid | 1 |
- component_count: 21, event_count: 32

### TSobo21 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu21.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 8 |
| TFlatEdit | 6 |
| TmyLabel3d | 5 |
| TFlatButton | 5 |
| TCornerButton | 4 |
| TFlatComboBox | 2 |
| TSobo21 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 40

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo21.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **72** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 19 | Edit101 | Edit101KeyDown |
| OnKeyPress | 19 | Edit101 | Edit111KeyPress |
| OnChange | 13 | Edit101 | Edit101Change |
| OnClick | 7 | Button101 | Button101Click |
| OnActivate | 2 | Sobo21 | FormActivate |
| OnClose | 2 | Sobo21 | FormClose |
| OnShow | 2 | Sobo21 | FormShow |
| OnEnter | 2 | DBGrid101 | DBGrid101Enter |
| OnExit | 2 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **45**, 타입 분포: INSERT×2, SELECT×40, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 9 |
| S1_Ssub | 8 |
| G4_Book | 7 |
| S1_Memo | 7 |
| H2_Gbun | 6 |
| G6_Ggeo | 2 |
| G7_Ggeo | 2 |
| T1_Gbun | 2 |
| T4_Ssub | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L289 **SELECT** `S1_Ssub` — `Select Time3,Time4 From S1_Ssub Where`
- L327 **SELECT** `G1_Ggeo` — `Select Grat9 From G1_Ggeo Where Hcode=`
- L334 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET Time4= now()`
- L336 **SELECT** `H2_Gbun` — `Select Gbigo From H2_Gbun Where`
- L362 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L397 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where Gcode=`
- L449 **SELECT** `G1_Ggeo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo`
- L467 **SELECT** `G1_Ggeo` — `Select Grat9 From G1_Ggeo Where`
- L475 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book`
- L476 **SELECT** `H2_Gbun` — `Select Gbigo From H2_Gbun Where`
- L495 **SELECT** `G6_Ggeo` — `Select Grat1,Gssum From G6_Ggeo`
- L503 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L527 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`
- L536 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L581 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`

_(상위 15건 표기, 전체 45건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **9**
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
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **13**

| line | type | message |
| --- | --- | --- |
| 309 | message | 재출력 명세서 입니다. 출력하시겠습니까? |
| 331 | message | 출고정지된 거래처입니다. 다시 선택해 주십시오. |
| 346 | message | 출고정지된 지점입니다. 다시 선택해 주십시오. |
| 390 | message | 재출력 명세서 입니다. 출력하시겠습니까? |
| 471 | message | 출고정지된 거래처입니다. 다시 선택해 주십시오. |
| 486 | message | 출고정지된 지점입니다. 다시 선택해 주십시오. |
| 851 | empty_check |  |
| 856 | empty_check |  |
| 998 | empty_check |  |
| 1003 | empty_check |  |
| 1262 | empty_check |  |
| 1409 | empty_check |  |
| 1680 | message | 재고가 부족합니다. 확인하여 주세요. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo21` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C6 거래/잔액 조회 (읽기 전용))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
