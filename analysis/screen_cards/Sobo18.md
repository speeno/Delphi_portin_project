# 화면 카드: Sobo18 (TSobo18)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu18.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu18.pas
- 컴포넌트 수: **17** / 이벤트 수: **8** / form 등록 수: **1**
- 주요 컴포넌트: TmyLabel3d×4, TCornerButton×3, TFlatPanel×3, TFlatEdit×2, TSobo18×1, TFlatComboBox×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **2** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo18 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu18.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TCornerButton | 3 |
| TFlatPanel | 3 |
| TFlatEdit | 2 |
| TSobo18 | 1 |
| TFlatComboBox | 1 |
| TFlatButton | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 17, event_count: 8

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo18.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **8** / 이벤트 종류: **7**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 2 | Button701 | Button701Click |
| OnActivate | 1 | Sobo18 | FormActivate |
| OnClose | 1 | Sobo18 | FormClose |
| OnShow | 1 | Sobo18 | FormShow |
| OnChange | 1 | Edit901 | Button709Click |
| OnKeyDown | 1 | Edit102 | Edit114KeyDown |
| OnKeyPress | 1 | Edit102 | Edit114KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: SELECT×3, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G7_Ggeo | 3 |
| G4_Book | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L285 **SELECT** `G7_Ggeo` — `Select Gcode From G7_Ggeo Where`
- L289 **SELECT** `G7_Ggeo` — `Select Yesno From G7_Ggeo Where`
- L300 **SELECT** `G4_Book` — `Select Gcode,Yesno From G4_Book Where`
- L364 **UPDATE** `G4_Book` — `UPDATE G4_Book SET Yesno=`
- L379 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET Yesno=`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
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
- (수동) 위 문서에서 form `Sobo18` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
