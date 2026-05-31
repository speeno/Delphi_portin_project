# 레이아웃 매핑: Sobo26 (제작명세서) — 거래관리 Menu206 / C6

DEC-028 의무 — dfm→html 산출물 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물 (Publisher 정본)

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu26/Sobo26.html`](../../tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu26/Sobo26.html)
- 원 dfm: [`WeLove_FTP/도서유통-출판/Subu26.dfm`](../../WeLove_FTP/도서유통-출판/Subu26.dfm) (caption `제작명세서`)
- PAS: [`WeLove_FTP/도서유통-출판/Subu26.pas`](../../WeLove_FTP/도서유통-출판/Subu26.pas) (Button101Click L306~L361, Button201Click L363~)

> **P0 정정(2026-05-31)**: 직전 추출본(물류 `legacy_source_root`)은 「출고접수현황」이라 블록이었으나,
> Publisher 정본 `Subu26.dfm`(제작명세서)을 `publisher_source_root` 로 재추출해 확정.

## 1. 검색 위젯 매핑 (Subu26.pas Button101Click)

| dfm ID | 클래스 | 역할 | WHERE 절 (S2_Ssub) | 모던 |
| --- | --- | --- | --- | --- |
| `Edit101` | TFlatMaskEdit | 시작일 | `Gdate >= '<from>'` | `Sobo26.Edit101` |
| `Edit102` | TFlatMaskEdit | 종료일 | `Gdate <= '<to>'` | `Sobo26.Edit102` |
| `Edit103` | TFlatComboBox | 전표구분 | `Gubun = '<v>'` | `Sobo26.Edit103` |
| `Edit104` | TFlatEdit | 도서코드 | `Bcode = '<v>'` | `Sobo26.Edit104` |
| `Edit105` | TFlatEdit | 거래처코드 | `Gcode = '<v>'`(보조 그리드) | `Sobo26.Edit105` |
| `Button101` | TFlatButton | 조회 | — | `Sobo26.Button101` |

고정 조건: `Ycode = '<로그인 hcode>'`(S2_Ssub 출판사 색인).  
정렬: `ORDER BY Gdate, Gcode`.  
행 보강: `Gcode→Gname`(거래처 G1_Ggeo), `Bcode→Bname`(도서 G4_Book).

## 2. 모던 라우트·서비스 (구현)

| route | 백엔드 | 서비스 |
| --- | --- | --- |
| `/transactions/production/statement` | `GET /api/v1/transactions/production/statement` | `production_service.list_production_statement` |

- 멀티 DB: `s2_ssub_adapt.list_select_sql` 동적 SELECT + `apply_limit_offset_syntax`/`limit_offset_bind`/`in_clause_lookup`.
- `crudParity: R`(조회). 인쇄(`CornerButton*`)는 DEC-017 OOS.
