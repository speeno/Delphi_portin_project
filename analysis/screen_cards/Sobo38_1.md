# 화면 카드: Sobo38_1 (TSobo38_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38_1.pas
- 컴포넌트 수: **20** / 이벤트 수: **11** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×7, TCornerButton×3, TmyLabel3d×3, TSobo38_1×1, TdxButton×1, TFlatMaskEdit×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **2** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo38_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu38_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo38_1 | 1 |
| TdxButton | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TFlatProgressBar | 1 |
| TProgressBar | 1 |
| TDBGridEh | 1 |
- component_count: 20, event_count: 11

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo38_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **11** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Sobo38_1 | FormActivate |
| OnClose | 1 | Sobo38_1 | FormClose |
| OnShow | 1 | Sobo38_1 | FormShow |
| OnClick | 1 | dxButton1 | Button709Click |
| OnChange | 1 | Edit101 | Edit101Change |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 1 | DBGrid101 | Button709Click |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: INSERT×1, SELECT×3, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T3_Ssub | 3 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L277 **SELECT** `G7_Ggeo` — `Select Gcode,Gname From G7_Ggeo`
- L288 **SELECT** `` — `Select Hcode,`
- L346 **SELECT** `T3_Ssub` — `Select Hcode From T3_Ssub Where`
- L357 **UPDATE** `T3_Ssub` — `UPDATE T3_Ssub SET`
- L379 **INSERT** `T3_Ssub` — `INSERT INTO T3_Ssub`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| T3_Ssub | 7 | 5 | 7 | 0 | 19 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 460 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo38_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
