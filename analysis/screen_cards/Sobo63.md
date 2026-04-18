# 화면 카드: Sobo63 (TSobo63)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu63.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu63.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu63.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu63.pas
- 컴포넌트 수: **62** / 이벤트 수: **60** / form 등록 수: **2**
- 주요 컴포넌트: TmyLabel3d×11, TFlatEdit×10, TFlatPanel×9, TFlatButton×9, TCornerButton×7, TFlatMaskEdit×4
- 핵심 SQL 수: **6** / 영향 테이블 수: **3** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo63 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu63.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 5 |
| TFlatPanel | 4 |
| TFlatButton | 4 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo63 | 1 |
| TFlatCheckBox | 1 |
| TdxButton | 1 |
| TImVarGrid | 1 |
- component_count: 28, event_count: 26

### TSobo63 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu63.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 6 |
| TFlatEdit | 6 |
| TFlatPanel | 5 |
| TFlatButton | 5 |
| TCornerButton | 4 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TSobo63 | 1 |
| TFlatCheckBox | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 34, event_count: 34

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo63.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **60** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 12 | Edit101 | Edit101KeyDown |
| OnKeyPress | 12 | Edit101 | Edit111KeyPress |
| OnClick | 11 | Button101 | Button101Click |
| OnChange | 9 | Edit101 | Edit101Change |
| OnAcceptDate | 4 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 4 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 2 | Sobo63 | FormActivate |
| OnClose | 2 | Sobo63 | FormClose |
| OnShow | 2 | Sobo63 | FormShow |
| OnDblClick | 1 | DBGrid101 | Button007Click |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **6**, 타입 분포: SELECT×6

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| H2_Gbun | 1 |
| T1_Gbun | 1 |
| Sg_Csum | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L320 **SELECT** `` — `Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L371 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where`
- L379 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where`
- L392 **SELECT** `Sg_Csum` — `Select Gdate,Gbsum From Sg_Csum Where`
- L416 **SELECT** `` — `Select Hcode,substring(Gdate,1,7),Sum(Gsqut)as Gsqut`
- L487 **SELECT** `` — `Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| Sg_Csum | 3 | 4 | 5 | 6 | 18 | ✓ |
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
- (수동) 위 문서에서 form `Sobo63` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
