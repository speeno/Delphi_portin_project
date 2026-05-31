# 레이아웃 매핑: Sobo27 (제작현황) — 거래관리 Menu207 / C7

DEC-028 의무 — dfm→html 산출물 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물 (Publisher 정본)

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu27/Sobo27.html`](../../tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu27/Sobo27.html)
- 원 dfm: [`WeLove_FTP/도서유통-출판/Subu27.dfm`](../../WeLove_FTP/도서유통-출판/Subu27.dfm) (caption `제작현황`)
- PAS: [`WeLove_FTP/도서유통-출판/Subu27.pas`](../../WeLove_FTP/도서유통-출판/Subu27.pas) (Button101Click L285~L341)

> **P0 정정(2026-05-31)**: 직전 추출본(물류)은 「출고접수관리」였으나 Publisher 정본 `Subu27.dfm`(제작현황) 재추출로 확정.

## 1. 검색 위젯 매핑 (Subu27.pas Button101Click)

| dfm ID | 클래스 | 역할 | WHERE 절 (S2_Ssub) | 모던 |
| --- | --- | --- | --- | --- |
| `Edit101` | TFlatMaskEdit | 시작일 | `Gdate >= '<from>'` | `Sobo27.Edit101` |
| `Edit102` | TFlatMaskEdit | 종료일 | `Gdate <= '<to>'` | `Sobo27.Edit102` |
| `Edit103` | TFlatComboBox | 전표구분 | `Gubun = '<v>'` | `Sobo27.Edit103` |
| `Edit104` | TFlatEdit | 거래처코드 | `Gcode = '<v>'` | `Sobo27.Edit104` |
| `Edit106` | TFlatEdit | 도서코드(시작) | `Bcode >= '<v>'` | `Sobo27.Edit106` |
| `Edit107` | TFlatEdit | 도서코드(끝) | `Bcode <= '<v>'` | `Sobo27.Edit107` |
| `Button101` | TFlatButton | 조회 | — | `Sobo27.Button101` |

고정 조건: `Ycode = '<로그인 hcode>'`. 정렬: `ORDER BY Gdate, Gcode`.  
행 보강: `Gcode→Gname`(G1_Ggeo), `Bcode→Bname`(G4_Book).

## 2. 모던 라우트·서비스 (구현)

| route | 백엔드 | 서비스 |
| --- | --- | --- |
| `/transactions/production/status` | `GET /api/v1/transactions/production/status` | `production_service.list_production_status` |

- 멀티 DB: `s2_ssub_adapt` + `apply_limit_offset_syntax`/`limit_offset_bind`/`in_clause_lookup`.
- `crudParity: R`. 인쇄 OOS(DEC-017).
