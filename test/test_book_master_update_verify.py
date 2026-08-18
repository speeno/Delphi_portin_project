"""
도서 마스터 PATCH(update_book) 저장 검증.

mysql3_protocol 서버는 execute_in_transaction 이 rowcount 를 항상 0 으로 반환한다.
이전 구현은 영향 행이 0 이면서 Gcode 만 존재할 때 성공으로 처리해 거짓 성공이 났다.
저장 후 SELECT 로 반영 여부를 검증한 뒤만 성공을 반환하는지 회귀 가드.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import g4_book_adapt  # noqa: E402
from app.services import masters_service  # noqa: E402

# update_book 은 g4_book_adapt.g4_book_column_meta(SHOW COLUMNS FROM G4_Book) 로 존재
# 컬럼을 먼저 조회한다. 어댑터는 자체 import 한 execute_query 를 쓰므로 masters_service
# 만 패치하면 실 DB 로 나가 'Unknown server id: remote_1' 이 난다 → 함께 fake 로 대체.
_G4_COLS = ["Gcode", "Gname", "Gjeja", "Gisbn", "Gdang", "Gpost", "Sname", "Jubun"]


async def _fake_g4_meta_query(_server_id, sql, params=None):
    if "SHOW COLUMNS" in sql:
        return [{"Field": c} for c in _G4_COLS]
    return []


async def _fake_tx_ok(*_a, **_k):
    return [0]


async def _fake_q_empty(*_a, **_k):
    return []


async def _fake_q_hit(*_a, **_k):
    return [
        {
            "gname": "제과제빵실기",
            "gjeja": "저자A",
            "gisbn": "9788994204659",
            "gdang": 26000,
            "gpost": "",
        }
    ]


def test_update_book_returns_none_when_post_verify_select_empty(monkeypatch) -> None:
    monkeypatch.setattr(masters_service, "execute_in_transaction", _fake_tx_ok)
    monkeypatch.setattr(masters_service, "execute_query", _fake_q_empty)
    monkeypatch.setattr(g4_book_adapt, "execute_query", _fake_g4_meta_query)
    g4_book_adapt.clear_g4_column_cache_for_tests()

    async def _run():
        return await masters_service.update_book(
            server_id="remote_1",
            gcode="0014",
            payload={
                "gname": "제과제빵실기",
                "gjeja": "저자A",
                "gisbn": "9788994204659",
                "gdang": 26000,
                "gpost": "",
                "match_gname": "구제목",
            },
        )

    out = asyncio.run(_run())
    g4_book_adapt.clear_g4_column_cache_for_tests()
    assert out is None


def test_update_book_ok_when_row_matches_payload(monkeypatch) -> None:
    monkeypatch.setattr(masters_service, "execute_in_transaction", _fake_tx_ok)
    monkeypatch.setattr(masters_service, "execute_query", _fake_q_hit)
    monkeypatch.setattr(g4_book_adapt, "execute_query", _fake_g4_meta_query)
    g4_book_adapt.clear_g4_column_cache_for_tests()

    async def _run():
        return await masters_service.update_book(
            server_id="remote_1",
            gcode="0014",
            payload={
                "gname": "제과제빵실기",
                "gjeja": "저자A",
                "gisbn": "978-89-94204-65-9",
                "gdang": 26000,
                "gpost": "",
            },
        )

    out = asyncio.run(_run())
    g4_book_adapt.clear_g4_column_cache_for_tests()
    assert out is not None
    assert out["gcode"] == "0014"
    assert "gname" in out["updated_fields"]
