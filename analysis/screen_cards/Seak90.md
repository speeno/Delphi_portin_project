# 화면 카드: Seak90 (TSeak90)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09_1.pas
- 컴포넌트 수: **267** / 이벤트 수: **218** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×116, TFlatNumber×91, TRadioButton×26, TFlatEdit×11, TmyLabel3d×7, TFlatMaskEdit×5
- 핵심 SQL 수: **6** / 영향 테이블 수: **1** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeak90 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09.dfm
| component_type | count |
| --- | --- |
| TFlatNumber | 68 |
| TFlatPanel | 58 |
| TmyLabel3d | 5 |
| TFlatCheckBox | 3 |
| TFlatEdit | 2 |
| TSeak90 | 1 |
| TFlatMaskEdit | 1 |
| TFlatButton | 1 |
- component_count: 139, event_count: 141

### TSeak90 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak09_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 58 |
| TRadioButton | 26 |
| TFlatNumber | 23 |
| TFlatEdit | 9 |
| TFlatMaskEdit | 4 |
| TFlatButton | 2 |
| TBitBtn | 2 |
| TmyLabel3d | 2 |
| TSeak90 | 1 |
| TFlatComboBox | 1 |
- component_count: 128, event_count: 77

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seak90.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **218** / 이벤트 종류: **5**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 106 | CheckBox1 | Edit111KeyDown |
| OnKeyPress | 106 | CheckBox1 | Edit111KeyPress |
| OnClose | 2 | Seak90 | FormClose |
| OnShow | 2 | Seak90 | FormShow |
| OnClick | 2 | BitBtn101 | BitBtn101Click |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **6**, 타입 분포: INSERT×1, SELECT×4, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| H4_Iyeo | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L196 **SELECT** `` — `Select Gnumb,Scode,Gname,Gposa,Date1,Date2,Date3,`
- L237 **SELECT** `` — `Select Hcode,`
- L289 **INSERT** `H4_Iyeo` — `INSERT INTO H4_Iyeo`
- L323 **SELECT** `` — `Select gen_id(`
- L324 **SELECT** `` — `Select LAST_INSERT_ID()`
- L334 **UPDATE** `H4_Iyeo` — `UPDATE H4_Iyeo SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **1**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| H4_Iyeo | 1 | 1 | 2 | 2 | 6 | ✓ |
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
- (수동) 위 문서에서 form `Seak90` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
