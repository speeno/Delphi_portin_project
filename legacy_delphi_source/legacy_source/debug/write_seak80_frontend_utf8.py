#!/usr/bin/env python3
"""Legacy: writes index.html + app.js. Prefer rewrite_seek_sample_html_utf8.py for HTML only
(so app.js is not reverted). Hangul via \\u escapes in this file."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "web" / "seak80-sample" / "frontend"

# Hangul and punctuation as Unicode escapes only (ASCII source file)
T = {
    "title": "\uCD9C\uD310\uC0AC\uAC80\uC0C9\uD604\uD669 \u2014 Seak80 sample",
    "h1": "\uCD9C\uD310\uC0AC\uAC80\uC0C9\uD604\uD669",
    "card_aria": "\uAC80\uC0C9 \uCE74\uB4DC",
    "db_server": "DB \uC11C\uBC84",
    "db_profile": "DB \uC11C\uBC84 \uD504\uB85C\uD544",
    "loading": "DB \uC11C\uBC84 \uBAA9\uB85D \uBD88\uB7EC\uC624\uB294 \uC911",
    "ph": "\uAC80\uC0C9 (Gcode / Gname / Gposa \uC811\uB450)",
    "search_aria": "\uAC80\uC0C9\uC5B4",
    "search_btn": "\uC870\uD68C",
    "grid_aria": "\uACB0\uACFC \uADF8\uB9AC\uB4DC",
    "sel": "\uC120\uD0DD",
    "cancel": "\uCDE8\uC18C",
}

INDEX = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{T["title"]}</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="page" data-wireframe="Seak80.svg 512x355">
    <header class="page-head">
      <h1 class="title">{T["h1"]}</h1>
      <p class="subtitle">Seak08 | Seak80 | TSeak80</p>
    </header>

    <section class="card" aria-label="{T["card_aria"]}">
      <div class="toolbar">
        <label class="server-label">
          <span class="server-label-text">{T["db_server"]}</span>
          <select id="serverSelect" class="server-select" title="{T["db_profile"]}">
            <option value="">{T["loading"]}</option>
          </select>
        </label>
        <div class="search-wrap">
          <input
            type="search"
            id="searchInput"
            class="search-input"
            placeholder="{T["ph"]}"
            autocomplete="off"
            aria-label="{T["search_aria"]}"
          />
        </div>
        <button type="button" id="searchBtn" class="btn-search">{T["search_btn"]}</button>
      </div>

      <div class="grid-wrap" role="region" aria-label="{T["grid_aria"]}">
        <table class="data-grid">
          <thead>
            <tr>
              <th>Gubun</th>
              <th>Jubun</th>
              <th>Gcode</th>
              <th>Ocode</th>
              <th>Gname</th>
              <th>Gposa</th>
              <th>Gtel1</th>
              <th>Gtel2</th>
              <th>Gadd1</th>
              <th>Gadd2</th>
            </tr>
          </thead>
          <tbody id="gridBody"></tbody>
        </table>
      </div>

      <p id="statusLine" class="status-line" role="status"></p>

      <footer class="card-footer">
        <button type="button" id="btnSelect" class="btn-foot btn-select">{T["sel"]}</button>
        <button type="button" id="btnCancel" class="btn-foot btn-cancel">{T["cancel"]}</button>
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

APP_JS = r'''(function () {
  "use strict";

  const API_BASE = (window.SEAK80_API_BASE ?? "").replace(/\/$/, "");

  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const searchInput = $("searchInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");
  const btnSelect = $("btnSelect");
  const btnCancel = $("btnCancel");

  let selectedRow = null;

  function apiUrl(path) {
    return API_BASE + path;
  }

  function setServerOptions(message, pairs) {
    serverSelect.innerHTML = "";
    for (const [value, label] of pairs) {
      const opt = document.createElement("option");
      opt.value = value;
      opt.textContent = label;
      serverSelect.appendChild(opt);
    }
    statusLine.textContent = message;
  }

  async function loadServers() {
    statusLine.textContent = "\uC11C\uBC84 \uBAA9\uB85D \uB85C\uB4DC \uC911\u2026";
    let res;
    try {
      res = await fetch(apiUrl("/api/servers"));
    } catch (e) {
      setServerOptions(
        "API\uC5D0 \uC5F0\uACB0\uD560 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4. \uBC31\uC5D4\uB4DC\uB97C \uB1A8\uC6E0\uB294\uC9C0, \uD3EC\uD2B8\u00B7SEAK80_API_BASE\uB97C \uD655\uC778\uD558\uC138\uC694. (" +
          (e && e.message ? e.message : e) +
          ")",
        [["", "(\uC5F0\uACB0 \uC2E4\uD328: \uBC31\uC5D4\uB4DC \uC8FC\uC18C \uD655\uC778)"]]
      );
      return;
    }
    if (!res.ok) {
      setServerOptions(
        "\uC11C\uBC84 \uBAA9\uB85D HTTP " + res.status + " - backend \uC2E4\uD589 \uBC0F /api/servers \uACBD\uB85C\uB97C \uD655\uC778\uD558\uC138\uC694.",
        [["", "(HTTP " + res.status + ")"]]
      );
      return;
    }
    let list;
    try {
      list = await res.json();
    } catch (e) {
      setServerOptions("\uC11C\uBC84 \uBAA9\uB85D \uC751\uB2F5\uC774 JSON\uC774 \uC544\uB2D9\uB2C8\uB2E4.", [["", "(\uC751\uB2F5 \uC624\uB958)"]]);
      return;
    }
    if (!Array.isArray(list)) {
      setServerOptions("\uC11C\uBC84 \uBAA9\uB85D \uD615\uC2DD\uC774 \uC62C\uBC14\uB974\uC9C0 \uC54A\uC2B5\uB2C8\uB2E4.", [["", "(\uD615\uC2DD \uC624\uB958)"]]);
      return;
    }
    serverSelect.innerHTML = "";
    if (!list.length) {
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "(servers.yaml \uC5C6\uC74C; backend\uC5D0\uC11C \uBCF5\uC0AC \uD544\uC694)";
      serverSelect.appendChild(opt);
      statusLine.textContent =
        "\uB4F1\uB85D\uB41C DB \uD504\uB85C\uD544\uC774 \uC5C6\uC2B5\uB2C8\uB2E4. backend/servers.example.yaml -> servers.yaml \uBCF5\uC0AC \uD6C4 \uC124\uC815\uD558\uC138\uC694.";
      return;
    }
    for (const s of list) {
      const opt = document.createElement("option");
      opt.value = s.id;
      opt.textContent = s.label || s.id;
      serverSelect.appendChild(opt);
    }
    statusLine.textContent = "DB \uC11C\uBC84\uB97C \uC120\uD0DD\uD55C \uB4A4 \uC870\uD68C\uD558\uC138\uC694.";
  }

  function renderRows(rows) {
    gridBody.innerHTML = "";
    selectedRow = null;
    const cols = [
      "gubun",
      "jubun",
      "gcode",
      "ocode",
      "gname",
      "gposa",
      "gtel1",
      "gtel2",
      "gadd1",
      "gadd2",
    ];
    for (const r of rows) {
      const tr = document.createElement("tr");
      for (const c of cols) {
        const td = document.createElement("td");
        const v = r[c];
        td.textContent = v == null ? "" : String(v);
        tr.appendChild(td);
      }
      tr.addEventListener("click", () => {
        gridBody.querySelectorAll("tr.selected").forEach((x) => x.classList.remove("selected"));
        tr.classList.add("selected");
        selectedRow = r;
      });
      tr.addEventListener("dblclick", () => {
        selectedRow = r;
        doSelect();
      });
      gridBody.appendChild(tr);
    }
  }

  async function doSearch() {
    const serverId = serverSelect.value;
    if (!serverId) {
      statusLine.textContent = "DB \uC11C\uBC84\uB97C \uC120\uD0DD\uD558\uC138\uC694.";
      return;
    }
    const q = searchInput.value.trim();
    const params = new URLSearchParams({ serverId, q });
    statusLine.textContent = "\uC870\uD68C \uC911\u2026";
    let res;
    try {
      res = await fetch(apiUrl("/api/publishers?") + params.toString());
    } catch (e) {
      statusLine.textContent = "\uB124\uD2B8\uC6CC\uD06C \uC624\uB958: " + (e && e.message ? e.message : e);
      return;
    }
    if (!res.ok) {
      let detail = "";
      try {
        const j = await res.json();
        detail = j.detail ? (typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail)) : "";
      } catch (_) {
        /* ignore */
      }
      statusLine.textContent = "\uC870\uD68C \uC2E4\uD328 HTTP " + res.status + (detail ? ": " + detail : "");
      gridBody.innerHTML = "";
      return;
    }
    const data = await res.json();
    renderRows(data.rows || []);
    statusLine.textContent =
      (data.count != null ? data.count + "\uAC74" : "0\uAC74") +
      (q ? ' \u00B7 \uAC80\uC0C9\uC5B4 "' + q + '"' : " \u00B7 \uC804\uCCB4(\uC0C1\uD55C \uB0B4)");
  }

  function doSelect() {
    if (!selectedRow) {
      statusLine.textContent = "\uD589\uC744 \uC120\uD0DD\uD558\uC138\uC694 (\uD074\uB9AD \uB610\uB294 \uB354\uBE14\uD074\uB9AD).";
      return;
    }
    const code = selectedRow.gcode != null ? String(selectedRow.gcode) : "";
    window.alert("\uC120\uD0DD: Gcode=" + code + " (\uC0D8\uD50C: \uC2E4\uC81C \uC5F0\uB3D9 \uC2DC \uBD80\uBAA8 \uD654\uBA74\uC73C\uB85C \uC804\uB2EC)");
  }

  function doCancel() {
    gridBody.querySelectorAll("tr.selected").forEach((x) => x.classList.remove("selected"));
    selectedRow = null;
    statusLine.textContent = "\uC120\uD0DD \uD574\uC81C\uB428.";
  }

  searchBtn.addEventListener("click", () => doSearch());
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });
  btnSelect.addEventListener("click", () => doSelect());
  btnCancel.addEventListener("click", () => doCancel());

  loadServers();
})();
'''


def main() -> None:
    FE.mkdir(parents=True, exist_ok=True)
    (FE / "index.html").write_text(INDEX, encoding="utf-8", newline="\n")
    (FE / "app.js").write_text(APP_JS, encoding="utf-8", newline="\n")
    print("Wrote UTF-8:", FE / "index.html", FE / "app.js")


if __name__ == "__main__":
    main()
