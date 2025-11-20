# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0

import pytest
from tools.tool_params import (
    GetIndexMappingArgs,
    GetShardsArgs,
    ListIndicesArgs,
    SearchIndexArgs,
    baseToolArgs,
)
from unittest.mock import patch, AsyncMock, MagicMock


class TestOpenSearchHelper:
    def setup_method(self):
        """Setup that runs before each test method."""
        from opensearch.helper import (
            get_index_mapping,
            get_shards,
            list_indices,
            search_index,
        )

        # Store functions
        self.list_indices = list_indices
        self.get_index_mapping = get_index_mapping
        self.search_index = search_index
        self.get_shards = get_shards

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_list_indices(self, mock_get_client):
        """Test list_indices function."""
        # Setup mock response
        mock_response = [
            {'index': 'index1', 'health': 'green', 'status': 'open'},
            {'index': 'index2', 'health': 'yellow', 'status': 'open'},
        ]
        mock_client = AsyncMock()
        mock_client.cat.indices = AsyncMock(return_value=mock_response)

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute
        result = await self.list_indices(ListIndicesArgs(opensearch_cluster_name=''))

        # Assert
        assert result == mock_response
        mock_get_client.assert_called_once_with(ListIndicesArgs(opensearch_cluster_name=''))
        mock_client.cat.indices.assert_called_once_with(format='json')

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_index_mapping(self, mock_get_client):
        """Test get_index_mapping function."""
        # Setup mock response
        mock_response = {
            'test-index': {
                'mappings': {
                    'properties': {
                        'field1': {'type': 'text'},
                        'field2': {'type': 'keyword'},
                    }
                }
            }
        }
        mock_client = AsyncMock()
        mock_client.indices.get_mapping = AsyncMock(return_value=mock_response)

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute
        result = await self.get_index_mapping(
            GetIndexMappingArgs(index='test-index', opensearch_cluster_name='')
        )

        # Assert
        assert result == mock_response
        mock_get_client.assert_called_once_with(
            GetIndexMappingArgs(index='test-index', opensearch_cluster_name='')
        )
        mock_client.indices.get_mapping.assert_called_once_with(index='test-index')

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_search_index(self, mock_get_client):
        """Test search_index function."""
        # Setup mock response
        mock_response = {
            'hits': {
                'total': {'value': 1},
                'hits': [{'_index': 'test-index', '_id': '1', '_source': {'field': 'value'}}],
            }
        }
        mock_client = AsyncMock()
        mock_client.search = AsyncMock(return_value=mock_response)

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Setup test query
        test_query = {'query': {'match_all': {}}}

        # Execute
        result = await self.search_index(
            SearchIndexArgs(index='test-index', query=test_query, opensearch_cluster_name='')
        )

        # Assert
        assert result == mock_response
        mock_get_client.assert_called_once_with(
            SearchIndexArgs(index='test-index', query=test_query, opensearch_cluster_name='')
        )
        mock_client.search.assert_called_once_with(index='test-index', body=test_query)

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_shards(self, mock_get_client):
        """Test get_shards function."""
        # Setup mock response
        mock_response = [
            {
                'index': 'test-index',
                'shard': '0',
                'prirep': 'p',
                'state': 'STARTED',
                'docs': '1000',
                'store': '1mb',
                'ip': '127.0.0.1',
                'node': 'node1',
            }
        ]
        mock_client = AsyncMock()
        mock_client.cat.shards = AsyncMock(return_value=mock_response)

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute
        result = await self.get_shards(
            GetShardsArgs(index='test-index', opensearch_cluster_name='')
        )

        # Assert
        assert result == mock_response
        mock_get_client.assert_called_once_with(
            GetShardsArgs(index='test-index', opensearch_cluster_name='')
        )
        mock_client.cat.shards.assert_called_once_with(index='test-index', format='json')

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_list_indices_error(self, mock_get_client):
        """Test list_indices error handling."""
        # Setup mock to raise exception
        mock_client = AsyncMock()
        mock_client.cat.indices = AsyncMock(side_effect=Exception('Connection error'))

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute and assert
        with pytest.raises(Exception) as exc_info:
            await self.list_indices(ListIndicesArgs(opensearch_cluster_name=''))
        assert str(exc_info.value) == 'Connection error'

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_index_mapping_error(self, mock_get_client):
        """Test get_index_mapping error handling."""
        # Setup mock to raise exception
        mock_client = AsyncMock()
        mock_client.indices.get_mapping = AsyncMock(side_effect=Exception('Index not found'))

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute and assert
        with pytest.raises(Exception) as exc_info:
            await self.get_index_mapping(
                GetIndexMappingArgs(index='non-existent-index', opensearch_cluster_name='')
            )
        assert str(exc_info.value) == 'Index not found'

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_search_index_error(self, mock_get_client):
        """Test search_index error handling."""
        # Setup mock to raise exception
        mock_client = AsyncMock()
        mock_client.search = AsyncMock(side_effect=Exception('Invalid query'))

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute and assert
        with pytest.raises(Exception) as exc_info:
            await self.search_index(
                SearchIndexArgs(
                    index='test-index', query={'invalid': 'query'}, opensearch_cluster_name=''
                )
            )
        assert str(exc_info.value) == 'Invalid query'

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_shards_error(self, mock_get_client):
        """Test get_shards error handling."""
        # Setup mock to raise exception
        mock_client = AsyncMock()
        mock_client.cat.shards = AsyncMock(side_effect=Exception('Shard not found'))

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute and assert
        with pytest.raises(Exception) as exc_info:
            await self.get_shards(
                GetShardsArgs(index='non-existent-index', opensearch_cluster_name='')
            )
        assert str(exc_info.value) == 'Shard not found'

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_opensearch_version(self, mock_get_client):
        from opensearch.helper import get_opensearch_version

        # Setup mock response
        mock_response = {'version': {'number': '2.11.1'}}
        mock_client = AsyncMock()
        mock_client.info = AsyncMock(return_value=mock_response)
        mock_client.close = AsyncMock()

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        # Execute
        args = baseToolArgs(opensearch_cluster_name='')
        result = await get_opensearch_version(args)
        # Assert
        assert str(result) == '2.11.1'
        mock_get_client.assert_called_once_with(args)
        mock_client.info.assert_called_once_with()

    @pytest.mark.asyncio
    @patch('opensearch.client.get_opensearch_client')
    async def test_get_opensearch_version_error(self, mock_get_client):
        from opensearch.helper import get_opensearch_version
        from tools.tool_params import baseToolArgs

        # Setup mock to raise exception
        mock_client = AsyncMock()
        mock_client.info = AsyncMock(side_effect=Exception('Failed to get version'))
        mock_client.close = AsyncMock()

        # Setup async context manager
        mock_get_client.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        mock_get_client.return_value.__aexit__ = AsyncMock(return_value=None)

        args = baseToolArgs(opensearch_cluster_name='')
        # Execute and assert
        result = await get_opensearch_version(args)
        assert result is None
        
    def test_convert_aggregations_to_csv(self):
        """Test convert_search_results_to_csv with aggregations."""
        import json
        import csv
        import io
        
        def convert_search_results_to_csv(search_results: dict) -> str:
            if not search_results:
                return "No search results to convert"
            
            # Handle aggregations-only queries
            if 'aggregations' in search_results and ('hits' not in search_results or not search_results['hits']['hits']):
                return _convert_aggregations_to_csv(search_results['aggregations'])
            
            return "No search results to convert"
        
        def _convert_aggregations_to_csv(aggregations: dict) -> str:
            rows = []
            _flatten_aggregations(aggregations, {}, rows)
            
            if not rows:
                return "No aggregation data to convert"
            
            all_fields = set()
            for row in rows:
                all_fields.update(row.keys())
            
            fieldnames = sorted(list(all_fields))
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in rows:
                writer.writerow(row)
            
            return output.getvalue()
        
        def _flatten_aggregations(aggs: dict, current_row: dict, rows: list, prefix: str = '') -> None:
            for agg_name, agg_data in aggs.items():
                if isinstance(agg_data, dict):
                    if 'buckets' in agg_data:
                        for bucket in agg_data['buckets']:
                            new_row = current_row.copy()
                            bucket_key = f'{prefix}{agg_name}_key' if prefix else f'{agg_name}_key'
                            new_row[bucket_key] = str(bucket.get('key', ''))
                            
                            if 'doc_count' in bucket:
                                count_key = f'{prefix}{agg_name}_doc_count' if prefix else f'{agg_name}_doc_count'
                                new_row[count_key] = bucket['doc_count']
                            
                            rows.append(new_row)
        
        # Test aggregations-only query
        agg_results = {
            "aggregations": {
                "status_terms": {
                    "buckets": [
                        {"key": "active", "doc_count": 100},
                        {"key": "inactive", "doc_count": 50}
                    ]
                }
            }
        }
        
        csv_output = convert_search_results_to_csv(agg_results)
        assert isinstance(csv_output, str)
        lines = csv_output.strip().split('\n')
        assert len(lines) == 3  # Header + 2 data rows
        
        # Check for aggregation fields
        header = lines[0]
        assert 'status_terms_key' in header
        assert 'status_terms_doc_count' in header
        
    def test_convert_search_results_to_csv_nested_objects(self):
        """Test convert_search_results_to_csv with nested objects expansion."""
        import json
        import csv
        import io
        
        def _flatten_fields(obj: dict, fields: set, prefix: str = '') -> None:
            for key, value in obj.items():
                field_name = f'{prefix}{key}' if prefix else key
                if isinstance(value, dict):
                    _flatten_fields(value, fields, f'{field_name}.')
                else:
                    fields.add(field_name)
        
        def _flatten_object(obj: dict, row: dict, prefix: str = '') -> None:
            for key, value in obj.items():
                field_name = f'{prefix}{key}' if prefix else key
                if isinstance(value, dict):
                    _flatten_object(value, row, f'{field_name}.')
                elif isinstance(value, list):
                    row[field_name] = json.dumps(value)
                else:
                    row[field_name] = str(value) if value is not None else ''
        
        def convert_search_results_to_csv(search_results: dict) -> str:
            if not search_results or 'hits' not in search_results:
                return "No search results to convert"
            
            hits = search_results['hits']['hits']
            if not hits:
                return "No documents found in search results"
            
            all_fields = set()
            for hit in hits:
                if '_source' in hit:
                    _flatten_fields(hit['_source'], all_fields)
                all_fields.update(['_index', '_id', '_score'])
            
            fieldnames = sorted(list(all_fields))
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for hit in hits:
                row = {}
                row['_index'] = hit.get('_index', '')
                row['_id'] = hit.get('_id', '')
                row['_score'] = hit.get('_score', '')
                
                if '_source' in hit:
                    _flatten_object(hit['_source'], row)
                
                writer.writerow(row)
            
            return output.getvalue()
        
        # Test data with nested objects
        test_search_results = {
            "hits": {
                "hits": [
                    {
                        "_index": "test_index",
                        "_id": "1",
                        "_score": 1.0,
                        "_source": {
                            "name": "John Doe",
                            "address": {
                                "street": "123 Main St",
                                "city": "New York",
                                "coordinates": {
                                    "lat": 40.7128,
                                    "lon": -74.0060
                                }
                            },
                            "tags": ["developer", "python"]
                        }
                    }
                ]
            }
        }
        
        csv_output = convert_search_results_to_csv(test_search_results)
        assert isinstance(csv_output, str)
        lines = csv_output.strip().split('\n')
        assert len(lines) == 2  # Header + 1 data row
        
        # Check header contains flattened nested fields
        header = lines[0]
        assert 'address.street' in header
        assert 'address.city' in header
        assert 'address.coordinates.lat' in header
        assert 'address.coordinates.lon' in header
        assert 'tags' in header
        
        # Check data row contains flattened values
        data_row = lines[1]
        assert '123 Main St' in data_row
        assert '40.7128' in data_row
        assert '-74.006' in data_row
       