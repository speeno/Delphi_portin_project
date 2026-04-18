# 화면 카드: Sobo43 (TSobo43)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu43.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu43.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu43.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu43.pas
- 컴포넌트 수: **40** / 이벤트 수: **50** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×10, TFlatEdit×8, TFlatButton×7, TCornerButton×3, TmyLabel3d×3, TSobo43×2
- 핵심 SQL 수: **4** / 영향 테이블 수: **2** / 검증 규칙 수: **6**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo43 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu43.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 5 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TSobo43 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TDBGrid | 1 |
- component_count: 17, event_count: 26

### TSobo43 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu43.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 5 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TFlatButton | 3 |
| TSobo43 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 23, event_count: 24

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo43.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **50** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 9 | Edit101 | Edit101KeyDown |
| OnKeyPress | 9 | Edit101 | Edit111KeyPress |
| OnChange | 8 | Edit101 | Edit101Change |
| OnClick | 8 | Button101 | Button101Click |
| OnActivate | 2 | Sobo43 | FormActivate |
| OnClose | 2 | Sobo43 | FormClose |
| OnShow | 2 | Sobo43 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 2 | DBGrid101 | DBGrid101Enter |
| OnExit | 2 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **4**, 타입 분포: SELECT×4

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T1_Ssub | 2 |
| G7_Ggeo | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L286 **SELECT** `T1_Ssub` — `Select * From T1_Ssub Where`
- L303 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where Gcode=`
- L332 **SELECT** `T1_Ssub` — `Select * From T1_Ssub Where`
- L347 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| T1_Ssub | 2 | 8 | 2 | 2 | 14 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **6**

| line | type | message |
| --- | --- | --- |
| 506 | empty_check |  |
| 572 | empty_check |  |
| 722 | message | 출판사를 등록해 주세요. |
| 769 | message | 검색을 먼저하세요 |
| 776 | message | Excel이 설치되어 있지 않습니다!!! |
| 797 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo43` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
