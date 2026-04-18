# 화면 카드: Exls70 (TExls70)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Exls07.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Exls07.pas
- 컴포넌트 수: **17** / 이벤트 수: **7** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×6, TCornerButton×3, TmyLabel3d×3, TExls70×1, TdxButton×1, TFlatProgressBar×1
- 핵심 SQL 수: **5** / 영향 테이블 수: **2** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### TExls70 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Exls07.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 6 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TExls70 | 1 |
| TdxButton | 1 |
| TFlatProgressBar | 1 |
| TProgressBar | 1 |
| TDBGridEh | 1 |
- component_count: 17, event_count: 7

- 레이아웃 메타: (없음 — `analysis/form_layouts/Exls70.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **7** / 이벤트 종류: **7**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnActivate | 1 | Exls70 | FormActivate |
| OnClose | 1 | Exls70 | FormClose |
| OnShow | 1 | Exls70 | FormShow |
| OnClick | 1 | dxButton1 | Button101Click |
| OnDrawColumnCell | 1 | DBGrid101 | DBGrid101DrawColumnCell |
| OnKeyDown | 1 | DBGrid101 | DBGrid101KeyDown |
| OnKeyPress | 1 | DBGrid101 | DBGrid101KeyPress |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: INSERT×1, SELECT×3, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Sm_Ggeo | 4 |
| G7_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L103 **SELECT** `G7_Ggeo` — `Select Gcode as Hcode, Gname as Hname From G7_Ggeo`
- L118 **SELECT** `Sm_Ggeo` — `Select Hcode,Name0 From Sm_Ggeo`
- L215 **SELECT** `Sm_Ggeo` — `Select * From Sm_Ggeo Where`
- L222 **UPDATE** `Sm_Ggeo` — `UPDATE Sm_Ggeo SET`
- L236 **INSERT** `Sm_Ggeo` — `INSERT INTO Sm_Ggeo`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Sm_Ggeo | 1 | 3 | 1 | 0 | 5 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 187 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Exls70` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
