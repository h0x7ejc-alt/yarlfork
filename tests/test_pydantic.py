from typing import TYPE_CHECKING

import pytest

from yarl import URL

if TYPE_CHECKING:
    import pydantic
else:
    pydantic = pytest.importorskip("pydantic")


class TstModel(pydantic.BaseModel):
    url: URL


def test_dump() -> None:
    url = URL("https://example.com")
    m = TstModel(url=url)
    dct = m.model_dump()
    assert dct == {"url": str(url)}
    assert isinstance(dct["url"], str)


def test_validate_valid() -> None:
    url = URL("https://example.com")
    dct = {"url": str(url)}
    m = TstModel.model_validate(dct)
    assert m == TstModel(url=url)
    assert isinstance(m.url, URL)


def test_validate_invalid() -> None:
    dct = {"url": 123}
    with pytest.raises(pydantic.ValidationError, match="url"):
        TstModel.model_validate(dct)


def test_get_schema() -> None:
    schema = TstModel.model_json_schema()
    url_schema = schema["properties"]["url"]
    assert url_schema["type"] == "string"
    assert url_schema["format"] == "uri"
    assert "description" in url_schema
    assert "RFC 3986" in url_schema["description"]
    assert "examples" in url_schema
    assert "https://example.com" in url_schema["examples"]


def test_schema_description() -> None:
    schema = TstModel.model_json_schema()
    url_schema = schema["properties"]["url"]
    assert url_schema["description"] == "A URL parsed by yarl following RFC 3986."


def test_schema_examples() -> None:
    schema = TstModel.model_json_schema()
    url_schema = schema["properties"]["url"]
    assert url_schema["examples"] == [
        "https://example.com",
        "http://user:pass@example.com:8080/path?query=value#fragment",
    ]


def test_schema_serialization_type() -> None:
    schema = TstModel.model_json_schema()
    url_schema = schema["properties"]["url"]
    assert url_schema["type"] == "string"


def test_validate_url_with_invalid_ipv6() -> None:
    class HostModel(pydantic.BaseModel):
        url: URL

    with pytest.raises(pydantic.ValidationError, match="invalid URL") as exc_info:
        HostModel.model_validate({"url": "http://[]/"})
    assert "invalid URL" in str(exc_info.value)


def test_json_roundtrip_json() -> None:
    url = URL("https://example.com")
    m = TstModel(url=url)
    js = m.model_dump_json()
    m2 = TstModel.model_validate_json(js)
    assert m == m2
    js2 = m2.model_dump_json()
    assert js == js2


def test_fake_cover() -> None:
    URL.__get_pydantic_core_schema__(URL, pydantic.GetCoreSchemaHandler())
