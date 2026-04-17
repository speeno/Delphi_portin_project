(function () {
  "use strict";

  const SC = window.Seak80Common;
  /** NDJSON stream can span many DB chunks; allow long wall time */
  const FETCH_TIMEOUT_MS =
    typeof window.SEAK80_FETCH_TIMEOUT_MS === "number" && window.SEAK80_FETCH_TIMEOUT_MS > 0
      ? window.SEAK80_FETCH_TIMEOUT_MS
      : 300000;
  const SOBO67_READ_TIMEOUT_SEC =
    typeof window.SEAK80_SOBO67_READ_TIMEOUT_SEC === "number" &&
    window.SEAK80_SOBO67_READ_TIMEOUT_SEC >= 10
      ? window.SEAK80_SOBO67_READ_TIMEOUT_SEC
      : 300;
  const SOBO67_DETAIL_CHUNK =
    typeof window.SEAK80_SOBO67_DETAIL_CHUNK === "number" && window.SEAK80_SOBO67_DETAIL_CHUNK >= 1
      ? Math.min(500, Math.floor(window.SEAK80_SOBO67_DETAIL_CHUNK))
      : 100;
  const $ = (id) => document.getElementById(id);

  const serverSelect = $("serverSelect");
  const dateFrom = $("dateFrom");
  const dateTo = $("dateTo");
  const hcodeInput = $("hcodeInput");
  const bookMode = $("bookMode");
  const chkScode = $("chkScode");
  const searchBtn = $("searchBtn");
  const btnPrint = $("btnPrint");
  const btnHcodeCheck = $("btnHcodeCheck");
  const bcodeFrom = $("bcodeFrom");
  const bcodeTo = $("bcodeTo");
  const t00Select = $("t00Select");
  const btnSeekBcodeFrom = $("btnSeekBcodeFrom");
  const btnSeekBcodeTo = $("btnSeekBcodeTo");
  const grid1Body = $("grid1Body");
  const grid2Body = $("grid2Body");
  const statusLine = $("statusLine");
  const footerTotalsLine = $("footerTotalsLine");
  const searchProgress = $("searchProgress");

  let selectedParentGcode = "";
  let seekBcodeTarget = null;

  /** Subu67.dfm DBGrid101 + Gpsum (Sg_Csum); gcode for row drill-down */
  const GRID1_COLS = [
    { key: "gdate", label: "\ub144\ub3c4" },
    { key: "gcode", label: "\ucf54\ub4dc" },
    { key: "gname", label: "\ub3c4 \uc11c \uba85" },
    { key: "giqut", label: "\uc785\uace0\uc218\ub7c9" },
    { key: "goqut", label: "\ucd9c\uace0\uc218\ub7c9" },
    { key: "gjqut", label: "\uc99d\uc815\uc218\ub7c9" },
    { key: "gbqut", label: "\ubc18\ud488\uc218\ub7c9" },
    { key: "gpqut", label: "\ud3d0\uae30\uc218\ub7c9" },
    { key: "gosum", label: "\ucd9c\uace0\uae08\uc561" },
    { key: "gbsum", label: "\ubc18\ud488\uae08\uc561" },
    { key: "gpsum", label: "Sg_Csum" },
  ];

  const GRID2_COLS = GRID1_COLS.map(function (c) {
    if (c.key === "gdate") return { key: "gdate", label: "\ub144\uc6d4" };
    return c;
  });

  function enrichHttpDetail(status, detail) {
    const d = (detail || "").trim();
    if (status === 404 && (!d || d === "Not Found")) {
      return (
        "Not Found - /api/sobo67/search \uac00 \uc11c\ubc84\uc5d0 \uc5c6\uc2b5\ub2c8\ub2e4. " +
        "\ucd5c\uc2e0 main.py \ub85c uvicorn\uc744 \uc7ac\uc2dc\uc791\ud588\ub294\uc9c0, \ub9ac\ubc84\uc2a4 \ud504\ub85d\uc2dc\uac00 /api \ub97c \ub3d9\uc77c \ubc31\uc5d4\ub514\ub85c \ub118\uae30\ub294\uc9c0 \ud655\uc778\ud558\uc138\uc694."
      );
    }
    return d || "HTTP " + status;
  }

  async function warnIfSobo67ApiMissing() {
    try {
      const res = await fetch(SC.apiUrl("/api/health"));
      if (!res.ok) return;
      const h = await res.json();
      if (h && h.capabilities && h.capabilities.sobo67Search === true) return;
      statusLine.textContent =
        "[\uacbd\uace0] \uc774 \ubc31\uc5d4\ub514\ub294 Sobo67 \uac80\uc0c9 API(capabilities.sobo67Search)\ub97c \uc54c\ub9ac\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4. " +
        "\uad6c\ubc84\uc804\uc774\uba74 \uc7ac\ubc30\ud3ec\u00b7\uc7ac\uc2dc\uc791 \ud6c4 /api/health JSON \uc5d0 capabilities\uac00 \uc788\ub294\uc9c0 \ud655\uc778\ud558\uc138\uc694.";
    } catch (_) {}
  }

  function initGridHeader(rowId, cols) {
    const tr = document.getElementById(rowId);
    if (!tr) return;
    tr.innerHTML = "";
    for (const col of cols) {
      const th = document.createElement("th");
      th.textContent = col.label;
      th.title = col.key;
      tr.appendChild(th);
    }
  }

  function setProgress(v) {
    if (searchProgress) searchProgress.value = Math.max(0, Math.min(100, v));
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
    await SC.loadServersInto(
      serverSelect,
      statusLine,
      {
        success:
          "\uae30\uac04\u00b7Hcode(\uad8c\uc7a5)\u00b7\uac80\uc0c9. \uc6d4\ubcc4 \uadf8\ub9ac\ub4dc\ub294 \ub144\ub3c4 \ud589\uc744 \ud074\ub9ad\ud558\uba74 \ub85d\ub4dc\ub429\ub2c8\ub2e4.",
      },
      function () {
        void warnIfSobo67ApiMissing();
      }
    );
  }

  function renderGrid(tbody, cols, rows) {
    tbody.innerHTML = "";
    const keys = cols.map(function (c) {
      return c.key;
    });
    for (const r of rows) {
      const tr = document.createElement("tr");
      for (const k of keys) {
        const td = document.createElement("td");
        const v = r[k];
        td.textContent = v == null ? "" : String(v);
        tr.appendChild(td);
      }
      tbody.appendChild(tr);
    }
  }

  function formatFooterTotals(ft) {
    if (!ft || typeof ft !== "object") return "";
    const parts = [];
    for (const k of Object.keys(ft)) {
      parts.push(k + "=" + (ft[k] != null ? String(ft[k]) : ""));
    }
    return parts.join("  ");
  }

  function defaultYm() {
    const d = new Date();
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    return y + "." + m;
  }

  function buildParamsBase() {
    const serverId = serverSelect.value;
    const df = (dateFrom && dateFrom.value.trim()) || defaultYm();
    const dt = (dateTo && dateTo.value.trim()) || defaultYm();
    if (dateFrom) dateFrom.value = df;
    if (dateTo) dateTo.value = dt;
    const p = new URLSearchParams({
      serverId,
      dateFrom: df,
      dateTo: dt,
      hcode: hcodeInput ? hcodeInput.value.trim() : "",
      bookMode: bookMode ? bookMode.value : "book",
      scodeFilter: chkScode && chkScode.checked ? "true" : "false",
      limit: "500",
      bcodeFrom: bcodeFrom ? bcodeFrom.value.trim() : "",
      bcodeTo: bcodeTo ? bcodeTo.value.trim() : "",
      t00: t00Select ? String(t00Select.value || "0") : "0",
      stream: "true",
      detailChunk: String(SOBO67_DETAIL_CHUNK),
      readTimeoutSec: String(SOBO67_READ_TIMEOUT_SEC),
    });
    return p;
  }

  async function fetchGrid(which, parentGcode) {
    const p = buildParamsBase();
    p.set("grid", which);
    if (parentGcode) p.set("parentGcode", parentGcode);
    const url = SC.apiUrl("/api/sobo67/search?") + p.toString();
    const res = await SC.fetchWithTimeout(url, FETCH_TIMEOUT_MS);
    if (!res.ok) {
      let detail = "";
      try {
        const j = await res.json();
        if (j.detail) detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail);
      } catch (_) {}
      detail = enrichHttpDetail(res.status, detail);
      throw new Error("HTTP " + res.status + ": " + detail);
    }
    const ct = (res.headers.get("content-type") || "").toLowerCase();
    if (ct.indexOf("ndjson") >= 0 || ct.indexOf("x-ndjson") >= 0) {
      return readSobo67NdjsonStream(res);
    }
    return res.json();
  }

  async function readSobo67NdjsonStream(res) {
    const body = res.body;
    if (!body || !body.getReader) {
      throw new Error("streaming response not supported");
    }
    const reader = body.getReader();
    const dec = new TextDecoder();
    let buf = "";
    let lastResult = null;
    let batchMax = 0;
    while (true) {
      const step = await reader.read();
      if (step.done) break;
      buf += dec.decode(step.value, { stream: true });
      let nl;
      while ((nl = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue;
        let ev;
        try {
          ev = JSON.parse(line);
        } catch (e) {
          throw new Error("NDJSON parse: " + (e && e.message ? e.message : e));
        }
        if (ev.type === "error") {
          const d = ev.detail;
          const msg =
            typeof d === "string"
              ? d
              : d && typeof d === "object" && d.message != null
                ? String(d.message)
                : JSON.stringify(d || "");
          throw new Error("API " + (ev.status || "") + ": " + msg);
        }
        if (ev.type === "progress" && statusLine && ev.message) {
          statusLine.textContent = ev.message;
          if (searchProgress && ev.batch != null) {
            const cap = ev.detailCap != null ? Number(ev.detailCap) : 0;
            const off = ev.detailOffset != null ? Number(ev.detailOffset) : 0;
            const lim = ev.detailLimit != null ? Number(ev.detailLimit) : 0;
            batchMax = Math.max(batchMax, Number(ev.batch) || 0);
            let pct = 15 + Math.min(75, batchMax * 8);
            if (cap > 0 && lim > 0) {
              pct = Math.min(92, 12 + Math.floor(((off + lim) / cap) * 80));
            }
            setProgress(pct);
          }
        }
        if (ev.type === "result") lastResult = ev;
      }
    }
    if (!lastResult) {
      throw new Error("NDJSON: no result event");
    }
    return {
      rows: lastResult.rows || [],
      count: lastResult.count != null ? lastResult.count : (lastResult.rows || []).length,
      footerTotals: lastResult.footerTotals || {},
    };
  }

  function clearGrid1Selection() {
    if (!grid1Body) return;
    grid1Body.querySelectorAll("tr.selected").forEach(function (x) {
      x.classList.remove("selected");
    });
  }

  async function loadGrid2ForParent(gcode) {
    if (!grid2Body) return;
    if (!gcode) {
      grid2Body.innerHTML = "";
      if (footerTotalsLine) footerTotalsLine.textContent = "";
      return;
    }
    setProgress(40);
    const d2 = await fetchGrid("2", gcode);
    setProgress(90);
    renderGrid(grid2Body, GRID2_COLS, d2.rows || []);
    if (footerTotalsLine) footerTotalsLine.textContent = formatFooterTotals(d2.footerTotals);
  }

  async function doSearch() {
    const serverId = serverSelect.value;
    if (!serverId) {
      statusLine.textContent = "DB \uc11c\ubc84\ub97c \uc120\ud0dd\ud558\uc138\uc694.";
      return;
    }

    selectedParentGcode = "";
    clearGrid1Selection();
    setProgress(0);
    statusLine.textContent = "\uc870\ud68c \uc911\u2026";
    if (footerTotalsLine) footerTotalsLine.textContent = "";

    try {
      setProgress(20);
      const d1 = await fetchGrid("1", "");
      setProgress(60);
      renderGrid(grid1Body, GRID1_COLS, d1.rows || []);
      if (footerTotalsLine) footerTotalsLine.textContent = formatFooterTotals(d1.footerTotals);
      grid2Body.innerHTML = "";
      statusLine.textContent =
        "\ub144\ub3c4 " +
        (d1.count != null ? d1.count : 0) +
        "\uac74. \uc6d4\ubcc4\ub294 \ub144\ub3c4 \ud589 \ud074\ub9ad.";

      if (grid1Body) {
        grid1Body.onclick = function (ev) {
          const tr = ev.target && ev.target.closest ? ev.target.closest("tr") : null;
          if (!tr || !grid1Body.contains(tr)) return;
          clearGrid1Selection();
          tr.classList.add("selected");
          const cells = tr.querySelectorAll("td");
          const gcode = cells[1] ? cells[1].textContent.trim() : "";
          /* cols: gdate, gcode, gname, ... */
          selectedParentGcode = gcode;
          void (async function () {
            try {
              await loadGrid2ForParent(gcode);
              statusLine.textContent =
                "\uc120\ud0dd Bcode=" +
                gcode +
                " \u00b7 \uc6d4\ubcc4 " +
                grid2Body.querySelectorAll("tr").length +
                "\uac74";
            } catch (e2) {
              statusLine.textContent = String(e2 && e2.message ? e2.message : e2);
            }
          })();
        };
      }
    } catch (e) {
      const name = e && e.name ? e.name : "";
      const aborted = name === "AbortError" || name === "TimeoutError";
      statusLine.textContent = aborted
        ? "\uc870\ud68c \uc2dc\uac04 \ucd08\uacfc(" +
          Math.round(FETCH_TIMEOUT_MS / 1000) +
          "s). \uae30\uac04\u00b7Hcode\u00b7\uc11c\ubc84 \ub85c\ub529\uc744 \uc904\uc774\uac70\ub098 \ubc31\uc5d4\ub4dc read_timeout\uc744 \ub298\ub824\ubcf4\uc138\uc694."
        : String(e && e.message ? e.message : e);
      grid1Body.innerHTML = "";
      grid2Body.innerHTML = "";
    } finally {
      setTimeout(function () {
        setProgress(0);
      }, 400);
    }
  }

  searchBtn.addEventListener("click", function () {
    void doSearch();
  });

  if (btnPrint) {
    btnPrint.addEventListener("click", function () {
      window.print();
    });
  }

  if (btnHcodeCheck && hcodeInput) {
    btnHcodeCheck.addEventListener("click", async function () {
      const serverId = serverSelect.value;
      const hc = hcodeInput.value.trim();
      if (!serverId || !hc) {
        statusLine.textContent = "\uc11c\ubc84\u00b7Hcode\ub97c \uc785\ub825\ud558\uc138\uc694.";
        return;
      }
      try {
        const res = await fetch(
          SC.apiUrl("/api/sobo67/hcode-check?") +
            new URLSearchParams({ serverId: serverId, hcode: hc }).toString()
        );
        const j = await res.json();
        statusLine.textContent = j.ok ? "Hcode OK (G4_Book)" : "Hcode \ubbf8\ud655\uc778";
      } catch (e) {
        statusLine.textContent = String(e && e.message ? e.message : e);
      }
    });
  }

  function openSeekBcode(target) {
    seekBcodeTarget = target;
    const u = "seek20.html?postMessage=1";
    window.open(u, "_blank", "noopener,noreferrer");
  }

  if (btnSeekBcodeFrom) btnSeekBcodeFrom.addEventListener("click", function () {
    openSeekBcode("from");
  });
  if (btnSeekBcodeTo) btnSeekBcodeTo.addEventListener("click", function () {
    openSeekBcode("to");
  });

  window.addEventListener("message", function (ev) {
    const d = ev.data;
    if (!d || d.type !== "seek20_pick") return;
    const code = d.gcode != null ? String(d.gcode) : "";
    if (seekBcodeTarget === "from" && bcodeFrom) bcodeFrom.value = code;
    if (seekBcodeTarget === "to" && bcodeTo) bcodeTo.value = code;
    seekBcodeTarget = null;
  });

  initGridHeader("grid1HeadRow", GRID1_COLS);
  initGridHeader("grid2HeadRow", GRID2_COLS);
  if (dateFrom && !dateFrom.value) dateFrom.value = defaultYm();
  if (dateTo && !dateTo.value) dateTo.value = defaultYm();
  loadServers();
})();
