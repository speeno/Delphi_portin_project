(function () {
  "use strict";

  const SC = window.Seak80Common;
  const API_PATH = "/api/seek20/search";
  const POST_BACK =
    typeof URLSearchParams !== "undefined" &&
    new URLSearchParams(location.search).get("postMessage") === "1";

  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const hcodeInput = $("hcodeInput");
  const searchInput = $("searchInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");
  const btnSelect = $("btnSelect");
  const btnCancel = $("btnCancel");
  const chkLimit200 = $("chkLimit200");
  const chkLower = $("chkLower");
  const chkExcludeGrat9 = $("chkExcludeGrat9");

  /** Seek02.dfm DBGrid101 (??????????) */
  const GRID_COLUMNS = [
    { key: "jubun", label: "\uc9c0\uc5ed" },
    { key: "gcode", label: "\ucf54\ub4dc" },
    { key: "sname", label: "\uc785\uace0\ucc98\uba85" },
    { key: "gposa", label: "\ub300\ud45c\uc790" },
    { key: "gtel1", label: "^" },
    { key: "gtel2", label: "\uc804\ud654\ubc88\ud638" },
  ];

  let selectedRow = null;

  function initGridHeader() {
    const tr = document.getElementById("gridHeadRow");
    if (!tr) return;
    tr.innerHTML = "";
    for (const col of GRID_COLUMNS) {
      const th = document.createElement("th");
      th.textContent = col.label;
      th.title = col.key;
      tr.appendChild(th);
    }
  }

  async function loadServers() {
    await SC.loadServersInto(serverSelect, statusLine, {
      success:
        "Hcode\u00b7\uac80\uc0c9\uc5b4\ub97c \uc785\ub825\ud558\uace0 \uc870\ud68c\ud558\uc138\uc694.",
    });
  }

  function renderRows(rows) {
    gridBody.innerHTML = "";
    selectedRow = null;
    const cols = GRID_COLUMNS.map((c) => c.key);
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
      statusLine.textContent = "DB \uc11c\ubc84\ub97c \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }
    const q = searchInput.value.trim();
    const params = new URLSearchParams({
      serverId,
      q,
      hcode: (hcodeInput && hcodeInput.value) ? hcodeInput.value.trim() : "",
    });
    if (chkLimit200 && chkLimit200.checked) params.set("limit200", "true");
    if (chkLower && chkLower.checked) params.set("lower", "true");
    if (chkExcludeGrat9 && chkExcludeGrat9.checked) params.set("excludeGrat9", "true");

    statusLine.textContent = "\uc870\ud68c \uc911\u2026";
    let res;
    try {
      res = await fetch(SC.apiUrl(API_PATH + "?") + params.toString());
    } catch (e) {
      statusLine.textContent = "\ub124\ud2b8\uc6cc\ud06c \uc624\ub958: " + (e && e.message ? e.message : e);
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
    renderRows(data.rows || []);
    const hcShown = (data.hcode || "").trim();
    statusLine.textContent =
      (data.count != null ? data.count + "\uac74" : "0\uac74") +
      (hcShown
        ? ' \u00b7 Hcode "' + hcShown + '"'
        : " \u00b7 Hcode \uc804\uccb4") +
      (q ? ' \u00b7 \uac80\uc0c9\uc5b4 "' + q + '"' : " \u00b7 \uc804\uccb4");
  }

  function doSelect() {
    if (!selectedRow) {
      statusLine.textContent = "\ud589\uc744 \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }
    const code = selectedRow.gcode != null ? String(selectedRow.gcode) : "";
    const nm = selectedRow.sname != null ? String(selectedRow.sname) : "";
    if (POST_BACK && window.opener && !window.opener.closed) {
      try {
        window.opener.postMessage(
          { type: "seek20_pick", gcode: code, sname: nm },
          window.location.origin
        );
      } catch (_) {}
      window.close();
      return;
    }
    window.alert("\uc120\ud0dd: \ucf54\ub4dc=" + code + " \uc785\uace0\ucc98\uba85=" + nm);
  }

  function doCancel() {
    gridBody.querySelectorAll("tr.selected").forEach((x) => x.classList.remove("selected"));
    selectedRow = null;
    statusLine.textContent = "\uc120\ud0dd \ud574\uc81c.";
  }

  searchBtn.addEventListener("click", () => doSearch());
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });
  if (hcodeInput) {
    hcodeInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") doSearch();
    });
  }
  btnSelect.addEventListener("click", () => doSelect());
  btnCancel.addEventListener("click", () => doCancel());

  initGridHeader();
  loadServers();
})();
