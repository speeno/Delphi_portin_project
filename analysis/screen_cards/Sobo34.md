# 화면 카드: Sobo34 (TSobo34)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu34.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu34.pas
- 컴포넌트 수: **19** / 이벤트 수: **24** / form 등록 수: **1**
- 주요 컴포넌트: TFlatEdit×6, TFlatPanel×5, TmyLabel3d×2, TFlatButton×2, TFlatMaskEdit×2, TSobo34×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **3** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo34 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu34.dfm
| component_type | count |
| --- | --- |
| TFlatEdit | 6 |
| TFlatPanel | 5 |
| TmyLabel3d | 2 |
| TFlatButton | 2 |
| TFlatMaskEdit | 2 |
| TSobo34 | 1 |
| TDBGrid | 1 |
- component_count: 19, event_count: 24

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo34.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **24** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 6 | Edit101 | Edit101KeyDown |
| OnKeyPress | 6 | Edit101 | Edit111KeyPress |
| OnChange | 5 | Edit101 | Edit101Change |
| OnClick | 2 | Button101 | Button101Click |
| OnActivate | 1 | Sobo34 | FormActivate |
| OnClose | 1 | Sobo34 | FormClose |
| OnShow | 1 | Sobo34 | FormShow |
| OnDblClick | 1 | DBGrid101 | Button007Click |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: SELECT×5

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 1 |
| Sv_Ghng | 1 |
| G4_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L302 **SELECT** `` — `Select Bcode,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L327 **SELECT** `G4_Book` — `Select Gname,Ocode,Gubun From G4_Book Where Gcode=`
- L394 **SELECT** `` — `Select Gcode,Sum(Gbsum)as Gbsum`
- L443 **SELECT** `Sv_Ghng` — `Select Max(Gdate)as Gdate From Sv_Ghng`
- L533 **SELECT** `G4_Gbun` — `Select Gname From G4_Gbun Where Gcode=`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| G4_Gbun | 1 | 12 | 1 | 1 | 15 | ✓ |
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
- (수동) 위 문서에서 form `Sobo34` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
