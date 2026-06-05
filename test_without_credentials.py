#!/usr/bin/env python3
"""Simple test script for without_credentials method"""

from yarl import URL

print("Testing without_credentials...")

# Test 1: Basic URL with username and password
url1 = URL("http://user:password@example.com:8888/path/to?a=1&b=2#fragment")
result1 = url1.without_credentials()
print(f"Test 1 - Original: {url1}")
print(f"Test 1 - Result:   {result1}")
assert result1 == URL("http://example.com:8888/path/to?a=1&b=2#fragment")
assert result1.user is None
assert result1.password is None
print("Test 1 passed!")
print()

# Test 2: Only username
url2 = URL("http://user@example.com:8888/path")
result2 = url2.without_credentials()
print(f"Test 2 - Original: {url2}")
print(f"Test 2 - Result:   {result2}")
assert result2 == URL("http://example.com:8888/path")
print("Test 2 passed!")
print()

# Test 3: IPv6
url3 = URL("http://user:password@[::1]:8888/path?a=1#frag")
result3 = url3.without_credentials()
print(f"Test 3 - Original: {url3}")
print(f"Test 3 - Result:   {result3}")
assert result3 == URL("http://[::1]:8888/path?a=1#frag")
print("Test 3 passed!")
print()

# Test 4: No credentials
url4 = URL("http://example.com:8888/path?a=1#frag")
result4 = url4.without_credentials()
print(f"Test 4 - Original: {url4}")
print(f"Test 4 - Result:   {result4}")
assert result4 is url4
print("Test 4 passed!")
print()

# Test 5: Default port
url5 = URL("http://user:password@example.com:80/path")
result5 = url5.without_credentials()
print(f"Test 5 - Original: {url5}")
print(f"Test 5 - Result:   {result5}")
assert result5 == URL("http://example.com/path")
print("Test 5 passed!")
print()

print("All tests passed!")
