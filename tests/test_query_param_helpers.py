from typing import Any
import pytest
from yarl import URL

def test_has_query_param() -> None:
    url = URL("http://example.com?a=1&b=2&a=3")
    assert url.has_query_param("a") is True
    assert url.has_query_param("b") is True
    assert url.has_query_param("c") is False

    url_empty = URL("http://example.com")
    assert url_empty.has_query_param("a") is False

    with pytest.raises(TypeError, match="Query parameter name must be a string"):
        url.has_query_param(123)  # type: ignore[arg-type]


def test_get_query_param() -> None:
    url = URL("http://example.com?a=1&b=2&a=3")
    assert url.get_query_param("a") == "1"
    assert url.get_query_param("b") == "2"
    assert url.get_query_param("c") is None
    assert url.get_query_param("c", default="default_value") == "default_value"

    url_empty = URL("http://example.com")
    assert url_empty.get_query_param("a") is None

    with pytest.raises(TypeError, match="Query parameter name must be a string"):
        url.get_query_param(123)  # type: ignore[arg-type]


def test_get_all_query_params() -> None:
    url = URL("http://example.com?a=1&b=2&a=3")
    assert url.get_all_query_params("a") == ("1", "3")
    assert url.get_all_query_params("b") == ("2",)
    assert url.get_all_query_params("c") == ()

    url_empty = URL("http://example.com")
    assert url_empty.get_all_query_params("a") == ()

    with pytest.raises(TypeError, match="Query parameter name must be a string"):
        url.get_all_query_params(123)  # type: ignore[arg-type]
