/**
 * Seak80 sample POC: shared apiUrl, server list load, fetch with timeout.
 * Load after SEAK80_API_BASE bootstrap, before page scripts.
 */
(function (global) {
  "use strict";

  /**
   * When SEAK80_API_BASE is empty, resolve /api/... against the current HTML directory
   * so subpath deployments work (e.g. https://host/app/masters-read.html -> .../app/api/...).
   * Root pages (https://host/m.html) still resolve to https://host/api/...
   */
  function pageDirHref() {
    const path = location.pathname;
    const last = path.lastIndexOf("/");
    const dir = last <= 0 ? "/" : path.slice(0, last + 1);
    return location.origin + dir;
  }

  function apiBase() {
    return String(global.SEAK80_API_BASE ?? "").replace(/\/$/, "");
  }

  function apiUrl(path) {
    const p = String(path || "");
    const q = p.startsWith("/") ? p : "/" + p;
    const b = apiBase();
    if (b) {
      return b + q;
    }
    const rel = q.replace(/^\//, "");
    return new URL(rel, pageDirHref()).href;
  }

  /**
   * @param {string} url
   * @param {number} ms
   * @param {RequestInit} [init]
   */
  function fetchWithTimeout(url, ms, init) {
    init = init || {};
    if (
      typeof AbortSignal !== "undefined" &&
      typeof AbortSignal.timeout === "function"
    ) {
      return fetch(url, Object.assign({}, init, { signal: AbortSignal.timeout(ms) }));
    }
    const ctrl = new AbortController();
    const t = setTimeout(function () {
      ctrl.abort();
    }, ms);
    return fetch(url, Object.assign({}, init, { signal: ctrl.signal })).finally(function () {
      clearTimeout(t);
    });
  }

  function setServerOptions(serverSelect, statusLine, message, pairs) {
    serverSelect.innerHTML = "";
    for (let i = 0; i < pairs.length; i++) {
      const opt = document.createElement("option");
      opt.value = pairs[i][0];
      opt.textContent = pairs[i][1];
      serverSelect.appendChild(opt);
    }
    statusLine.textContent = message;
  }

  /**
   * @param {HTMLSelectElement} serverSelect
   * @param {HTMLElement} statusLine
   * @param {Record<string, string|function>} [msgs]
   * @param {function(): void} [onLoadedOk] after non-empty server list filled
   */
  async function loadServersInto(serverSelect, statusLine, msgs, onLoadedOk) {
    msgs = msgs || {};
    const loading =
      msgs.loading != null
        ? msgs.loading
        : "\uc11c\ubc84 \ubaa9\ub85d \ub85c\ub4dc \uc911\u2026";

    statusLine.textContent = loading;
    let res;
    try {
      res = await fetch(apiUrl("/api/servers"));
    } catch (e) {
      const fe =
        typeof msgs.fetchError === "function"
          ? msgs.fetchError(e)
          : msgs.fetchError != null
            ? msgs.fetchError
            : "API \uc5f0\uacb0 \uc2e4\ud328 (" + (e && e.message ? e.message : e) + ")";
      setServerOptions(serverSelect, statusLine, fe, [["", "(\uc5f0\uacb0 \uc2e4\ud328)"]]);
      return;
    }
    if (!res.ok) {
      const he =
        typeof msgs.httpError === "function"
          ? msgs.httpError(res.status)
          : msgs.httpError != null
            ? msgs.httpError
            : "HTTP " + res.status;
      setServerOptions(serverSelect, statusLine, he, [["", "(HTTP " + res.status + ")"]]);
      return;
    }
    let list;
    try {
      list = await res.json();
    } catch (_) {
      const bj =
        msgs.badJson != null
          ? msgs.badJson
          : "\uc11c\ubc84 \ubaa9\ub85d \uc751\ub2f5\uc774 JSON\uc774 \uc544\ub2d9\ub2c8\ub2e4.";
      setServerOptions(serverSelect, statusLine, bj, [["", "(\uc751\ub2f5 \uc624\ub958)"]]);
      return;
    }
    if (!Array.isArray(list)) {
      const bs =
        msgs.badShape != null
          ? msgs.badShape
          : "\uc11c\ubc84 \ubaa9\ub85d \ud615\uc2dd\uc774 \uc62c\ubc14\ub974\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.";
      setServerOptions(serverSelect, statusLine, bs, [["", "(\ud615\uc2dd \uc624\ub958)"]]);
      return;
    }
    serverSelect.innerHTML = "";
    if (!list.length) {
      const optText =
        msgs.emptyList != null
          ? msgs.emptyList
          : "servers.yaml \uc5c6\uc74c";
      const opt0 = document.createElement("option");
      opt0.value = "";
      opt0.textContent = optText;
      serverSelect.appendChild(opt0);
      statusLine.textContent =
        msgs.emptyListStatus != null ? msgs.emptyListStatus : optText;
      return;
    }
    for (let j = 0; j < list.length; j++) {
      const s = list[j];
      const o = document.createElement("option");
      o.value = s.id;
      o.textContent = s.label || s.id;
      serverSelect.appendChild(o);
    }
    statusLine.textContent =
      msgs.success != null
        ? msgs.success
        : "DB \uc11c\ubc84\ub97c \uc120\ud0dd\ud558\uc138\uc694.";
    if (typeof onLoadedOk === "function") onLoadedOk();
  }

  global.Seak80Common = {
    apiBase: apiBase,
    apiUrl: apiUrl,
    fetchWithTimeout: fetchWithTimeout,
    loadServersInto: loadServersInto,
  };
})(typeof window !== "undefined" ? window : globalThis);
