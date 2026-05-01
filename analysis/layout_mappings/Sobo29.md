# Sobo29 layout mapping — 기타명세서 / 신간명세서

## Legacy Inputs

- Generated DFM HTML: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu29/Sobo29.html`
- Form JSON: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu29/Sobo29.form.json`
- Screen card: `analysis/screen_cards/Sobo29.md`

## Areas

| area | legacy container | modern route |
|---|---|---|
| 검색 | `Panel001` | `/transactions/other` 검색 폼 |
| 후보 도서 | `DBGrid102` | 도서코드 필터 및 향후 lookup |
| 명세 그리드 | `Panel002`, `DBGrid101` | `DataGrid` |
| 전체메모 | `Panel300`, `Panel301`, `Edit203`, `Edit204` | 메모 입력 + 저장 |

## Widget Mapping

| legacy_id | TabOrder | role | modern selector |
|---|---:|---|---|
| `Sobo29.Panel001` | 0 | 검색 영역 | 검색 폼 wrapper |
| `Sobo29.Edit101` | 0 | 거래일자 | 시작일 input |
| `Sobo29.DateEdit1` | 18 | 거래일자 선택 | 종료일 input |
| `Sobo29.Edit107` | 1 | 거래처/출판사 코드 | hcode input |
| `Sobo29.Edit104` | 6 | 도서코드 | bcode input |
| `Sobo29.Edit106` | 3 | 전표구분 | jubun input |
| `Sobo29.Button101` | 13 | 조회 | 검색 버튼 |
| `Sobo29.DBGrid101` | 0 | 명세 그리드 | DataGrid table |
| `Sobo29.DBGrid101.PUBUN` | - | 구분 | grid header |
| `Sobo29.DBGrid101.GCODE` | - | 코드 | grid header |
| `Sobo29.DBGrid101.GNAME` | - | 거래처명 | grid header |
| `Sobo29.DBGrid101.GSQUT` | - | 수량 | grid header |
| `Sobo29.DBGrid101.GDANG` | - | 단가 | grid header |
| `Sobo29.DBGrid101.GRAT1` | - | 비율 | grid header |
| `Sobo29.DBGrid101.GSSUM` | - | 금액 | grid header |
| `Sobo29.DBGrid101.GBIGO` | - | 비고 | grid header |
| `Sobo29.DBGrid101.YESNO` | - | 배송 | grid header |
| `Sobo29.DBGrid102.BCODE` | - | 도서코드 후보 | bcode column reference |
| `Sobo29.Panel300` | 4 | 전체메모 영역 | memo card |
| `Sobo29.Panel301` | 0 | 전체메모 label | memo label |
| `Sobo29.Edit203` | 1 | 전체메모 1 | memo input |
| `Sobo29.Edit204` | 2 | 전체메모 2 | memo input |
| `Sobo29.Button301` | - | 전체메모 저장 | save button |

## Data / Events

| legacy event | legacy SQL | modern mapping |
|---|---|---|
| `Button101Click` | `SELECT * FROM S1_Ssub WHERE ...` | `GET /api/v1/transactions/other` |
| `Edit*KeyDown` / lookup | `G4_Book`, `G1_Ggeo` lookup | first phase: explicit filters; lookup can be added without changing endpoint |
| `Button301Click` | `SELECT/UPDATE/INSERT S1_Memo` | `PATCH /api/v1/transactions/other/memo` |

## Notes

The generated DFM caption is `신간명세서`. The menu keeps `기타명세서` naming for the mobile/modern group, while the default `jubun` filter is `신간` to preserve the legacy default.
