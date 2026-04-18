# 화면 카드: Sobo15 (TSobo15)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu15.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu15.pas
- 컴포넌트 수: **9** / 이벤트 수: **8** / form 등록 수: **1**
- 주요 컴포넌트: TCornerButton×3, TmyLabel3d×3, TSobo15×1, TFlatPanel×1, TDBGrid×1
- 핵심 SQL 수: **11** / 영향 테이블 수: **2** / 검증 규칙 수: **11**
- 매핑 시나리오: **C9 상품·고객 마스터 등록**

## 1. UI 구성
### TSobo15 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu15.dfm
| component_type | count |
| --- | --- |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo15 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 9, event_count: 8

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo15.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **8** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Sobo15 | FormActivate |
| OnClose | 1 | Sobo15 | FormClose |
| OnPaint | 1 | Sobo15 | FormPaint |
| OnDblClick | 1 | DBGrid101 | DBGrid101DblClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **11**, 타입 분포: DELETE×2, INSERT×2, SELECT×4, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G1_Ggeo | 5 |
| G1_Gbun | 5 |

### 주요 SQL (line 오름차순 상위 15개)
- L421 **INSERT** `G1_Ggeo` — `INSERT INTO G1_Ggeo`
- L438 **SELECT** `G1_Gbun` — `Select Gcode From G1_Gbun Where`
- L506 **UPDATE** `G1_Ggeo` — `UPDATE G1_Ggeo SET`
- L667 **DELETE** `G1_Ggeo` — `DELETE FROM G1_Ggeo WHERE Gcode=`
- L724 **INSERT** `G1_Gbun` — `INSERT INTO G1_Gbun ( Gcode, Gname, Hcode ) VALUES`
- L743 **UPDATE** `G1_Gbun` — `UPDATE G1_Gbun SET Gcode=`
- L780 **DELETE** `G1_Gbun` — `DELETE FROM G1_Gbun WHERE Gcode=`
- L808 **SELECT** `G1_Ggeo` — `Select Gcode From G1_Ggeo Where`
- L1001 **UPDATE** `G1_Ggeo` — `UPDATE G1_Ggeo SET Scode=`
- L1054 **SELECT** `G1_Gbun` — `Select * From G1_Gbun Where`
- L1105 **SELECT** `` — `Select ID,Hcode,Gubun,Jubun,Pubun,Scode,Gcode,Ocode,Gname,Gposa,Gnumb,Guper,`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| G1_Gbun | 2 | 9 | 2 | 2 | 15 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **11**

| line | type | message |
| --- | --- | --- |
| 415 | message | 저장 하시겠습니까? |
| 663 | message | 삭제 하시겠습니까? |
| 678 | empty_check |  |
| 692 | empty_check |  |
| 719 | message | 저장 하시겠습니까? |
| 776 | message | 삭제 하시겠습니까? |
| 791 | empty_check |  |
| 800 | message | 코드를 입력하세요. |
| 804 | message | 코드를 (9)로 시작해 주세요. |
| 814 | message | 코드가 이미 등록되어있습니다. 다시 입력하세요. |
| 824 | message | 거래처에 코드가 이미 등록되어있습니다. 다시 입력하세요. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo15` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C9 상품·고객 마스터 등록)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
