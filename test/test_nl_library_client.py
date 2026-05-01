from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

from app.core import config
from app.services import nl_library_client


class _FakeResponse:
    headers: dict[str, str]
    status = 200

    def __init__(self, payload: dict[str, object] | None = None, *, raw: bytes | None = None):
        self.headers = {"content-type": "application/json"}
        if raw is not None:
            self._raw = raw
            self.headers = {"content-type": "application/xml"}
        else:
            self._raw = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8")

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


_SASEO_XML = """<?xml version="1.0" encoding="UTF-8"?>
<channel>
<totalCount>1</totalCount>
<list>
   <item>
        <recomtitle>\ubc29\uad00\uc2dc\ub300\uc758 \uc0ac\ub78c\ub4e4</recomtitle>
        <recomauthor>\ub958\uc804\uc708</recomauthor>
        <recompublisher>\uae00\ud56d\uc544\ub9ac</recompublisher>
        <recomisbn>9788967356743</recomisbn>
   </item>
</list>
</channel>
""".encode("utf-8")


def test_nl_librarian_picks_parses_saseo_xml(monkeypatch) -> None:
    called: dict[str, str] = {}

    def fake_urlopen(req, *, timeout: float):  # noqa: ANN001, ARG001
        called["url"] = req.full_url
        return _FakeResponse(raw=_SASEO_XML)

    monkeypatch.setattr(config, "NL_API_KEY", "same-secret")
    monkeypatch.setattr(config, "NL_BASE_URL", "https://www.nl.go.kr")
    monkeypatch.setattr(config, "NL_CACHE_TTL_SEC", 300)
    monkeypatch.setattr(config, "NL_SASEO_LOOKBACK_DAYS", 30)
    monkeypatch.setattr(config, "NL_SASEO_DRCODE", "")
    monkeypatch.setattr(nl_library_client.open_api_http, "urlopen", fake_urlopen)
    nl_library_client._CACHE.clear()

    result = nl_library_client.librarian_picks(limit=3)

    qs = parse_qs(urlparse(called["url"]).query)
    assert qs["key"] == ["same-secret"]
    assert "startRowNumApi" in qs and qs["startRowNumApi"] == ["1"]
    assert "endRowNumApi" in qs and qs["endRowNumApi"] == ["3"]
    assert "start_date" in qs and "end_date" in qs
    assert "apiType" not in qs
    assert result["status"] == "ok"
    assert len(result["items"]) >= 1
    assert result["items"][0]["title"] == "방관시대의 사람들"
    assert result["items"][0]["isbn"] == "9788967356743"


def test_nl_normalize_book_maps_recom_fields() -> None:
    row = {
        "recomtitle": "Title",
        "recomauthor": "Author",
        "recompublisher": "Pub",
        "recomisbn": "9791188535040",
    }
    book = nl_library_client._normalize_book(row)
    assert book["title"] == "Title"
    assert book["author"] == "Author"
    assert book["publisher"] == "Pub"
    assert book["isbn"] == "9791188535040"
