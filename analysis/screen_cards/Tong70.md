# 화면 카드: Tong70 (TTong70)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong07.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong07.pas
- 컴포넌트 수: **12** / 이벤트 수: **6** / form 등록 수: **1**
- 주요 컴포넌트: TFlatButton×4, TFlatPanel×3, TRadioButton×2, TTong70×1, TFlatEdit×1, TFlatNumber×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **4** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TTong70 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong07.dfm
| component_type | count |
| --- | --- |
| TFlatButton | 4 |
| TFlatPanel | 3 |
| TRadioButton | 2 |
| TTong70 | 1 |
| TFlatEdit | 1 |
| TFlatNumber | 1 |
- component_count: 12, event_count: 6

- 레이아웃 메타: (없음 — `analysis/form_layouts/Tong70.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **6** / 이벤트 종류: **3**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 4 | Button101 | Button101Click |
| OnKeyDown | 1 | Edit101 | Edit101KeyDown |
| OnKeyPress | 1 | Edit101 | Edit101KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: SELECT×5

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 2 |
| G1_Ggeo | 1 |
| G2_Ggwo | 1 |
| G6_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L80 **SELECT** `G4_Book` — `Select Gcode,Gname,Gjeja,Ocode,Gdang From G4_Book`
- L126 **SELECT** `G1_Ggeo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo`
- L159 **SELECT** `G2_Ggwo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G2_Ggwo`
- L254 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G4_Book`
- L269 **SELECT** `G6_Ggeo` — `Select Grat1,Gssum From G6_Ggeo`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
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
- (수동) 위 문서에서 form `Tong70` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
