# 화면 카드: Sobo97 (TSobo97)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu97.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu97.pas
- 컴포넌트 수: **18** / 이벤트 수: **23** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatEdit×4, TFlatButton×4, TSobo97×1, TmyLabel3d×1, TFlatMaskEdit×1
- 핵심 SQL 수: **16** / 영향 테이블 수: **8** / 검증 규칙 수: **2**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo97 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu97.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TSobo97 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 18, event_count: 23

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo97.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **23** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 5 | Button101 | Button101Click |
| OnKeyDown | 4 | Edit101 | Edit101KeyDown |
| OnKeyPress | 4 | Edit101 | Edit111KeyPress |
| OnChange | 3 | Edit101 | Edit101Change |
| OnActivate | 1 | Sobo97 | FormActivate |
| OnClose | 1 | Sobo97 | FormClose |
| OnShow | 1 | Sobo97 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnDrawColumnCell | 1 | DBGrid101 | DBGrid101DrawColumnCell |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **16**, 타입 분포: SELECT×15, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 6 |
| G7_Ggeo | 2 |
| G5_Ggeo | 2 |
| T1_Gbun | 2 |
| S4_Ssub | 1 |
| G4_Book | 1 |
| H2_Gbun | 1 |
| T4_Ssub | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L408 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where`
- L445 **SELECT** `S1_Ssub` — `Select Hcode,Count(*) From S1_Ssub Where`
- L518 **SELECT** `S1_Ssub` — `Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where`
- L592 **SELECT** `S4_Ssub` — `Select Count(*) From S4_Ssub Where`
- L631 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L655 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L661 **SELECT** `G5_Ggeo` — `Select Gname From G5_Ggeo Where`
- L678 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L697 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET Yesno=`
- L766 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`
- L816 **SELECT** `T1_Gbun` — `Select Gname From T1_Gbun Where`
- L827 **SELECT** `T1_Gbun` — `Select Gname,Bebon From T1_Gbun Where`
- L860 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L918 **SELECT** `G5_Ggeo` — `Select Gubun From G5_Ggeo Where`
- L978 **SELECT** `T4_Ssub` — `Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where`

_(상위 15건 표기, 전체 16건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **8**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| S4_Ssub | 2 | 9 | 4 | 2 | 17 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 601 | message | 가입고된 자료가 있습니다. |
| 1287 | message | 접속 장애가 발생하여 프로그램을 종료합니다. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo97` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
