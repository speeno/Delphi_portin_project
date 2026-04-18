# 화면 카드: Seek80 (TSeek80)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek08.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek08.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek08.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek08.pas
- 컴포넌트 수: **16** / 이벤트 수: **10** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×6, TFlatEdit×4, TSeek80×2, TFlatSpeedButton×2, TDBGrid×2
- 핵심 SQL 수: **2** / 영향 테이블 수: **2** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeek80 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek08.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 3 |
| TFlatEdit | 2 |
| TSeek80 | 1 |
| TFlatSpeedButton | 1 |
| TDBGrid | 1 |
- component_count: 8, event_count: 5

### TSeek80 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek08.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 3 |
| TFlatEdit | 2 |
| TSeek80 | 1 |
| TFlatSpeedButton | 1 |
| TDBGrid | 1 |
- component_count: 8, event_count: 5

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seek80.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **10** / 이벤트 종류: **5**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnShow | 2 | Seek80 | FormShow |
| OnClick | 2 | Button001 | Button001Click |
| OnEnter | 2 | Edit1 | Edit1Enter |
| OnKeyPress | 2 | Edit1 | Edit1KeyPress |
| OnDblClick | 2 | DBGrid101 | DBGrid101DblClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **2**, 타입 분포: SELECT×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| H5_Bang | 1 |
| G8_Ggeo | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L85 **SELECT** `H5_Bang` — `Select ID,Gcode,Gname,Gnumb,Gtels From H5_Bang Where`
- L85 **SELECT** `G8_Ggeo` — `Select Gcode,Gname,Gphon,Gtel1,Gtel2 From G8_Ggeo Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **2**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| H5_Bang | 0 | 3 | 2 | 0 | 5 | ✓ |
| G8_Ggeo | 0 | 1 | 0 | 0 | 1 |  |
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
- (수동) 위 문서에서 form `Seek80` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
