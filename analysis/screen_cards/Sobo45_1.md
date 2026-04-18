# 화면 카드: Sobo45_1 (TSobo45_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45_1.pas
- 컴포넌트 수: **19** / 이벤트 수: **22** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatButton×4, TFlatEdit×4, TSobo45_1×1, TmyLabel3d×1, TFlatMaskEdit×1
- 핵심 SQL 수: **40** / 영향 테이블 수: **15** / 검증 규칙 수: **2**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo45_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu45_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TSobo45_1 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TFlatComboBox | 1 |
| TdxButton | 1 |
| TStatusBar | 1 |
- component_count: 19, event_count: 22

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo45_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **22** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 5 | Button101 | Button101Click |
| OnChange | 4 | Edit100 | Edit101Change |
| OnKeyDown | 4 | Edit100 | Edit101KeyDown |
| OnKeyPress | 4 | Edit100 | Edit111KeyPress |
| OnActivate | 1 | Sobo45_1 | FormActivate |
| OnClose | 1 | Sobo45_1 | FormClose |
| OnShow | 1 | Sobo45_1 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **40**, 타입 분포: INSERT×2, SELECT×35, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T2_Ssub | 7 |
| S1_Ssub | 5 |
| G7_Ggeo | 4 |
| G1_Ggeo | 3 |
| T3_Ssub | 3 |
| H2_Gbun | 2 |
| T1_Gbun | 2 |
| T4_Ssub | 2 |
| G4_Book | 2 |
| Id_Logn | 1 |
| T1_Ssub | 1 |
| T6_Ssub | 1 |
| G5_Ggeo | 1 |
| T5_Ssub | 1 |
| Sv_Ghng | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L426 **UPDATE** `Id_Logn` — `UPDATE Id_Logn SET Gpass=`
- L576 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where`
- L584 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where`
- L592 **SELECT** `T4_Ssub` — `Select Hcode,Gcode,Gdate,Gjisa,Jubun,Pubun,Gqut1,Gqut2,Gqut3 From T4_Ssub`
- L613 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2,Jumin,Giqut,Gisum,Yes35,Gssum,Chek1 From G7_Ggeo Where`
- L652 **SELECT** `T2_Ssub` — `Select Hcode,Chek1,Chek2 From T2_Ssub`
- L723 **SELECT** `S1_Ssub` — `Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut,Substring(S.Gdate,9,2) From S1_Ssub S, G4_Book Y`
- L822 **SELECT** `S1_Ssub` — `Select Substring(Gdate,9,2),Gcode,Jubun,Gjisa,Sum(Gsqut) From S1_Ssub Where`
- L883 **SELECT** `T4_Ssub` — `Select Gqut1,Gqut2 From T4_Ssub Where`
- L905 **SELECT** `T1_Gbun` — `Select Gname From T1_Gbun Where`
- L915 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L979 **SELECT** `G1_Ggeo` — `Select Pubun From G1_Ggeo Where`
- L1008 **SELECT** `G1_Ggeo` — `Select Gubun From G1_Ggeo Where`
- L1039 **SELECT** `T1_Ssub` — `Select Gdate,Gcode,Gname,Name1,Name2,Gssum From T1_Ssub Where`
- L1083 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`

_(상위 15건 표기, 전체 40건은 `analysis/query_catalog.json` 참조)_

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
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 433 | message | 수정되었습니다. |
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
- (수동) 위 문서에서 form `Sobo45_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
