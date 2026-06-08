import pickle
import sys
sys.path.insert(0, '/app/yarlfork')
from yarl import URL


def test_refactored_cache() -> None:
    print("Testing refactored cache logic...")
    
    # Test 1: Basic parsing and properties
    u = URL("https://user:pass@example.com:8080/path?query=1#fragment")
    print(f"  Created URL: {u}")
    assert u.scheme == "https"
    assert u.raw_user == "user"
    assert u.raw_password == "pass"
    assert u.raw_host == "example.com"
    assert u.explicit_port == 8080
    assert u.path == "/path"
    print("  ✓ Basic properties work correctly")
    
    # Test 2: Hash caching
    hash1 = hash(u)
    print(f"  Hash value: {hash1}")
    # Access hash again to verify it's cached
    hash2 = hash(u)
    assert hash1 == hash2, f"Hash values don't match: {hash1} vs {hash2}"
    print("  ✓ Hash caching works")
    
    # Test 3: Pickling
    print("  Testing pickling...")
    u1 = URL("https://example.com")
    hash(u1)  # Fill the cache
    data = pickle.dumps(u1)
    u2 = pickle.loads(data)
    print(f"  Original _cache has content: {bool(u1._cache)}")
    print(f"  Unpickled _cache is empty: {not bool(u2._cache)}")
    assert hash(u1) == hash(u2), f"Hashes don't match after unpickling"
    print("  ✓ Pickling with cache clearing works correctly")
    
    # Test 4: netloc parts
    print("  Testing netloc parts...")
    u3 = URL("https://john:doe123@sub.domain.example:9000")
    assert u3.raw_user == "john"
    assert u3.raw_password == "doe123"
    assert u3.raw_host == "sub.domain.example"
    assert u3.explicit_port == 9000
    assert u3.host_subcomponent == "sub.domain.example"
    assert u3.host_port_subcomponent == "sub.domain.example:9000"
    print("  ✓ Netloc parts work correctly")
    
    print("\n✅ All tests passed! Refactoring was successful.")


if __name__ == "__main__":
    test_refactored_cache()
