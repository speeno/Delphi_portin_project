# 화면 카드: Seak20 (TSeak20)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak02.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak02.pas
- 컴포넌트 수: **45** / 이벤트 수: **26** / form 등록 수: **1**
- 주요 컴포넌트: TFlatComboBox×16, TRadioButton×6, TFlatGroupBox×4, TFlatSpeedButton×4, TLabel×4, TFlatEdit×4
- 핵심 SQL 수: **6** / 영향 테이블 수: **6** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeak20 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak02.dfm
| component_type | count |
| --- | --- |
| TFlatComboBox | 16 |
| TRadioButton | 6 |
| TFlatGroupBox | 4 |
| TFlatSpeedButton | 4 |
| TLabel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 2 |
| TBitBtn | 2 |
| TSeak20 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 45, event_count: 26

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seak20.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **26** / 이벤트 종류: **7**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnChange | 12 | Edit21 | Edit21Change |
| OnClick | 6 | SpeedButton21 | SpeedButton21Click |
| OnKeyPress | 4 | Edit21 | Edit21KeyPress |
| OnClose | 1 | Seak20 | FormClose |
| OnShow | 1 | Seak20 | FormShow |
| OnDblClick | 1 | DBGrid1 | DBGrid1DblClick |
| OnExit | 1 | DBGrid1 | DBGrid1Exit |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **6**, 타입 분포: SELECT×6

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Gbun | 1 |
| G2_Gbun | 1 |
| G3_Gbun | 1 |
| G4_Gbun | 1 |
| G5_Gbun | 1 |
| G7_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L544 **SELECT** `G1_Gbun` — `Select ID, Gcode, Gname From G1_Gbun Where`
- L561 **SELECT** `G2_Gbun` — `Select ID, Gcode, Gname From G2_Gbun Where`
- L578 **SELECT** `G3_Gbun` — `Select ID, Gcode, Gname From G3_Gbun Where`
- L595 **SELECT** `G4_Gbun` — `Select ID, Gcode, Gname From G4_Gbun Where`
- L612 **SELECT** `G5_Gbun` — `Select ID, Gcode, Gname From G5_Gbun Where`
- L629 **SELECT** `G7_Gbun` — `Select ID, Gcode, Gname From G7_Gbun Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Gbun | 3 | 7 | 3 | 3 | 16 | ✓ |
| G1_Gbun | 2 | 9 | 2 | 2 | 15 | ✓ |
| G4_Gbun | 1 | 12 | 1 | 1 | 15 | ✓ |
| G2_Gbun | 1 | 3 | 1 | 1 | 6 | ✓ |
| G3_Gbun | 0 | 1 | 0 | 0 | 1 |  |
| G5_Gbun | 0 | 1 | 0 | 0 | 1 |  |
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
- (수동) 위 문서에서 form `Seak20` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
