# 레이아웃 매핑: Sobo26_1 (내역조회(저자)-거래현황) — 거래관리 C10

DEC-028 의무 — dfm→html 산출물 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물 (Publisher 정본)

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu26_1/Sobo26_1.html`](../../tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu26_1/Sobo26_1.html)
- 원 dfm: [`WeLove_FTP/도서유통-출판/MySQL/Subu26_1.dfm`](../../WeLove_FTP/도서유통-출판/MySQL/Subu26_1.dfm) (caption `내역조회(저자)-거래현황`)
- PAS: [`WeLove_FTP/도서유통-출판/MySQL/Subu26_1.pas`](../../WeLove_FTP/도서유통-출판/MySQL/Subu26_1.pas) (Button101Click L362~L418)

> **P0 정정(2026-05-31)**: 직전 P0 문서는 「표준 Menu200 트리에 없음 → 정본 미확정(scaffold)」로 보류했다.
> 실제 Publisher MySQL 빌드 정본 `MySQL/Subu26_1.dfm`(내역조회(저자)-거래현황)을 `publisher_source_root` 로
> 재추출해 본 매핑을 확정했다.

## 1. 검색 위젯 매핑 (Subu26_1.pas Button101Click 기준)

| dfm ID | 클래스 | 역할 | WHERE 절 (S1_Ssub) | 모던 |
| --- | --- | --- | --- | --- |
| `Edit101` | TFlatMaskEdit | 시작일 | `Gdate >= '<from>'` | `Sobo26_1.Edit101` |
| `Edit102` | TFlatMaskEdit | 종료일 | `Gdate <= '<to>'` | `Sobo26_1.Edit102` |
| `Edit103` | TFlatComboBox | 전표구분 | `Gubun = '<출고\|반품\|폐기\|...>'` | `Sobo26_1.Edit103` |
| `Edit105` | TFlatEdit | 거래처코드 | `Gcode = '<v>'` | `Sobo26_1.Edit105` |
| `Edit108` | TFlatEdit | 도서코드 | `Bcode = '<v>'` | `Sobo26_1.Edit108` |
| `Edit110` | TFlatEdit | 저자번호(Idnum) | (표시) `Idnum` | `Sobo26_1.Edit110` |
| `Button101` | TFlatButton | 조회 | — | `Sobo26_1.Button101` |

고정 조건: `Scode='X'`(거래처명/판매), `Ocode='B'`(창고 기본), `Hcode='<로그인 hcode>'`.
정렬: `ORDER BY Gdate, Idnum, Gcode, Gubun, Jubun, Gjisa, ID` · `LIMIT 0,1000`.

## 2. 저자 차원

- 라인 단위 조회(거래명세서 LIST 의 GROUP BY 와 달리 행을 그대로 나열).
- 저자명은 도서에서 끌어온다: `SELECT Gname, Gjeja FROM G4_Book`(Subu26_1.pas L471). `Gjeja` = 저자.
- `Idnum` = 저자번호(Edit110, 5자리).

## 3. 모던 라우트·서비스 (구현)

| route | 백엔드 | 서비스 |
| --- | --- | --- |
| `/transactions/author-history` | `GET /api/v1/transactions/author-history` | `author_history_service.list_author_history` |

- 멀티 DB: `apply_limit_offset_syntax`/`limit_offset_bind`/`in_clause_lookup` 공통 헬퍼(파생 테이블·거대 IN 금지).
- `crudParity: R`(조회 전용). registry id `Sobo_author_history` (preview → phase1).

## 4. Out-of-scope

- `Button201`(신규)·인쇄(`CornerButton*`) — 조회 화면.
- 본사(Ocode='A') 데이터: 기본 창고(B) 고정 — 필요 시 store_kind 후속 확장.
