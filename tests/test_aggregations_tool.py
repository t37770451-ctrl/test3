import json, os, sys, asyncio, pytest
from pathlib import Path

# Make "src" importable when running tests from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from tools.tool_params import AggregationsArgs
from tools.tools import aggregations_tool
import opensearch.helper as helper


class FakeClient:
    def search(self, index, body, request_timeout=None):
        assert body['size'] == 0
        assert 'aggs' in body
        return {
            'took': 42,
            'timed_out': False,
            '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
            'hits': {'max_score': None, 'hits': []},
            'aggregations': {'by_status': {'buckets': [{'key': '200', 'doc_count': 2}]}},
        }


@pytest.mark.asyncio
async def test_aggregations_tool_trimmed(monkeypatch):
    monkeypatch.setattr(helper, 'get_client', lambda: FakeClient())

    args = AggregationsArgs(
        index='logs',
        aggs={'by_status': {'terms': {'field': 'status', 'size': 5}}},
        timeout='5s',
        raw=False,
    )
    out = await aggregations_tool(args)
    data = json.loads(out[0]['text'])
    assert 'took_ms' in data and data['timed_out'] is False
    assert 'aggregations' in data


@pytest.mark.asyncio
async def test_aggregations_tool_raw(monkeypatch):
    monkeypatch.setattr(helper, 'get_client', lambda: FakeClient())

    args = AggregationsArgs(
        index='logs',
        aggs={'by_status': {'terms': {'field': 'status', 'size': 5}}},
        timeout='5s',
        raw=True,
    )
    out = await aggregations_tool(args)
    data = json.loads(out[0]['text'])
    assert 'took' in data and 'aggregations' in data
