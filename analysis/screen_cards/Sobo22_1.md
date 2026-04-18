# 화면 카드: Sobo22_1 (TSobo22_1)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22_1.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22_1.pas
- 컴포넌트 수: **22** / 이벤트 수: **29** / form 등록 수: **1**
- 주요 컴포넌트: TFlatPanel×7, TFlatEdit×4, TFlatButton×3, TmyLabel3d×2, TFlatComboBox×2, TSobo22_1×1
- 핵심 SQL 수: **10** / 영향 테이블 수: **3** / 검증 규칙 수: **7**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSobo22_1 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Subu22_1.dfm
| component_type | count |
| --- | --- |
| TFlatPanel | 7 |
| TFlatEdit | 4 |
| TFlatButton | 3 |
| TmyLabel3d | 2 |
| TFlatComboBox | 2 |
| TSobo22_1 | 1 |
| TFlatMaskEdit | 1 |
| TdxButton | 1 |
| TDBGridEh | 1 |
- component_count: 22, event_count: 29

- 레이아웃 메타: (없음 — `analysis/form_layouts/Sobo22_1.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **29** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnKeyDown | 8 | Edit101 | Edit101KeyDown |
| OnKeyPress | 8 | Edit101 | Edit111KeyPress |
| OnClick | 4 | Button101 | Button101Click |
| OnChange | 4 | Edit101 | Edit101Change |
| OnActivate | 1 | Sobo22_1 | FormActivate |
| OnClose | 1 | Sobo22_1 | FormClose |
| OnShow | 1 | Sobo22_1 | FormShow |
| OnEnter | 1 | DBGrid101 | DBGrid101Enter |
| OnExit | 1 | DBGrid101 | DBGrid101Exit |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **10**, 타입 분포: DELETE×1, INSERT×1, SELECT×5, UPDATE×3

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S4_Ssub | 7 |
| G7_Ggeo | 2 |
| H2_Gbun | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L332 **SELECT** `G7_Ggeo` — `Select Scode From G7_Ggeo Where`
- L375 **UPDATE** `G7_Ggeo` — `UPDATE G7_Ggeo SET Scode=`
- L409 **SELECT** `S4_Ssub` — `Select * From S4_Ssub Where`
- L612 **SELECT** `H2_Gbun` — `Select Gname,Jubun From H2_Gbun Where`
- L829 **SELECT** `S4_Ssub` — `Select Max(Idnum) From S4_Ssub Where`
- L866 **SELECT** `S4_Ssub` — `Select Max(Jubun),Count(*) From S4_Ssub Where`
- L943 **DELETE** `S4_Ssub` — `DELETE FROM S4_Ssub WHERE ID=@ID and Gdate=`
- L950 **UPDATE** `S4_Ssub` — `UPDATE S4_Ssub SET Scode=`
- L970 **INSERT** `S4_Ssub` — `INSERT INTO S4_Ssub`
- L997 **UPDATE** `S4_Ssub` — `UPDATE S4_Ssub SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **3**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| H2_Gbun | 3 | 40 | 3 | 3 | 49 | ✓ |
| S4_Ssub | 2 | 9 | 4 | 2 | 17 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **7**

| line | type | message |
| --- | --- | --- |
| 381 | message | 체크완료 |
| 395 | message | 거래일자를 다시 선택해 주십시오. |
| 565 | empty_check |  |
| 570 | empty_check |  |
| 764 | empty_check |  |
| 882 | message | 입력된 자료가 있습니다. |
| 938 | message | 삭제 하시겠습니까? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Sobo22_1` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
