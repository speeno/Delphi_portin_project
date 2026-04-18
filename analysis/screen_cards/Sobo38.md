# 화면 카드: Sobo38 (TSobo38)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu38.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu38.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu38.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu38.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38.pas
- 컴포넌트 수: **25** / 이벤트 수: **11** / form 등록 수: **3**
- 주요 컴포넌트: TFlatPanel×5, TFlatButton×4, TFlatEdit×4, TSobo38×3, TFlatRadioButton×3, TmyLabel3d×2
- 핵심 SQL 수: **2** / 영향 테이블 수: **2** / 검증 규칙 수: **4**
- 매핑 시나리오: **C3 입고 접수**

## 1. UI 구성
### TSobo38 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu38.dfm
| component_type | count |
| --- | --- |
| TSobo38 | 1 |
| TmyLabel3d | 1 |
| TFlatPanel | 1 |
| TDBGridEh | 1 |
- component_count: 4, event_count: 5

### TSobo38 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu38.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TFlatRadioButton | 3 |
| TSobo38 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGrid | 1 |
- component_count: 20, event_count: 3

### TSobo38 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38.dfm
| component_type | count |
| --- | --- |
| TSobo38 | 1 |
- component_count: 1, event_count: 3

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo38.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **11** / 이벤트 종류: **5**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 3 | Sobo38 | FormActivate |
| OnClose | 3 | Sobo38 | FormClose |
| OnShow | 3 | Sobo38 | FormShow |
| OnKeyDown | 1 | DBGrid101 | DBGrid201KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid201KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **2**, 타입 분포: SELECT×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 1 |
| G4_Book | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L513 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L520 **SELECT** `G4_Book` — `Select Gname From G4_Book Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 507 | empty_check |  |
| 552 | empty_check |  |
| 583 | empty_check |  |
| 621 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo38` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C3 입고 접수)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
