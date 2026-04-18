# 화면 카드: Sobo32 (TSobo32)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32_9.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32_9.pas
- 컴포넌트 수: **52** / 이벤트 수: **62** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×12, TFlatEdit×12, TmyLabel3d×7, TFlatButton×7, TFlatMaskEdit×4, TCornerButton×3
- 핵심 SQL 수: **17** / 영향 테이블 수: **5** / 검증 규칙 수: **2**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo32 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32.dfm
| component_type | count |
| --- | --- |
| TFlatEdit | 6 |
| TmyLabel3d | 5 |
| TFlatPanel | 5 |
| TFlatButton | 5 |
| TCornerButton | 3 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo32 | 1 |
| TdxButton | 1 |
| TDBGrid | 1 |
- component_count: 31, event_count: 32

### TSobo32 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu32_9.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TFlatEdit | 6 |
| TmyLabel3d | 2 |
| TFlatButton | 2 |
| TFlatMaskEdit | 2 |
| TSobo32 | 1 |
| TDBGrid | 1 |
- component_count: 21, event_count: 30

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo32.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **62** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 14 | Edit101 | Edit101KeyDown |
| OnKeyPress | 14 | Edit101 | Edit111KeyPress |
| OnChange | 12 | Edit101 | Edit101Change |
| OnClick | 8 | Button101 | Button101Click |
| OnActivate | 2 | Sobo32 | FormActivate |
| OnClose | 2 | Sobo32 | FormClose |
| OnShow | 2 | Sobo32 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnDblClick | 2 | DBGrid101 | Button007Click |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **17**, 타입 분포: SELECT×17

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 2 |
| Sv_Ghng | 2 |
| G7_Ggeo | 1 |
| G4_Gbun | 1 |
| Sb_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L293 **SELECT** `G7_Ggeo` — `Select Scode From G7_Ggeo Where`
- L303 **SELECT** `Sv_Ghng` — `Select Max(Gdate)as Gdate From Sv_Ghng`
- L328 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Bcode,Gbigo,Gsqut,Gssum`
- L392 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L400 **SELECT** `` — `Select Gdate,Gcode,Gbigo,Gbsum`
- L426 **SELECT** `G4_Book` — `Select Gname,Ocode,Gubun,Gdang From G4_Book Where`
- L516 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Gcode,Gbigo,Grat1,Gsqut,Gssum,Gjisa`
- L654 **SELECT** `` — `Select Scode,Gdate,Sum(Gbsum)as Gbsum`
- L720 **SELECT** `Sv_Ghng` — `Select Max(Gdate)as Gdate From Sv_Ghng`
- L924 **SELECT** `G4_Gbun` — `Select Gname From G4_Gbun Where`
- L1010 **SELECT** `` — `Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L1116 **SELECT** `` — `Select Scode,Gcode,Sum(Gbsum)as Gbsum`
- L1276 **SELECT** `Sb_Csum` — `Select Gcode,Gubun,Gsqut From Sb_Csum Where`
- L1590 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Bcode,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L1623 **SELECT** `G4_Book` — `Select Grat8 From G4_Book Where`

_(상위 15건 표기, 전체 17건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **5**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| Sb_Csum | 2 | 10 | 4 | 2 | 18 | ✓ |
| G4_Gbun | 1 | 12 | 1 | 1 | 15 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 719 | empty_check |  |
| 724 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo32` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
