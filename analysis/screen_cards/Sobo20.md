# 화면 카드: Sobo20 (TSobo20)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu20.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu20.pas
- 컴포넌트 수: **21** / 이벤트 수: **26** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×7, TFlatEdit×5, TFlatComboBox×2, TFlatButton×2, TBitBtn×2, TSobo20×1
- 핵심 SQL 수: **3** / 영향 테이블 수: **3** / 검증 규칙 수: **8**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo20 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu20.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TFlatEdit | 5 |
| TFlatComboBox | 2 |
| TFlatButton | 2 |
| TBitBtn | 2 |
| TSobo20 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
- component_count: 21, event_count: 26

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo20.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **26** / 이벤트 종류: **6**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnChange | 7 | Edit101 | Edit101Change |
| OnClose | 1 | Sobo20 | FormClose |
| OnShow | 1 | Sobo20 | FormShow |
| OnClick | 1 | BitBtn101 | Button101Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×1, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 1 |
| S1_Memo | 1 |
| H2_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L332 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET`
- L364 **UPDATE** `S1_Memo` — `UPDATE S1_Memo SET`
- L592 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **8**

| line | type | message |
| --- | --- | --- |
| 568 | empty_check |  |
| 573 | empty_check |  |
| 620 | empty_check |  |
| 625 | empty_check |  |
| 672 | empty_check |  |
| 677 | empty_check |  |
| 724 | empty_check |  |
| 729 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo20` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
