(function () {
  "use strict";

  const SC = window.Seak80Common;

  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const searchInput = $("searchInput");
  const searchBtn = $("searchBtn");
  const gridBody = $("gridBody");
  const statusLine = $("statusLine");
  const btnSelect = $("btnSelect");
  const btnCancel = $("btnCancel");

  /** Seak08.dfm (chul_09) DBGrid101 Title.Caption + same SELECT column order as Seak08.pas */
  const GRID_COLUMNS = [
    { key: "gubun", label: "\uad6c\ubd84" },
    { key: "jubun", label: "\uc9c0\uc5ed" },
    { key: "gcode", label: "\ucf54\ub4dc" },
    { key: "ocode", label: "\uad6c\ucf54\ub4dc" },
    { key: "gname", label: "\ucd9c\ud310\uc0ac\uba85" },
    { key: "gposa", label: "\ub300\ud45c\uc790" },
    { key: "gtel1", label: "\uc804\ud654(\uc55e)" },
    { key: "gtel2", label: "\uc804\ud654\ubc88\ud638" },
    { key: "gadd1", label: "\uc8fc\uc18c" },
    { key: "gadd2", label: "\uc0c1\uc138\uc8fc\uc18c" },
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
      loading: "\uC11C\uBC84 \uBAA9\uB85D \uB85C\uB4DC \uC911\u2026",
      fetchError: function (e) {
        return (
          "API\uC5D0 \uC5F0\uACB0\uD560 \uC218 \uC5C6\uC2B5\uB2C8\uB2E4. \uBC31\uC5D4\uB4DC\uB97C \uB1A8\uC6E0\uB294\uC9C0, \uD3EC\uD2B8\u00B7SEAK80_API_BASE\uB97C \uD655\uC778\uD558\uC138\uC694. (" +
          (e && e.message ? e.message : e) +
          ")"
        );
      },
      httpError: function (status) {
        return (
          "\uC11C\uBC84 \uBAA9\uB85D HTTP " +
          status +
          " - backend \uC2E4\uD589 \uBC0F /api/servers \uACBD\uB85C\uB97C \uD655\uC778\uD558\uC138\uC694."
        );
      },
      badJson: "\uC11C\uBC84 \uBAA9\uB85D \uC751\uB2F5\uC774 JSON\uC774 \uC544\uB2D9\uB2C8\uB2E4.",
      badShape: "\uC11C\uBC84 \uBAA9\uB85D \uD615\uC2DD\uC774 \uC62C\uBC14\uB974\uC9C0 \uC54A\uC2B5\uB2C8\uB2E4.",
      emptyList: "(servers.yaml \uC5C6\uC74C; backend\uC5D0\uC11C \uBCF5\uC0AC \uD544\uC694)",
      emptyListStatus:
        "\uB4F1\uB85D\uB41C DB \uD504\uB85C\uD544\uC774 \uC5C6\uC2B5\uB2C8\uB2E4. backend/servers.example.yaml -> servers.yaml \uBCF5\uC0AC \uD6C4 \uC124\uC815\uD558\uC138\uC694.",
      success: "DB \uC11C\uBC84\uB97C \uC120\uD0DD\uD55C \uB4A4 \uC870\uD68C\uD558\uC138\uC694.",
    });
  }

  function renderRows(rows) {
    gridBody.innerHTML = "";
    selectedRow = null;
    const cols = GRID_COLUMNS.map(function (c) {
      return c.key;
    });
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
      res = await fetch(SC.apiUrl("/api/publishers?") + params.toString());
    } catch (e) {
      statusLine.textContent = "\uB124\uD2B8\uC6CC\uD06C \uC624\uB958: " + (e && e.message ? e.message : e);
      return;
    }
    if (!res.ok) {
      let detail = "";
      try {
        const j = await res.json();
        const d = j.detail;
        if (typeof d === "string") {
          detail = d;
        } else if (d && typeof d === "object" && d.message != null) {
          detail = (d.stage ? "[" + d.stage + "] " : "") + String(d.message);
        } else if (d != null) {
          detail = JSON.stringify(d);
        }
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
      (q ? ' \u00B7 \uAC80\uC0C9\uC5B4 "' + q + '"' : " \u00B7 \uC804\uCCB4");
  }

  function doSelect() {
    if (!selectedRow) {
      statusLine.textContent = "\uD589\uC744 \uC120\uD0DD\uD558\uC138\uC694 (\uD074\uB9AD \uB610\uB294 \uB354\uBE14\uD074\uB9AD).";
      return;
    }
    const code = selectedRow.gcode != null ? String(selectedRow.gcode) : "";
    window.alert(
      "\uC120\uD0DD: \ucf54\ub4dc=" +
        code +
        " (\uC0D8\uD50C: \uC2E4\uC81C \uC5F0\uB3D9 \uC2DC \uBD80\uBAA8 \uD654\uBA74\uC73C\uB85C \uC804\uB2EC)"
    );
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

  initGridHeader();
  loadServers();
})();
