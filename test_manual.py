#!/usr/bin/env python
"""手动测试新功能的脚本"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from yarl import URL


def test_has_query_param():
    print("测试 has_query_param() 方法:")
    
    # 测试空查询
    url1 = URL("http://example.com")
    assert not url1.has_query_param("a")
    print("  ✓ 空查询: 正确返回 False")
    
    # 测试存在单个键
    url2 = URL("http://example.com?a=1")
    assert url2.has_query_param("a")
    assert not url2.has_query_param("b")
    print("  ✓ 单个键存在: 正确返回 True")
    
    # 测试多个键
    url3 = URL("http://example.com?a=1&b=2")
    assert url3.has_query_param("a")
    assert url3.has_query_param("b")
    assert not url3.has_query_param("c")
    print("  ✓ 多个键存在: 正确返回 True")
    
    # 测试重复键
    url4 = URL("http://example.com?a=1&a=2")
    assert url4.has_query_param("a")
    print("  ✓ 重复键存在: 正确返回 True")
    
    print("✓ has_query_param() 测试全部通过!\n")


def test_has_multiple_query_values():
    print("测试 has_multiple_query_values() 方法:")
    
    # 测试空查询
    url1 = URL("http://example.com")
    assert not url1.has_multiple_query_values("a")
    print("  ✓ 空查询: 正确返回 False")
    
    # 测试单个值
    url2 = URL("http://example.com?a=1")
    assert not url2.has_multiple_query_values("a")
    print("  ✓ 单个值: 正确返回 False")
    
    # 测试多个值
    url3 = URL("http://example.com?a=1&a=2")
    assert url3.has_multiple_query_values("a")
    print("  ✓ 多个值: 正确返回 True")
    
    # 测试多个值和其他键
    url4 = URL("http://example.com?a=1&b=2&a=3")
    assert url4.has_multiple_query_values("a")
    assert not url4.has_multiple_query_values("b")
    print("  ✓ 混合情况: 正确返回结果")
    
    # 测试三个值
    url5 = URL("http://example.com?a=1&a=2&a=3")
    assert url5.has_multiple_query_values("a")
    print("  ✓ 三个值: 正确返回 True")
    
    print("✓ has_multiple_query_values() 测试全部通过!\n")


if __name__ == "__main__":
    print("开始手动测试新的 URL 查询参数功能...\n")
    test_has_query_param()
    test_has_multiple_query_values()
    print("✅ 所有测试通过！新功能工作正常！")
