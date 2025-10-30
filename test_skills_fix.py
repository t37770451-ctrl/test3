#!/usr/bin/env python3
"""
测试脚本：验证skills tools的timeField参数修复
"""

import json
from src.tools.skills_tools import DataDistributionToolArgs, LogPatternAnalysisToolArgs

def test_default_values():
    """测试默认值是否正确设置"""
    
    # 测试DataDistributionTool
    data_args = DataDistributionToolArgs(
        index="test-index",
        selectionTimeRangeStart="2024-01-01T00:00:00Z",
        selectionTimeRangeEnd="2024-01-02T00:00:00Z"
    )
    
    print("DataDistributionTool 默认值测试:")
    print(f"  timeField: {data_args.timeField}")
    assert data_args.timeField == "@timestamp", f"Expected '@timestamp', got '{data_args.timeField}'"
    
    # 测试LogPatternAnalysisTool
    log_args = LogPatternAnalysisToolArgs(
        index="log-index",
        logFieldName="message",
        selectionTimeRangeStart="2024-01-01T00:00:00Z",
        selectionTimeRangeEnd="2024-01-02T00:00:00Z"
    )
    
    print("LogPatternAnalysisTool 默认值测试:")
    print(f"  timeField: {log_args.timeField}")
    assert log_args.timeField == "@timestamp", f"Expected '@timestamp', got '{log_args.timeField}'"

def test_json_schema():
    """测试JSON schema是否包含默认值"""
    
    # 测试DataDistributionTool schema
    data_schema = DataDistributionToolArgs.model_json_schema()
    time_field_schema = data_schema['properties']['timeField']
    
    print("\nDataDistributionTool JSON Schema:")
    print(f"  timeField default: {time_field_schema.get('default', 'NOT SET')}")
    assert time_field_schema.get('default') == "@timestamp", "timeField should have default value '@timestamp'"
    
    # 测试LogPatternAnalysisTool schema
    log_schema = LogPatternAnalysisToolArgs.model_json_schema()
    time_field_schema = log_schema['properties']['timeField']
    
    print("LogPatternAnalysisTool JSON Schema:")
    print(f"  timeField default: {time_field_schema.get('default', 'NOT SET')}")
    assert time_field_schema.get('default') == "@timestamp", "timeField should have default value '@timestamp'"

def test_custom_time_field():
    """测试自定义timeField值"""
    
    # 测试自定义timeField
    custom_args = DataDistributionToolArgs(
        index="test-index",
        selectionTimeRangeStart="2024-01-01T00:00:00Z",
        selectionTimeRangeEnd="2024-01-02T00:00:00Z",
        timeField="custom_timestamp"
    )
    
    print("\n自定义timeField测试:")
    print(f"  timeField: {custom_args.timeField}")
    assert custom_args.timeField == "custom_timestamp", f"Expected 'custom_timestamp', got '{custom_args.timeField}'"

if __name__ == "__main__":
    print("开始测试skills tools的timeField修复...")
    
    try:
        test_default_values()
        test_json_schema()
        test_custom_time_field()
        
        print("\n✅ 所有测试通过！timeField问题已修复。")
        print("\n修复总结:")
        print("1. timeField现在有默认值'@timestamp'")
        print("2. agent不再需要显式提供timeField参数")
        print("3. 用户仍可以自定义timeField值")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        exit(1)