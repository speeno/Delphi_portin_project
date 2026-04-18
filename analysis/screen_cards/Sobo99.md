# 화면 카드: Sobo99 (TSobo99)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu99.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu99.pas
- 컴포넌트 수: **3** / 이벤트 수: **6** / form 등록 수: **1**
- 주요 컴포넌트: TSobo99×1, TFlatPanel×1, TDBGridEh×1
- 핵심 SQL 수: **17** / 영향 테이블 수: **6** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo99 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu99.dfm
| component_type | count |
| --- | --- |
| TSobo99 | 1 |
| TFlatPanel | 1 |
| TDBGridEh | 1 |
- component_count: 3, event_count: 6

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo99.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **6** / 이벤트 종류: **6**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Sobo99 | FormActivate |
| OnClose | 1 | Sobo99 | FormClose |
| OnShow | 1 | Sobo99 | FormShow |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **17**, 타입 분포: INSERT×1, SELECT×15, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T4_Ssub | 6 |
| T1_Gbun | 3 |
| S1_Ssub | 3 |
| H2_Gbun | 2 |
| G5_Ggeo | 2 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L396 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where`
- L404 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where`
- L412 **SELECT** `T4_Ssub` — `Select Hcode,Gcode,Gdate,Gjisa,Jubun,Gqut1,Gqut2,Gqut3 From T4_Ssub`
- L462 **SELECT** `S1_Ssub` — `Select Hcode,Gcode,Gjisa,Jubun,Sum(Gsqut)as Gsqut From S1_Ssub Where`
- L481 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L557 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L563 **SELECT** `G5_Ggeo` — `Select Gname From G5_Ggeo Where`
- L580 **SELECT** `T1_Gbun` — `Select Gname From T1_Gbun Where`
- L640 **SELECT** `G5_Ggeo` — `Select Gubun From G5_Ggeo Where`
- L663 **SELECT** `T4_Ssub` — `Select Gqut1,Gqut2,Gqut3 From T4_Ssub Where`
- L797 **SELECT** `S1_Ssub` — `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where`
- L872 **SELECT** `T1_Gbun` — `Select Gname,Bebon From T1_Gbun Where`
- L1005 **SELECT** `T4_Ssub` — `Select Sum(Gqut1)as Gqut1,Sum(Gqut2)as Gqut2,Sum(Gqut3)as Gqut3 From T4_Ssub Where`
- L1103 **SELECT** `S1_Ssub` — `Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut From S1_Ssub S, G4_Book Y`
- L1324 **SELECT** `T4_Ssub` — `Select * From T4_Ssub Where`

_(상위 15건 표기, 전체 17건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **6**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
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
- (수동) 위 문서에서 form `Sobo99` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
