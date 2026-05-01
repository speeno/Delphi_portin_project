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

from app.services import masters_service  # noqa: E402


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
    assert out is None


def test_update_book_ok_when_row_matches_payload(monkeypatch) -> None:
    monkeypatch.setattr(masters_service, "execute_in_transaction", _fake_tx_ok)
    monkeypatch.setattr(masters_service, "execute_query", _fake_q_hit)

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
    assert out is not None
    assert out["gcode"] == "0014"
    assert "gname" in out["updated_fields"]
