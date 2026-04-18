# 화면 카드: Sobo30 (TSobo30)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu30.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu30.pas
- 컴포넌트 수: **4** / 이벤트 수: **3** / form 등록 수: **1**
- 주요 컴포넌트: TSobo30×1, TImage×1, TmyLabel3d×1, TdxButton×1
- 핵심 SQL 수: **0** / 영향 테이블 수: **0** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo30 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu30.dfm
| component_type | count |
| --- | --- |
| TSobo30 | 1 |
| TImage | 1 |
| TmyLabel3d | 1 |
| TdxButton | 1 |
- component_count: 4, event_count: 3

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo30.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **3** / 이벤트 종류: **2**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 2 | myLabel3d1 | myLabel3d1Click |
| OnShow | 1 | Sobo30 | FormShow |

## 3. 데이터 액세스 (SQL)
- (query_catalog 매칭 0건)

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 70 | message | 익스플로러 실행 실패 |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo30` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
