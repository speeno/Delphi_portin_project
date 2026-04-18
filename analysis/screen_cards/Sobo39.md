# 화면 카드: Sobo39 (TSobo39)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu39.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu39.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu39.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu39.pas
- 컴포넌트 수: **6** / 이벤트 수: **13** / form 등록 수: **2**
- 주요 컴포넌트: TSobo39×2, TFlatPanel×2, TDBGrid×1, TDBGridEh×1
- 핵심 SQL 수: **26** / 영향 테이블 수: **7** / 검증 규칙 수: **4**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo39 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Data/Subu39.dfm
| component_type | count |
| --- | --- |
| TSobo39 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 3, event_count: 7

### TSobo39 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu39.dfm
| component_type | count |
| --- | --- |
| TSobo39 | 1 |
| TFlatPanel | 1 |
| TDBGridEh | 1 |
- component_count: 3, event_count: 6

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo39.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **13** / 이벤트 종류: **7**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 2 | Sobo39 | FormActivate |
| OnClose | 2 | Sobo39 | FormClose |
| OnShow | 2 | Sobo39 | FormShow |
| OnKeyDown | 2 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 2 | DBGrid101 | DBGrid101KeyPress |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **26**, 타입 분포: DELETE×1, INSERT×2, SELECT×22, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T4_Ssub | 6 |
| Sv_Csum | 5 |
| G1_Ggeo | 4 |
| H2_Gbun | 3 |
| T1_Gbun | 3 |
| S1_Ssub | 3 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L346 **SELECT** `Sv_Csum` — `Select Scode,Gdate,Gcode,Goqut,Gbqut From Sv_Csum Where`
- L368 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where Gcode=`
- L396 **SELECT** `H2_Gbun` — `Select Hcode,Scode,Gcode,Gname,Jubun,Gdate From H2_Gbun Where`
- L404 **SELECT** `T1_Gbun` — `Select Hcode,Gcode,Gjisa,Jubun,Gname From T1_Gbun Where`
- L407 **SELECT** `Sv_Csum` — `Select Scode,Gdate,Gcode,Gosum,Gbsum From Sv_Csum Where`
- L412 **SELECT** `T4_Ssub` — `Select Hcode,Gcode,Gdate,Gjisa,Jubun,Gqut1,Gqut2,Gqut3 From T4_Ssub`
- L459 **SELECT** `S1_Ssub` — `Select Hcode,Gcode,Gjisa,Jubun,Sum(Gsqut)as Gsqut From S1_Ssub Where`
- L460 **SELECT** `` — `Select Gcode,Scode,Gjisa,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum`
- L478 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where`
- L484 **SELECT** `G1_Ggeo` — `Select Pubun,Gcode,Gname From G1_Ggeo Where Gcode=`
- L495 **SELECT** `H2_Gbun` — `Select Gdate From H2_Gbun Where Scode=`
- L544 **SELECT** `Sv_Csum` — `Select Distinct Gdate From Sv_Csum Where`
- L554 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L560 **DELETE** `Sv_Csum` — `DELETE FROM Sv_Csum Where`
- L560 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`

_(상위 15건 표기, 전체 26건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **7**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| Sv_Csum | 3 | 5 | 3 | 2 | 13 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 554 | message | 등록된 자료가 있습니다. 삭제하고 등록할까요? |
| 626 | message | 저장되었습니다. |
| 858 | empty_check |  |
| 909 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo39` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
