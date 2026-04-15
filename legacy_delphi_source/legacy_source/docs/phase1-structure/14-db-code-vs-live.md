# Code vs live DB tables

*When live MySQL is available, run `python3 debug/check_mysql_hosts.py --export --database <db>`; this file is refreshed automatically after export (use `--no-crossref` to skip). To regenerate only this doc from an existing CSV: `python3 debug/check_mysql_hosts.py --crossref-only`.*

- **Code inventory**: [`13-db-sql-references.csv`](13-db-sql-references.csv) (44 unique `table` values).
- **Live DB**: [`14-mysql-columns.csv`](14-mysql-columns.csv) (79 tables, schema `chul_09_db`).

## Summary

| Metric | Count |
|--------|------:|
| In both | 41 |
| Code only (not in live export) | 3 |
| Live only (not in code heuristic) | 38 |

## In both

`G0_Gbun`, `G1_Gbun`, `G1_Ggeo`, `G2_Gbun`, `G2_Ggwo`, `G3_Gbun`, `G3_Gjeo`, `G4_Book`, `G4_Gbun`, `G5_Gbun`, `G5_Ggeo`, `G6_Ggeo`, `G7_Gbun`, `G7_Ggeo`, `G8_Ggeo`, `Gg_Magn`, `Gg_Megn`, `Gg_Post`, `H1_Gbun`, `H1_Ssub`, `H2_Gbun`, `H5_Bang`, `Id_Logn`, `Me_Sage`, `S1_Chek`, `S1_Memo`, `S1_Ssub`, `S3_Ssub`, `Sb_Csum`, `Sg_Csum`, `Sg_Gsum`, `Sv_Chng`, `Sv_Ghng`, `Sv_Gsum`, `T1_Gbun`, `T1_Ssub`, `T2_Ssub`, `T3_Ssub`, `T4_Ssub`, `T5_Ssub`, `T6_Ssub`
## Code only

*Referenced in Delphi closure scan but no matching `TABLE_NAME` in live export.*

- `S4_Ssub`
- `T0_Gbun`
- `T8_Gbun`

## Live only

*Present in MySQL but not captured as a table token in [`extract_db_sql_references.py`](../../debug/extract_db_sql_references.py) scan.*

- `G1_Ggeo_1`
- `G1_Logn`
- `G7_Logn`
- `G8_Gbun`
- `Gg_Book`
- `Gg_Memo`
- `Gg_Prnt`
- `Gs_Csum`
- `Gs_Gsum`
- `H4_Iyeo`
- `Id_Memo`
- `Ie_Logn`
- `Ie_Memo`
- `In_Csum`
- `In_Gsum`
- `J1_Sub1`
- `J2_Sub1`
- `J2_Sub2`
- `J3_Sub1`
- `J4_Sub1`
- `J5_Sub1`
- `J6_Sub1`
- `J6_Sub2`
- `J6_Sub3`
- `J7_Sub1`
- `J8_Sub1`
- `J9_Sub1`
- `J9_Sub2`
- `S2_Ssub`
- `S7_Memo`
- `S7_Ssub`
- `Sm_Ggeo`
- `Sm_Ssub`
- `Sv_Csum`
- `Sx_Chek`
- `Sx_Host`
- `Sx_Memo`
- `T7_Ssub`
