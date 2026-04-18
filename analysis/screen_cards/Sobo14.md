# 화면 카드: Sobo14 (TSobo14)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14.pas
- 컴포넌트 수: **9** / 이벤트 수: **8** / form 등록 수: **1**
- 주요 컴포넌트: TCornerButton×3, TmyLabel3d×3, TSobo14×1, TFlatPanel×1, TDBGrid×1
- 핵심 SQL 수: **13** / 영향 테이블 수: **2** / 검증 규칙 수: **8**
- 매핑 시나리오: **C9 상품·고객 마스터 등록**

## 1. UI 구성
### TSobo14 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu14.dfm
| component_type | count |
| --- | --- |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TSobo14 | 1 |
| TFlatPanel | 1 |
| TDBGrid | 1 |
- component_count: 9, event_count: 8

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo14.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **8** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Sobo14 | FormActivate |
| OnClose | 1 | Sobo14 | FormClose |
| OnPaint | 1 | Sobo14 | FormPaint |
| OnDblClick | 1 | DBGrid101 | DBGrid101DblClick |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **13**, 타입 분포: DELETE×2, INSERT×2, SELECT×6, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 7 |
| G4_Gbun | 6 |

### 주요 SQL (line 오름차순 상위 15개)
- L298 **SELECT** `G4_Book` — `Select * From G4_Book Where`
- L488 **INSERT** `G4_Book` — `INSERT INTO G4_Book`
- L502 **SELECT** `G4_Gbun` — `Select Gcode From G4_Gbun Where`
- L560 **UPDATE** `G4_Book` — `UPDATE G4_Book SET`
- L693 **DELETE** `G4_Book` — `DELETE FROM G4_Book WHERE Gcode=`
- L730 **INSERT** `G4_Gbun` — `INSERT INTO G4_Gbun ( Gcode, Gname, Hcode ) VALUES`
- L749 **UPDATE** `G4_Gbun` — `UPDATE G4_Gbun SET Gcode=`
- L786 **DELETE** `G4_Gbun` — `DELETE FROM G4_Gbun WHERE Gcode=`
- L809 **SELECT** `G4_Book` — `Select Gcode From G4_Book Where`
- L1004 **UPDATE** `G4_Book` — `UPDATE G4_Book SET Scode=`
- L1057 **SELECT** `G4_Gbun` — `Select * From G4_Gbun Where`
- L1109 **SELECT** `G4_Book` — `Select Hcode,Gubun,Gcode,Gname,Gdang,Gisbn,Gpost From G4_Book Where`
- L1124 **SELECT** `G4_Gbun` — `Select ID,Gcode,Gname From G4_Gbun Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G4_Gbun | 1 | 12 | 1 | 1 | 15 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **8**

| line | type | message |
| --- | --- | --- |
| 482 | message | 저장 하시겠습니까? |
| 689 | message | 삭제 하시겠습니까? |
| 704 | empty_check |  |
| 725 | message | 저장 하시겠습니까? |
| 782 | message | 삭제 하시겠습니까? |
| 797 | empty_check |  |
| 806 | message | 코드를 입력하세요. |
| 815 | message | 코드가 이미 등록되어있습니다. 다시 입력하세요. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo14` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C9 상품·고객 마스터 등록)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
