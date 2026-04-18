# 화면 카드: Tong40 (TTong40)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Tong04.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong04.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Tong04.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong04.pas
- 컴포넌트 수: **6** / 이벤트 수: **4** / form 등록 수: **2**
- 주요 컴포넌트: TTong40×2, TmyLabel3d×2, TFontDialog×2
- 핵심 SQL 수: **62** / 영향 테이블 수: **9** / 검증 규칙 수: **4**
- 매핑 시나리오: **-**

## 1. UI 구성
### TTong40 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Tong04.dfm
| component_type | count |
| --- | --- |
| TTong40 | 1 |
| TmyLabel3d | 1 |
| TFontDialog | 1 |
- component_count: 3, event_count: 2

### TTong40 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong04.dfm
| component_type | count |
| --- | --- |
| TTong40 | 1 |
| TmyLabel3d | 1 |
| TFontDialog | 1 |
- component_count: 3, event_count: 2

- 레이아웃 메타: (없음 — `analysis/form_layouts/Tong40.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **4** / 이벤트 종류: **2**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnHide | 2 | Tong40 | FormHide |
| OnShow | 2 | Tong40 | FormShow |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **62**, 타입 분포: SELECT×62

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 6 |
| G1_Ggeo | 4 |
| S3_Ssub | 2 |
| G2_Ggwo | 2 |
| G5_Ggeo | 2 |
| Sv_Chng | 2 |
| Gg_Magn | 2 |
| Sv_Ghng | 2 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L319 **SELECT** `S3_Ssub` — `Select * From S3_Ssub Where`
- L356 **SELECT** `S3_Ssub` — `Select * From S3_Ssub Where`
- L652 **SELECT** `G1_Ggeo` — `Select Gname,Gtel1,Gtel2 From G1_Ggeo Where Gcode=`
- L667 **SELECT** `G2_Ggwo` — `Select Gname,Gtel1,Gtel2 From G2_Ggwo Where Gcode=`
- L682 **SELECT** `G5_Ggeo` — `Select Gname,Gtel1,Gtel2 From G5_Ggeo Where Gcode=`
- L691 **SELECT** `G1_Ggeo` — `Select Gname,Gtel1,Gtel2 From G1_Ggeo Where`
- L706 **SELECT** `G2_Ggwo` — `Select Gname,Gtel1,Gtel2 From G2_Ggwo Where`
- L721 **SELECT** `G5_Ggeo` — `Select Gname,Gtel1,Gtel2 From G5_Ggeo Where`
- L745 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where Gcode=`
- L784 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`
- L919 **SELECT** `` — `Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo`
- L958 **SELECT** `` — `Select Gnumb,Gname,Gposa,Gadd1,Gadd2,Guper,Gjomo`
- L1445 **SELECT** `` — `Select Gname,Gposa,Gadd1,Gadd2,Oadd1,Oadd2,Gnumb,Gnum1`
- L1484 **SELECT** `` — `Select Gname,Gposa,Gadd1,Gadd2,Oadd1,Oadd2,Gnumb,Gnum1`
- L1658 **SELECT** `G1_Ggeo` — `Select Gbigo From G1_Ggeo Where Gcode=`

_(상위 15건 표기, 전체 62건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **9**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G5_Ggeo | 1 | 28 | 1 | 2 | 32 | ✓ |
| Sv_Ghng | 2 | 24 | 3 | 1 | 30 | ✓ |
| G2_Ggwo | 1 | 22 | 3 | 2 | 28 | ✓ |
| Sv_Chng | 2 | 6 | 4 | 1 | 13 | ✓ |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | ✓ |
| S3_Ssub | 0 | 2 | 1 | 1 | 4 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 2003 | empty_check |  |
| 2007 | empty_check |  |
| 2042 | empty_check |  |
| 2046 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Tong40` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
