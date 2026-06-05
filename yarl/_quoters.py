"""Quoting and unquoting utilities for URL parts."""

from typing import TypedDict as _TypedDict
from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter


class _QuoterKwargs(_TypedDict, total=False):
    safe: str
    protected: str
    qs: bool
    requote: bool


class _UnquoterKwargs(_TypedDict, total=False):
    ignore: str
    unsafe: str
    qs: bool
    plus: bool


_PATH_SAFE = "@:"
_PATH_PROTECTED = "/+"
_QUERY_SAFE = "?/:@"
_QUERY_PROTECTED = "=+&;"
_PATH_UNSAFE = "+"
_PATH_SAFE_IGNORE = "/%"


def _make_quoters(definitions: dict[str, _QuoterKwargs]) -> dict[str, _Quoter]:
    return {name: _Quoter(**kwargs) for name, kwargs in definitions.items()}


def _make_unquoters(definitions: dict[str, _UnquoterKwargs]) -> dict[str, _Unquoter]:
    return {name: _Unquoter(**kwargs) for name, kwargs in definitions.items()}


_QUOTERS = _make_quoters(
    {
        "QUOTER": {"requote": False},
        "REQUOTER": {},
        "PATH_QUOTER": {
            "safe": _PATH_SAFE,
            "protected": _PATH_PROTECTED,
            "requote": False,
        },
        "PATH_REQUOTER": {"safe": _PATH_SAFE, "protected": _PATH_PROTECTED},
        "QUERY_QUOTER": {
            "safe": _QUERY_SAFE,
            "protected": _QUERY_PROTECTED,
            "qs": True,
            "requote": False,
        },
        "QUERY_REQUOTER": {
            "safe": _QUERY_SAFE,
            "protected": _QUERY_PROTECTED,
            "qs": True,
        },
        "QUERY_PART_QUOTER": {
            "safe": _QUERY_SAFE,
            "qs": True,
            "requote": False,
        },
        "FRAGMENT_QUOTER": {"safe": _QUERY_SAFE, "requote": False},
        "FRAGMENT_REQUOTER": {"safe": _QUERY_SAFE},
    }
)

_UNQUOTERS = _make_unquoters(
    {
        "UNQUOTER": {},
        "PATH_UNQUOTER": {"unsafe": _PATH_UNSAFE},
        "PATH_SAFE_UNQUOTER": {"ignore": _PATH_SAFE_IGNORE, "unsafe": _PATH_UNSAFE},
        "QS_UNQUOTER": {"qs": True},
        "UNQUOTER_PLUS": {"plus": True},
    }
)

QUOTER = _QUOTERS["QUOTER"]
REQUOTER = _QUOTERS["REQUOTER"]
PATH_QUOTER = _QUOTERS["PATH_QUOTER"]
PATH_REQUOTER = _QUOTERS["PATH_REQUOTER"]
QUERY_QUOTER = _QUOTERS["QUERY_QUOTER"]
QUERY_REQUOTER = _QUOTERS["QUERY_REQUOTER"]
QUERY_PART_QUOTER = _QUOTERS["QUERY_PART_QUOTER"]
FRAGMENT_QUOTER = _QUOTERS["FRAGMENT_QUOTER"]
FRAGMENT_REQUOTER = _QUOTERS["FRAGMENT_REQUOTER"]

UNQUOTER = _UNQUOTERS["UNQUOTER"]
PATH_UNQUOTER = _UNQUOTERS["PATH_UNQUOTER"]
PATH_SAFE_UNQUOTER = _UNQUOTERS["PATH_SAFE_UNQUOTER"]
QS_UNQUOTER = _UNQUOTERS["QS_UNQUOTER"]
UNQUOTER_PLUS = _UNQUOTERS["UNQUOTER_PLUS"]


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
