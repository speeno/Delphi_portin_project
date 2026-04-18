# 화면 카드: Sobo17 (TSobo17)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu17.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu17.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17.pas
- 컴포넌트 수: **12** / 이벤트 수: **19** / form 등록 수: **2**
- 주요 컴포넌트: TCornerButton×3, TmyLabel3d×3, TSobo17×2, TFlatPanel×2, TDBGrid×2
- 핵심 SQL 수: **26** / 영향 테이블 수: **3** / 검증 규칙 수: **22**
- 매핑 시나리오: **C9 상품·고객 마스터 등록**

## 1. UI 구성
### TSobo17 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Subu17.dfm
| component_type | count |
| --- | --- |
| TSobo17 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 3, event_count: 9

### TSobo17 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17.dfm
| component_type | count |
| --- | --- |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo17 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 9, event_count: 10

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo17.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **19** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 2 | Sobo17 | FormActivate |
| OnClose | 2 | Sobo17 | FormClose |
| OnCreate | 2 | Sobo17 | FormCreate |
| OnPaint | 2 | Sobo17 | FormPaint |
| OnDblClick | 2 | DBGrid101 | DBGrid101DblClick |
| OnEnter | 2 | DBGrid101 | DBGrid101Enter |
| OnExit | 2 | DBGrid101 | DBGrid101Exit |
| OnKeyDown | 2 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 2 | DBGrid101 | DBGrid101KeyPress |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **26**, 타입 분포: DELETE×4, INSERT×4, SELECT×12, UPDATE×6

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G7_Ggeo | 15 |
| G7_Gbun | 10 |
| Id_Logn | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L387 **INSERT** `G7_Ggeo` — `INSERT INTO G7_Ggeo`
- L398 **SELECT** `G7_Gbun` — `Select Gcode From G7_Gbun Where Gname =`
- L445 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET`
- L552 **SELECT** `G7_Ggeo` — `Select Hcode,Gcode,Gname,Chek1,Chek2 From G7_Ggeo Where`
- L555 **DELETE** `G7_Ggeo` — `DELETE FROM G7_Ggeo WHERE Gcode=`
- L597 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET Ocode=`
- L609 **INSERT** `G7_Gbun` — `INSERT INTO G7_Gbun ( Gcode, Gname ) VALUES`
- L627 **UPDATE** `G7_Gbun` — `UPDATE G7_Gbun SET Gcode=`
- L663 **DELETE** `G7_Gbun` — `DELETE FROM G7_Gbun WHERE Gcode=`
- L685 **SELECT** `G7_Ggeo` — `Select Gcode From G7_Ggeo Where Gcode =`
- L765 **INSERT** `G7_Ggeo` — `INSERT INTO G7_Ggeo`
- L777 **SELECT** `G7_Gbun` — `Select Gcode From G7_Gbun Where`
- L836 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET`
- L858 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET Scode=`
- L908 **SELECT** `G7_Gbun` — `Select * From G7_Gbun Order By Gcode`

_(상위 15건 표기, 전체 26건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G7_Gbun | 3 | 7 | 3 | 3 | 16 | ✓ |
| Id_Logn | 0 | 9 | 4 | 0 | 13 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **22**

| line | type | message |
| --- | --- | --- |
| 381 | message | 저장 하시겠습니까? |
| 400 | empty_check |  |
| 551 | message | 삭제 하시겠습니까? |
| 565 | empty_check |  |
| 577 | empty_check |  |
| 604 | message | 저장 하시겠습니까? |
| 659 | message | 삭제 하시겠습니까? |
| 673 | empty_check |  |
| 682 | message | 코드를 입력하세요. |
| 690 | message | 코드가 이미 등록되어있습니다. 다시 입력하세요. |
| 758 | message | 저장 하시겠습니까? |
| 965 | message | 삭제 하시겠습니까? |
| 979 | empty_check |  |
| 993 | empty_check |  |
| 1020 | message | 저장 하시겠습니까? |
| 1075 | message | 삭제 하시겠습니까? |
| 1089 | empty_check |  |
| 1098 | message | 코드를 입력하세요. |
| 1106 | message | 코드가 이미 등록되어있습니다. 다시 입력하세요. |
| 2021 | message | 저장완료 |

_(상위 20건, 전체 22건)_

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo17` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C9 상품·고객 마스터 등록)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
