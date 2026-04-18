# 화면 카드: Sobo13_1 (TSobo13_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu13_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu13_1.pas
- 컴포넌트 수: **26** / 이벤트 수: **19** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×8, TFlatEdit×4, TCornerButton×3, TmyLabel3d×3, TFlatButton×3, TSobo13_1×1
- 핵심 SQL 수: **6** / 영향 테이블 수: **3** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo13_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu13_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 8 |
| TFlatEdit | 4 |
| TCornerButton | 3 |
| TmyLabel3d | 3 |
| TFlatButton | 3 |
| TSobo13_1 | 1 |
| TFlatProgressBar | 1 |
| TProgressBar | 1 |
| TdxButton | 1 |
| TDBGrid | 1 |
- component_count: 26, event_count: 19

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo13_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **19** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 4 | Edit102 | Edit102KeyDown |
| OnKeyPress | 4 | Edit102 | Edit114KeyPress |
| OnClick | 4 | Button101 | Button101Click |
| OnChange | 3 | Edit102 | Edit101Change |
| OnActivate | 1 | Sobo13_1 | FormActivate |
| OnClose | 1 | Sobo13_1 | FormClose |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **6**, 타입 분포: INSERT×1, SELECT×4, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| T0_Gbun | 4 |
| G1_Ggeo | 1 |
| H2_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L295 **SELECT** `G1_Ggeo` — `Select Hcode,Gcode,Gname From G1_Ggeo Where`
- L325 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`
- L354 **SELECT** `T0_Gbun` — `Select Hcode,Gcode,Gjisa,Bebon From T0_Gbun Where`
- L623 **SELECT** `T0_Gbun` — `Select Count(*) From T0_Gbun Where`
- L630 **INSERT** `T0_Gbun` — `INSERT INTO T0_Gbun`
- L645 **UPDATE** `T0_Gbun` — `UPDATE T0_Gbun SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T0_Gbun | 1 | 2 | 1 | 0 | 4 | ✓ |
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
- (수동) 위 문서에서 form `Sobo13_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
