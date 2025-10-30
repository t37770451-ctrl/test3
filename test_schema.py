#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.skills_tools import LogPatternAnalysisToolArgs, DataDistributionToolArgs
import json

print("=== LogPatternAnalysisToolArgs Schema ===")
schema = LogPatternAnalysisToolArgs.model_json_schema()
print(json.dumps(schema, indent=2))
print(f"\nRequired fields: {schema.get('required', [])}")

print("\n=== DataDistributionToolArgs Schema ===")
schema2 = DataDistributionToolArgs.model_json_schema()
print(json.dumps(schema2, indent=2))
print(f"\nRequired fields: {schema2.get('required', [])}")