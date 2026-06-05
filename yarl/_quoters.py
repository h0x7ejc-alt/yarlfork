"""Quoting and unquoting utilities for URL parts."""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter

def _make_quoter_pair(
    *,
    safe: str = "",
    protected: str = "",
    qs: bool = False,
) -> tuple[_Quoter, _Quoter]:
    return (
        _Quoter(safe=safe, protected=protected, qs=qs, requote=False),
        _Quoter(safe=safe, protected=protected, qs=qs, requote=True),
    )


QUOTER, REQUOTER = _make_quoter_pair()

_PATH_SAFE = "@:"
_PATH_PROTECTED = "/+"
PATH_QUOTER, PATH_REQUOTER = _make_quoter_pair(
    safe=_PATH_SAFE, protected=_PATH_PROTECTED
)

_QUERY_SAFE = "?/:@"
_QUERY_PROTECTED = "=+&;"
QUERY_QUOTER, QUERY_REQUOTER = _make_quoter_pair(
    safe=_QUERY_SAFE, protected=_QUERY_PROTECTED, qs=True
)
QUERY_PART_QUOTER = _Quoter(safe=_QUERY_SAFE, qs=True, requote=False)

FRAGMENT_QUOTER, FRAGMENT_REQUOTER = _make_quoter_pair(safe=_QUERY_SAFE)

_PATH_UNSAFE = "+"
UNQUOTER = _Unquoter()
PATH_UNQUOTER = _Unquoter(unsafe=_PATH_UNSAFE)
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe=_PATH_UNSAFE)
QS_UNQUOTER = _Unquoter(qs=True)
UNQUOTER_PLUS = _Unquoter(plus=True)  # to match urllib.parse.unquote_plus


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
