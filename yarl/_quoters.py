"""Quoting and unquoting utilities for URL parts."""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter

_PATH_SAFE = "@:"
_PATH_PROTECTED = "/+"
_QF_SAFE = "?/:@"
_Q_PROTECTED = "=+&;"

# -- generic ----------------------------------------------------------------

QUOTER = _Quoter(requote=False)
REQUOTER = _Quoter()

# -- path -------------------------------------------------------------------

PATH_QUOTER = _Quoter(safe=_PATH_SAFE, protected=_PATH_PROTECTED, requote=False)
PATH_REQUOTER = _Quoter(safe=_PATH_SAFE, protected=_PATH_PROTECTED)
PATH_UNQUOTER = _Unquoter(unsafe="+")
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe="+")

# -- query ------------------------------------------------------------------

QUERY_QUOTER = _Quoter(safe=_QF_SAFE, protected=_Q_PROTECTED, qs=True, requote=False)
QUERY_REQUOTER = _Quoter(safe=_QF_SAFE, protected=_Q_PROTECTED, qs=True)
QUERY_PART_QUOTER = _Quoter(safe=_QF_SAFE, qs=True, requote=False)
QS_UNQUOTER = _Unquoter(qs=True)
UNQUOTER_PLUS = _Unquoter(plus=True)  # to match urllib.parse.unquote_plus

# -- fragment ---------------------------------------------------------------

FRAGMENT_QUOTER = _Quoter(safe=_QF_SAFE, requote=False)
FRAGMENT_REQUOTER = _Quoter(safe=_QF_SAFE)

# -- generic unquoter -------------------------------------------------------

UNQUOTER = _Unquoter()


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
