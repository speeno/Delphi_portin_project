from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

from app.core import config
from app.services import nl_library_client


class _FakeResponse:
    headers = {"content-type": "application/json"}
    status = 200

    def __init__(self, payload: dict[str, object]):
        self._raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    def read(self, _size: int = -1) -> bytes:
        return self._raw

    def getcode(self) -> int:
        return self.status

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *_exc: object) -> None:
        return None


def test_nl_build_url_uses_same_key_value_for_key_and_cert_key(monkeypatch) -> None:
    monkeypatch.setattr(config, "NL_BASE_URL", "https://www.nl.go.kr")
    api_key = "same-secret"

    search_url = nl_library_client.build_url(
        "/NL/search/openApi/search.do",
        {"key": api_key, "kwd": "테스트"},
    )
    isbn_url = nl_library_client.build_url(
        "/seoji/SearchApi.do",
        {"cert_key": api_key, "isbn": "9791190000000"},
    )

    assert parse_qs(urlparse(search_url).query)["key"] == [api_key]
    assert parse_qs(urlparse(isbn_url).query)["cert_key"] == [api_key]


def test_nl_isbn_lookup_normalizes_json_response(monkeypatch) -> None:
    called: dict[str, str] = {}

    def fake_urlopen(req, *, timeout: float):  # noqa: ANN001
        called["url"] = req.full_url
        assert timeout == 1.0
        return _FakeResponse(
            {
                "items": [
                    {
                        "title": "테스트 도서",
                        "author": "홍길동",
                        "publisher": "테스트출판",
                        "isbn": "979-11-90000-00-0",
                        "price": "12000",
                        "pubDate": "2026-05-01",
                        "classNo": "813.7",
                    }
                ]
            }
        )

    monkeypatch.setattr(config, "NL_API_KEY", "same-secret")
    monkeypatch.setattr(config, "NL_BASE_URL", "https://www.nl.go.kr")
    monkeypatch.setattr(config, "NL_REQUEST_TIMEOUT_SEC", 1.0)
    monkeypatch.setattr(config, "NL_CACHE_TTL_SEC", 300)
    monkeypatch.setattr(nl_library_client.open_api_http, "urlopen", fake_urlopen)

    result = nl_library_client.isbn_lookup("979-11-90000-00-0")

    qs = parse_qs(urlparse(called["url"]).query)
    assert qs["cert_key"] == ["same-secret"]
    assert "key" not in qs
    assert result["status"] == "ok"
    assert result["items"][0]["title"] == "테스트 도서"
    assert result["items"][0]["isbn"] == "9791190000000"
    assert result["items"][0]["price"] == 12000


def test_nl_search_uses_key_parameter(monkeypatch) -> None:
    called: dict[str, str] = {}

    def fake_urlopen(req, *, timeout: float):  # noqa: ANN001, ARG001
        called["url"] = req.full_url
        return _FakeResponse({"items": [{"title": "검색 도서", "author": "저자"}]})

    monkeypatch.setattr(config, "NL_API_KEY", "same-secret")
    monkeypatch.setattr(config, "NL_BASE_URL", "https://www.nl.go.kr")
    monkeypatch.setattr(config, "NL_CACHE_TTL_SEC", 300)
    monkeypatch.setattr(nl_library_client.open_api_http, "urlopen", fake_urlopen)

    result = nl_library_client.search_books("검색 도서", limit=3)

    qs = parse_qs(urlparse(called["url"]).query)
    assert qs["key"] == ["same-secret"]
    assert "cert_key" not in qs
    assert qs["kwd"] == ["검색 도서"]
    assert qs["pageSize"] == ["3"]
    assert result["status"] == "ok"
