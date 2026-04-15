# Delphi DFM vs Seak80 HTML POC — layout audit (implemented screens only)

UTF-8. Scope: `web/seak80-sample/frontend/*.html` (10 files).  
Purpose: record what matches Delphi geometry vs generic/wireframe-based layout, and point to `.dfm` paths.

Legend: **geometry** = Left/Top/Width/Height-style layout; **behaviour** = API/SQL/columns.

| HTML POC | Delphi unit (typical) | DFM path (example under repo) | Delphi geometry (summary) | HTML layout | Geometry match | Notes |
|----------|----------------------|--------------------------------|----------------------------|--------------|----------------|-------|
| `index.html` | Seak08 | `도서유통/.../Seak08.dfm` (variant) | MDI child, panels, grid pixels | `styles.css` card ~512px, single grid | Low | `styles.css` header cites **wireframe `Seak80.svg`** sizes |
| `seek20.html` | Seek02 | `도서유통/.../Seek02.dfm` | Form client + DBGrid | Same card pattern | Low | JS comments: **columns/SQL**, not layout |
| `seek30.html` | Seek03 | `도서유통/.../Seek03.dfm` | Same | Same | Low | Same |
| `masters-hub.html` | (none) | — | N/A | Link list + card | N/A | No single Delphi form |
| `masters-read.html` | Subu11 etc. | `Subu11.dfm` etc. | Multi-panel possible | Single toolbar + one table | Low | POC: primary table only |
| `sobo12.html` | Subu12 | `도서유통/한국도서유통/출판/MySQL/도서유통/chul_09(위러브)/Subu12.dfm` | e.g. `ClientWidth=901`, `Panel001` 265×405, left `CornerButton*` | Card `max-width`, no left rail | Low | One grid only |
| `sobo13.html` | Subu13 | `도서유통/한국도서유통/출판/MySQL/Subu13.dfm` | Left/right panels | Same | Low | Partial fields in HTML |
| `sobo67.html` | Subu67 | `Subu67.dfm` (several variants) | e.g. `Panel002` 873×206 + `DBGrid101`; `Panel003` + `DBGrid201`; `ClientWidth=901` | `sobo67-dual-grids` flex, toolbar row | Medium | **Two grids + DBGrid labels** align conceptually; **pixel rail, EhGrid footer** not in HTML |
| `stub-sobo10.html` | Subu10 | `Subu10.dfm` | Login UI | Text stub | N/A | Web auth separate |
| `stub-sobo19.html` | Subu19 | `Subu19.dfm` | Modal/exit | Text stub | N/A | Same |

## Conclusions (implemented POC only)

1. **HTML is not generated from `.dfm` coordinates.** Shared `styles.css` card/toolbar/grid + page modifiers (`page--sobo67`).
2. **Delphi linkage** is mostly **behaviour** (`*.js`, `seak80-column-labels.js`, backend SQL), not pixel-perfect geometry.
3. To tighten layout similarity, use the dump tool below and map numbers into CSS manually (or build a generator later).

## Tools

- Wireframe/size hints: `web/seak80-sample/frontend/styles.css` top comment; `data-wireframe` on `<div class="page">` (traceability only).
- **DFM → JSON geometry:** `debug/dfm_layout_dump.py` (run from repo root `도서유통-New`).

### Example commands

```bash
cd 도서유통-New
python3 debug/dfm_layout_dump.py Subu67.dfm
python3 debug/dfm_layout_dump.py "도서유통/한국도서유통/출판/MySQL/도서유통/chul_09(위러브)/Subu12.dfm" --max-depth 6
```

Compare output `nodes[].geometry` with `max-width`, `.grid-wrap` heights, etc. in `styles.css`.
