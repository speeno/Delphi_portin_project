# 화면 카드: Sobo37 (TSobo37)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu37.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu37.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu37.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu37.pas
- 컴포넌트 수: **45** / 이벤트 수: **55** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×10, TFlatEdit×10, TmyLabel3d×6, TFlatButton×5, TFlatMaskEdit×4, TCornerButton×3
- 핵심 SQL 수: **8** / 영향 테이블 수: **6** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo37 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu37.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 5 |
| TmyLabel3d | 4 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TFlatButton | 3 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo37 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 26, event_count: 31

### TSobo37 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu37.dfm
| component_type | count |
| --- | --- |
| TFlatEdit | 6 |
| TFlatPanel | 5 |
| TmyLabel3d | 2 |
| TFlatButton | 2 |
| TFlatMaskEdit | 2 |
| TSobo37 | 1 |
| TDBGrid | 1 |
- component_count: 19, event_count: 24

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo37.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **55** / 이벤트 종류: **13**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 12 | Edit101 | Edit101KeyDown |
| OnKeyPress | 12 | Edit101 | Edit111KeyPress |
| OnChange | 10 | Edit101 | Edit101Change |
| OnClick | 6 | Button101 | Button101Click |
| OnActivate | 2 | Sobo37 | FormActivate |
| OnClose | 2 | Sobo37 | FormClose |
| OnShow | 2 | Sobo37 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnDblClick | 1 | DBGrid101 | Button007Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **8**, 타입 분포: SELECT×8

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T6_Ssub | 1 |
| G7_Ggeo | 1 |
| G1_Ggeo | 1 |
| G2_Ggwo | 1 |
| G5_Ggeo | 1 |
| Sv_Chng | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L301 **SELECT** `` — `Select Gcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L327 **SELECT** `G1_Ggeo` — `Select Gname,Ocode,Gpper From G1_Ggeo Where Gcode=`
- L329 **SELECT** `G2_Ggwo` — `Select Gname,Ocode,Gpper From G2_Ggwo Where Gcode=`
- L331 **SELECT** `G5_Ggeo` — `Select Gname,Ocode,Gpper,Gposa From G5_Ggeo Where Gcode=`
- L333 **SELECT** `T6_Ssub` — `Select * From T6_Ssub Where`
- L348 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L503 **SELECT** `` — `Select Gcode,Sum(Gbsum)as Gbsum`
- L582 **SELECT** `Sv_Chng` — `Select Max(Gdate)as Gdate From Sv_Chng`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
| Sv_Chng | 2 | 6 | 4 | 1 | 13 | ✓ |
| T6_Ssub | 1 | 4 | 1 | 1 | 7 | ✓ |
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
- (수동) 위 문서에서 form `Sobo37` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
