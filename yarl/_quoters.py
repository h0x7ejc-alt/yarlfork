"""Quoting and unquoting utilities for URL parts.

The quoters in this module follow these principles:
- QUOTER: For new strings that don't have %XX encoded sequences yet
  - Does not re-encode existing %XX sequences (requote=False)
  - Used for: Newly constructed URL parts in URL.build(), with_*() methods
  
- REQUOTER: For existing strings that may already have %XX encoding
  - Validates and normalizes existing %XX sequences (requote=True)
  - Used for: Parsing URL strings from external sources (encode_url())

- PATH_*: Specialized for path component, protects / and +
- QUERY_*: Specialized for query strings
- FRAGMENT_*: Specialized for URL fragments
"""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter

# For general use: When we are quoting a new string that does not have
# %XX encoding already (e.g., URL.build(), with_*() methods)
# Does not re-encode existing %XX sequences
QUOTER = _Quoter(requote=False)

# For parsing existing URL strings: When we need to normalize/validate
# existing %XX encoded sequences (e.g., encode_url())
# Re-encodes invalid %XX sequences and normalizes valid ones
REQUOTER = _Quoter()

# PATH QUOTERS:
# - Protects / (path separators) and + from being encoded
# - Treats @ and : as safe characters
PATH_QUOTER = _Quoter(safe="@:", protected="/+", requote=False)
PATH_REQUOTER = _Quoter(safe="@:", protected="/+")

# QUERY QUOTERS:
# - Treats ? / : @ as safe
# - Protects = + & ; from being encoded
# - Special handling for spaces (encoded as + instead of %20)
QUERY_QUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True, requote=False)
QUERY_REQUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True)
QUERY_PART_QUOTER = _Quoter(safe="?/:@", qs=True, requote=False)

# FRAGMENT QUOTERS:
# - Treats ? / : @ as safe
# - No special characters to protect
FRAGMENT_QUOTER = _Quoter(safe="?/:@", requote=False)
FRAGMENT_REQUOTER = _Quoter(safe="?/:@")

# UNQUOTERS:
# UNQUOTER: General purpose unquoter for most URL components
UNQUOTER = _Unquoter()

# PATH_UNQUOTER: Specialized for paths, treats + as literal
PATH_UNQUOTER = _Unquoter(unsafe="+")

# PATH_SAFE_UNQUOTER: For paths where / and % should remain encoded
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe="+")

# QS_UNQUOTER: Specialized for query strings, properly handles + and qs chars
QS_UNQUOTER = _Unquoter(qs=True)

# UNQUOTER_PLUS: Like urllib.parse.unquote_plus, decodes + to space
UNQUOTER_PLUS = _Unquoter(plus=True)


def human_quote(s: str | None, unsafe: str) -> str | None:
    """Quote a string for human-readable display.
    
    This function is only for display purposes (human_repr()),
    not for actual URL construction. It prioritizes readability
    over strict URL spec compliance.
    """
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
