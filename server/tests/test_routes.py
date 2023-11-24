import json
from unittest.mock import Mock, patch

import pytest
from app import app as application
from dotenv import load_dotenv

load_dotenv("/home/laudanum/projects/toniebox-audio-match/.env")

# Mock the `get_item_from_request` and `g.tonie_api_client.get_tonie_content` functions
# if they involve network calls or other side-effects you don't want in tests.

mock_tonie1 = Mock(id="tonie_1")
mock_tonie2 = Mock(id="tonie_2")

def mock_get_item_from_request(*args, **kwargs):
    if "valid_tonie" in args[0]["tonie_id"]:
        return ["valid_tonie"]
    return ["some_mocked_tonie_id_1", "some_mocked_tonie_id_2"]

@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client

def test_tonie_overview_invalid_tonie(client):
    payload = json.dumps({"tonie_id": "invalid_tonie"})
    rv = client.post("/tonie_overview", data=payload, content_type="application/json")
    assert rv.status_code == 400
    assert rv.json["status"] == "failure"
    assert rv.json["message"] == "No matching tonie found"

def test_tonie_overview_multiple_tonies(client):
    mock_tonie1_dict = {'id': 'tonie_1', 'some_other_attribute': 'value1'}
    mock_tonie2_dict = {'id': 'tonie_2', 'some_other_attribute': 'value2'}
    payload = json.dumps({"tonie_id": [mock_tonie1_dict, mock_tonie2_dict]})

    with patch('app.get_item_from_request', side_effect=mock_get_item_from_request):
        rv = client.post("/tonie_overview", data=payload, content_type="application/json")
        assert rv.status_code == 400
        assert rv.json["status"] == "failure"
        assert rv.json["message"] == "Multiple tonies provided, can only handle one"

def test_tonie_overview_valid_tonie(client):
    payload = json.dumps({"tonie_id": "valid_tonie"})    
    with application.app_context(): 
        with patch('app.get_item_from_request', side_effect=mock_get_item_from_request):
            with patch('toniecloud.client.TonieCloud.get_tonie_content', Mock(return_value="test")):
                rv = client.post("/tonie_overview", data=payload, content_type="application/json")
                assert rv.status_code == 200
                assert rv.json["status"] == "success"
                assert "tracks" in rv.json
