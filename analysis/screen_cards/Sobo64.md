# 화면 카드: Sobo64 (TSobo64)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu64.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu64.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu64.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu64.pas
- 컴포넌트 수: **63** / 이벤트 수: **62** / form 등록 수: **2**
- 주요 컴포넌트: TmyLabel3d×11, TFlatEdit×10, TFlatPanel×9, TFlatButton×9, TCornerButton×7, TFlatMaskEdit×4
- 핵심 SQL 수: **8** / 영향 테이블 수: **4** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo64 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu64.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 5 |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo64 | 1 |
| TFlatCheckBox | 1 |
| TdxButton | 1 |
| TImVarGrid | 1 |
- component_count: 28, event_count: 26

### TSobo64 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu64.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 6 |
| TFlatEdit | 6 |
| TFlatPanel | 5 |
| TFlatButton | 5 |
| TCornerButton | 4 |
| TFlatMaskEdit | 2 |
| TFlatCheckBox | 2 |
| TDateEdit | 2 |
| TSobo64 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 36

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo64.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **62** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 13 | Edit101 | Edit101KeyDown |
| OnKeyPress | 13 | Edit101 | Edit111KeyPress |
| OnClick | 11 | Button101 | Button101Click |
| OnChange | 9 | Edit101 | Edit101Change |
| OnAcceptDate | 4 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 4 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 2 | Sobo64 | FormActivate |
| OnClose | 2 | Sobo64 | FormClose |
| OnShow | 2 | Sobo64 | FormShow |
| OnDblClick | 1 | DBGrid101 | Button007Click |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **8**, 타입 분포: SELECT×8

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 2 |
| H2_Gbun | 1 |
| T1_Gbun | 1 |
| Sg_Gsum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L322 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L394 **SELECT** `Sg_Gsum` — `Select Gdate,Gbsum From Sg_Gsum Where`
- L397 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where`
- L405 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where`
- L442 **SELECT** `` — `Select substring(Gdate,1,7),Gcode,Hcode,Gjisa,Sum(Gsqut)as Gsqut`
- L490 **SELECT** `` — `Select Gcode,Scode,Gubun,Pubun,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L527 **SELECT** `G1_Ggeo` — `Select Pubun From G1_Ggeo Where`
- L602 **SELECT** `G1_Ggeo` — `Select Gubun From G1_Ggeo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| Sg_Gsum | 2 | 1 | 4 | 3 | 10 | ✓ |
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
- (수동) 위 문서에서 form `Sobo64` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
