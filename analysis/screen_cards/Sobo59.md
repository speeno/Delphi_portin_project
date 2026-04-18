# 화면 카드: Sobo59 (TSobo59)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_9.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_9.pas
- 컴포넌트 수: **38** / 이벤트 수: **34** / form 등록 수: **2**
- 주요 컴포넌트: TFlatEdit×7, TmyLabel3d×6, TFlatPanel×5, TFlatButton×5, TFlatMaskEdit×4, TSobo59×2
- 핵심 SQL 수: **24** / 영향 테이블 수: **20** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo59 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TmyLabel3d | 2 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo59 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 21, event_count: 27

### TSobo59 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_9.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TFlatEdit | 3 |
| TRadioGroup | 2 |
| TGroupBox | 2 |
| TFlatMaskEdit | 2 |
| TSobo59 | 1 |
| TFlatPanel | 1 |
| TFlatButton | 1 |
| TGauge | 1 |
- component_count: 17, event_count: 7

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo59.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **34** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyPress | 7 | Edit101 | Edit111KeyPress |
| OnClick | 7 | Button101 | Button101Click |
| OnKeyDown | 5 | Edit101 | Edit101KeyDown |
| OnChange | 4 | Edit101 | Edit101Change |
| OnActivate | 2 | Sobo59 | FormActivate |
| OnClose | 2 | Sobo59 | FormClose |
| OnShow | 2 | Sobo59 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **24**, 타입 분포: DELETE×19, SELECT×5

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 2 |
| G4_Book | 2 |
| G3_Gjeo | 2 |
| G7_Ggeo | 1 |
| S1_Ssub | 1 |
| H1_Ssub | 1 |
| Sv_Gsum | 1 |
| Sv_Chng | 1 |
| Gs_Gsum | 1 |
| Sg_Gsum | 1 |
| In_Gsum | 1 |
| G6_Ggeo | 1 |
| G2_Ggwo | 1 |
| G5_Ggeo | 1 |
| S3_Ssub | 1 |
| Sv_Csum | 1 |
| Sv_Ghng | 1 |
| Gs_Csum | 1 |
| Sg_Csum | 1 |
| In_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L243 **SELECT** `G3_Gjeo` — `Select Gcode From G3_Gjeo Where Gcode=`
- L273 **DELETE** `S1_Ssub` — `DELETE FROM S1_Ssub WHERE`
- L280 **DELETE** `H1_Ssub` — `DELETE FROM H1_Ssub WHERE`
- L287 **DELETE** `Sv_Gsum` — `DELETE FROM Sv_Gsum WHERE`
- L294 **DELETE** `Sv_Chng` — `DELETE FROM Sv_Chng WHERE`
- L301 **DELETE** `Gs_Gsum` — `DELETE FROM Gs_Gsum WHERE`
- L306 **DELETE** `Sg_Gsum` — `DELETE FROM Sg_Gsum WHERE`
- L311 **DELETE** `In_Gsum` — `DELETE FROM In_Gsum WHERE`
- L323 **DELETE** `G6_Ggeo` — `DELETE FROM G6_Ggeo WHERE`
- L335 **DELETE** `G1_Ggeo` — `DELETE FROM G1_Ggeo WHERE`
- L347 **DELETE** `G2_Ggwo` — `DELETE FROM G2_Ggwo WHERE`
- L359 **DELETE** `G5_Ggeo` — `DELETE FROM G5_Ggeo WHERE`
- L372 **DELETE** `S3_Ssub` — `DELETE FROM S3_Ssub WHERE`
- L377 **DELETE** `G3_Gjeo` — `DELETE FROM G3_Gjeo WHERE`
- L388 **SELECT** `` — `Select S.Hcode,Count(S.Hcode),Sum(S.Gsqut)as Gsqut,Sum(S.Gssum)as Gssum`

_(상위 15건 표기, 전체 24건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **20**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
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
| G3_Gjeo | 0 | 2 | 1 | 1 | 4 | ✓ |
| S3_Ssub | 0 | 2 | 1 | 1 | 4 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 472 | message | 완료 |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo59` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
