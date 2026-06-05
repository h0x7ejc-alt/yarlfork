"""Quoting and unquoting utilities for URL parts."""

from urllib.parse import quote
from typing import TYPE_CHECKING

from ._quoting import _Quoter, _Unquoter

# 配置化定义所有 quoter 和 unquoter 实例，便于维护
_QUOTER_CONFIGS = {
    "QUOTER": {"requote": False},
    "REQUOTER": {},
    "PATH_QUOTER": {"safe": "@:", "protected": "/+", "requote": False},
    "PATH_REQUOTER": {"safe": "@:", "protected": "/+"},
    "QUERY_QUOTER": {
        "safe": "?/:@",
        "protected": "=+&;",
        "qs": True,
        "requote": False,
    },
    "QUERY_REQUOTER": {"safe": "?/:@", "protected": "=+&;", "qs": True},
    "QUERY_PART_QUOTER": {"safe": "?/:@", "qs": True, "requote": False},
    "FRAGMENT_QUOTER": {"safe": "?/:@", "requote": False},
    "FRAGMENT_REQUOTER": {"safe": "?/:@"},
}

_UNQUOTER_CONFIGS = {
    "UNQUOTER": {},
    "PATH_UNQUOTER": {"unsafe": "+"},
    "PATH_SAFE_UNQUOTER": {"ignore": "/%", "unsafe": "+"},
    "QS_UNQUOTER": {"qs": True},
    "UNQUOTER_PLUS": {"plus": True},  # to match urllib.parse.unquote_plus
}

# 动态创建所有 quoter 实例
for _name, _kwargs in _QUOTER_CONFIGS.items():
    globals()[_name] = _Quoter(**_kwargs)

# 动态创建所有 unquoter 实例
for _name, _kwargs in _UNQUOTER_CONFIGS.items():
    globals()[_name] = _Unquoter(**_kwargs)


def human_quote(s: str | None, unsafe: str) -> str | None:
    if not s:
        return s
    for c in "%" + unsafe:
        if c in s:
            s = s.replace(c, f"%{ord(c):02X}")
    if s.isprintable():
        return s
    return "".join(c if c.isprintable() else quote(c) for c in s)


# 类型注解声明，用于静态类型检查器（如 mypy）
if TYPE_CHECKING:
    # Quoters
    QUOTER: _Quoter
    REQUOTER: _Quoter
    PATH_QUOTER: _Quoter
    PATH_REQUOTER: _Quoter
    QUERY_QUOTER: _Quoter
    QUERY_REQUOTER: _Quoter
    QUERY_PART_QUOTER: _Quoter
    FRAGMENT_QUOTER: _Quoter
    FRAGMENT_REQUOTER: _Quoter

    # Unquoters
    UNQUOTER: _Unquoter
    PATH_UNQUOTER: _Unquoter
    PATH_SAFE_UNQUOTER: _Unquoter
    QS_UNQUOTER: _Unquoter
    UNQUOTER_PLUS: _Unquoter
