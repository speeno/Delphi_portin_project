# 화면 카드: Sobo91 (TSobo91)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu91.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu91.pas
- 컴포넌트 수: **35** / 이벤트 수: **40** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×8, TFlatEdit×6, TmyLabel3d×5, TFlatButton×5, TCornerButton×4, TFlatComboBox×2
- 핵심 SQL 수: **31** / 영향 테이블 수: **11** / 검증 규칙 수: **7**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo91 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu91.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 8 |
| TFlatEdit | 6 |
| TmyLabel3d | 5 |
| TFlatButton | 5 |
| TCornerButton | 4 |
| TFlatComboBox | 2 |
| TSobo91 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 40

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo91.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **40** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 10 | Edit101 | Edit101KeyDown |
| OnKeyPress | 10 | Edit101 | Edit111KeyPress |
| OnChange | 7 | Edit101 | Edit101Change |
| OnClick | 5 | Button101 | Button101Click |
| OnActivate | 1 | Sobo91 | FormActivate |
| OnClose | 1 | Sobo91 | FormClose |
| OnShow | 1 | Sobo91 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **31**, 타입 분포: DELETE×2, INSERT×3, SELECT×21, UPDATE×5

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 8 |
| G4_Book | 4 |
| S1_Memo | 4 |
| G5_Ggeo | 3 |
| H2_Gbun | 3 |
| Sg_Csum | 3 |
| G1_Ggeo | 2 |
| G6_Ggeo | 1 |
| G7_Ggeo | 1 |
| T1_Gbun | 1 |
| T4_Ssub | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L378 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET Time4= now()`
- L474 **SELECT** `G5_Ggeo` — `Select Grat9 From G5_Ggeo Where`
- L483 **SELECT** `H2_Gbun` — `Select Gbigo From H2_Gbun Where`
- L510 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L543 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L597 **SELECT** `G5_Ggeo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G5_Ggeo`
- L623 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book`
- L643 **SELECT** `G6_Ggeo` — `Select Grat1,Gssum From G6_Ggeo`
- L676 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`
- L733 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`
- L741 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L757 **SELECT** `T1_Gbun` — `Select Gname From T1_Gbun Where`
- L766 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L776 **SELECT** `G1_Ggeo` — `Select Gubun From G1_Ggeo Where`
- L785 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`

_(상위 15건 표기, 전체 31건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **11**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
| Sg_Csum | 3 | 4 | 5 | 6 | 18 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **7**

| line | type | message |
| --- | --- | --- |
| 478 | message | 출고정지된 거래처입니다. 다시 선택해 주십시오. |
| 493 | message | 출고정지된 지점입니다. 다시 선택해 주십시오. |
| 1005 | empty_check |  |
| 1010 | empty_check |  |
| 1416 | empty_check |  |
| 1687 | message | 재고가 부족합니다. 확인하여 주세요. |
| 1861 | message | 삭제 하시겠습니까? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo91` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
