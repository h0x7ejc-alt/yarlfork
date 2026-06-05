from collections.abc import Callable
from functools import partial

import pytest

from yarl._quoters import (
    FRAGMENT_QUOTER,
    FRAGMENT_REQUOTER,
    PATH_QUOTER,
    PATH_REQUOTER,
    PATH_SAFE_UNQUOTER,
    PATH_UNQUOTER,
    QS_UNQUOTER,
    QUERY_PART_QUOTER,
    QUERY_QUOTER,
    QUERY_REQUOTER,
    QUOTER,
    REQUOTER,
    UNQUOTER,
    UNQUOTER_PLUS,
)
from yarl._quoting import _Quoter, _Unquoter


@pytest.mark.parametrize(
    ("quoter", "factory", "value"),
    [
        (QUOTER, partial(_Quoter, requote=False), "a b/c"),
        (REQUOTER, partial(_Quoter), "a b/c"),
        (
            PATH_QUOTER,
            partial(_Quoter, safe="@:", protected="/+", requote=False),
            "a/b+c:d@",
        ),
        (
            PATH_REQUOTER,
            partial(_Quoter, safe="@:", protected="/+"),
            "a/b+c:d@",
        ),
        (
            QUERY_QUOTER,
            partial(_Quoter, safe="?/:@", protected="=+&;", qs=True, requote=False),
            "a=1&b=2+3/c?d:e@f;",
        ),
        (
            QUERY_REQUOTER,
            partial(_Quoter, safe="?/:@", protected="=+&;", qs=True),
            "a=1&b=2+3/c?d:e@f;",
        ),
        (
            QUERY_PART_QUOTER,
            partial(_Quoter, safe="?/:@", qs=True, requote=False),
            "a=1&b=2+3",
        ),
        (FRAGMENT_QUOTER, partial(_Quoter, safe="?/:@", requote=False), "a/b?c:d@e"),
        (FRAGMENT_REQUOTER, partial(_Quoter, safe="?/:@"), "a/b?c:d@e"),
    ],
)
def test_module_quoters_match_explicit_configs(
    quoter: _Quoter,
    factory: Callable[[], _Quoter],
    value: str,
) -> None:
    assert quoter(value) == factory()(value)


@pytest.mark.parametrize(
    ("unquoter", "factory", "value"),
    [
        (UNQUOTER, partial(_Unquoter), "a%20b%2Fc"),
        (PATH_UNQUOTER, partial(_Unquoter, unsafe="+"), "/a+b%2Bc"),
        (
            PATH_SAFE_UNQUOTER,
            partial(_Unquoter, ignore="/%", unsafe="+"),
            "/a%2Fb%2520",
        ),
        (QS_UNQUOTER, partial(_Unquoter, qs=True), "a+b%2Bc%26d"),
        (UNQUOTER_PLUS, partial(_Unquoter, plus=True), "a+b"),
    ],
)
def test_module_unquoters_match_explicit_configs(
    unquoter: _Unquoter,
    factory: Callable[[], _Unquoter],
    value: str,
) -> None:
    assert unquoter(value) == factory()(value)
