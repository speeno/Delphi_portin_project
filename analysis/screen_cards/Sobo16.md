# 화면 카드: Sobo16 (TSobo16)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu16.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu16.pas
- 컴포넌트 수: **17** / 이벤트 수: **17** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatEdit×4, TCornerButton×3, TmyLabel3d×3, TSobo16×1, TFlatButton×1
- 핵심 SQL 수: **3** / 영향 테이블 수: **3** / 검증 규칙 수: **7**
- 매핑 시나리오: **C9 상품·고객 마스터 등록**

## 1. UI 구성
### TSobo16 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu16.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo16 | 1 |
| TFlatButton | 1 |
| TDBGrid | 1 |
- component_count: 17, event_count: 17

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo16.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **17** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 4 | Edit102 | Edit102KeyDown |
| OnKeyPress | 4 | Edit102 | Edit114KeyPress |
| OnChange | 3 | Edit102 | Edit101Change |
| OnActivate | 1 | Sobo16 | FormActivate |
| OnClose | 1 | Sobo16 | FormClose |
| OnShow | 1 | Sobo16 | FormShow |
| OnClick | 1 | Button101 | Button101Click |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G6_Ggeo | 1 |
| G4_Book | 1 |
| G1_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L311 **SELECT** `G6_Ggeo` — `Select * From G6_Ggeo Where`
- L335 **SELECT** `G4_Book` — `Select Gname From G4_Book Where`
- L401 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **7**

| line | type | message |
| --- | --- | --- |
| 601 | empty_check |  |
| 606 | empty_check |  |
| 642 | empty_check |  |
| 647 | empty_check |  |
| 750 | empty_check |  |
| 801 | empty_check |  |
| 852 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo16` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C9 상품·고객 마스터 등록)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
