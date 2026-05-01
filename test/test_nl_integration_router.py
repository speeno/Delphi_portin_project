from __future__ import annotations

import asyncio

from app.routers import integrations_nl


def test_nl_isbn_router_returns_service_payload(monkeypatch) -> None:
    def fake_isbn_lookup(isbn: str) -> dict[str, object]:
        return {"status": "ok", "kind": "isbn", "items": [{"isbn": isbn}]}

    monkeypatch.setattr(integrations_nl.nl_library_client, "isbn_lookup", fake_isbn_lookup)

    result = asyncio.run(
        integrations_nl.get_nl_isbn(server_id="remote_153", isbn="9791190000000")
    )

    assert result["status"] == "ok"
    assert result["items"] == [{"isbn": "9791190000000"}]


def test_nl_bibliography_status_router_returns_non_500_shape(monkeypatch) -> None:
    def fake_status(*, isbn: str = "", title: str = "") -> dict[str, object]:
        return {
            "status": "config_missing",
            "confirmed": False,
            "label": "서지 미확인",
            "items": [],
            "isbn": isbn,
            "title": title,
        }

    monkeypatch.setattr(integrations_nl.nl_library_client, "bibliography_status", fake_status)

    result = asyncio.run(
        integrations_nl.get_nl_bibliography_status(
            server_id="remote_153",
            isbn="",
            title="테스트 도서",
        )
    )

    assert result["status"] == "config_missing"
    assert result["confirmed"] is False
    assert result["label"] == "서지 미확인"
