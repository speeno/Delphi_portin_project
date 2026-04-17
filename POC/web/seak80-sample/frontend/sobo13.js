(function () {
  "use strict";

  const SC = window.Seak80Common;
  const API_PATH = "/api/sobo13/t1-gbun";
  const GRID_TABLE = "T1_Gbun";

  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const hcodeInput = $("hcodeInput");
  const gcodeInput = $("gcodeInput");
  const limitInput = $("limitInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");

  let gridKeys = [];

  function headerLabelFor(key) {
    const CL = window.Seak80ColumnLabels;
    if (CL && typeof CL.columnLabel === "function")
      return CL.columnLabel(GRID_TABLE, key);
    return key;
  }

  function initGridHeader(keys) {
    const tr = document.getElementById("gridHeadRow");
    if (!tr) return;
    tr.innerHTML = "";
    gridKeys = keys.slice();
    for (const k of gridKeys) {
      const th = document.createElement("th");
      th.textContent = headerLabelFor(k);
      th.title = k;
      tr.appendChild(th);
    }
  }

  function renderRows(rows) {
    gridBody.innerHTML = "";
    if (!rows || !rows.length || !gridKeys.length) return;
    for (const r of rows) {
      const tr = document.createElement("tr");
      for (const c of gridKeys) {
        const td = document.createElement("td");
        const v = r[c];
        td.textContent = v == null ? "" : String(v);
        tr.appendChild(td);
      }
      gridBody.appendChild(tr);
    }
  }

  async function loadServers() {
    await SC.loadServersInto(serverSelect, statusLine, {
      success:
        "Hcode\u00b7Gcode(\uc120\ud0dd)\u00b7limit \ud6c4 \uc870\ud68c. Hcode\ub97c \ube44\uc6b0\uba74 \uc804\uccb4\uc785\ub2c8\ub2e4. (" +
        "GET " +
        API_PATH +
        ")",
    });
  }

  async function doSearch() {
    const serverId = serverSelect.value;
    if (!serverId) {
      statusLine.textContent = "DB \uc11c\ubc84\ub97c \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }
    const hc = (hcodeInput && hcodeInput.value) ? hcodeInput.value.trim() : "";
    const gc = (gcodeInput && gcodeInput.value) ? gcodeInput.value.trim() : "";
    let lim = 500;
    if (limitInput && limitInput.value !== "") {
      const n = parseInt(String(limitInput.value), 10);
      if (!isNaN(n) && n >= 1) lim = Math.min(2000, n);
    }
    const params = new URLSearchParams({
      serverId,
      limit: String(lim),
    });
    if (hc) params.set("hcode", hc);
    if (gc) params.set("gcode", gc);
    statusLine.textContent = "\uc870\ud68c \uc911\u2026";
    let res;
    try {
      res = await fetch(SC.apiUrl(API_PATH + "?") + params.toString());
    } catch (e) {
      statusLine.textContent =
        "\ub124\ud2b8\uc6cc\ud06c \uc624\ub958: " + (e && e.message ? e.message : e);
      return;
    }
    if (!res.ok) {
      let detail = "";
      try {
        const j = await res.json();
        const d = j.detail;
        if (typeof d === "string") detail = d;
        else if (d && typeof d === "object" && d.message != null)
          detail = (d.stage ? "[" + d.stage + "] " : "") + String(d.message);
      } catch (_) {}
      statusLine.textContent = "HTTP " + res.status + (detail ? ": " + detail : "");
      gridBody.innerHTML = "";
      return;
    }
    const data = await res.json();
    const rows = data.rows || [];
    if (rows.length) {
      gridKeys = Object.keys(rows[0]).sort();
      initGridHeader(gridKeys);
      renderRows(rows);
    } else {
      gridBody.innerHTML = "";
      if (!gridKeys.length) initGridHeader([]);
    }
    const hcShown = ((data.hcode != null ? data.hcode : hc) || "").trim();
    const hcodePart = hcShown
      ? " \u00b7 Hcode \"" + hcShown + "\""
      : " \u00b7 Hcode \uc804\uccb4";
    const gshown = (data.gcode || gc || "").trim();
    const gcodePart = gshown ? " \u00b7 Gcode \"" + gshown + "\"" : "";
    statusLine.textContent =
      (data.count != null ? data.count + "\uac74" : rows.length + "\uac74") +
      hcodePart +
      gcodePart +
      " \u00b7 T1_Gbun";
  }

  searchBtn.addEventListener("click", () => doSearch());
  if (hcodeInput) {
    hcodeInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doSearch();
    });
  }
  if (gcodeInput) {
    gcodeInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doSearch();
    });
  }

  initGridHeader([]);
  loadServers();
})();
