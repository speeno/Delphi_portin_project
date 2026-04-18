# 화면 카드: Sobo27 (TSobo27)

_생성: 2026-04-18 04:12 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27_1.pas
- 컴포넌트 수: **36** / 이벤트 수: **46** / form 등록 수: **2**
- 주요 컴포넌트: TFlatPanel×8, TFlatEdit×8, TFlatButton×8, TSobo27×2, TmyLabel3d×2, TFlatMaskEdit×2
- 핵심 SQL 수: **32** / 영향 테이블 수: **8** / 검증 규칙 수: **4**
- 매핑 시나리오: **C2 출고 접수(주문 입력)**

## 1. UI 구성
### TSobo27 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TSobo27 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 18, event_count: 23

### TSobo27 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu27_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 4 |
| TFlatEdit | 4 |
| TFlatButton | 4 |
| TSobo27 | 1 |
| TmyLabel3d | 1 |
| TFlatMaskEdit | 1 |
| TDateEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 18, event_count: 23

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo27.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **46** / 이벤트 종류: **11**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 10 | Button101 | Button101Click |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnChange | 6 | Edit101 | Edit101Change |
| OnActivate | 2 | Sobo27 | FormActivate |
| OnClose | 2 | Sobo27 | FormClose |
| OnShow | 2 | Sobo27 | FormShow |
| OnAcceptDate | 2 | DateEdit1 | DateEdit1AcceptDate |
| OnButtonClick | 2 | DateEdit1 | DateEdit1ButtonClick |
| OnDrawColumnCell | 2 | DBGrid101 | DBGrid101DrawColumnCell |
| OnTitleClick | 2 | DBGrid101 | DBGrid101TitleClick |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **32**, 타입 분포: SELECT×30, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 12 |
| G7_Ggeo | 4 |
| G1_Ggeo | 4 |
| T1_Gbun | 4 |
| S4_Ssub | 2 |
| G4_Book | 2 |
| H2_Gbun | 2 |
| T4_Ssub | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L351 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where`
- L354 **SELECT** `G7_Ggeo` — `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where`
- L385 **SELECT** `S1_Ssub` — `Select Hcode,Count(*) From S1_Ssub Where`
- L391 **SELECT** `S1_Ssub` — `Select Hcode,Count(*) From S1_Ssub Where`
- L452 **SELECT** `S1_Ssub` — `Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where`
- L464 **SELECT** `S1_Ssub` — `Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where`
- L523 **SELECT** `S4_Ssub` — `Select Count(*) From S4_Ssub Where`
- L538 **SELECT** `S4_Ssub` — `Select Count(*) From S4_Ssub Where`
- L562 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L577 **SELECT** `S1_Ssub` — `Select * From S1_Ssub Where`
- L586 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L592 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L601 **SELECT** `G7_Ggeo` — `Select Gname From G7_Ggeo Where`
- L607 **SELECT** `G1_Ggeo` — `Select Gname From G1_Ggeo Where`
- L609 **SELECT** `G4_Book` — `Select Gname,Gjeja From G4_Book Where`

_(상위 15건 표기, 전체 32건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- 본 폼이 접근하는 테이블: **8**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| S1_Ssub | 4 | 90 | 24 | 6 | 124 | ✓ |
| G4_Book | 1 | 112 | 5 | 2 | 120 | ✓ |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| G1_Ggeo | 3 | 86 | 6 | 4 | 99 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| T1_Gbun | 2 | 30 | 2 | 2 | 36 | ✓ |
| T4_Ssub | 4 | 26 | 4 | 0 | 34 | ✓ |
| S4_Ssub | 2 | 9 | 4 | 2 | 17 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **4**

| line | type | message |
| --- | --- | --- |
| 532 | message | 가입고된 자료가 있습니다. |
| 547 | message | 가입고된 자료가 있습니다. |
| 1519 | message | 접속 장애가 발생하여 프로그램을 종료합니다. |
| 1541 | message | 접속 장애가 발생하여 프로그램을 종료합니다. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo27` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C2 출고 접수(주문 입력))
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)


## 10. C2 1차 포팅 범위 (수동 보강 — `screen_card_builder.py` 가 보존)

### 10.1 1차 in_scope (CRUD 4종)

| 기능 | 1차 | 비고 |
|---|---|---|
| 신규 등록 (S1_Ssub INSERT + 라인 INSERT N건, 단일 트랜잭션) | O | DEC-003 위험 기반 순서: INSERT 우선 |
| 수정 (헤더/라인 UPDATE + 라인 추가·삭제) | O | 흡수 시나리오 C11 |
| 취소 (cancel flag UPDATE, 소프트 삭제) | O | DEC-012 (물리 삭제는 후속) |
| 조회 (목록 페이징 + 상세) | O | — |

### 10.2 1차 deferred (후속 이관)

| 항목 | 결정 | 후속 | 사유 요약 |
|---|---|---|---|
| 권한키 분기 (F21/F22/F26) | DEC-009 | C10 권한관리 | 모든 인증 사용자 동등 권한 |
| 바코드 결합 (Tong08) | DEC-010 | C8 (가칭) 바코드 시나리오 | 디바이스/브라우저 호환성 별도 사이클 |
| 인쇄 트리거 (거래명세서/라벨) | DEC-011 | C7 인쇄 | 양식·용지 검토 별도 사이클 |
| 물리 삭제 (DELETE) | DEC-012 | 참조 무결성 검토 후 | 1차는 cancel flag 만 |

### 10.3 관련 폼 요약 (개별 카드는 후속 사이클)

| 폼 | 용도 | C2 1차 포함 여부 |
|---|---|---|
| `TSobo27` (Subu27.pas/.dfm) | **출고접수관리 (본 화면)** | O — CRUD 전체 |
| `TSobo27` (Subu27_1.pas/.dfm) | TSobo27 변형(고객사 분기 추정) | △ — 1차는 본판만, 변형은 customer_variants 분석 후 |
| `TSobo26` (Subu26.pas/.dfm) | 출고접수현황 (조회) | X — 별도 시나리오로 분리 가능 |
| `TSobo28` (Subu28.pas/.dfm) | 출고택배관리 | X — 별도 후속 |
| `TSobo23` (Subu23.pas/.dfm) | 반품명세서 (연계) | X — C4 반품 처리 시나리오 |

### 10.4 데이터 흐름 (서비스 레이어 매핑)

| 레거시 핸들러(추정) | 웹 엔드포인트 | 트랜잭션 |
|---|---|---|
| `FormCreate` / `FormShow` | `GET /api/v1/outbound/orders` (목록) | 읽기 (autocommit) |
| 그리드 행 클릭 | `GET /api/v1/outbound/orders/{id}` (상세) | 읽기 |
| `BtnSaveClick` (신규) | `POST /api/v1/outbound/orders` | BEGIN→INSERT S1_Ssub→INSERT 라인 N→COMMIT |
| `BtnSaveClick` (수정) | `PUT /api/v1/outbound/orders/{id}` | BEGIN→UPDATE/INSERT/DELETE 라인 diff→COMMIT |
| `BtnCancelClick` | `PATCH /api/v1/outbound/orders/{id}/cancel` | UPDATE cancel flag (단일) |

### 10.5 후속 보강 항목

- query_capture 실행 후 SQL 본문(파라미터 포함) 로 SQL-OUT-1~7 정의 보강.
- `analysis/form_layouts/Sobo27.json` 생성 시 UI 레이아웃 기반 화면 검증 보강.
- 변형판 `Subu27_1.pas` 와의 diff 분석 → customer_variants 등록 (1차 외).
- POC 자산 ([`POC/web/seak80-sample/backend/sobo_phase1_sql.py`](../../POC/web/seak80-sample/backend/sobo_phase1_sql.py), [`sobo67_sql.py`](../../POC/web/seak80-sample/backend/sobo67_sql.py)) 의 SQL diff 결과는 [`analysis/c2_outbound_flow.md`](../c2_outbound_flow.md) 에 기록.
