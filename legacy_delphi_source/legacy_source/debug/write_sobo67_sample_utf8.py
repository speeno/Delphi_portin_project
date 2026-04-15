#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write sobo67.html (UTF-8, ASCII + \\u in source). Run from repo root."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "web" / "seak80-sample" / "frontend"

Z = {
    "title": "\ub3c4\uc11c\ubcc4\ub144\ub9d0\uc9d1\uacc4 \u2014 Sobo67 sample",
    "h1": "\ub3c4\uc11c\ubcc4\ub144\ub9d0\uc9d1\uacc4",
    "sub": "Subu67 | Sobo67 | TSobo67",
    "nav80": "Seak80",
    "nav20": "Seek20",
    "nav30": "Seek30",
    "md": "\u00b7",
    "db": "DB \uc11c\ubc84",
    "dbt": "DB \uc11c\ubc84 \uc120\ud0dd",
    "ld": "\ubd88\ub7ec\uc624\ub294 \uc911",
    "lbl_from": "\uae30\uac04 \uc2dc\uc791 (yyyy.mm)",
    "lbl_to": "\uae30\uac04 \ub05d (yyyy.mm)",
    "lbl_h": "Hcode",
    "ph_h": "\ube44\uc6b0\uba74 \uc804\uccb4",
    "lbl_mode": "\ub3c4\uc11c\uad6c\ubd84",
    "opt_book": "\ub3c4\uc11c\uba85/\ucc3d\uace0",
    "opt_hq": "\ubcf8\uc0ac",
    "opt_wh": "\ucc3d\uace0",
    "chk_sc": "CheckBox2 Scode \ud544\ud130",
    "btn_search": "\uac80\uc0c9",
    "btn_print": "\uc778\uc1c4 (\uc608\uc815)",
    "pan1": "\ub144\ub3c4 \uadf8\ub9ac\ub4dc (DBGrid101)",
    "pan2": "\ub144\uc6d4 \uadf8\ub9ac\ub4dc (DBGrid201)",
    "prog_l": "\uac80\uc0c9 \uc9c4\ud589",
    "st": "\uc0c1\ud0dc",
}


def sobo67_html() -> str:
    z = Z
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{z["title"]}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page page--sobo67" data-wireframe="Sobo67.svg 921x585">
    <header class="page-head">
      <h1 class="title">{z["h1"]}</h1>
      <p class="subtitle">{z["sub"]}</p>
      <p class="sample-nav">
        <a href="index.html">{z["nav80"]}</a> {z["md"]}
        <a href="seek20.html">{z["nav20"]}</a> {z["md"]}
        <a href="seek30.html">{z["nav30"]}</a>
      </p>
    </header>

    <section class="card card--sobo67" aria-label="Sobo67">
      <div class="toolbar toolbar--sobo67">
        <label class="server-label">
          <span class="server-label-text">{z["db"]}</span>
          <select id="serverSelect" class="server-select" title="{z["dbt"]}">
            <option value="">{z["ld"]}</option>
          </select>
        </label>
        <label class="server-label"><span class="server-label-text">{z["lbl_from"]}</span>
          <input type="text" id="dateFrom" class="search-input sobo67-date" maxlength="7" autocomplete="off" />
        </label>
        <label class="server-label"><span class="server-label-text">{z["lbl_to"]}</span>
          <input type="text" id="dateTo" class="search-input sobo67-date" maxlength="7" autocomplete="off" />
        </label>
        <label class="server-label hcode-label"><span class="server-label-text">{z["lbl_h"]}</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input" placeholder="{z["ph_h"]}" autocomplete="off" />
        </label>
        <label class="server-label"><span class="server-label-text">{z["lbl_mode"]}</span>
          <select id="bookMode" class="server-select" title="{z["lbl_mode"]}">
            <option value="book">{z["opt_book"]}</option>
            <option value="hq">{z["opt_hq"]}</option>
            <option value="warehouse">{z["opt_wh"]}</option>
          </select>
        </label>
        <label class="chk-label"><input type="checkbox" id="chkScode" /> {z["chk_sc"]}</label>
        <button type="button" id="searchBtn" class="btn-search">{z["btn_search"]}</button>
        <button type="button" id="btnPrintStub" class="btn-search btn-stub">{z["btn_print"]}</button>
      </div>

      <div class="sobo67-dual-grids">
        <div class="sobo67-grid-block" role="region" aria-label="{z["pan1"]}">
          <p class="sobo67-grid-label">{z["pan1"]}</p>
          <div class="grid-wrap grid-wrap--sobo67">
            <table class="data-grid">
              <thead><tr id="grid1HeadRow"></tr></thead>
              <tbody id="grid1Body"></tbody>
            </table>
          </div>
        </div>
        <div class="sobo67-grid-block" role="region" aria-label="{z["pan2"]}">
          <p class="sobo67-grid-label">{z["pan2"]}</p>
          <div class="grid-wrap grid-wrap--sobo67">
            <table class="data-grid">
              <thead><tr id="grid2HeadRow"></tr></thead>
              <tbody id="grid2Body"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="sobo67-progress-row">
        <span class="sobo67-progress-label">{z["prog_l"]}</span>
        <progress id="searchProgress" max="100" value="0"></progress>
      </div>
      <p id="statusLine" class="status-line" role="status">{z["st"]}</p>
    </section>
  </div>
  <script>
    (function () {{
      if (window.SEAK80_API_BASE !== undefined && window.SEAK80_API_BASE !== null) return;
      if (location.protocol === "file:")
        window.SEAK80_API_BASE = "http://127.0.0.1:8000";
      else
        window.SEAK80_API_BASE = "";
    }})();
  </script>
  <script src="sobo67.js"></script>
</body>
</html>
"""


def main() -> None:
    FE.mkdir(parents=True, exist_ok=True)
    p = FE / "sobo67.html"
    p.write_text(sobo67_html(), encoding="utf-8", newline="\n")
    p.read_bytes().decode("utf-8")
    print("Wrote", p)


if __name__ == "__main__":
    main()
