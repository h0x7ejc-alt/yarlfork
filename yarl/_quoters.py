"""Quoting and unquoting utilities for URL parts."""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter

QUOTER = _Quoter(requote=False)
REQUOTER = _Quoter()
PATH_QUOTER = _Quoter(safe="@:", protected="/+", requote=False)
PATH_REQUOTER = _Quoter(safe="@:", protected="/+")
QUERY_QUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True, requote=False)
QUERY_REQUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True)
QUERY_PART_QUOTER = _Quoter(safe="?/:@", qs=True, requote=False)
FRAGMENT_QUOTER = _Quoter(safe="?/:@", requote=False)
FRAGMENT_REQUOTER = _Quoter(safe="?/:@")

UNQUOTER = _Unquoter()
PATH_UNQUOTER = _Unquoter(unsafe="+")
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe="+")
QS_UNQUOTER = _Unquoter(qs=True)
UNQUOTER_PLUS = _Unquoter(plus=True)  # to match urllib.parse.unquote_plus


def quote_userinfo(value: str | None) -> str | None:
    return QUOTER(value)


def requote_userinfo(value: str | None) -> str | None:
    return REQUOTER(value)


def unquote(value: str | None) -> str | None:
    return UNQUOTER(value)


def unquote_userinfo(value: str | None) -> str | None:
    return unquote(value)


def quote_path(value: str | None) -> str | None:
    return PATH_QUOTER(value)


def requote_path(value: str | None) -> str | None:
    return PATH_REQUOTER(value)


def unquote_path(value: str | None) -> str | None:
    return PATH_UNQUOTER(value)


def unquote_path_safe(value: str | None) -> str | None:
    return PATH_SAFE_UNQUOTER(value)


def quote_query(value: str | None) -> str | None:
    return QUERY_QUOTER(value)


def requote_query(value: str | None) -> str | None:
    return QUERY_REQUOTER(value)


def quote_query_part(value: str | None) -> str | None:
    return QUERY_PART_QUOTER(value)


def unquote_query(value: str | None) -> str | None:
    return QS_UNQUOTER(value)


def unquote_query_part(value: str | None) -> str | None:
    return UNQUOTER_PLUS(value)


def quote_fragment(value: str | None) -> str | None:
    return FRAGMENT_QUOTER(value)


def requote_fragment(value: str | None) -> str | None:
    return FRAGMENT_REQUOTER(value)


def unquote_fragment(value: str | None) -> str | None:
    return unquote(value)


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)


def human_quote_userinfo(value: str | None) -> str | None:
    return human_quote(value, "#/:?@[]\\")


def human_quote_path(value: str | None) -> str | None:
    return human_quote(value, "#?")


def human_quote_query_part(value: str | None) -> str | None:
    return human_quote(value, "#&+;=")


def human_quote_fragment(value: str | None) -> str | None:
    return human_quote(value, "")
