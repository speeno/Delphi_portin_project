# 레이아웃 매핑: Sobo28 (원천징수관리) — 거래관리 Menu208 / C8

DEC-028 의무 — dfm→html 산출물 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물 (Publisher 정본)

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu28/Sobo28.html`](../../tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu28/Sobo28.html)
- 원 dfm: [`WeLove_FTP/도서유통-출판/Subu28.dfm`](../../WeLove_FTP/도서유통-출판/Subu28.dfm) (caption `원천징수관리`)
- PAS: [`WeLove_FTP/도서유통-출판/Subu28.pas`](../../WeLove_FTP/도서유통-출판/Subu28.pas) (Button101Click L290~L342)

> **P0 정정(2026-05-31)**: 직전 추출본(물류)은 「출고택배관리」였으나 Publisher 정본 `Subu28.dfm`(원천징수관리) 재추출로 확정.

## 1. 검색 위젯 매핑 (Subu28.pas Button101Click)

| dfm ID | 클래스 | 역할 | WHERE 절 (S3_Ssub) | 모던 |
| --- | --- | --- | --- | --- |
| `Edit101` | TFlatMaskEdit | 시작일 | `Gdate >= '<from>'` | `Sobo28.Edit101` |
| `Edit102` | TFlatMaskEdit | 종료일 | `Gdate <= '<to>'` | `Sobo28.Edit102` |
| `Edit103` | TFlatEdit | 저자코드(시작) | `Gcode >= '<v>'` | `Sobo28.Edit103` |
| `Edit105` | TFlatEdit | 저자코드(끝) | `Gcode <= '<v>'` | `Sobo28.Edit105` |
| `Button101` | TFlatButton | 조회 | — | `Sobo28.Button101` |
| `DBGrid101` | TDBGridEh | 결과 그리드 | — | `Sobo28.DBGrid101` |

고정 조건: `Hcode = '<로그인 hcode>'`(S3_Ssub 출판사 색인).  
정렬: `ORDER BY Gdate, Gcode`.  
행 보강: `Gcode→Gname` = **저자명** `G3_Gjeo.Gposa` (Subu28.pas L320~L325, ('', Gcode) 폴백 포함).

## 2. 모던 라우트·서비스 (구현)

| route | 백엔드 | 서비스 |
| --- | --- | --- |
| `/transactions/withholding` | `GET /api/v1/transactions/withholding` | `withholding_service.list_withholding` |

- 컬럼: 지급액(Gssum)·세율(Grat1)·소득세(Gisum)·주민세(Gosum)·실지급(Gbsum).
- 멀티 DB: `s3_ssub_adapt` + `apply_limit_offset_syntax`/`limit_offset_bind`/`in_clause_lookup`.
- `crudParity: R`. 인쇄(`CornerButton*`·`Button701/702`)는 DEC-017 OOS.
