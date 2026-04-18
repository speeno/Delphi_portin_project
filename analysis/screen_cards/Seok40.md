# 화면 카드: Seok40 (TSeok40)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok04.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok04.pas
- 컴포넌트 수: **9** / 이벤트 수: **4** / form 등록 수: **1**
- 주요 컴포넌트: TRxRichEdit×3, TFlatPanel×2, TSeok40×1, TFlatCheckBox×1, TFlatButton×1, TZMySqlQuery×1
- 핵심 SQL 수: **3** / 영향 테이블 수: **1** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeok40 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok04.dfm
| component_type | count |
| --- | --- |
| TRxRichEdit | 3 |
| TFlatPanel | 2 |
| TSeok40 | 1 |
| TFlatCheckBox | 1 |
| TFlatButton | 1 |
| TZMySqlQuery | 1 |
- component_count: 9, event_count: 4

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seok40.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **4** / 이벤트 종류: **3**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 2 | CheckBox1 | CheckBox1Click |
| OnClose | 1 | Seok40 | FormClose |
| OnShow | 1 | Seok40 | FormShow |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Me_Sage | 3 |

### 주요 SQL (line 오름차순 상위 15개)
- L50 **SELECT** `Me_Sage` — `Select Gbigo From Me_Sage`
- L82 **SELECT** `Me_Sage` — `Select Gbigo From Me_Sage Where Hcode=`
- L182 **SELECT** `Me_Sage` — `Select Date1,Date2 From Me_Sage Where Hcode=`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **1**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| Me_Sage | 2 | 13 | 2 | 2 | 19 | ✓ |
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
- (수동) 위 문서에서 form `Seok40` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
