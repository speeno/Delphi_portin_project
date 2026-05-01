# Sobo48 layout mapping — 출판사관리(설정)

## Legacy Inputs

- Generated DFM HTML: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu48/Sobo48.html`
- Form JSON: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu48/Sobo48.form.json`
- Screen card: `analysis/screen_cards/Sobo48.md`

## Areas

| area | legacy container | modern route |
|---|---|---|
| 검색 | `Panel001`, `dxButton1` | `/ledger/comparison` 검색 폼 |
| 설정 그리드 | `Panel002`, `DBGrid101` | `DataGrid` |
| 저장 상태 | `Panel007`, `ProgressBar*` | 행별 저장 상태 |

## Widget Mapping

| legacy_id | TabOrder | role | modern selector |
|---|---:|---|---|
| `Sobo48.Panel001` | 0 | 검색 영역 | 검색 폼 wrapper |
| `Sobo48.dxButton1` | 0 | 검색 버튼 | 검색 버튼 |
| `Sobo48.Panel002` | 1 | 결과 영역 | 결과 카드 |
| `Sobo48.DBGrid101` | 0 | 출판사 설정 그리드 | DataGrid table |
| `Sobo48.DBGrid101.GCODE` | - | 출판사코드 | grid header/input |
| `Sobo48.DBGrid101.GNAME` | - | 출판사명 | grid header |
| `Sobo48.DBGrid101.CHEK3` | - | SET재고적용 | grid select |
| `Sobo48.DBGrid101.YESNO` | - | 출고정지유무(`Scode AS Yesno`) | grid select |

## Data / Events

| legacy event | legacy SQL | modern mapping |
|---|---|---|
| `Button101Click` / search | `SELECT Gcode,Gname,Chek3,Scode AS Yesno FROM G7_Ggeo` | `GET /api/v1/ledger/comparison` |
| `Button300Click` / save | `UPDATE G7_Ggeo SET Scode=...` | `PATCH /api/v1/ledger/comparison/{gcode}` body `yesno` |
| `Button300Click` / save | `UPDATE G7_Ggeo SET Chek3=...` | `PATCH /api/v1/ledger/comparison/{gcode}` body `chek3` |

## Notes

`Sobo48` was previously catalogued as ledger comparison, but the generated DFM caption and static SQL point to publisher settings. The modern route is kept for menu compatibility; the implemented behavior follows the legacy form data contract.
