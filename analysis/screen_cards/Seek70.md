# 화면 카드: Seek70 (TSeek70)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek07.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek07.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek07.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek07.pas
- 컴포넌트 수: **25** / 이벤트 수: **17** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×12, TFlatEdit×6, TSeek70×2, TFlatNumber×2, TDBGrid×2, TBitBtn×1
- 핵심 SQL 수: **15** / 영향 테이블 수: **6** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeek70 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek07.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 6 |
| TFlatEdit | 3 |
| TSeek70 | 1 |
| TFlatNumber | 1 |
| TDBGrid | 1 |
- component_count: 12, event_count: 8

### TSeek70 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek07.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 6 |
| TFlatEdit | 3 |
| TSeek70 | 1 |
| TFlatNumber | 1 |
| TBitBtn | 1 |
| TDBGrid | 1 |
- component_count: 13, event_count: 9

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seek70.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **17** / 이벤트 종류: **7**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyPress | 6 | Edit1 | Edit1KeyPress |
| OnActivate | 2 | Seek70 | FormActivate |
| OnClose | 2 | Seek70 | FormClose |
| OnShow | 2 | Seek70 | FormShow |
| OnKeyDown | 2 | DBGrid1 | DBGrid1KeyDown |
| OnTitleClick | 2 | DBGrid1 | DBGrid1TitleClick |
| OnClick | 1 | BitBtn001 | BitBtn001Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **15**, 타입 분포: SELECT×13, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 4 |
| G6_Ggeo | 4 |
| H2_Gbun | 2 |
| G1_Ggeo | 2 |
| G1_Gbun | 1 |
| S1_Ssub | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L82 **SELECT** `G6_Ggeo` — `Select Hcode,Gcode,Bcode,Grat1 From G6_Ggeo`
- L85 **SELECT** `G4_Book` — `Select Grat1 From G4_Book Where Gcode=`
- L90 **SELECT** `G4_Book` — `Select Gdang From G4_Book Where Gcode=`
- L98 **SELECT** `G4_Book` — `Select Grat1 From G4_Book Where`
- L102 **SELECT** `` — `Select Gubun,Jubun,Gcode,Ocode,Gname,Gposa,`
- L103 **SELECT** `G4_Book` — `Select Gdang From G4_Book Where`
- L116 **SELECT** `G6_Ggeo` — `Select S.Gcode,S.Bcode,S.Grat1,S.Gssum,Y.Gname,Y.Gposa,Y.Jubun,Y.Gtel1,Y.Gtel2 From G6_Ggeo S, G1_Ggeo Y`
- L119 **SELECT** `G1_Gbun` — `Select Gname From G1_Gbun Where Gcode=`
- L125 **SELECT** `G6_Ggeo` — `Select Grat1 From G6_Ggeo`
- L161 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`
- L168 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`
- L206 **SELECT** `G1_Ggeo` — `Select Gcode,Gubun,Grat1,Gqut1,Gname,Gposa,Jubun,Gtel1,Gtel2 From G1_Ggeo`
- L347 **UPDATE** `G6_Ggeo` — `UPDATE G6_Ggeo SET Gssum=@Gssum`
- L348 **UPDATE** `G1_Ggeo` — `UPDATE G1_Ggeo SET Gqut1=@Gqut1`
- L404 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Grat1,Gsqut From S1_Ssub Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| G6_Ggeo | 2 | 11 | 5 | 4 | 22 | ✓ |
| G1_Gbun | 2 | 9 | 2 | 2 | 15 | ✓ |
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
- (수동) 위 문서에서 form `Seek70` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
