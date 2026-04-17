(function () {
  "use strict";

  const SC = window.Seak80Common;

  /** form_id -> [grid label unicode escapes, API table hint for status] */
  const PHASE2_META = {
    sobo11: {
      label: "\uac70\ub798\ucc98\uad00\ub9ac-\ud1b5\ud569",
      unitTitle: "Subu11.pas \u00b7 TSobo11 \u00b7 Seek_Uses F13",
    },
    sobo15: {
      label: "\uac70\ub798\ucc98\uad00\ub9ac-\uac1c\ubcc4",
      unitTitle: "Subu15.pas \u00b7 TSobo15 \u00b7 Seek_Uses F13",
    },
    sobo14: {
      label: "\ub3c4\uc11c\uad00\ub9ac",
      unitTitle: "Subu14.pas \u00b7 TSobo14 \u00b7 Seek_Uses F14",
    },
    sobo16: {
      label: "\ud2b9\ubcc4\uad00\ub9ac",
      unitTitle: "Subu16.pas \u00b7 TSobo16 \u00b7 Seek_Uses F16",
    },
    sobo17: {
      label: "\ucd9c\ud310\uc0ac\uad00\ub9ac",
      unitTitle: "Subu17.pas \u00b7 TSobo17 \u00b7 Seek_Uses F11",
    },
    sobo17_1: {
      label: "\ucd9c\ud310\uc0ac\uad00\ub9ac-\ud0dd\ubc30",
      unitTitle: "Subu17_1.pas \u00b7 TSobo17_1 \u00b7 Seek_Uses F11",
    },
    sobo18: {
      label: "\uc885\ub2f9\uad00\ub9ac(\ub3c4\uc11c)",
      unitTitle: "Subu18.pas \u00b7 TSobo18 \u00b7 Seek_Uses F15",
    },
    sobo48: {
      label: "\ucd9c\ud310\uc0ac\uad00\ub9ac(\uc124\uc815)",
      unitTitle: "Subu48.pas \u00b7 TSobo48 \u00b7 Seek_Uses F11",
    },
    sobo13_1: {
      label: "\ucd9c\uace0\uc99d\uc815\ub82c",
      unitTitle: "Subu13_1.pas \u00b7 TSobo13_1 \u00b7 Seek_Uses F17",
    },
  };

  const $ = (id) => document.getElementById(id);

  const params = new URLSearchParams(location.search);
  const formId = (params.get("id") || "").trim().toLowerCase();
  const meta = PHASE2_META[formId];
  const API_PATH =
    formId && meta
      ? "/api/phase2/" + encodeURIComponent(formId) + "/list"
      : "";

  const serverSelect = $("serverSelect");
  const hcodeInput = $("hcodeInput");
  const limitInput = $("limitInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");
  const pageTitle = $("pageTitle");
  const pageSubtitle = $("pageSubtitle");

  let gridKeys = [];
  let gridTableName = "";

  function headerLabelFor(table, key) {
    const CL = window.Seak80ColumnLabels;
    if (CL && typeof CL.columnLabel === "function")
      return CL.columnLabel(table, key);
    return key;
  }

  function initGridHeader(keys) {
    const tr = document.getElementById("gridHeadRow");
    if (!tr) return;
    tr.innerHTML = "";
    gridKeys = keys.slice();
    for (const k of gridKeys) {
      const th = document.createElement("th");
      th.textContent = headerLabelFor(gridTableName, k);
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

  function soboLabelFromFormId(fid) {
    if (!fid || fid.indexOf("sobo") !== 0) return fid || "";
    return "Sobo" + fid.slice(4);
  }

  function applyPageMeta() {
    if (!meta || !formId) {
      document.title =
        "\uc798\ubabb\ub41c id \u2014 \uae30\ucd08\uad00\ub9ac \uc870\ud68c";
      if (pageTitle)
        pageTitle.textContent =
          "\uc798\ubabb\ub41c \uac1c\uc694 (id)";
      if (pageSubtitle)
        pageSubtitle.textContent =
          "masters-hub.html\uc5d0\uc11c \ub9c1\ud06c\ub97c \uc0ac\uc6a9\ud558\uc138\uc694. id=sobo11 \ub4f1";
      if (statusLine)
        statusLine.textContent =
          "id \ud30c\ub77c\ubbf8\ud130\uac00 \uc5c6\uac70\ub098 \uc9c0\uc6d0\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.";
      return;
    }
    const label = soboLabelFromFormId(formId);
    document.title =
      label + " (" + meta.label + ") \u2014 \uae30\ucd08\uad00\ub9ac \uc870\ud68c";
    if (pageTitle) pageTitle.textContent = label + " (" + meta.label + ")";
    if (pageSubtitle) pageSubtitle.textContent = meta.unitTitle;
  }

  applyPageMeta();

  async function loadServers() {
    if (!API_PATH) return;
    await SC.loadServersInto(serverSelect, statusLine, {
      success:
        "Hcode\u00b7limit\uc744 \uc124\uc815\ud55c \ub4a4 \uc870\ud68c\ud558\uc138\uc694. (" +
        "GET " +
        API_PATH +
        ")",
    });
  }

  async function doSearch() {
    if (!API_PATH) return;
    const serverId = serverSelect.value;
    if (!serverId) {
      statusLine.textContent =
        "DB \uc11c\ubc84\ub97c \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }
    const hc = hcodeInput && hcodeInput.value ? hcodeInput.value.trim() : "";
    let lim = 500;
    if (limitInput && limitInput.value !== "") {
      const n = parseInt(String(limitInput.value), 10);
      if (!isNaN(n) && n >= 1) lim = Math.min(2000, n);
    }
    const q = new URLSearchParams({ serverId: serverId, limit: String(lim) });
    if (hc) q.set("hcode", hc);
    statusLine.textContent = "\uc870\ud68c \uc911\u2026";
    let res;
    try {
      res = await fetch(SC.apiUrl(API_PATH + "?") + q.toString());
    } catch (e) {
      statusLine.textContent =
        "\ub124\ud2b8\uc6cc\ud06c \uc624\ub958: " +
        (e && e.message ? e.message : e);
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
      statusLine.textContent =
        "HTTP " + res.status + (detail ? ": " + detail : "");
      gridBody.innerHTML = "";
      return;
    }
    const data = await res.json();
    const rows = data.rows || [];
    gridTableName = (data.table != null ? String(data.table) : "").trim();
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
    const tbl = data.table != null ? String(data.table) : "";
    statusLine.textContent =
      (data.count != null ? data.count + "\uac74" : rows.length + "\uac74") +
      hcodePart +
      (tbl ? " \u00b7 " + tbl : "");
  }

  if (API_PATH && searchBtn) {
    searchBtn.addEventListener("click", () => doSearch());
    if (hcodeInput) {
      hcodeInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") doSearch();
      });
    }
    loadServers().then(() => doSearch());
  }
})();
