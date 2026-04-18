# 화면 카드: Sobo61 (TSobo61)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu61.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu61.pas
- 컴포넌트 수: **35** / 이벤트 수: **36** / form 등록 수: **1**
- 주요 컴포넌트: TmyLabel3d×6, TFlatEdit×6, TFlatPanel×5, TFlatButton×5, TCornerButton×4, TFlatMaskEdit×2
- 핵심 SQL 수: **3** / 영향 테이블 수: **0** / 검증 규칙 수: **0**
- 매핑 시나리오: **C6 거래/잔액 조회 (읽기 전용)**

## 1. UI 구성
### TSobo61 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu61.dfm
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
| TSobo61 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 36

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo61.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **36** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnClick | 6 | Button101 | Button101Click |
| OnChange | 5 | Edit101 | Edit101Change |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 1 | Sobo61 | FormActivate |
| OnClose | 1 | Sobo61 | FormClose |
| OnShow | 1 | Sobo61 | FormShow |
| OnDblClick | 1 | DBGrid101 | Button007Click |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |

### 주요 SQL (line 오름차순 상위 15개)
- L324 **SELECT** `` — `Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L405 **SELECT** `` — `Select Gcode,Sum(Gbsum)as Gbsum`
- L502 **SELECT** `` — `Select Gcode,Scode,Gubun,Pubun,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

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
- (수동) 위 문서에서 form `Sobo61` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C6 거래/잔액 조회 (읽기 전용))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
