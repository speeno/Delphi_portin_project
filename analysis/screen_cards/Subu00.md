# 화면 카드: Subu00 (TSubu00)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Chul.dfm, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Chul.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Chul.pas, /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Chul.pas
- 컴포넌트 수: **298** / 이벤트 수: **197** / form 등록 수: **2**
- 주요 컴포넌트: TMenuItem×199, TToolButton×66, TStringGrid×4, TPopupMenu×3, TImageList×3, TTimer×3
- 핵심 SQL 수: **11** / 영향 테이블 수: **4** / 검증 규칙 수: **32**
- 매핑 시나리오: **C1 로그인·세션 시작**

## 1. UI 구성
### TSubu00 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Chul.dfm
| component_type | count |
| --- | --- |
| TMenuItem | 130 |
| TToolButton | 33 |
| TStringGrid | 2 |
| TPopupMenu | 2 |
| TImageList | 2 |
| TTimer | 2 |
| TSubu00 | 1 |
| TToolBar | 1 |
| TWebBrowser | 1 |
| TMainMenu | 1 |
| TOpenDialog | 1 |
| TSaveDialog | 1 |
| TPrintDialog | 1 |
| TPrinterSetupDialog | 1 |
| TPing | 1 |
| TMDIWallpaper | 1 |
| TApplicationEvents | 1 |
- component_count: 182, event_count: 123

### TSubu00 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Interbase/Chul.dfm
| component_type | count |
| --- | --- |
| TMenuItem | 69 |
| TToolButton | 33 |
| TStringGrid | 2 |
| TSubu00 | 1 |
| TToolBar | 1 |
| TMainMenu | 1 |
| TPopupMenu | 1 |
| TOpenDialog | 1 |
| TSaveDialog | 1 |
| TPrintDialog | 1 |
| TPrinterSetupDialog | 1 |
| TImageList | 1 |
| TPing | 1 |
| TTimer | 1 |
| TMDIWallpaper | 1 |
- component_count: 116, event_count: 74

- 레이아웃 메타: (없음 — `analysis/form_layouts/Subu00.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **197** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 184 | ToolButton01 | ToolButton01Click |
| OnClose | 2 | Subu00 | FormClose |
| OnShow | 2 | Subu00 | FormShow |
| OnEchoRequest | 2 | Ping1 | Ping1EchoRequest |
| OnEchoReply | 2 | Ping1 | Ping1EchoReply |
| OnDnsLookupDone | 2 | Ping1 | Ping1DnsLookupDone |
| OnNewWindow2 | 1 | WebBrowser1 | WebBrowser1NewWindow2 |
| OnMessage | 1 | ApplicationEvents1 | ApplicationEvents1Message |
| OnTimer | 1 | Timer2 | Timer2Timer |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **11**, 타입 분포: SELECT×9, UPDATE×2

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Id_Logn | 7 |
| Gg_Magn | 2 |
| G7_Ggeo | 1 |
| Me_Sage | 1 |

### 주요 SQL (line 오름차순 상위 15개)
- L327 **SELECT** `Id_Logn` — `Select Hcode,Hname,Gpass From Id_Logn`
- L441 **SELECT** `Id_Logn` — `Select Hcode,Hname,Gpass From Id_Logn`
- L490 **SELECT** `G7_Ggeo` — `Select Gcode From G7_Ggeo`
- L1902 **SELECT** `Gg_Magn` — `Select Top,L11,L61,L62 From Gg_Magn Where`
- L1959 **SELECT** `Id_Logn` — `Select Gpass From Id_Logn Where`
- L1967 **UPDATE** `Id_Logn` — `UPDATE Id_Logn SET Gcode=`
- L2255 **UPDATE** `Id_Logn` — `UPDATE Id_Logn SET Gcode=`
- L2318 **SELECT** `Gg_Magn` — `Select Top,L11,L61,L62 From Gg_Magn Where`
- L3302 **SELECT** `Id_Logn` — `Select Gname From Id_Logn Where`
- L3736 **SELECT** `Id_Logn` — `Select Gcode From Id_Logn Where`
- L4508 **SELECT** `Me_Sage` — `Select Date1,Date2 From Me_Sage Where Hcode=`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **4**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | ✓ |
| Me_Sage | 2 | 13 | 2 | 2 | 19 | ✓ |
| Id_Logn | 0 | 9 | 4 | 0 | 13 | ✓ |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **32**

| line | type | message |
| --- | --- | --- |
| 339 | message | 비밀번호가 틀립니다. |
| 343 | message | 사용자 또는 아이디가 틀립니다. |
| 359 | message | Program Key를 등록해 주세요. |
| 364 | message | 다시 시도해 주십시오. |
| 398 | message | 00 |
| 434 | message | 01 |
| 437 | message | 02 |
| 453 | message | 비밀번호가 틀립니다. |
| 457 | message | 사용자 또는 아이디가 틀립니다. |
| 477 | message | Program Key를 등록해 주세요. |
| 482 | message | 다시 시도해 주십시오. |
| 580 | message | 03 |
| 583 | message | 04 |
| 586 | message | 05 |
| 588 | message | 06 |
| 594 | message | 07 |
| 1840 | message | IP: |
| 1841 | message | IP: |
| 1874 | message | 서버와 연결실패...  |
| 1888 | message | 환경설정 실패...  |

_(상위 20건, 전체 32건)_

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Subu00` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: C1 로그인·세션 시작)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
