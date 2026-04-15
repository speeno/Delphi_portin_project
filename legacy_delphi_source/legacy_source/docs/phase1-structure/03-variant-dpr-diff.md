# Representative DPR diff: `uses` unit name sets vs root

- Baseline: root `Chulpan.dpr` unit count **129**.

## `도서유통/book_00(위러브)/Chulpan.dpr`

- Variant unit count: **97**
- Only in baseline (-): **32** / only in variant (+): **0**

### Units only in baseline (up to 40)

`Seak04_1`, `Seak08_1`, `Seok04`, `Seok08`, `Subu13_1`, `Subu17_1`, `Subu22_1`, `Subu22_2`, `Subu23_1`, `Subu24_9`, `Subu32_1`, `Subu34_1`, `Subu34_2`, `Subu34_3`, `Subu34_4`, `Subu38_1`, `Subu39_3`, `Subu39_4`, `Subu39_5`, `Subu42_1`, `Subu45_1`, `Subu55_1`, `Subu58_1`, `Subu59_1`, `Subu59_2`, `Subu59_3`, `Subu91`, `Subu93`, `Subu96`, `Subu97`, `Subu98`, `Subu99`

## `도서유통/book_07(북앤북NEW)/Chulpan.dpr`

- Variant unit count: **106**
- Only in baseline (-): **23** / only in variant (+): **0**

### Units only in baseline (up to 40)

`Seak04_1`, `Seok04`, `Seok08`, `Subu13_1`, `Subu17_1`, `Subu24_9`, `Subu32_1`, `Subu34_1`, `Subu34_2`, `Subu34_3`, `Subu34_4`, `Subu38_1`, `Subu39_5`, `Subu45_1`, `Subu59_1`, `Subu59_2`, `Subu59_3`, `Subu91`, `Subu93`, `Subu96`, `Subu97`, `Subu98`, `Subu99`

## `도서유통/book_04(협진도서)/도서유통-New/Chulpan.dpr`

- Variant unit count: **106**
- Only in baseline (-): **23** / only in variant (+): **0**

### Units only in baseline (up to 40)

`Seak04_1`, `Seok04`, `Seok08`, `Subu13_1`, `Subu17_1`, `Subu24_9`, `Subu32_1`, `Subu34_1`, `Subu34_2`, `Subu34_3`, `Subu34_4`, `Subu38_1`, `Subu39_5`, `Subu45_1`, `Subu59_1`, `Subu59_2`, `Subu59_3`, `Subu91`, `Subu93`, `Subu96`, `Subu97`, `Subu98`, `Subu99`

## `도서유통/book_12(플러스비)/도서유통-New/Chulpan.dpr`

- Variant unit count: **106**
- Only in baseline (-): **23** / only in variant (+): **0**

### Units only in baseline (up to 40)

`Seak04_1`, `Seok04`, `Seok08`, `Subu13_1`, `Subu17_1`, `Subu24_9`, `Subu32_1`, `Subu34_1`, `Subu34_2`, `Subu34_3`, `Subu34_4`, `Subu38_1`, `Subu39_5`, `Subu45_1`, `Subu59_1`, `Subu59_2`, `Subu59_3`, `Subu91`, `Subu93`, `Subu96`, `Subu97`, `Subu98`, `Subu99`

## `Interbase/Chulpan.dpr`

- Variant unit count: **94**
- Only in baseline (-): **35** / only in variant (+): **0**

### Units only in baseline (up to 40)

`Seak04_1`, `Seak08_1`, `Seok04`, `Seok08`, `Seok09`, `Subu13_1`, `Subu17_1`, `Subu22_1`, `Subu22_2`, `Subu23_1`, `Subu24_9`, `Subu32_1`, `Subu34_1`, `Subu34_2`, `Subu34_3`, `Subu34_4`, `Subu38_1`, `Subu39_1`, `Subu39_2`, `Subu39_3`, `Subu39_4`, `Subu39_5`, `Subu42_1`, `Subu45_1`, `Subu55_1`, `Subu58_1`, `Subu59_1`, `Subu59_2`, `Subu59_3`, `Subu91`, `Subu93`, `Subu96`, `Subu97`, `Subu98`, `Subu99`

## Notes

- Same unit *names* can still point to different `in '...'` paths; see [04-variant-core-matrix.md](04-variant-core-matrix.md).
- `Interbase/Chulpan.dpr` suggests DB stack fork (**plan type T4**).
