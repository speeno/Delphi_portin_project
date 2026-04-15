"""
Rewrite selected Seak80 sample HTML files as UTF-8 (LF).

Source uses only ASCII + ast.literal_eval(\\"\\\\u....\\") so this script stays encoding-safe.
Run from repo: python3 debug/emit_frontend_html_utf8.py
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "frontend"


def J(s: str) -> str:
    return ast.literal_eval('"' + s + '"')


def write(name: str, body: str) -> None:
    p = ROOT / name
    p.write_text(body, encoding="utf-8", newline="\n")
    p.read_bytes().decode("utf-8")


def main() -> None:
    masters_read = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{J(r'\uae30\ucd08\uad00\ub9ac \uc870\ud68c \u2014 phase2')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="phase2-masters-read">
    <header class="page-head">
      <h1 class="title" id="pageTitle">{J(r'\uae30\ucd08\uad00\ub9ac \uc870\ud68c')}</h1>
      <p class="subtitle" id="pageSubtitle"></p>
      <p class="sample-nav">
        <a href="masters-hub.html">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac \ud5c8\ube0c')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a> {J(r'\u00b7')}
        <a href="sobo12.html" title="Subu12.pas {J(r'\u00b7')} TSobo12 {J(r'\u00b7')} Seek_Uses F12">Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')})</a> {J(r'\u00b7')}
        <a href="sobo13.html" title="Subu13.pas {J(r'\u00b7')} TSobo13 {J(r'\u00b7')} Seek_Uses F17">Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')})</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uc870\ud68c')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'\ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\ube44\uc6b0\uba74 \uc804\uccb4 Hcode')}" autocomplete="off" aria-label="Hcode" />
        </label>
        <label class="server-label">
          <span class="server-label-text">limit</span>
          <input type="number" id="limitInput" class="search-input hcode-input" min="1" max="2000" value="500" aria-label="limit" />
        </label>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
    </section>
  </div>
  <script>
    (function () {{
      if (window.SEAK80_API_BASE !== undefined && window.SEAK80_API_BASE !== null) return;
      if (location.protocol === "file:")
        window.SEAK80_API_BASE = "http://127.0.0.1:8000";
      else if (location.port === "5500")
        window.SEAK80_API_BASE = "http://" + location.hostname + ":8000";
      else
        window.SEAK80_API_BASE = "";
    }})();
  </script>
  <script src="seak80-common.js"></script>
  <script src="seak80-column-labels.js"></script>
  <script src="masters-read.js"></script>
</body>
</html>"""

    sobo12 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>G2_Gbun {J(r'\uc870\ud68c')} {J(r'\u2014')} Sobo12 sample</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Sobo12-phase1">
    <header class="page-head">
      <h1 class="title">G2_Gbun ({J(r'\uc785\uace0\ucc98 \uad6c\ubd84')})</h1>
      <p class="subtitle">Subu12 | TSobo12 | Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')}) | {J(r'\u0031\ub2e8\uacc4 POC \uc77d\uae30 \uc804\uc6a9')}</p>
      <p class="sample-nav">
        <a href="masters-hub.html" title="{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a> {J(r'\u00b7')}
        <a href="seek20.html">Seek20</a> {J(r'\u00b7')}
        <a href="seek30.html">Seek30</a> {J(r'\u00b7')}
        <a href="sobo13.html" title="Subu13.pas {J(r'\u00b7')} TSobo13 {J(r'\u00b7')} Seek_Uses F17">Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')})</a> {J(r'\u00b7')}
        <a href="sobo67.html">Sobo67</a>
      </p>
    </header>
    <section class="card" aria-label="G2_Gbun {J(r'\uc870\ud68c')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'\ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\ube44\uc6b0\uba74 \uc804\uccb4 Hcode')}" autocomplete="off" aria-label="Hcode" />
        </label>
        <label class="server-label">
          <span class="server-label-text">limit</span>
          <input type="number" id="limitInput" class="search-input hcode-input" min="1" max="2000" value="500" aria-label="limit" />
        </label>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
    </section>
  </div>
  <script>
    (function () {{
      if (window.SEAK80_API_BASE !== undefined && window.SEAK80_API_BASE !== null) return;
      if (location.protocol === "file:")
        window.SEAK80_API_BASE = "http://127.0.0.1:8000";
      else if (location.port === "5500")
        window.SEAK80_API_BASE = "http://" + location.hostname + ":8000";
      else
        window.SEAK80_API_BASE = "";
    }})();
  </script>
  <script src="seak80-common.js"></script>
  <script src="seak80-column-labels.js"></script>
  <script src="sobo12.js"></script>
</body>
</html>"""

    sobo13 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>T1_Gbun {J(r'\uc870\ud68c')} {J(r'\u2014')} Sobo13 sample</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Sobo13-phase1">
    <header class="page-head">
      <h1 class="title">T1_Gbun ({J(r'\ub3c4\uc11c \uad6c\ubd84')})</h1>
      <p class="subtitle">Subu13 | TSobo13 | Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')}) | {J(r'\u0031\ub2e8\uacc4 POC \uc77d\uae30 \uc804\uc6a9')}</p>
      <p class="sample-nav">
        <a href="masters-hub.html" title="{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a> {J(r'\u00b7')}
        <a href="seek20.html">Seek20</a> {J(r'\u00b7')}
        <a href="seek30.html">Seek30</a> {J(r'\u00b7')}
        <a href="sobo12.html" title="Subu12.pas {J(r'\u00b7')} TSobo12 {J(r'\u00b7')} Seek_Uses F12">Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')})</a> {J(r'\u00b7')}
        <a href="sobo67.html">Sobo67</a>
      </p>
    </header>
    <section class="card" aria-label="T1_Gbun {J(r'\uc870\ud68c')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'\ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\ube44\uc6b0\uba74 \uc804\uccb4 Hcode')}" autocomplete="off" aria-label="Hcode" />
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Gcode</span>
          <input type="text" id="gcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\uc120\ud0dd')}" autocomplete="off" aria-label="Gcode" />
        </label>
        <label class="server-label">
          <span class="server-label-text">limit</span>
          <input type="number" id="limitInput" class="search-input hcode-input" min="1" max="2000" value="500" aria-label="limit" />
        </label>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
    </section>
  </div>
  <script>
    (function () {{
      if (window.SEAK80_API_BASE !== undefined && window.SEAK80_API_BASE !== null) return;
      if (location.protocol === "file:")
        window.SEAK80_API_BASE = "http://127.0.0.1:8000";
      else if (location.port === "5500")
        window.SEAK80_API_BASE = "http://" + location.hostname + ":8000";
      else
        window.SEAK80_API_BASE = "";
    }})();
  </script>
  <script src="seak80-common.js"></script>
  <script src="seak80-column-labels.js"></script>
  <script src="sobo13.js"></script>
</body>
</html>"""

    index = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{J(r'\ucd9c\ud310\uc0ac\uac80\uc0c9\ud604\ud669 \u2014 Seak80 sample')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seak80.svg 512x355">
    <header class="page-head">
      <h1 class="title">{J(r'\ucd9c\ud310\uc0ac\uac80\uc0c9\ud604\ud669')}</h1>
      <p class="subtitle">Seak08 | Seak80 | TSeak80</p>
      <p class="sample-nav">
        <a href="masters-hub.html" title="{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}</a> {J(r'\u00b7')}
        <a href="seek20.html">Seek20 {J(r'\uc785\uace0\ucc98')}</a> {J(r'\u00b7')}
        <a href="seek30.html">Seek30 {J(r'\uc800\uc790')}</a> {J(r'\u00b7')}
        <a href="sobo12.html" title="Subu12.pas {J(r'\u00b7')} TSobo12 {J(r'\u00b7')} Seek_Uses F12">Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')})</a> {J(r'\u00b7')}
        <a href="sobo13.html" title="Subu13.pas {J(r'\u00b7')} TSobo13 {J(r'\u00b7')} Seek_Uses F17">Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')})</a> {J(r'\u00b7')}
        <a href="sobo67.html">Sobo67 {J(r'\ub3c4\uc11c\ubcc4\ub144\ub9d0')}</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uac80\uc0c9 \uce74\ub4dc')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'DB \uc11c\ubc84 \ubaa9\ub85d \ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <div class="search-wrap">
          <input type="search" id="searchInput" class="search-input"
            placeholder="{J(r'\uac80\uc0c9 (\ucf54\ub4dc\u00b7\ucd9c\ud310\uc0ac\uba85\u00b7\ub300\ud45c\uc790 \ub4f1')}"
            autocomplete="off" aria-label="{J(r'\uac80\uc0c9\uc5b4')}" />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{J(r'\uc120\ud0dd')}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{J(r'\ucde8\uc18c')}</button>
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
  <script src="seak80-common.js"></script>
  <script src="app.js"></script>
</body>
</html>"""

    seek20 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{J(r'\uc785\uace0\ucc98\uac80\uc0c9\ud604\ud669 \u2014 Seek20 sample')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seek20.svg 512x355">
    <header class="page-head">
      <h1 class="title">{J(r'\uc785\uace0\ucc98\uac80\uc0c9\ud604\ud669')}</h1>
      <p class="subtitle">Seek02 | Seek20 | TSeek20</p>
      <p class="sample-nav">
        <a href="masters-hub.html" title="{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a> {J(r'\u00b7')}
        <a href="seek30.html">Seek30 {J(r'\uc800\uc790')}</a> {J(r'\u00b7')}
        <a href="sobo12.html" title="Subu12.pas {J(r'\u00b7')} TSobo12 {J(r'\u00b7')} Seek_Uses F12">Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')})</a> {J(r'\u00b7')}
        <a href="sobo13.html" title="Subu13.pas {J(r'\u00b7')} TSobo13 {J(r'\u00b7')} Seek_Uses F17">Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')})</a> {J(r'\u00b7')}
        <a href="sobo67.html">Sobo67 {J(r'\ub3c4\uc11c\ubcc4\ub144\ub9d0')}</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uc785\uace0\ucc98 \uac80\uc0c9')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'\ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\uc608: H0001 (\ube44\uc6b0\uba74 \uc804\uccb4 Hcode)')}" autocomplete="off" aria-label="Hcode" />
        </label>
        <div class="search-wrap">
          <input type="search" id="searchInput" class="search-input"
            placeholder="{J(r'\uc785\uace0\ucc98\uba85\u00b7\ucf54\ub4dc\u00b7\uc804\ud654 \ub4f1')}"
            autocomplete="off" aria-label="{J(r'\uac80\uc0c9\uc5b4')}" />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="options-row" role="group" aria-label="{J(r'\uc870\ud68c \uc635\uc158')}">
        <label class="chk-label"><input type="checkbox" id="chkLimit200" /> {J(r'\u0032\u0030\u0030\uac74 \uc81c\ud55c (Limit)')}</label>
        <label class="chk-label"><input type="checkbox" id="chkLower" /> {J(r'\uac80\uc0c9\uc5b4 \uc18c\ubb38\uc790 \ud5c8\uc6a9 (LOWER)')}</label>
        <label class="chk-label"><input type="checkbox" id="chkExcludeGrat9" /> Grat9 {J(r'\uc81c\uc678')}</label>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{J(r'\uc120\ud0dd')}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{J(r'\ucde8\uc18c')}</button>
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
  <script src="seak80-common.js"></script>
  <script src="seek20.js"></script>
</body>
</html>"""

    seek30 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{J(r'\uc800\uc790\uac80\uc0c9\ud604\ud669 \u2014 Seek30 sample')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seek30.svg 512x355">
    <header class="page-head">
      <h1 class="title">{J(r'\uc800\uc790\uac80\uc0c9\ud604\ud669')}</h1>
      <p class="subtitle">Seek03 | Seek30 | TSeek30</p>
      <p class="sample-nav">
        <a href="masters-hub.html" title="{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac (\uc870\ud68c POC)')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a> {J(r'\u00b7')}
        <a href="seek20.html">Seek20 {J(r'\uc785\uace0\ucc98')}</a> {J(r'\u00b7')}
        <a href="sobo12.html" title="Subu12.pas {J(r'\u00b7')} TSobo12 {J(r'\u00b7')} Seek_Uses F12">Sobo12 ({J(r'\uc785\uace0\ucc98\uad00\ub9ac')})</a> {J(r'\u00b7')}
        <a href="sobo13.html" title="Subu13.pas {J(r'\u00b7')} TSobo13 {J(r'\u00b7')} Seek_Uses F17">Sobo13 ({J(r'\uc9c0\uc5ed\ubd84\ub958(\uc2dc\ub0b4+\uc9c0\ubc29)')})</a> {J(r'\u00b7')}
        <a href="sobo67.html">Sobo67 {J(r'\ub3c4\uc11c\ubcc4\ub144\ub9d0')}</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uc800\uc790 \uac80\uc0c9')}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{J(r'DB \uc11c\ubc84')}</span>
          <select id="serverSelect" class="server-select" title="{J(r'DB \uc11c\ubc84 \uc120\ud0dd')}">
            <option value="">{J(r'\ubd88\ub7ec\uc624\ub294 \uc911')}</option>
          </select>
        </label>
        <label class="server-label hcode-label">
          <span class="server-label-text">Hcode</span>
          <input type="text" id="hcodeInput" class="search-input hcode-input"
            placeholder="{J(r'\uc608: Edit3 (\ube44\uc6b0\uba74 \uc804\uccb4 Hcode)')}" autocomplete="off" aria-label="Hcode" />
        </label>
        <div class="search-wrap">
          <input type="search" id="searchInput" class="search-input"
            placeholder="{J(r'\uc800\uc790\uba85\u00b7\ucf54\ub4dc\u00b7\uc804\ud654 \ub4f1')}"
            autocomplete="off" aria-label="{J(r'\uac80\uc0c9\uc5b4')}" />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{J(r'\uc870\ud68c')}</button>
      </div>
      <div class="options-row" role="group" aria-label="{J(r'\uc870\ud68c \uc635\uc158')}">
        <label class="chk-label"><input type="checkbox" id="chkLimit200" /> {J(r'\u0032\u0030\u0030\uac74 \uc81c\ud55c (Limit)')}</label>
        <label class="chk-label"><input type="checkbox" id="chkLower" /> {J(r'\uac80\uc0c9\uc5b4 \uc18c\ubb38\uc790 \ud5c8\uc6a9 (LOWER)')}</label>
      </div>
      <div class="grid-wrap" role="region" aria-label="{J(r'\uacb0\uacfc \uadf8\ub9ac\ub4dc')}">
        <table class="data-grid"><thead><tr id="gridHeadRow"></tr></thead><tbody id="gridBody"></tbody></table>
      </div>
      <p id="statusLine" class="status-line" role="status"></p>
      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{J(r'\uc120\ud0dd')}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{J(r'\ucde8\uc18c')}</button>
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
  <script src="seak80-common.js"></script>
  <script src="seek30.js"></script>
</body>
</html>"""

    stub10 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sobo10 ({J(r'\ub85c\uadf8\uc778')}) {J(r'\u2014')} {J(r'\uc2a4\ud15d')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page">
    <header class="page-head">
      <h1 class="title">Sobo10 ({J(r'\ub85c\uadf8\uc778')})</h1>
      <p class="subtitle">Subu10.pas {J(r'\u00b7')} TSobo10 {J(r'\u00b7')} Seek_Uses F18</p>
      <p class="sample-nav">
        <a href="masters-hub.html">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac \ud5c8\ube0c')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uc2a4\ud15d \uc548\ub0b4')}">
      <p class="status-line">
        Delphi {J(r'\uc804\uc6a9 \ub85c\uadf8\uc778\u00b7\ud658\uacbd\uc124\uc815 \ud654\uba74\uc785\ub2c8\ub2e4. \uc6f9 POC\uc5d0\uc11c\ub294 DB \uc5f0\uacb0\u00b7\uc778\uc99d\uc744 \ubcc4\ub3c4\ub85c \ub450\uace0,')}
        {J(r'\ubaa9\ub85d API\ub294 \uc81c\uacf5\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.')}
      </p>
    </section>
  </div>
</body>
</html>"""

    stub19 = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sobo19 {J(r'\u2014')} {J(r'\uc2a4\ud15d')}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page">
    <header class="page-head">
      <h1 class="title">Sobo19 (Sobo19)</h1>
      <p class="subtitle">Subu19.pas {J(r'\u00b7')} TSobo19 {J(r'\u00b7')} Seek_Uses F19 {J(r'\u00b7')} {J(r'\uba54\ub274')} E&amp;xit</p>
      <p class="sample-nav">
        <a href="masters-hub.html">{J(r'\u0032\ub2e8\uacc4 \uae30\ucd08\uad00\ub9ac \ud5c8\ube0c')}</a> {J(r'\u00b7')}
        <a href="index.html">Seak80</a>
      </p>
    </header>
    <section class="card" aria-label="{J(r'\uc2a4\ud15d \uc548\ub0b4')}">
      <p class="status-line">
        Delphi{J(r'\uc5d0\uc11c\ub294 \uc885\ub8cc \ud655\uc778 \ub4f1 \ubaa8\ub2ec\ub85c \uc4f0\uc774\ub294 \ud654\uba74\uc785\ub2c8\ub2e4. \uc6f9 POC\uc5d0\uc11c\ub294 \ubaa9\ub85d API \uc5c6\uc774')}
        {J(r'\ud5c8\ube0c \ub9c1\ud06c\ub9cc \uc720\uc9c0\ud569\ub2c8\ub2e4.')}
      </p>
    </section>
  </div>
</body>
</html>"""

    write("masters-read.html", masters_read)
    write("sobo12.html", sobo12)
    write("sobo13.html", sobo13)
    write("index.html", index)
    write("seek20.html", seek20)
    write("seek30.html", seek30)
    write("stub-sobo10.html", stub10)
    write("stub-sobo19.html", stub19)
    print("wrote 8 utf-8 html files under", ROOT)


if __name__ == "__main__":
    main()
