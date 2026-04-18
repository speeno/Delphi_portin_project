# 화면 카드: Sobo14_1 (TSobo14_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14_1.pas
- 컴포넌트 수: **19** / 이벤트 수: **14** / form 등록 수: **1**
- 주요 컴포넌트: TmyLabel3d×4, TCornerButton×3, TFlatPanel×3, TFlatEdit×3, TdxButton×2, TSobo14_1×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **2** / 검증 규칙 수: **5**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo14_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14_1.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TCornerButton | 3 |
| TFlatPanel | 3 |
| TFlatEdit | 3 |
| TdxButton | 2 |
| TSobo14_1 | 1 |
| TFlatComboBox | 1 |
| TFlatButton | 1 |
| TDBGridEh | 1 |
- component_count: 19, event_count: 14

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo14_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **14** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 3 | Edit102 | Edit114KeyDown |
| OnKeyPress | 3 | Edit102 | Edit114KeyPress |
| OnClick | 3 | Button701 | Button701Click |
| OnActivate | 1 | Sobo14_1 | FormActivate |
| OnClose | 1 | Sobo14_1 | FormClose |
| OnShow | 1 | Sobo14_1 | FormShow |
| OnDrawColumnCell | 1 | DBGrid101 | DBGrid101DrawColumnCell |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: SELECT×4, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 4 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L291 **SELECT** `G7_Ggeo` — `Select Gcode From G7_Ggeo Where`
- L296 **SELECT** `G4_Book` — `Select Id,Gcode,Gname,Gisbn,Gpost,Opost From G4_Book Where`
- L381 **SELECT** `G4_Book` — `Select count(*) From G4_Book Where`
- L396 **UPDATE** `G4_Book` — `UPDATE G4_Book SET`
- L466 **SELECT** `G4_Book` — `select gcode from G4_Book`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **5**

| line | type | message |
| --- | --- | --- |
| 309 | empty_check |  |
| 486 | empty_check |  |
| 502 | empty_check |  |
| 504 | message | 출판사코드, 도서명을 확인하시기 바랍니다 |
| 558 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo14_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
