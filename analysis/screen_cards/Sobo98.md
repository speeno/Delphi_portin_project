# 화면 카드: Sobo98 (TSobo98)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu98.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu98.pas
- 컴포넌트 수: **18** / 이벤트 수: **24** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatEdit×4, TFlatButton×4, TSobo98×1, TmyLabel3d×1, TFlatMaskEdit×1
- 핵심 SQL 수: **3** / 영향 테이블 수: **2** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo98 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu98.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TSobo98 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 18, event_count: 24

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo98.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **24** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 5 | Button101 | Button101Click |
| OnKeyDown | 4 | Edit101 | Edit101KeyDown |
| OnKeyPress | 4 | Edit101 | Edit111KeyPress |
| OnChange | 3 | Edit101 | Edit101Change |
| OnActivate | 1 | Sobo98 | FormActivate |
| OnClose | 1 | Sobo98 | FormClose |
| OnShow | 1 | Sobo98 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnDblClick | 1 | DBGrid101 | DBGrid101DblClick |
| OnDrawColumnCell | 1 | DBGrid101 | DBGrid101DrawColumnCell |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G7_Ggeo | 1 |
| S1_Memo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L373 **SELECT** `` — `Select S.Gdate,S.Hcode,S.Gcode,S.Jubun,S.Gjisa,Y.Gname,Y.Gtel1,Y.Gtel2,Sum(S.Gsqut),Sum(S.Gssum)`
- L404 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L499 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
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
- (수동) 위 문서에서 form `Sobo98` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
