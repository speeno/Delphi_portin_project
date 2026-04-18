# 화면 카드: Sobo17_1 (TSobo17_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17_1.pas
- 컴포넌트 수: **9** / 이벤트 수: **10** / form 등록 수: **1**
- 주요 컴포넌트: TCornerButton×3, TmyLabel3d×3, TSobo17_1×1, TFlatPanel×1, TDBGrid×1
- 핵심 SQL 수: **15** / 영향 테이블 수: **3** / 검증 규칙 수: **13**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo17_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu17_1.dfm
| component_type | count |
| --- | --- |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo17_1 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 9, event_count: 10

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo17_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **10** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Sobo17_1 | FormActivate |
| OnClose | 1 | Sobo17_1 | FormClose |
| OnCreate | 1 | Sobo17_1 | FormCreate |
| OnPaint | 1 | Sobo17_1 | FormPaint |
| OnDblClick | 1 | DBGrid101 | DBGrid101DblClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **15**, 타입 분포: DELETE×2, INSERT×2, SELECT×8, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G7_Ggeo | 9 |
| G7_Gbun | 5 |
| Id_Logn | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L599 **SELECT** `G7_Ggeo` — `Select Hcode,Gcode,Gname,Chek1,Chek2 From G7_Ggeo Where`
- L644 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET Ocode=`
- L811 **INSERT** `G7_Ggeo` — `INSERT INTO G7_Ggeo`
- L823 **SELECT** `G7_Gbun` — `Select Gcode From G7_Gbun Where`
- L882 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET`
- L1015 **DELETE** `G7_Ggeo` — `DELETE FROM G7_Ggeo WHERE Gcode=`
- L1071 **INSERT** `G7_Gbun` — `INSERT INTO G7_Gbun ( Gcode, Gname ) VALUES`
- L1089 **UPDATE** `G7_Gbun` — `UPDATE G7_Gbun SET Gcode=`
- L1125 **DELETE** `G7_Gbun` — `DELETE FROM G7_Gbun WHERE Gcode=`
- L1147 **SELECT** `G7_Ggeo` — `Select Gcode From G7_Ggeo Where`
- L1375 **SELECT** `G7_Gbun` — `Select * From G7_Gbun Where`
- L1433 **SELECT** `G7_Ggeo` — `Select * From G7_Ggeo Where`
- L1476 **SELECT** `G7_Ggeo` — `Select distinct Bigo2 From G7_Ggeo`
- L1914 **SELECT** `Id_Logn` — `Select Gpass From Id_Logn Where`
- L2097 **SELECT** `G7_Ggeo` — `Select Memos From G7_Ggeo`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G7_Gbun | 3 | 7 | 3 | 3 | 16 | ✓ |
| Id_Logn | 0 | 9 | 4 | 0 | 13 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **13**

| line | type | message |
| --- | --- | --- |
| 447 | empty_check |  |
| 805 | message | 저장 하시겠습니까? |
| 1011 | message | 삭제 하시겠습니까? |
| 1025 | empty_check |  |
| 1039 | empty_check |  |
| 1066 | message | 저장 하시겠습니까? |
| 1121 | message | 삭제 하시겠습니까? |
| 1135 | empty_check |  |
| 1144 | message | 코드를 입력하세요. |
| 1152 | message | 코드가 이미 등록되어있습니다. 다시 입력하세요. |
| 2077 | message | 저장완료 |
| 2079 | message | 패스워드 확인요망 |
| 2127 | message | 저장 완료. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo17_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
