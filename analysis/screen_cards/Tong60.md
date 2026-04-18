# 화면 카드: Tong60 (TTong60)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong06.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong06.pas
- 컴포넌트 수: **46** / 이벤트 수: **14** / form 등록 수: **1**
- 주요 컴포넌트: TfrReport×10, TfrDBDataSet×9, TfrUserDataset×8, TTong60×1, TfrOLEObject×1, TfrRichObject×1
- 핵심 SQL 수: **29** / 영향 테이블 수: **9** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TTong60 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong06.dfm
| component_type | count |
| --- | --- |
| TfrReport | 10 |
| TfrDBDataSet | 9 |
| TfrUserDataset | 8 |
| TTong60 | 1 |
| TfrOLEObject | 1 |
| TfrRichObject | 1 |
| TfrRoundRectObject | 1 |
| TfrCheckBoxObject | 1 |
| TfrBarCodeObject | 1 |
| TfrShapeObject | 1 |
| TfrDialogControls | 1 |
| TfrCrossObject | 1 |
| TfrTextExport | 1 |
| TfrCSVExport | 1 |
| TfrRTFExport | 1 |
| TfrHTMExport | 1 |
| TfrHTML2Export | 1 |
| TfrOLEExcelExport | 1 |
| TfrBMPExport | 1 |
| TfrJPEGExport | 1 |
| TfrTIFFExport | 1 |
| TfrRtfAdvExport | 1 |
- component_count: 46, event_count: 14

- 레이아웃 메타: (없음 — `analysis/form_layouts/Tong60.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **14** / 이벤트 종류: **2**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnBeginPage | 7 | frReport21_01 | frReport21_01BeginPage |
| OnGetValue | 7 | frReport21_01 | frReport21_01GetValue |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **29**, 타입 분포: SELECT×29

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 9 |
| G1_Ggeo | 4 |
| G2_Ggwo | 3 |
| G5_Ggeo | 3 |
| G7_Ggeo | 3 |
| S1_Memo | 2 |
| H2_Gbun | 1 |
| S1_Ssub | 1 |
| T4_Ssub | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L223 **SELECT** `G4_Book` — `Select Gqut1,Gqut2 From G4_Book`
- L273 **SELECT** `G1_Ggeo` — `Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G1_Ggeo`
- L279 **SELECT** `G2_Ggwo` — `Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G2_Ggwo`
- L285 **SELECT** `G5_Ggeo` — `Select Gname,Gtel1,Gtel2,Gfax1,Gfax2,Gadd1,Gadd2,Gnum1 From G5_Ggeo`
- L336 **SELECT** `G4_Book` — `Select Apost From G4_Book`
- L342 **SELECT** `G7_Ggeo` — `Select Gnum1 From G7_Ggeo Where`
- L358 **SELECT** `H2_Gbun` — `Select Gnum1 From H2_Gbun Where`
- L435 **SELECT** `G7_Ggeo` — `Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Gtel1,Gtel2,Gfax1,Gfax2 From G7_Ggeo`
- L491 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname From S1_Memo Where`
- L630 **SELECT** `S1_Ssub` — `Select Idnum From S1_Ssub Where`
- L717 **SELECT** `T4_Ssub` — `Select Gqut1 From T4_Ssub Where`
- L831 **SELECT** `G1_Ggeo` — `Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G1_Ggeo`
- L837 **SELECT** `G2_Ggwo` — `Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G2_Ggwo`
- L843 **SELECT** `G5_Ggeo` — `Select Gname,Gtel1,Gtel2,Gadd1,Gadd2,Gpper,Gbigo From G5_Ggeo`
- L962 **SELECT** `S1_Memo` — `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where`

_(상위 15건 표기, 전체 29건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **9**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S1_Memo | 9 | 20 | 10 | 0 | 39 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- (validation_rules 매칭 0건)

## 6. 고객사 분기
- L568 `한강북` — `if (gCompany_name = '한강물류') or (gCompany_name = '한강북'`
- L571 `한강북` — `if (gCompany_name = '한강물류') or (gCompany_name = '한강북'`
- L1335 `해피데이` — `if gCompany_name = '해피데이'`
- L1724 `해피데이` — `if gCompany_name = '해피데이'`

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Tong60` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
