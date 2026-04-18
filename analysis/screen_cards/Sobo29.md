# 화면 카드: Sobo29 (TSobo29)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu29.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu29.pas
- 컴포넌트 수: **26** / 이벤트 수: **20** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×7, TmyLabel3d×6, TCornerButton×3, TFlatEdit×3, TFlatButton×2, TFlatComboBox×2
- 핵심 SQL 수: **11** / 영향 테이블 수: **4** / 검증 규칙 수: **4**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo29 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu29.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TmyLabel3d | 6 |
| TCornerButton | 3 |
| TFlatEdit | 3 |
| TFlatButton | 2 |
| TFlatComboBox | 2 |
| TSobo29 | 1 |
| TFlatMaskEdit | 1 |
| TDBGrid | 1 |
- component_count: 26, event_count: 20

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo29.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **20** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 5 | Edit101 | Edit112KeyDown |
| OnKeyPress | 5 | Edit101 | Edit111KeyPress |
| OnChange | 4 | Edit103 | Edit101Change |
| OnClick | 2 | Button101 | Button101Click |
| OnActivate | 1 | Sobo29 | FormActivate |
| OnClose | 1 | Sobo29 | FormClose |
| OnShow | 1 | Sobo29 | FormShow |
| OnDblClick | 1 | DBGrid102 | DBGrid102DblClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **11**, 타입 분포: INSERT×1, SELECT×9, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 4 |
| S1_Memo | 3 |
| S1_Ssub | 2 |
| G1_Ggeo | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L358 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L389 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L403 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L459 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book`
- L496 **SELECT** `S1_Ssub` — `Select Gdate,Bcode,Jubun From S1_Ssub Where`
- L509 **SELECT** `G4_Book` — `Select Gname From G4_Book Where`
- L713 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Ocode From G4_Book`
- L765 **SELECT** `G1_Ggeo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G1_Ggeo`
- L898 **SELECT** `S1_Memo` — `Select Gbigo From S1_Memo Where`
- L917 **UPDATE** `S1_Memo` — `UPDATE S1_Memo SET Gbigo=`
- L956 **INSERT** `S1_Memo` — `INSERT INTO S1_Memo`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 634 | empty_check |  |
| 639 | empty_check |  |
| 835 | empty_check |  |
| 996 | message | 전체메모 저장완료 |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo29` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
