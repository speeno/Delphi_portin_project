/**
 * DB column key (lowercase) -> Korean header label for Seak80 sample grids.
 * Source inventory: docs/phase1-structure/seak80-column-label-inventory.md
 * Load after seak80-common.js is optional; exposes window.Seak80ColumnLabels.
 */
(function (global) {
  "use strict";

  /** Shared keys (lowercase) seen on *_Ggeo / *_Gbun / G4_Book */
  var COMMON = {
    hcode: "Hcode",
    gcode: "\ucf54\ub4dc",
    jubun: "\uc8fc\ubd84",
    gubun: "\uad6c\ubd84",
    pubun: "\ud488\ubd84",
    ocode: "Ocode",
    scode: "^",
    gtel1: "\uc804\ud6541",
    gtel2: "\uc804\ud6542",
    gadd1: "\uc8fc\uc18c1",
    gadd2: "\uc8fc\uc18c2",
    gposa: "\ub300\ud45c",
    gjisa: "\uc9c0\uc0ac",
    gname: "\uba85",
    bcode: "Bcode",
    gdate: "\uc77c\uc790",
    squt: "\uc218\ub9cc",
    ssum: "\uae08\uc561",
    gsqut: "\uc218\ub9cc",
    gssum: "\uae08\uc561",
    isbn: "ISBN",
    pname: "\ud488\uba85",
    writer: "\uc800\uc790",
    pub: "\ucd9c\ud310\uc0ac",
    price: "\ub2e8\uac00",
    page: "\uba74",
    size: "\ud06c\uae30",
    gtype: "\uc720\ud615",
    gkind: "\uc885\ubcc4",
    gstat: "\uc0c1\ud0dc",
    gmemo: "\uba54\ubaa8",
    gdate2: "\uc77c\uc7902",
    guser: "\uc791\uc131\uc790",
    gtime: "\uc2dc\uac04",
  };

  /** Per physical table (lowercase table name from API `table` field). */
  var BY_TABLE = {
    g1_ggeo: {
      gname: "\uac70\ub798\ucc98\uba85",
      scode: "^",
    },
    g2_gbun: {
      gname: "\uc785\uace0\ucc98\uba85",
      scode: "^",
    },
    t1_gbun: {
      gname: "\uc800\uc790\uad6c\ubd84",
      scode: "^",
    },
    g4_book: {
      gname: "\ub3c4\uc11c\uba85",
      bcode: "\ub3c4\uc11c\ucf54\ub4dc",
    },
    g6_ggeo: {
      gname: "\ud2b9\ubcc4\uac70\ub798\ucc98",
    },
    g7_gbun: {
      gname: "\ucd9c\ud310\uc0ac\uad6c\ubd84",
    },
    g7_ggeo: {
      gname: "\ucd9c\ud310\uc0ac\uba85",
    },
    t0_gbun: {
      gname: "\ucd9c\uace0\uc99d\uad6c\ubd84",
    },
  };

  function normTable(t) {
    return String(t || "")
      .trim()
      .toLowerCase();
  }

  function normKey(k) {
    return String(k || "")
      .trim()
      .toLowerCase();
  }

  /**
   * @param {string|null|undefined} tableName from API `table` (e.g. G1_Ggeo)
   * @param {string} fieldKey row object key (already lowercased by API normalizer)
   * @returns {string} Korean label or original key if unknown
   */
  function columnLabel(tableName, fieldKey) {
    var k = normKey(fieldKey);
    if (!k) return "";
    var t = normTable(tableName);
    if (t && BY_TABLE[t] && BY_TABLE[t][k]) return BY_TABLE[t][k];
    if (COMMON[k]) return COMMON[k];
    return fieldKey;
  }

  global.Seak80ColumnLabels = {
    columnLabel: columnLabel,
  };
})(typeof window !== "undefined" ? window : globalThis);
