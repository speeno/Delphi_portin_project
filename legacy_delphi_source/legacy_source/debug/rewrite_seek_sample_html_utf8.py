#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write Seak80 sample HTML as UTF-8. Source is ASCII + \\u escapes only (avoids editor double-encoding)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "web" / "seak80-sample" / "frontend"

# All non-ASCII as \\u escapes (ASCII-only file body)
H = {
    "middot": "\u00b7",
    "title80": "\uCD9C\uD310\uC0AC\uAC80\uC0C9\uD604\uD669 \u2014 Seak80 sample",
    "h1_80": "\uCD9C\uD310\uC0AC\uAC80\uC0C9\uD604\uD669",
    "nav20": "Seek20 \uC785\uACE0\uCC98",
    "nav30": "Seek30 \uC800\uC790",
    "card_search": "\uAC80\uC0C9 \uCE74\uB4DC",
    "db_srv": "DB \uC11C\uBC84",
    "db_srv_title": "DB \uC11C\uBC84 \uC120\uD0DD",
    "loading_srv": "DB \uC11C\uBC84 \uBAA9\uB85D \uBD88\uB7EC\uC624\uB294 \uC911",
    "ph80": "\uAC80\uC0C9 (\uCF54\uB4DC\u00B7\uCD9C\uD310\uC0AC\uBA85\u00B7\uB300\uD45C\uC790 \uB4F1)",
    "search_word": "\uAC80\uC0C9\uC5B4",
    "btn_q": "\uC870\uD68C",
    "grid_aria": "\uACB0\uACFC \uADF8\uB9AC\uB4DC",
    "sel": "\uC120\uD0DD",
    "cancel": "\uCDE8\uC18C",
    "title20": "\uC785\uACE0\uCC98\uAC80\uC0C9\uD604\uD669 \u2014 Seek20 sample",
    "h1_20": "\uC785\uACE0\uCC98\uAC80\uC0C9\uD604\uD669",
    "card20": "\uC785\uACE0\uCC98 \uAC80\uC0C9",
    "loading": "\uBD88\uB7EC\uC624\uB294 \uC911",
    "hcode_ph": "\uC704\uB7EC\uBE0C Hnnnn (\uBE44\uC6B0\uBA74 \uC804\uCCB4 Hcode)",
    "ph20": "\uC785\uACE0\uCC98\uBA85\u00B7\uCF54\uB4DC\u00B7\uB300\uD45C \uB4F1",
    "opt_row": "\uC870\uD68C \uC635\uC158",
    "chk200": "200\uAC74\uB9CC (Limit)",
    "chk_lower": "\uB300\uC18C\uBB38\uC790 \uBB34\uC2DC (LOWER)",
    "chk_grat": "Grat9 \uC81C\uC678",
    "title30": "\uC800\uC790\uAC80\uC0C9\uD604\uD669 \u2014 Seek30 sample",
    "h1_30": "\uC800\uC790\uAC80\uC0C9\uD604\uD669",
    "card30": "\uC800\uC790 \uAC80\uC0C9",
    "hcode_ph30": "\uC6D0\uBCF8 Edit3 (\uBE44\uC6B0\uBA74 \uC804\uCCB4 Hcode)",
    "ph30": "\uC800\uC790\u00B7\uCF54\uB4DC\u00B7\uC9C1\uC7A5 \uB4F1",
    "nav67": "Sobo67 \uB3C4\uC11C\uBCC4\uB144\uB9D0",
}


def index_html() -> str:
    z = H
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{z["title80"]}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seak80.svg 512x355">
    <header class="page-head">
      <h1 class="title">{z["h1_80"]}</h1>
      <p class="subtitle">Seak08 | Seak80 | TSeak80</p>
      <p class="sample-nav">
        <a href="seek20.html">{z["nav20"]}</a> {z["middot"]}
        <a href="seek30.html">{z["nav30"]}</a> {z["middot"]}
        <a href="sobo67.html">{z["nav67"]}</a>
      </p>
    </header>

    <section class="card" aria-label="{z["card_search"]}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{z["db_srv"]}</span>
          <select id="serverSelect" class="server-select" title="{z["db_srv_title"]}">
            <option value="">{z["loading_srv"]}</option>
          </select>
        </label>
        <div class="search-wrap">
          <input
            type="search"
            id="searchInput"
            class="search-input"
            placeholder="{z["ph80"]}"
            autocomplete="off"
            aria-label="{z["search_word"]}"
          />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{z["btn_q"]}</button>
      </div>

      <div class="grid-wrap" role="region" aria-label="{z["grid_aria"]}">
        <table class="data-grid">
          <thead>
            <tr id="gridHeadRow"></tr>
          </thead>
          <tbody id="gridBody"></tbody>
        </table>
      </div>

      <p id="statusLine" class="status-line" role="status"></p>

      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{z["sel"]}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{z["cancel"]}</button>
      </footer>
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
  <script src="app.js"></script>
</body>
</html>
"""


def seek20_html() -> str:
    z = H
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{z["title20"]}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seek20.svg 512x355">
    <header class="page-head">
      <h1 class="title">{z["h1_20"]}</h1>
      <p class="subtitle">Seek02 | Seek20 | TSeek20</p>
      <p class="sample-nav">
        <a href="index.html">Seak80</a> {z["middot"]}
        <a href="seek30.html">{z["nav30"]}</a> {z["middot"]}
        <a href="sobo67.html">{z["nav67"]}</a>
      </p>
    </header>

    <section class="card" aria-label="{z["card20"]}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{z["db_srv"]}</span>
          <select id="serverSelect" class="server-select" title="{z["db_srv_title"]}">
            <option value="">{z["loading"]}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input
            type="text"
            id="hcodeInput"
            class="search-input hcode-input"
            placeholder="{z["hcode_ph"]}"
            autocomplete="off"
            aria-label="Hcode"
          />
        </label>
        <div class="search-wrap">
          <input
            type="search"
            id="searchInput"
            class="search-input"
            placeholder="{z["ph20"]}"
            autocomplete="off"
            aria-label="{z["search_word"]}"
          />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{z["btn_q"]}</button>
      </div>
      <div class="options-row" role="group" aria-label="{z["opt_row"]}">
        <label class="chk-label"><input type="checkbox" id="chkLimit200" /> {z["chk200"]}</label>
        <label class="chk-label"><input type="checkbox" id="chkLower" /> {z["chk_lower"]}</label>
        <label class="chk-label"><input type="checkbox" id="chkExcludeGrat9" /> {z["chk_grat"]}</label>
      </div>

      <div class="grid-wrap" role="region" aria-label="{z["grid_aria"]}">
        <table class="data-grid">
          <thead>
            <tr id="gridHeadRow"></tr>
          </thead>
          <tbody id="gridBody"></tbody>
        </table>
      </div>

      <p id="statusLine" class="status-line" role="status"></p>

      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{z["sel"]}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{z["cancel"]}</button>
      </footer>
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
  <script src="seek20.js"></script>
</body>
</html>
"""


def seek30_html() -> str:
    z = H
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{z["title30"]}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seek30.svg 512x355">
    <header class="page-head">
      <h1 class="title">{z["h1_30"]}</h1>
      <p class="subtitle">Seek03 | Seek30 | TSeek30</p>
      <p class="sample-nav">
        <a href="index.html">Seak80</a> {z["middot"]}
        <a href="seek20.html">{z["nav20"]}</a> {z["middot"]}
        <a href="sobo67.html">{z["nav67"]}</a>
      </p>
    </header>

    <section class="card" aria-label="{z["card30"]}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{z["db_srv"]}</span>
          <select id="serverSelect" class="server-select" title="{z["db_srv_title"]}">
            <option value="">{z["loading"]}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input
            type="text"
            id="hcodeInput"
            class="search-input hcode-input"
            placeholder="{z["hcode_ph30"]}"
            autocomplete="off"
            aria-label="Hcode"
          />
        </label>
        <div class="search-wrap">
          <input
            type="search"
            id="searchInput"
            class="search-input"
            placeholder="{z["ph30"]}"
            autocomplete="off"
            aria-label="{z["search_word"]}"
          />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{z["btn_q"]}</button>
      </div>
      <div class="options-row" role="group" aria-label="{z["opt_row"]}">
        <label class="chk-label"><input type="checkbox" id="chkLimit200" /> {z["chk200"]}</label>
        <label class="chk-label"><input type="checkbox" id="chkLower" /> {z["chk_lower"]}</label>
      </div>

      <div class="grid-wrap" role="region" aria-label="{z["grid_aria"]}">
        <table class="data-grid">
          <thead>
            <tr id="gridHeadRow"></tr>
          </thead>
          <tbody id="gridBody"></tbody>
        </table>
      </div>

      <p id="statusLine" class="status-line" role="status"></p>

      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{z["sel"]}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{z["cancel"]}</button>
      </footer>
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
  <script src="seek30.js"></script>
</body>
</html>
"""


def main() -> None:
    FE.mkdir(parents=True, exist_ok=True)
    (FE / "index.html").write_text(index_html(), encoding="utf-8", newline="\n")
    (FE / "seek20.html").write_text(seek20_html(), encoding="utf-8", newline="\n")
    (FE / "seek30.html").write_text(seek30_html(), encoding="utf-8", newline="\n")
    for name in ("index.html", "seek20.html", "seek30.html"):
        p = FE / name
        p.read_bytes().decode("utf-8")
    subprocess.run([sys.executable, str(ROOT / "debug" / "write_sobo67_sample_utf8.py")], check=True)
    print("Wrote valid UTF-8:", FE / "index.html", FE / "seek20.html", FE / "seek30.html", FE / "sobo67.html")


if __name__ == "__main__":
    main()
