"""Unit tests for Subu67-style S1_Ssub line aggregation (sobo67_aggregate)."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "backend"
sys.path.insert(0, str(BACKEND))

from sobo67_aggregate import (  # noqa: E402
    aggregate_detail_rows,
    footer_totals,
    merge_aggregate_grids,
    merge_sg_csum_gpsum,
)


def test_aggregate_year_grain_y_inbound():
    rows = [
        {
            "bcode": "B001",
            "gdate": "2024.01.15",
            "scode": "Y",
            "gubun": "\uc785\uace0",
            "pubun": "",
            "gsqut": 10,
            "gssum": 0,
            "gname": "BookA",
        },
        {
            "bcode": "B001",
            "gdate": "2024.03.20",
            "scode": "Y",
            "gubun": "\ubc18\ud488",
            "pubun": "",
            "gsqut": 2,
            "gssum": 0,
            "gname": "BookA",
        },
    ]
    out = aggregate_detail_rows(rows, year_grain=True)
    assert len(out) == 1
    r = out[0]
    assert r["gdate"] == "2024"
    assert r["gcode"] == "B001"
    assert r["giqut"] == 8.0


def test_aggregate_month_grain_outbound():
    rows = [
        {
            "bcode": "B002",
            "gdate": "2024.05.01",
            "scode": "X",
            "gubun": "\ucd9c\uace0",
            "pubun": "\ucd9c\uace0",
            "gsqut": 5,
            "gssum": 100,
            "gname": "X",
        },
    ]
    out = aggregate_detail_rows(rows, year_grain=False)
    assert out[0]["gdate"] == "2024.05"
    assert out[0]["goqut"] == 5.0
    assert out[0]["gosum"] == 100.0


def test_merge_aggregate_grids_same_book_two_chunks():
    a = aggregate_detail_rows(
        [
            {
                "bcode": "B1",
                "gdate": "2024.01.01",
                "scode": "Y",
                "gubun": "\uc785\uace0",
                "pubun": "",
                "gsqut": 3,
                "gssum": 0,
                "gname": "G",
            },
        ],
        year_grain=True,
    )
    b = aggregate_detail_rows(
        [
            {
                "bcode": "B1",
                "gdate": "2024.06.01",
                "scode": "Y",
                "gubun": "\uc785\uace0",
                "pubun": "",
                "gsqut": 2,
                "gssum": 0,
                "gname": "G",
            },
        ],
        year_grain=True,
    )
    m = merge_aggregate_grids(a, b, year_grain=True)
    assert len(m) == 1
    assert m[0]["gdate"] == "2024"
    assert m[0]["gcode"] == "B1"
    assert m[0]["giqut"] == 5.0


def test_merge_sg_csum_gpsum():
    grid = [
        {
            "gdate": "2024",
            "gcode": "C1",
            "gname": "N",
            "giqut": 1,
            "goqut": 0,
            "gjqut": 0,
            "gbqut": 0,
            "gpqut": 0,
            "gosum": 0,
            "gbsum": 0,
            "gpsum": 0,
        }
    ]
    sg = [{"gcode": "C1", "gdate": "2024.06.01", "gbsum": 7}]
    merge_sg_csum_gpsum(grid, sg, year_grain=True)
    assert grid[0]["gpsum"] == 7.0


def test_footer_totals():
    rows = [{"giqut": 1, "goqut": 2, "gpsum": 3}]
    ft = footer_totals(rows)  # type: ignore[arg-type]
    assert ft["giqut"] == 1.0
    assert ft["goqut"] == 2.0
    assert ft["gpsum"] == 3.0
