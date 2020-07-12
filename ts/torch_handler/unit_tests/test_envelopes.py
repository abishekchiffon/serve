# pylint: disable=W0621
# Using the same name as global function is part of pytest
"""
Basic unit test for BaseHandler class.
Ensures it can load and execute an example model
"""

import sys
import pytest
from ts.torch_handler.base_handler import BaseHandler
from ts.torch_handler.request_envelope.body import BodyEnvelope
from ts.torch_handler.request_envelope.json import JSONEnvelope
from .test_utils.mock_context import MockContext

sys.path.append('ts/torch_handler/unit_tests/models/tmp')

@pytest.fixture()
def handle_fn():
    ctx = MockContext()
    handler = BaseHandler()
    handler.initialize(ctx)

    return handler.handle

def test_json(handle_fn):
    test_data = [{'body':{
        'instances': [[1.0, 2.0]]
    }}]
    expected_result = ['{"predictions": [1]}']

    envelope = JSONEnvelope(handle_fn)
    results = envelope.handle(test_data, None)
    assert(results == expected_result)

def test_body(handle_fn):
    test_data = [{
        'body':[1.0, 2.0]
    }]
    expected_result = [1]

    envelope = BodyEnvelope(handle_fn)
    results = envelope.handle(test_data, None)
    assert(results == expected_result)

def test_binary():
    test_data = [{
        'instances': [{'b64': 'YQ=='}]
    }]

    envelope = JSONEnvelope(lambda x,y: [row.decode('utf-8') for row in x])
    results = envelope.handle(test_data, None)
    assert(results = ['{"predictions": ["a"]}'])
