# Member delta sheet (priority samples)

Tags: **D_UI** (.dfm), **D_BIZ** (SQL/constants/logic), **D_CFG** (integration paths).

## Plan T1-T4 mapping (quick read)

- **T1**: `Chulpan.dpr` `uses` differs mainly in `in` paths; unit names often match baseline (see DPR uses delta per folder).
- **T2**: Same unit set as baseline but a few `Subu*`/`Seok*` sources differ (business/FTP tweaks).
- **T3**: `Base01` / `Chul` content diverges (sha/size): menu/data model fork risk.
- **T4**: DB stack fork: see `Interbase` in [03-variant-dpr-diff.md](03-variant-dpr-diff.md) and `Interbase/Base01.pas` in matrix.

## `도서유통/book_07(북앤북)`

- **DPR uses delta vs root** (`도서유통/book_07(북앤북)/Chulpan.dpr`): only in baseline (-) **29**, only in variant (+) **1**.
- `Base01.pas`: *(not in folder; build may use root or other path)*
- `Chul.pas`: **differs from root** size=115310 sha=4f9293a45575f014 (root: (157467, '8a0da04e845658f0')) — `shell / menu`
- `Subu30.pas`: **differs from root** size=5283 sha=e7523a06f8089968 (root: (5253, '09abeda4b0143001')) — `sample work form`
- `Subu30.dfm`: size=1604221 (root dfm size=2020320) — D_UI likely

## `도서유통/book_07(북앤북Skin)`

- **DPR uses delta vs root** (`도서유통/book_07(북앤북Skin)/Chulpan.dpr`): only in baseline (-) **19**, only in variant (+) **2**.
- `Base01.pas`: *(not in folder; build may use root or other path)*
- `Chul.pas`: **differs from root** size=118283 sha=f37c6ec4adb8bf96 (root: (157467, '8a0da04e845658f0')) — `shell / menu`
- `Subu30.pas`: **differs from root** size=5335 sha=ec9bfeb8e0852584 (root: (5253, '09abeda4b0143001')) — `sample work form`
- `Subu30.dfm`: size=1604402 (root dfm size=2020320) — D_UI likely

## `도서유통/book_07(북앤북NEW)`

- **DPR uses delta vs root** (`도서유통/book_07(북앤북NEW)/Chulpan.dpr`): only in baseline (-) **23**, only in variant (+) **0**.
- `Base01.pas`: **differs from root** size=327102 sha=830bc9c8e2a285bf (root: (359196, '60da1304da741db3')) — `D_BIZ / T3`
- `Chul.pas`: **differs from root** size=119959 sha=0805f0ee84f54ec4 (root: (157467, '8a0da04e845658f0')) — `shell / menu`
- `Subu30.pas`: **identical to root** (size=5253, sha=09abeda4b0143001)
- `Subu30.dfm`: size=2020329 (root dfm size=2020320) — D_UI likely

## `도서유통/book_07(up)`

- **DPR uses delta**: *(no Chulpan.dpr under this folder within maxdepth 6)*
- `Base01.pas`: **differs from root** size=375449 sha=43298cad743863ff (root: (359196, '60da1304da741db3')) — `D_BIZ / T3`
- `Chul.pas`: *(not in folder; build may use root or other path)*
- `Subu30.pas`: *(not in folder; build may use root or other path)*

## `도서유통/book_11(고려출판물류)`

- **DPR uses delta vs root** (`도서유통/book_11(고려출판물류)/Chulpan.dpr`): only in baseline (-) **4**, only in variant (+) **16**.
- `Base01.pas`: *(not in folder; build may use root or other path)*
- `Chul.pas`: **differs from root** size=148777 sha=9de2940281ed06e4 (root: (157467, '8a0da04e845658f0')) — `shell / menu`
- `Subu30.pas`: **differs from root** size=6353 sha=d1e827e2cd22487e (root: (5253, '09abeda4b0143001')) — `sample work form`
- `Subu30.dfm`: size=599696 (root dfm size=2020320) — D_UI likely

## `도서유통/book_11(정진물류)`

- **DPR uses delta vs root** (`도서유통/book_11(정진물류)/Chulpan.dpr`): only in baseline (-) **7**, only in variant (+) **9**.
- `Base01.pas`: *(not in folder; build may use root or other path)*
- `Chul.pas`: **differs from root** size=146079 sha=783cca48ab9b2b25 (root: (157467, '8a0da04e845658f0')) — `shell / menu`
- `Subu30.pas`: **differs from root** size=6390 sha=875d50e4a11867a5 (root: (5253, '09abeda4b0143001')) — `sample work form`
- `Subu30.dfm`: size=8190 (root dfm size=2020320) — D_UI likely

## book_11 pair: Base01 comparison

