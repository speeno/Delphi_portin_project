# 화면 카드: Sobo31 (TSobo31)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu31.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu31.pas
- 컴포넌트 수: **34** / 이벤트 수: **36** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×7, TmyLabel3d×6, TFlatEdit×6, TCornerButton×4, TFlatButton×4, TFlatMaskEdit×2
- 핵심 SQL 수: **9** / 영향 테이블 수: **3** / 검증 규칙 수: **4**
- 매핑 시나리오: **C6 거래/잔액 조회 (읽기 전용)**

## 1. UI 구성
### TSobo31 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu31.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TmyLabel3d | 6 |
| TFlatEdit | 6 |
| TCornerButton | 4 |
| TFlatButton | 4 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo31 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 34, event_count: 36

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo31.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **36** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnChange | 7 | Edit101 | Edit101Change |
| OnClick | 5 | Button101 | Button101Click |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 1 | Sobo31 | FormActivate |
| OnClose | 1 | Sobo31 | FormClose |
| OnShow | 1 | Sobo31 | FormShow |
| OnDblClick | 1 | DBGrid101 | Button007Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **9**, 타입 분포: SELECT×9

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G7_Ggeo | 2 |
| Sv_Ghng | 1 |
| Sb_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L282 **SELECT** `G7_Ggeo` — `Select Scode From G7_Ggeo Where`
- L336 **SELECT** `Sv_Ghng` — `Select Max(Gdate)as Gdate From Sv_Ghng`
- L366 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Bcode,Gbigo,Gsqut,Gssum`
- L472 **SELECT** `` — `Select Bdate,Scode,Gubun,Pubun,Bcode,Gbigo,Gsqut,Gssum`
- L576 **SELECT** `` — `Select Gdate,Gcode,Gbigo,Gbsum,Scode`
- L892 **SELECT** `Sb_Csum` — `Select Gdate,Gubun,Gsqut From Sb_Csum Where`
- L1078 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Gcode,Gbigo,Grat1,Gsqut,Gssum,Gjisa`
- L1232 **SELECT** `` — `Select Bdate,Scode,Gubun,Pubun,Gcode,Gbigo,Grat1,Gsqut,Gssum,Gjisa`
- L1786 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| Sb_Csum | 2 | 10 | 4 | 2 | 18 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 1776 | empty_check |  |
| 1781 | empty_check |  |
| 1816 | empty_check |  |
| 1821 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo31` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C6 거래/잔액 조회 (읽기 전용))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
