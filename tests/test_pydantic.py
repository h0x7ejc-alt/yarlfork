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
    # Check that the schema contains the required fields and our new additions
    assert schema["properties"]["url"]["format"] == "uri"
    assert schema["properties"]["url"]["type"] == "string"
    assert "description" in schema["properties"]["url"]
    assert "examples" in schema["properties"]["url"]


def test_json_roundtrip_json() -> None:
    url = URL("https://example.com")
    m = TstModel(url=url)
    js = m.model_dump_json()
    m2 = TstModel.model_validate_json(js)
    assert m == m2
    js2 = m2.model_dump_json()
    assert js == js2


def test_fake_cover() -> None:
    # The test exists only for getting ocverage for __get_pydantic_core_schema__,
    # otherwise a call of python code back from rust is not measured
    # by coverage tool

    URL.__get_pydantic_core_schema__(URL, pydantic.GetCoreSchemaHandler())


def test_enhanced_json_schema() -> None:
    # Test that our enhanced JSON schema has description and examples
    schema = TstModel.model_json_schema()
    url_schema = schema["properties"]["url"]
    assert url_schema["description"] == "A yarl.URL object representing a URL"
    assert url_schema["examples"] == [
        "https://example.com",
        "http://localhost:8000/path?query=1#fragment",
    ]


def test_improved_error_message() -> None:
    # Test that invalid URLs produce clear, descriptive error messages
    with pytest.raises(pydantic.ValidationError, match="invalid_url"):
        TstModel.model_validate({"url": "not a valid url"})
    with pytest.raises(pydantic.ValidationError, match="Invalid URL"):
        TstModel.model_validate({"url": "ftp://"})
