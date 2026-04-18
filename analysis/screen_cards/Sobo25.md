# 화면 카드: Sobo25 (TSobo25)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu25.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu25.pas
- 컴포넌트 수: **23** / 이벤트 수: **25** / form 등록 수: **1**
- 주요 컴포넌트: TmyLabel3d×4, TFlatPanel×4, TCornerButton×3, TFlatButton×3, TFlatMaskEdit×2, TFlatEdit×2
- 핵심 SQL 수: **2** / 영향 테이블 수: **1** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo25 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu25.dfm
| component_type | count |
| --- | --- |
| TmyLabel3d | 4 |
| TFlatPanel | 4 |
| TCornerButton | 3 |
| TFlatButton | 3 |
| TFlatMaskEdit | 2 |
| TFlatEdit | 2 |
| TDateEdit | 2 |
| TSobo25 | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 23, event_count: 25

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo25.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **25** / 이벤트 종류: **12**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 4 | Button101 | Button101Click |
| OnKeyDown | 4 | Edit101 | Edit101KeyDown |
| OnKeyPress | 4 | Edit101 | Edit111KeyPress |
| OnChange | 3 | Edit101 | Edit101Change |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnActivate | 1 | Sobo25 | FormActivate |
| OnClose | 1 | Sobo25 | FormClose |
| OnShow | 1 | Sobo25 | FormShow |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |
| OnTitleClick | 1 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **2**, 타입 분포: SELECT×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| G4_Book | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L299 **SELECT** `` — `Select ID,Bdate as Gdate,Hcode,Gcode,Bcode,Gsqut,Gdang,Gssum,Gbigo`
- L319 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **1**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 511 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo25` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
