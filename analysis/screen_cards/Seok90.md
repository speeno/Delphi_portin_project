# 화면 카드: Seok90 (TSeok90)

_생성: 2026-04-18 04:10 UTC — `tools/analysis/screen_card_builder.py`_

## 0. 한눈 요약
- 파일(DFM): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok09.dfm
- 파일(PAS 추정): /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok09.pas
- 컴포넌트 수: **21** / 이벤트 수: **11** / form 등록 수: **1**
- 주요 컴포넌트: TLabel×6, TSpeedButton×4, TPanel×3, TSeok90×1, TShape×1, TFileListBox×1
- 핵심 SQL 수: **0** / 영향 테이블 수: **0** / 검증 규칙 수: **7**
- 매핑 시나리오: **-**

## 1. UI 구성
### TSeok90 — /Users/speeno/Delphi_porting/legacy_delphi_source/legacy_source/Seok09.dfm
| component_type | count |
| --- | --- |
| TLabel | 6 |
| TSpeedButton | 4 |
| TPanel | 3 |
| TSeok90 | 1 |
| TShape | 1 |
| TFileListBox | 1 |
| TProgressBar | 1 |
| TCheckListBox | 1 |
| TTimer | 1 |
| TIdFTP | 1 |
| TIdAntiFreeze | 1 |
- component_count: 21, event_count: 11

- 레이아웃 메타: (없음 — `analysis/form_layouts/Seok90.json` 미생성)

## 2. 이벤트 흐름
- 핸들러 합계: **11** / 이벤트 종류: **8**

| event | count | 예시 component | 예시 handler |
| --- | --- | --- | --- |
| OnClick | 4 | btnConnect | btnConnectClick |
| OnCreate | 1 | Seok90 | FormCreate |
| OnShow | 1 | Seok90 | FormShow |
| OnTimer | 1 | Timer1 | Timer1Timer |
| OnWork | 1 | IdFTP1 | IdFTP1Work |
| OnWorkBegin | 1 | IdFTP1 | IdFTP1WorkBegin |
| OnWorkEnd | 1 | IdFTP1 | IdFTP1WorkEnd |
| OnlyWhenIdle | 1 | IdAntiFreeze1 | False |

## 3. 데이터 액세스 (SQL)
- (query_catalog 매칭 0건)

## 4. DB 영향
- (db_impact_matrix 매칭 0건)

## 5. 검증 규칙
- 합계: **7**

| line | type | message |
| --- | --- | --- |
| 136 | message | FTP 서버  |
| 232 | message | 프로그램을 다운 받으시겠습니까? |
| 235 | message | INI파일에 서버IP를 등록하세요... |
| 410 | empty_check |  |
| 412 | message | 다운로드 프로그램을 종료하고  |
| 419 | message | 호스트에 접속되어 있지 않습니다!. |
| 516 | message | 파일받기를 완료하였습니다!. |

## 6. 고객사 분기
- (customer_variants 매칭 0건)

## 7. 관련 OQ·GAP·DEC
- Open Questions: [`legacy-analysis/open-questions.md`](../../legacy-analysis/open-questions.md)
- DB Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md)
- Decisions: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md)
- (수동) 본 화면 관련 항목 ID 를 위 문서에서 grep 하여 갱신.

## 8. 인쇄·바코드 연관
- 인쇄/바코드 매칭 정밀 조사: [`docs/legacy-print-scanner-integration-survey.md`](../../docs/legacy-print-scanner-integration-survey.md)
- (수동) 위 문서에서 form `Seok90` 또는 인접 unit 검색.

## 9. 포팅 체크리스트(자동 생성)
- [x] 본 화면을 다루는 Migration Contract 존재 (시나리오 매칭: -)
- [x] 5축 임계값(eval-axes-and-dod-draft.md) 정의됨
- [ ] 본 화면 SQL 이 query_capture 로 보강됨 (0건 매칭)
