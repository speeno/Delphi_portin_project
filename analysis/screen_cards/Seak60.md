# 화면 카드: Seak60 (TSeak60)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak06.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak06.pas
- 컴포넌트 수: **250** / 이벤트 수: **7** / form 등록 수: **1**
- 주요 컴포넌트: TFlatSpinEditFloat×145, TLabel×50, TFlatEdit×37, TFlatButton×7, TFlatGroupBox×6, TTabSheet×3
- 핵심 SQL 수: **10** / 영향 테이블 수: **1** / 검증 규칙 수: **0**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeak60 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seak06.dfm
| component_type | count |
| --- | --- |
| TFlatSpinEditFloat | 145 |
| TLabel | 50 |
| TFlatEdit | 37 |
| TFlatButton | 7 |
| TFlatGroupBox | 6 |
| TTabSheet | 3 |
| TSeak60 | 1 |
| TPageControl | 1 |
- component_count: 250, event_count: 7

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seak60.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **7** / 이벤트 종류: **4**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 4 | Button101 | Button101Click |
| OnClose | 1 | Seak60 | FormClose |
| OnShow | 1 | Seak60 | FormShow |
| OnChange | 1 | PageControl1 | PageControl1Change |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **10**, 타입 분포: SELECT×9, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Gg_Magn | 2 |

### 주요 SQL (line 오름차순 상위 15개)
- L298 **SELECT** `` — `Select Top,L91,L92,L93,L94,L95,L96,L97,L98,L99`
- L321 **SELECT** `` — `Select Top,L11,L12,L13,L14,L15,L16,L17,L18,L19`
- L337 **SELECT** `` — `Select Top,L21,L22,L23,L24,L25,L26,L27,L28,L29`
- L354 **SELECT** `` — `Select Top,L31,L32,L33,L34,L35,L36,L37,L38,L39`
- L370 **SELECT** `` — `Select Top,L41,L42,L43,L44,L45,L46,L47,L48,L49`
- L386 **SELECT** `` — `Select Top,L51,L52,L53,L54,L55,L56,L57,L58,L59`
- L408 **SELECT** `` — `Select Top,L61,L62,L63,L64,L65,L66,L67,L68,L69`
- L566 **SELECT** `` — `Select Top,L71,L72,L73,L74,L75,L76,L77,L78,L79`
- L742 **UPDATE** `Gg_Magn` — `UPDATE Gg_Magn SET`
- L968 **SELECT** `Gg_Magn` — `Select * From Gg_Magn Where Gu`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **1**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | ✓ |
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
- (수동) 위 문서에서 form `Seak60` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
