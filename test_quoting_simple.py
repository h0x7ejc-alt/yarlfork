#!/usr/bin/env python3
"""Simple test script to verify that quoting functionality still works."""

import sys
sys.path.insert(0, '/app/yarlfork')

from yarl import URL
from yarl._quoters import (
    QUOTER, REQUOTER,
    PATH_QUOTER, PATH_REQUOTER,
    QUERY_QUOTER, QUERY_REQUOTER,
    FRAGMENT_QUOTER, FRAGMENT_REQUOTER,
    UNQUOTER, PATH_UNQUOTER, QS_UNQUOTER
)

print("Testing quoters...")

# Test basic quoting
test_str = "hello world!@#$%^&*()"
quoted = QUOTER(test_str)
print(f"  QUOTER('{test_str}') = '{quoted}'")

# Test requoting with existing %XX
requote_str = "test%20space%zzinvalid"
requoted = REQUOTER(requote_str)
print(f"  REQUOTER('{requote_str}') = '{requoted}'")

# Test URL construction
url1 = URL.build(scheme="https", host="example.com", path="/test path", query={"q": "search query"})
print(f"  URL.build() = {url1}")

# Test URL parsing
url2 = URL("https://example.com/test%20path?q=search%20query")
print(f"  URL() parsed = {url2}")
print(f"  url2.path = {url2.path}")

# Test update_query
url3 = url2.update_query({"new": "param value"})
print(f"  update_query() = {url3}")

# Test human_repr
print(f"  human_repr() = {url3.human_repr()}")

print("\nAll tests completed successfully!")