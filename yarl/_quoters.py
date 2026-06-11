"""Quoting and unquoting utilities for URL parts.

Quoting strategy
----------------

yarl stores every URL component (scheme, netloc, path, query, fragment) in
**percent-encoded** form internally.  The quoting layer is responsible for
converting between the user-facing "raw" (decoded) representation and the
internal "wire" (percent-encoded) representation.

There are three distinct operations, each with its own set of quoters:

1. **Quote** (fresh encoding) – the input is a *raw, unencoded* string
   provided by the user.  Every character that is not in the safe set is
   percent-encoded.  ``%`` in the input is treated as a literal character
   and encoded to ``%25``.

   Used by: ``URL.build()``, ``with_*()`` modifier methods.

   Instances: ``QUOTER``, ``PATH_QUOTER``, ``QUERY_QUOTER``,
   ``QUERY_PART_QUOTER``, ``FRAGMENT_QUOTER`` (all with ``requote=False``).

2. **Requote** (normalisation) – the input is a URL string that *may already
   contain* percent-encoded sequences.  Existing ``%XX`` tokens are decoded,
   then the resulting character is compared against the safe/protected sets:

   * *safe* → the raw (decoded) character is emitted.
   * *protected* → the original ``%XX`` token is kept as-is.
   * *otherwise* → the character is re-encoded (possibly to a different form).

   Used by: ``URL(str)`` constructor (``encode_url``) for each component,
   because user-supplied URL strings may mix encoded and unencoded parts.

   Instances: ``REQUOTER``, ``PATH_REQUOTER``, ``QUERY_REQUOTER``,
   ``FRAGMENT_REQUOTER`` (all with ``requote=True``).

3. **Unquote** (decode) – the input is the internally stored percent-encoded
   form.  ``%XX`` tokens are decoded back to raw characters, subject to an
   ``unsafe`` list that prevents decoding of certain characters (e.g. ``+``
   in paths must stay as literal ``+`` rather than becoming a space).

   Used by: decoded accessor properties (``.user``, ``.path``,
   ``.query_string``, ``.fragment``, ``.parts``, etc.).

   Instances: ``UNQUOTER``, ``PATH_UNQUOTER``, ``PATH_SAFE_UNQUOTER``,
   ``QS_UNQUOTER``, ``UNQUOTER_PLUS``.

Display layer
-------------

``human_repr()`` operates on a fourth, separate path.  It starts from
*already-decoded* values and selectively re-encodes only the characters
that would break URL readability or parsing when displayed.  It uses
``human_quote()``, which encodes a caller-supplied ``unsafe`` set plus
non-printable characters.  This is purely a display concern and does not
participate in the internal encoding/decoding round-trip.

Quoter selection table
----------------------

+-------------+----------+--------------+-------------+---------------------+
| Component   | Quote    | Requote      | Unquote     | Safe / Protected    |
+=============+==========+==============+=============+=====================+
| user        | QUOTER   | REQUOTER     | UNQUOTER    | ``ALLOWED``         |
+-------------+----------+--------------+-------------+---------------------+
| password    | QUOTER   | REQUOTER     | UNQUOTER    | ``ALLOWED``         |
+-------------+----------+--------------+-------------+---------------------+
| path        | PATH_    | PATH_        | PATH_       | safe ``@:``         |
|             | QUOTER   | REQUOTER     | UNQUOTER    | prot ``/+``         |
+-------------+----------+--------------+-------------+---------------------+
| query       | QUERY_   | QUERY_       | QS_         | safe ``?/:@``       |
| (whole)     | QUOTER   | REQUOTER     | UNQUOTER    | prot ``=+&;``       |
+-------------+----------+--------------+-------------+---------------------+
| query       | QUERY_   | (N/A)        | (N/A)       | safe ``?/:@``       |
| (key/val)   | PART_    |              |             |                     |
|             | QUOTER   |              |             |                     |
+-------------+----------+--------------+-------------+---------------------+
| fragment    | FRAGMENT | FRAGMENT_    | UNQUOTER    | safe ``?/:@``       |
|             | _QUOTER  | REQUOTER     |             |                     |
+-------------+----------+--------------+-------------+---------------------+

References
----------
* RFC 3986 – Uniform Resource Identifier (URI): Generic Syntax
* RFC 6874 – Representing IPv6 Zone Identifiers in Address Literals
* https://url.spec.whatwg.org/
"""

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


def human_quote(s: str | None, unsafe: str) -> str | None:
    """Percent-encode *unsafe* characters in *s* for human-readable display.

    Unlike ``_Quoter`` this works on already-decoded values and only
    encodes the caller-specified ``unsafe`` set plus non-printable
    characters.  It is used exclusively by ``URL.human_repr()`` and
    does **not** participate in the internal storage round-trip.
    """
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)
