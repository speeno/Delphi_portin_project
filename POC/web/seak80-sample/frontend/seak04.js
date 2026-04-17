(function () {
  "use strict";

  const SC = window.Seak80Common;
  const API_PATH = "/api/seak04/search";
  const POST_BACK =
    typeof URLSearchParams !== "undefined" &&
    new URLSearchParams(location.search).get("postMessage") === "1";

  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const searchInput = $("searchInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");
  const btnSelect = $("btnSelect");
  const btnCancel = $("btnCancel");

  /** Seak04.dfm DBGrid101 visible columns (POST/ADDR/DDDD/DONG). */
  const GRID_COLUMNS = [
    { key: "post", label: "\uc6b0\ud3b8\ubc88\ud638" },
    { key: "addr", label: "\uc8fc\uc18c" },
    { key: "dddd", label: "^" },
    { key: "dong", label: "\uc9c0\uc5ed" },
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
        "\uac80\uc0c9\uc5b4 4\uc790 \uc774\uc0c1\uc744 \uc785\ub825\ud558\uace0 \uc870\ud68c\ud558\uc138\uc694.",
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
    if (!q) {
      statusLine.textContent = "\uac80\uc0c9\uc5b4\ub97c \uc785\ub825\ud558\uc138\uc694.";
      renderRows([]);
      return;
    }
    if (q.length < 4) {
      statusLine.textContent =
        "\ud55c\uae002\uc790,\uc22b\uc7904\uc790 \uc774\uc0c1 \uc785\ub825\ud558\uc138\uc694.";
      renderRows([]);
      return;
    }
    const params = new URLSearchParams({ serverId, q });
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
    statusLine.textContent =
      (data.count != null ? data.count + "\uac74" : "0\uac74") +
      (q ? ' \u00b7 "' + q + '"' : "");
  }

  function doSelect() {
    if (!selectedRow) {
      statusLine.textContent = "\ud589\uc744 \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }
    const post = selectedRow.post != null ? String(selectedRow.post) : "";
    const addr = selectedRow.addr != null ? String(selectedRow.addr) : "";
    const dddd = selectedRow.dddd != null ? String(selectedRow.dddd) : "";
    const dong = selectedRow.dong != null ? String(selectedRow.dong) : "";
    const city = selectedRow.city != null ? String(selectedRow.city) : "";
    if (POST_BACK && window.opener && !window.opener.closed) {
      try {
        window.opener.postMessage(
          { type: "seak04_pick", post, addr, dddd, dong, city },
          window.location.origin
        );
      } catch (_) {}
      window.close();
      return;
    }
    window.alert(
      "\uc120\ud0dd: \uc6b0\ud3b8=" + post + " \uc8fc\uc18c=" + addr
    );
  }

  function doCancel() {
    if (POST_BACK && window.opener && !window.opener.closed) {
      try {
        window.opener.postMessage({ type: "seak04_cancel" }, window.location.origin);
      } catch (_) {}
      window.close();
      return;
    }
    gridBody.querySelectorAll("tr.selected").forEach((x) => x.classList.remove("selected"));
    selectedRow = null;
    statusLine.textContent = "\uc120\ud0dd \ud574\uc81c.";
  }

  searchBtn.addEventListener("click", () => doSearch());
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") doSearch();
  });
  btnSelect.addEventListener("click", () => doSelect());
  btnCancel.addEventListener("click", () => doCancel());

  initGridHeader();
  loadServers();
})();
