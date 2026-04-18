# 화면 카드: Sobo65 (TSobo65)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu65.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu65.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu65.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu65.pas
- 컴포넌트 수: **68** / 이벤트 수: **80** / form 등록 수: **2**
- 주요 컴포넌트: TFlatEdit×16, TFlatButton×13, TFlatPanel×10, TmyLabel3d×8, TCornerButton×4, TFlatMaskEdit×4
- 핵심 SQL 수: **6** / 영향 테이블 수: **2** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo65 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu65.dfm
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
| TSobo65 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 36

### TSobo65 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu65.dfm
| component_type | count |
| --- | --- |
| TFlatEdit | 10 |
| TFlatButton | 8 |
| TFlatPanel | 5 |
| TmyLabel3d | 2 |
| TFlatMaskEdit | 2 |
| TFlatCheckBox | 2 |
| TDateEdit | 2 |
| TSobo65 | 1 |
| TDBGrid | 1 |
- component_count: 33, event_count: 44

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo65.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **80** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 18 | Edit101 | Edit101KeyDown |
| OnKeyPress | 18 | Edit101 | Edit111KeyPress |
| OnClick | 14 | Button101 | Button101Click |
| OnChange | 12 | Edit101 | Edit101Change |
| OnAcceptDate | 4 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 4 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 2 | Sobo65 | FormActivate |
| OnClose | 2 | Sobo65 | FormClose |
| OnShow | 2 | Sobo65 | FormShow |
| OnDblClick | 2 | DBGrid101 | Button007Click |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **6**, 타입 분포: SELECT×6

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 1 |
| G1_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L322 **SELECT** `` — `Select Hcode,Scode,Gubun,Pubun,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L330 **SELECT** `` — `Select Gcode,Scode,Gubun,Pubun,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L364 **SELECT** `G1_Ggeo` — `Select Gname,Gubun From G1_Ggeo Where Gcode=`
- L434 **SELECT** `` — `Select Gcode,Sum(Gbsum)as Gbsum`
- L451 **SELECT** `G1_Gbun` — `Select Gname From G1_Gbun Where Gcode=`
- L529 **SELECT** `` — `Select Gcode,Scode,Gubun,Pubun,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G1_Gbun | 2 | 9 | 2 | 2 | 15 | ✓ |
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
- (수동) 위 문서에서 form `Sobo65` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
