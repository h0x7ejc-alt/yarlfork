"""Quoting and unquoting utilities for URL parts."""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter


def _make_quoter_pair(
    *,
    safe: str = "",
    protected: str = "",
    qs: bool = False,
) -> tuple[_Quoter, _Quoter]:
    """Create a (quoter, requoter) pair sharing the same safe/protected/qs."""
    return (
        _Quoter(safe=safe, protected=protected, qs=qs, requote=False),
        _Quoter(safe=safe, protected=protected, qs=qs, requote=True),
    )


# --- Quoters ---

QUOTER, REQUOTER = _make_quoter_pair()
PATH_QUOTER, PATH_REQUOTER = _make_quoter_pair(safe="@:", protected="/+")
QUERY_QUOTER, QUERY_REQUOTER = _make_quoter_pair(safe="?/:@", protected="=+&;", qs=True)
QUERY_PART_QUOTER = _Quoter(safe="?/:@", qs=True, requote=False)
FRAGMENT_QUOTER, FRAGMENT_REQUOTER = _make_quoter_pair(safe="?/:@")

# --- Unquoters ---

UNQUOTER = _Unquoter()
PATH_UNQUOTER = _Unquoter(unsafe="+")
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe="+")
QS_UNQUOTER = _Unquoter(qs=True)
UNQUOTER_PLUS = _Unquoter(plus=True)


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
