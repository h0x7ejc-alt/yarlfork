"""Quoting and unquoting utilities for URL parts.

This module centralizes all quoting/unquoting logic and defines clear
responsibility boundaries for when to quote, requote, or preserve
unsafe characters.

## Quoting Contexts

### Build Context (requote=False)
Used when input is raw/unencoded values (e.g., URL.build(), with_* methods).
Assumes input should be fully encoded; existing %XX sequences are treated
as literal percent signs.

### Parse Context (requote=True)
Used when parsing URL strings that may already be partially encoded.
Decodes %XX sequences, then re-encodes if the decoded character is safe.
Normalizes hex case (%2f -> %2F) and decodes over-encoded characters.

### Display Context (human_repr)
Used for human-readable URL representation. Decodes percent-encoded
sequences, then re-encodes only characters that would be ambiguous
in the display context (like % itself, or unsafe chars for that part).

## URL Part Safety Rules

Path:
  - Safe: unreserved + sub-delims (without +&=;) + @:
  - Protected: /+ (kept encoded when re-quoting)
  - Unsafe for display: #?

Query:
  - Safe: unreserved + sub-delims + ?/:@
  - Protected: =+&; (query syntax characters)
  - qs=True: space -> +, handles query-specific encoding
  - Unsafe for display: #&+=

Fragment:
  - Safe: unreserved + sub-delims + ?/:@
  - Unsafe for display: (none - all fragment chars are displayable)

Userinfo (user/password):
  - Safe: unreserved + sub-delims + :
  - Unsafe for display: #/:?@[]\\

Host:
  - Already encoded by _encode_host()
  - Display uses host property (IDNA decoded for international domains)
"""

from urllib.parse import quote

from ._quoting import _Quoter, _Unquoter

# ---------------------------------------------------------------------------
# Base Quoters - for general purpose quoting
# ---------------------------------------------------------------------------

# Build context: input is raw/unencoded
QUOTER = _Quoter(requote=False)

# Parse context: input may be partially encoded, normalize it
REQUOTER = _Quoter()

# ---------------------------------------------------------------------------
# Path Quoters
# ---------------------------------------------------------------------------

# Build context: path parts are unencoded
PATH_QUOTER = _Quoter(safe="@:", protected="/+", requote=False)

# Parse context: path may contain %XX sequences to normalize
PATH_REQUOTER = _Quoter(safe="@:", protected="/+")

# ---------------------------------------------------------------------------
# Query Quoters
# ---------------------------------------------------------------------------

# Build context: entire query string is unencoded
QUERY_QUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True, requote=False)

# Parse context: query string may be partially encoded
QUERY_REQUOTER = _Quoter(safe="?/:@", protected="=+&;", qs=True)

# Build context: individual query key/value pairs (no protected chars needed
# since each pair is quoted separately)
QUERY_PART_QUOTER = _Quoter(safe="?/:@", qs=True, requote=False)

# ---------------------------------------------------------------------------
# Fragment Quoters
# ---------------------------------------------------------------------------

# Build context: fragment is unencoded
FRAGMENT_QUOTER = _Quoter(safe="?/:@", requote=False)

# Parse context: fragment may be partially encoded
FRAGMENT_REQUOTER = _Quoter(safe="?/:@")

# ---------------------------------------------------------------------------
# Unquoters
# ---------------------------------------------------------------------------

# General purpose unquoter - decodes %XX sequences
UNQUOTER = _Unquoter()

# Path unquoter - keeps + encoded (since + is protected in path context)
PATH_UNQUOTER = _Unquoter(unsafe="+")

# Path unquoter that ignores / and % during decoding (for path segments)
PATH_SAFE_UNQUOTER = _Unquoter(ignore="/%", unsafe="+")

# Query string unquoter - handles qs-specific rules (+ -> space)
QS_UNQUOTER = _Unquoter(qs=True)

# Matches urllib.parse.unquote_plus behavior
UNQUOTER_PLUS = _Unquoter(plus=True)

# ---------------------------------------------------------------------------
# Human-readable display quoting
# ---------------------------------------------------------------------------

# Unsafe characters for each URL part in human-readable representation
# These characters should be percent-encoded even in display context
# to avoid ambiguity or breaking URL structure
HUMAN_UNSAFE = {
    "userinfo": "#/:?@[]\\",  # user, password
    "host": "",  # host is already IDNA-decoded, no extra encoding needed
    "path": "#?",  # path should not contain delimiters
    "query_key": "#&+;=",  # query keys should not contain delimiters
    "query_value": "#&+;=",  # query values should not contain delimiters
    "fragment": "",  # fragment can contain anything
}


def human_quote(s: str | None, unsafe: str) -> str | None:
    """Quote a string for human-readable URL representation.

    This function:
    1. Encodes % characters to avoid ambiguity with percent-encoded sequences
    2. Encodes characters in the unsafe set
    3. Encodes non-printable characters

    Unlike _Quoter, this function works on already-decoded strings and
    only encodes characters that would be problematic for display.
    """
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
