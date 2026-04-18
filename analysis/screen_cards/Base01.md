# 화면 카드: Base01 (unknown)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Base01.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Base01.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Base01.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Base01.pas
- 컴포넌트 수: **0** / 이벤트 수: **0** / form 등록 수: **2**
- 주요 컴포넌트: -
- 핵심 SQL 수: **175** / 영향 테이블 수: **0** / 검증 규칙 수: **77**
- 매핑 시나리오: **-**

## 1. UI 구성
### unknown — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Base01.dfm
- component_count: 0, event_count: 0

### unknown — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Base01.dfm
- component_count: 0, event_count: 0

- 레이아웃 메타: (없음 — `analysis/form_layouts/Base01.json` 미생성)

## 2. 이벤트 흐름
- (event_flow 매칭 0건)

## 3. 데이터 액세스 (SQL)
- SQL 합계: **175**, 타입 분포: DELETE×29, INSERT×39, SELECT×61, UPDATE×46

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| S1_Ssub | 16 |
| Sg_Csum | 8 |
| H1_Gbun | 8 |
| Sv_Gsum | 8 |
| G1_Ggeo | 7 |
| G2_Ggwo | 7 |
| G6_Ggeo | 6 |
| S2_Ssub | 6 |
| T1_Gbun | 6 |
| H2_Gbun | 6 |
| H1_Ssub | 6 |
| T1_Ssub | 6 |
| Sg_Gsum | 6 |
| In_Gsum | 6 |
| In_Csum | 6 |
| Gs_Gsum | 6 |
| Gs_Csum | 6 |
| Sv_Csum | 6 |
| Sv_Chng | 6 |
| Sv_Ghng | 6 |

### 주요 SQL (line 오름차순 상위 15개)
- L3426 **DELETE** `G6_Ggeo` — `DELETE FROM G6_Ggeo WHERE ID=@ID`
- L3443 **INSERT** `G6_Ggeo` — `INSERT INTO G6_Ggeo`
- L3461 **UPDATE** `G6_Ggeo` — `UPDATE G6_Ggeo SET`
- L3598 **DELETE** `S1_Ssub` — `DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=`
- L3618 **INSERT** `S1_Ssub` — `INSERT INTO S1_Ssub`
- L3658 **UPDATE** `S1_Ssub` — `UPDATE S1_Ssub SET`
- L4389 **DELETE** `S2_Ssub` — `DELETE FROM S2_Ssub WHERE ID=@ID and Ycode=`
- L4408 **INSERT** `S2_Ssub` — `INSERT INTO S2_Ssub`
- L4442 **UPDATE** `S2_Ssub` — `UPDATE S2_Ssub SET`
- L4508 **DELETE** `T1_Gbun` — `DELETE FROM T1_Gbun WHERE ID=@ID`
- L4525 **INSERT** `T1_Gbun` — `INSERT INTO T1_Gbun`
- L4544 **UPDATE** `T1_Gbun` — `UPDATE T1_Gbun SET`
- L4575 **DELETE** `G6_Ggeo` — `DELETE FROM G6_Ggeo WHERE ID=@ID`
- L4592 **INSERT** `G6_Ggeo` — `INSERT INTO G6_Ggeo`
- L4620 **UPDATE** `G6_Ggeo` — `UPDATE G6_Ggeo SET`

_(상위 15건 표기, 전체 175건은 `analysis/query_catalog.json` 참조)_

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

## 5. 검증 규칙
- 합계: **77**

| line | type | message |
| --- | --- | --- |
| 3405 | message | Excel이 설치되어 있지 않습니다. |
| 3422 | message | 삭제 하시겠습니까? |
| 3503 | message | Excel이 설치되어 있지 않습니다. |
| 3507 | message | 삭제 하시겠습니까? |
| 3594 | message | 삭제 하시겠습니까? |
| 3603 | message | Excel이 설치되어 있지 않습니다. |
| 3702 | message | Excel이 설치되어 있지 않습니다. |
| 3726 | message | 삭제 하시겠습니까? |
| 3800 | message | Excel이 설치되어 있지 않습니다. |
| 3858 | message | 삭제 하시겠습니까? |
| 3991 | message | 삭제 하시겠습니까? |
| 4067 | message | Excel이 설치되어 있지 않습니다. |
| 4124 | message | 삭제 하시겠습니까? |
| 4167 | message | Excel이 설치되어 있지 않습니다. |
| 4256 | message | 삭제 하시겠습니까? |
| 4290 | message | Excel이 설치되어 있지 않습니다. |
| 4385 | message | 삭제 하시겠습니까? |
| 4415 | message | Excel이 설치되어 있지 않습니다. |
| 4504 | message | 삭제 하시겠습니까? |
| 4571 | message | 삭제 하시겠습니까? |

_(상위 20건, 전체 77건)_

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Base01` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
