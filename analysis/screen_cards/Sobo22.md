# 화면 카드: Sobo22 (TSobo22)

_생성: 2026-04-18 21:56 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22.pas
- 컴포넌트 수: **35** / 이벤트 수: **40** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×8, TFlatEdit×6, TmyLabel3d×5, TFlatButton×5, TCornerButton×4, TFlatComboBox×2
- 핵심 SQL 수: **14** / 영향 테이블 수: **6** / 검증 규칙 수: **3**
- 매핑 시나리오: **C3 입고 접수**
- dfm→html 산출물 (DEC-028): **3세트** — 신규 화면 포팅 시 공식 입력
  - `Subu22` → [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22/Sobo22.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22/Sobo22.html) + form.json + tree.json
  - `Subu22_1` → [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_1/Sobo22_1.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_1/Sobo22_1.html) + form.json + tree.json
  - `Subu22_2` → [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_2/Sobo22_2.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu22_2/Sobo22_2.html) + form.json + tree.json


## 1. UI 구성
### TSobo22 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 8 |
| TFlatEdit | 6 |
| TmyLabel3d | 5 |
| TFlatButton | 5 |
| TCornerButton | 4 |
| TFlatComboBox | 2 |
| TSobo22 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 35, event_count: 40

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo22.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **40** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 10 | Edit101 | Edit101KeyDown |
| OnKeyPress | 10 | Edit101 | Edit111KeyPress |
| OnChange | 7 | Edit101 | Edit101Change |
| OnClick | 5 | Button101 | Button101Click |
| OnActivate | 1 | Sobo22 | FormActivate |
| OnClose | 1 | Sobo22 | FormClose |
| OnShow | 1 | Sobo22 | FormShow |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **14**, 타입 분포: INSERT×1, SELECT×11, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Memo | 4 |
| S1_Ssub | 3 |
| G4_Book | 3 |
| G2_Ggwo | 2 |
| G6_Ggeo | 1 |
| H2_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L243 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET Time4= now()`
- L398 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L431 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L481 **SELECT** `G2_Ggwo` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G2_Ggwo`
- L507 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6,Gname,Gjeja,Gdang,Scode From G4_Book`
- L527 **SELECT** `G6_Ggeo` — `Select Grat1,Gssum From G6_Ggeo`
- L560 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`
- L760 **SELECT** `S1_Ssub` — `Select Max(Idnum) From S1_Ssub Where`
- L798 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`
- L1017 **SELECT** `G4_Book` — `Select Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 From G4_Book`
- L1197 **SELECT** `S1_Memo` — `Select Gbigo From S1_Memo Where`
- L1216 **UPDATE** `S1_Memo` — `UPDATE S1_Memo SET Gbigo=`
- L1259 **INSERT** `S1_Memo` — `INSERT INTO S1_Memo`
- L1307 **SELECT** `G2_Ggwo` — `Select Gname,Gadd1,Gadd2,Gtel1,Gtel2,Gposa From G2_Ggwo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **3**

| line | type | message |
| --- | --- | --- |
| 747 | empty_check |  |
| 752 | empty_check |  |
| 1151 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo22` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C3 입고 접수)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
- [x] dfm→html 산출물 인벤토리됨 (DEC-028, 3세트)
- [ ] layout_mappings 노트 작성됨 — `analysis/layout_mappings/Sobo22.md` (미작성 — 신규 화면 포팅 시 의무)
