# 화면 카드: Sobo59_1 (TSobo59_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_1.pas
- 컴포넌트 수: **23** / 이벤트 수: **27** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×4, TFlatEdit×4, TFlatButton×4, TmyLabel3d×2, TFlatMaskEdit×2, TDateEdit×2
- 핵심 SQL 수: **9** / 영향 테이블 수: **4** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo59_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu59_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TmyLabel3d | 2 |
| TFlatMaskEdit | 2 |
| TDateEdit | 2 |
| TFlatRadioButton | 2 |
| TSobo59_1 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 23, event_count: 27

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo59_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **27** / 이벤트 종류: **10**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 5 | Edit101 | Edit101KeyDown |
| OnKeyPress | 5 | Edit101 | Edit111KeyPress |
| OnClick | 5 | Button101 | Button101Click |
| OnChange | 4 | Edit101 | Edit101Change |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 1 | Sobo59_1 | FormActivate |
| OnClose | 1 | Sobo59_1 | FormClose |
| OnShow | 1 | Sobo59_1 | FormShow |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **9**, 타입 분포: INSERT×1, SELECT×7, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Chek | 4 |
| G7_Ggeo | 1 |
| G1_Ggeo | 1 |
| G5_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L359 **SELECT** `` — `Select Hcode,Count(Hcode),Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L387 **SELECT** `` — `Select Hcode,Scode,Gdate,Gcode,Idnum,Gubun,Jubun,Gjisa,Count(*)as Gdang,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L432 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L439 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L446 **SELECT** `G5_Ggeo` — `Select Gname From G5_Ggeo Where`
- L469 **SELECT** `S1_Chek` — `Select Yesno,Time1 From S1_Chek Where`
- L778 **SELECT** `S1_Chek` — `Select Time1 From S1_Chek Where`
- L792 **INSERT** `S1_Chek` — `INSERT INTO S1_Chek`
- L834 **UPDATE** `S1_Chek` — `UPDATE S1_Chek SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| S1_Chek | 4 | 8 | 4 | 0 | 16 | ✓ |
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
- (수동) 위 문서에서 form `Sobo59_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
