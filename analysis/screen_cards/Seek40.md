# 화면 카드: Seek40 (TSeek40)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek04.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek04.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek04.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek04.pas
- 컴포넌트 수: **20** / 이벤트 수: **10** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×8, TFlatEdit×4, TSeek40×2, TFlatSpeedButton×2, TFlatNumber×2, TDBGrid×2
- 핵심 SQL 수: **3** / 영향 테이블 수: **0** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeek40 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Seek04.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 2 |
| TSeek40 | 1 |
| TFlatSpeedButton | 1 |
| TFlatNumber | 1 |
| TDBGrid | 1 |
- component_count: 10, event_count: 5

### TSeek40 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seek04.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 2 |
| TSeek40 | 1 |
| TFlatSpeedButton | 1 |
| TFlatNumber | 1 |
| TDBGrid | 1 |
- component_count: 10, event_count: 5

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seek40.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **10** / 이벤트 종류: **5**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnShow | 2 | Seek40 | FormShow |
| OnClick | 2 | Button001 | Button001Click |
| OnEnter | 2 | Edit1 | Edit1Enter |
| OnKeyPress | 2 | Edit1 | Edit1KeyPress |
| OnDblClick | 2 | DBGrid101 | DBGrid101DblClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: SELECT×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |

### 주요 SQL (line 오름차순 상위 15개)
- L78 **SELECT** `` — `Select Scode,Gubun,Gcode,Ocode,Gname,Gjeja,`
- L79 **SELECT** `` — `Select Scode,Gubun,Gcode,Ocode,Gname,Gjeja,`
- L185 **SELECT** `` — `Select Scode,Hcode as Gubun ,Gcode,Ocode,Gname,Gjeja,`

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

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
- (수동) 위 문서에서 form `Seek40` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
