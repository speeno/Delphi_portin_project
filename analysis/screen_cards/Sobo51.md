# 화면 카드: Sobo51 (TSobo51)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu51.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu51.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu51.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu51.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu51.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu51.pas
- 컴포넌트 수: **52** / 이벤트 수: **46** / form 등록 수: **3**
- 주요 컴포넌트: TFlatPanel×9, TmyLabel3d×9, TFlatEdit×8, TFlatButton×6, TFlatMaskEdit×4, TSobo51×3
- 핵심 SQL 수: **40** / 영향 테이블 수: **20** / 검증 규칙 수: **4**
- 매핑 시나리오: **C4 반품 처리**

## 1. UI 구성
### TSobo51 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu51.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TFlatEdit | 4 |
| TRadioGroup | 2 |
| TGroupBox | 2 |
| TSobo51 | 1 |
| TFlatPanel | 1 |
| TFlatButton | 1 |
| TGauge | 1 |
- component_count: 16, event_count: 7

### TSobo51 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu51.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 2 |
| TFlatMaskEdit | 2 |
| TFlatEdit | 2 |
| TSobo51 | 1 |
| TmyLabel3d | 1 |
| TStatusBar | 1 |
- component_count: 13, event_count: 14

### TSobo51 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu51.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TFlatPanel | 4 |
| TCornerButton | 3 |
| TFlatButton | 3 |
| TFlatMaskEdit | 2 |
| TFlatEdit | 2 |
| TDateEdit | 2 |
| TSobo51 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 23, event_count: 25

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo51.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **46** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyPress | 9 | Edit101 | Edit114KeyPress |
| OnClick | 8 | RadioGroup1 | Button201Click |
| OnKeyDown | 7 | Edit101 | Edit101KeyDown |
| OnChange | 6 | Edit101 | Edit101Change |
| OnActivate | 3 | Sobo51 | FormActivate |
| OnClose | 3 | Sobo51 | FormClose |
| OnShow | 3 | Sobo51 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **40**, 타입 분포: DELETE×3, INSERT×2, SELECT×6, UPDATE×29

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 3 |
| G6_Ggeo | 3 |
| G1_Ggeo | 3 |
| G5_Ggeo | 3 |
| Sv_Ghng | 3 |
| Sg_Csum | 3 |
| G3_Gjeo | 2 |
| H1_Ssub | 2 |
| Sv_Gsum | 2 |
| Sv_Chng | 2 |
| Gs_Gsum | 2 |
| Sg_Gsum | 2 |
| In_Gsum | 2 |
| G4_Book | 2 |
| S2_Ssub | 1 |
| G2_Ggwo | 1 |
| S3_Ssub | 1 |
| Sv_Csum | 1 |
| Gs_Csum | 1 |
| In_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L262 **SELECT** `G3_Gjeo` — `Select Gcode From G3_Gjeo Where Gcode=`
- L281 **SELECT** `Sg_Csum` — `Select * From Sg_Csum Where`
- L296 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET Gcode=`
- L299 **SELECT** `Sg_Csum` — `Select * From Sg_Csum Where`
- L307 **UPDATE** `H1_Ssub` — `UPDATE H1_Ssub SET Gcode=`
- L318 **UPDATE** `Sv_Gsum` — `UPDATE Sv_Gsum SET Gcode=`
- L329 **UPDATE** `Sv_Chng` — `UPDATE Sv_Chng SET Gcode=`
- L338 **UPDATE** `Gs_Gsum` — `UPDATE Gs_Gsum SET Gcode=`
- L347 **UPDATE** `Sg_Gsum` — `UPDATE Sg_Gsum SET Gcode=`
- L356 **UPDATE** `In_Gsum` — `UPDATE In_Gsum SET Gcode=`
- L370 **UPDATE** `G6_Ggeo` — `UPDATE G6_Ggeo SET Gcode=`
- L378 **UPDATE** `G1_Ggeo` — `UPDATE G1_Ggeo SET Gcode=`
- L391 **UPDATE** `S2_Ssub` — `UPDATE S2_Ssub SET Gcode=`
- L399 **UPDATE** `G2_Ggwo` — `UPDATE G2_Ggwo SET Gcode=`
- L411 **UPDATE** `G5_Ggeo` — `UPDATE G5_Ggeo SET Gcode=`

_(상위 15건 표기, 전체 40건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **20**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
| Sg_Csum | 3 | 4 | 5 | 6 | 18 | ✓ |
| Sv_Chng | 2 | 6 | 4 | 1 | 13 | ✓ |
| Sv_Csum | 3 | 5 | 3 | 2 | 13 | ✓ |
| Sv_Gsum | 2 | 4 | 4 | 1 | 11 | ✓ |
| Sg_Gsum | 2 | 1 | 4 | 3 | 10 | ✓ |
| Gs_Gsum | 2 | 2 | 4 | 1 | 9 | ✓ |
| H1_Ssub | 2 | 0 | 4 | 3 | 9 | ✓ |
| In_Gsum | 2 | 0 | 4 | 3 | 9 | ✓ |
| Gs_Csum | 2 | 2 | 3 | 1 | 8 | ✓ |
| In_Csum | 2 | 0 | 3 | 3 | 8 | ✓ |
| S2_Ssub | 2 | 0 | 3 | 2 | 7 | ✓ |
| G3_Gjeo | 0 | 2 | 1 | 1 | 4 | ✓ |
| S3_Ssub | 0 | 2 | 1 | 1 | 4 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 521 | empty_check |  |
| 538 | empty_check |  |
| 759 | message | 완료 |
| 1327 | message | 완료 |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo51` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C4 반품 처리)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
