# 화면 카드: Sobo36 (TSobo36)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu36.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu36.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu36.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu36.pas
- 컴포넌트 수: **43** / 이벤트 수: **48** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×10, TFlatEdit×10, TmyLabel3d×6, TFlatButton×5, TCornerButton×3, TFlatMaskEdit×3
- 핵심 SQL 수: **11** / 영향 테이블 수: **3** / 검증 규칙 수: **3**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo36 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu36.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 5 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TFlatButton | 3 |
| TSobo36 | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 23, event_count: 24

### TSobo36 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu36.dfm
| component_type | count |
| --- | --- |
| TFlatEdit | 6 |
| TFlatPanel | 5 |
| TmyLabel3d | 3 |
| TFlatButton | 2 |
| TFlatMaskEdit | 2 |
| TSobo36 | 1 |
| TDBGrid | 1 |
- component_count: 20, event_count: 24

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo36.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **48** / 이벤트 종류: **13**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 10 | Edit101 | Edit101KeyDown |
| OnKeyPress | 10 | Edit101 | Edit113KeyPress |
| OnChange | 9 | Edit101 | Edit101Change |
| OnClick | 6 | Button101 | Button101Click |
| OnActivate | 2 | Sobo36 | FormActivate |
| OnClose | 2 | Sobo36 | FormClose |
| OnShow | 2 | Sobo36 | FormShow |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |
| OnAcceptDate | 1 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 1 | DateEdit1 | DateEdit1ButtonClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnDblClick | 1 | DBGrid101 | Button007Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **11**, 타입 분포: DELETE×1, INSERT×1, SELECT×8, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T6_Ssub | 4 |
| G7_Ggeo | 1 |
| Sv_Ghng | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L289 **SELECT** `Sv_Ghng` — `Select Max(Gdate)as Gdate From Sv_Ghng Where`
- L302 **SELECT** `` — `Select Gcode,Giqut,Goqut,Gjqut,Gbqut,Gpqut,Gsusu,Gsqut,Gosum,Gbsum`
- L358 **SELECT** `` — `Select Gcode,Sum(Gbsum)as Gbsum`
- L364 **SELECT** `T6_Ssub` — `Select * From T6_Ssub Where`
- L379 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L394 **SELECT** `` — `Select Bcode,Scode,Gubun,Pubun,`
- L566 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L661 **SELECT** `` — `Select Gdate,Gbsum`
- L808 **DELETE** `T6_Ssub` — `DELETE FROM T6_Ssub WHERE ID=@ID and Gdate=`
- L826 **INSERT** `T6_Ssub` — `INSERT INTO T6_Ssub`
- L849 **UPDATE** `T6_Ssub` — `UPDATE T6_Ssub SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| T6_Ssub | 1 | 4 | 1 | 1 | 7 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **3**

| line | type | message |
| --- | --- | --- |
| 601 | empty_check |  |
| 747 | message | 출판사를 등록해 주세요. |
| 804 | message | 삭제 하시겠습니까? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo36` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
