# 화면 카드: Sobo59_3 (TSobo59_3)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3 - 복사본.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3 - 복사본.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3.pas
- 컴포넌트 수: **47** / 이벤트 수: **25** / form 등록 수: **2**
- 주요 컴포넌트: TmyLabel3d×21, TSpinEdit×6, TFlatPanel×4, TFlatButton×4, TFlatEdit×3, TSobo59_3×2
- 핵심 SQL 수: **33** / 영향 테이블 수: **6** / 검증 규칙 수: **11**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo59_3 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3 - 복사본.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 6 |
| TSpinEdit | 3 |
| TFlatPanel | 2 |
| TFlatButton | 2 |
| TSobo59_3 | 1 |
| TFlatEdit | 1 |
| TFlatNumber | 1 |
| TFlatCheckBox | 1 |
| TDBGridEh | 1 |
- component_count: 18, event_count: 11

### TSobo59_3 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_3.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 15 |
| TSpinEdit | 3 |
| TFlatPanel | 2 |
| TFlatButton | 2 |
| TFlatEdit | 2 |
| TSobo59_3 | 1 |
| TFlatNumber | 1 |
| TFlatCheckBox | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 29, event_count: 14

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo59_3.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **25** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 5 | Button101 | Button101Click |
| OnKeyDown | 5 | Edit201 | Edit201KeyDown |
| OnKeyPress | 4 | Edit201 | Edit115KeyPress |
| OnActivate | 2 | Sobo59_3 | FormActivate |
| OnClose | 2 | Sobo59_3 | FormClose |
| OnShow | 2 | Sobo59_3 | FormShow |
| OnDblClick | 2 | DBGrid201 | DBGrid201DblClick |
| OnTitleClick | 2 | DBGrid201 | DBGrid201TitleClick |
| OnCreate | 1 | Sobo59_3 | FormCreate |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **33**, 타입 분포: INSERT×4, SELECT×25, UPDATE×4

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Chek | 8 |
| T4_Ssub | 7 |
| S1_Ssub | 6 |
| G1_Ggeo | 4 |
| G4_Book | 4 |
| G7_Ggeo | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L413 **SELECT** `` — `Select Hcode,Scode,Gdate,Gcode,Bcode,Jubun,Gjisa,Idnum,Count(*)as Gdang,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L434 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L451 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L460 **SELECT** `` — `Select Hcode,Scode,Gdate,Gcode,Bcode,Jubun,Gjisa,Idnum,Count(*)as Gdang,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L495 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L500 **SELECT** `G4_Book` — `Select Gisbn From G4_Book Where`
- L505 **SELECT** `S1_Chek` — `Select Yesno From S1_Chek Where`
- L512 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L523 **SELECT** `S1_Chek` — `Select Time1 From S1_Chek Where`
- L564 **SELECT** `G4_Book` — `Select Gisbn From G4_Book Where`
- L569 **SELECT** `S1_Chek` — `Select Yesno,Gnumb From S1_Chek Where`
- L571 **INSERT** `S1_Chek` — `INSERT INTO S1_Chek`
- L600 **SELECT** `S1_Chek` — `Select Time1 From S1_Chek Where`
- L623 **SELECT** `T4_Ssub` — `Select * From T4_Ssub Where`
- L629 **SELECT** `T4_Ssub` — `Select Gqut1,Gqut2,Gqut3 From T4_Ssub Where`

_(상위 15건 표기, 전체 33건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| S1_Chek | 4 | 8 | 4 | 0 | 16 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **11**

| line | type | message |
| --- | --- | --- |
| 837 | empty_check |  |
| 1023 | empty_check |  |
| 1031 | empty_check |  |
| 1218 | empty_check |  |
| 1282 | message | 검증작업이 완료되지 않았습니다. |
| 1455 | message | 검색한 자료가 없습니다. 확인해주세요. |
| 1460 | message | 검색한 출판사가 없습니다. 확인해주세요. |
| 1681 | message | 검색한 자료가 없습니다. 확인해주세요. |
| 1686 | message | 검색한 출판사가 없습니다. 확인해주세요. |
| 1860 | message | 검증작업이 완료된 거래처는 다시 검증할 수 없습니다. |
| 1863 | message | 검증된 자료는 다시 검증할 수 없습니다. |

## 6. 고객사 분기
- L1877 `해피데이` — `if gCompany_name = '해피데이'`
- L1889 `해피데이` — `if gCompany_name = '해피데이'`

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo59_3` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
