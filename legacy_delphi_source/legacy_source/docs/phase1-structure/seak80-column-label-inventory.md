# Seak80 sample: DB grid column label inventory (DFM source)

UTF-8. Label maps live in `web/seak80-sample/frontend/seak80-column-labels.js`.

## G2_Gbun (Sobo12 / `GET /api/sobo12/g2-gbun`)

- Source: `도서유통/한국도서유통/출판/MySQL/도서유통/chul_09(위러브)/Subu12.dfm`, object `DBGrid101`, `DataSource1` (G2_Gbun list).
- Captions: `GCODE` → 코드, `GNAME` → 입고처명, `SCODE` → `^`.

## G1_Ggeo (Sobo11 / Sobo15, phase2 `sobo11` / `sobo15`)

- Source: `도서유통/한국도서유통/출판/MySQL/도서유통/chul_09(위러브)/Subu11.dfm`, object `DBGrid101`.
- Captions: `GCODE` → 코드, `GNAME` → 거래처명, `SCODE` → `^`.

## T1_Gbun (Sobo13 phase1 / `GET /api/sobo13/t1-gbun`)

- Web POC uses `SELECT * FROM T1_Gbun` (see `web/seak80-sample/backend/sobo_phase1_sql.py`).
- Caption hints from `도서유통/한국도서유통/출판/MySQL/Subu13.dfm`, object `DBGrid201`: `GCODE` → 코드, `GNAME` → 저자구분 (same unit; lower grid).
- Other `T1_Gbun` columns: use shared `_Gbun` / common keys in JS, or raw field name.

## Phase2 tables (partial)

`G4_Book`, `G6_Ggeo`, `G7_Gbun`, `G7_Ggeo`, `T0_Gbun`: shared lowercase labels in JS where safe; unknown columns keep the DB field name.

## Editor note

These HTML/MD files must be saved as **UTF-8** (no BOM). If the IDE re-saves Korean as CP949 while `<meta charset="UTF-8">` remains, browsers will show mojibake. Use `python3` to re-encode if needed (see prior `cp949` → `utf-8` recovery).
