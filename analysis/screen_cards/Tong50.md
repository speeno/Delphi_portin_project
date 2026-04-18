# 화면 카드: Tong50 (TTong50)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong05.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong05.pas
- 컴포넌트 수: **33** / 이벤트 수: **23** / form 등록 수: **1**
- 주요 컴포넌트: TPanel×5, TSpeedButton×5, TMenuItem×5, TLabel×3, TEdit×3, TButton×2
- 핵심 SQL 수: **3** / 영향 테이블 수: **1** / 검증 규칙 수: **2**
- 매핑 시나리오: **-**

## 1. UI 구성
### TTong50 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Tong05.dfm
| component_type | count |
| --- | --- |
| TPanel | 5 |
| TSpeedButton | 5 |
| TMenuItem | 5 |
| TLabel | 3 |
| TEdit | 3 |
| TButton | 2 |
| TTong50 | 1 |
| TPaintBox | 1 |
| TCheckBox | 1 |
| TListView | 1 |
| TRichEdit | 1 |
| TOpenDialog | 1 |
| TImageList | 1 |
| TEmail | 1 |
| TFontDialog | 1 |
| TPopupMenu | 1 |
- component_count: 33, event_count: 23

- 레이아웃 메타: (없음 — `analysis/form_layouts/Tong50.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **23** / 이벤트 종류: **9**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 10 | btnRecip | btnRecipClick |
| OnExit | 4 | txtSubject | txtRecipientExit |
| OnEnter | 3 | txtSubject | txtRecipientEnter |
| OnClose | 1 | Tong50 | FormClose |
| OnCreate | 1 | Tong50 | FormCreate |
| OnDestroy | 1 | Tong50 | FormDestroy |
| OnShow | 1 | Tong50 | FormShow |
| OnMouseMove | 1 | pnlVSplit | pnlVSplitMouseMove |
| OnPopup | 1 | PopupMenu1 | PopupMenu1Popup |

## 3. 데이터 액세스 (SQL)
- SQL 합계: **3**, 타입 분포: INSERT×1, SELECT×1, UPDATE×1

### 영향 테이블 (작업 빈도)
| table | count |
| --- | --- |
| Gg_Magn | 3 |

### 주요 SQL (line 오름차순 상위 15개)
- L197 **SELECT** `Gg_Magn` — `Select F11,F12,F21,F22,F31,F32 From Gg_Magn`
- L210 **INSERT** `Gg_Magn` — `INSERT INTO Gg_Magn`
- L223 **UPDATE** `Gg_Magn` — `UPDATE Gg_Magn SET`

## 4. DB 영향
- 본 폼이 접근하는 테이블: **1**
| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | ✓ |
- 트랜잭션 경계는 정적 분석 미산출 — query_capture 결과로 보강 권장.

## 5. 검증 규칙
- 합계: **2**

| line | type | message |
| --- | --- | --- |
| 447 | empty_check |  |
| 463 | empty_check |  |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Tong50` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
