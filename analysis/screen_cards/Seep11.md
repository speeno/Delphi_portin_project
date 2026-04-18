# 화면 카드: Seep11 (unknown)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seep11.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seep11.pas
- 컴포넌트 수: **0** / 이벤트 수: **0** / form 등록 수: **1**
- 주요 컴포넌트: -
- 핵심 SQL 수: **5** / 영향 테이블 수: **0** / 검증 규칙 수: **1**
- 매핑 시나리오: **-**

## 1. UI 구성
### unknown — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seep11.dfm
- component_count: 0, event_count: 0

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seep11.json` 미생성)

## 2. 이벤트 흐름
- (event_flow 매칭 0건)

## 3. 데이터 액세스 (SQL)
- SQL 합계: **5**, 타입 분포: DELETE×1, INSERT×1, SELECT×2, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Gg_Megn | 5 |

### 주요 SQL (line 오름차순 상위 15개)
- L101 **SELECT** `Gg_Megn` — `Select Gubun,Gname,Gfild,Gnumb From Gg_Megn Where Gubun`
- L337 **INSERT** `Gg_Megn` — `INSERT INTO Gg_Megn`
- L364 **DELETE** `Gg_Megn` — `DELETE FROM Gg_Megn WHERE Gubun=`
- L386 **UPDATE** `Gg_Megn` — `UPDATE Gg_Megn SET`
- L409 **SELECT** `Gg_Megn` — `Select Gubun,Gname,Gfild,Gnumb From Gg_Megn Where`

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

## 5. 검증 규칙
- 합계: **1**

| line | type | message |
| --- | --- | --- |
| 362 | message | 자료를 삭제하시겠습니까 ? |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Seep11` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
