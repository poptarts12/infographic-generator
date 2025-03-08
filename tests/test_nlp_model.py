import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from models.text_processing import NLP_model

class DummyResponse:
    def __init__(self, text):
        self.text = text

class DummyModel:
    def __init__(self, response_text):
        self.response_text = response_text
    def send(self, text):
        return DummyResponse(self.response_text)

@pytest.fixture
def nlp_model_instance():
    return NLP_model()

def test_nlp_empty_response(nlp_model_instance):
    nlp_model_instance.model = DummyModel("")
    result = nlp_model_instance.NLP_procces("some text")
    assert result["status"] == 0
    assert "Empty response" in result["message"]

def test_nlp_false_response(nlp_model_instance):
    nlp_model_instance.model = DummyModel("False")
    result = nlp_model_instance.NLP_procces("some text")
    assert result["status"] == 0
    assert "Client Error" in result["message"]

def test_nlp_information_false_response(nlp_model_instance):
    nlp_model_instance.model = DummyModel("Information False")
    result = nlp_model_instance.NLP_procces("some text")
    assert result["status"] == 0
    assert "Client Error" in result["message"]

def test_nlp_fjson_response(nlp_model_instance):
    nlp_model_instance.model = DummyModel("Fjson")
    result = nlp_model_instance.NLP_procces("some text")
    assert result["status"] == 0
    assert "problem with json" in result["message"]

def test_nlp_valid_response(nlp_model_instance):
    valid_text = '{"title": {"text": "Safe"}, "subtitle": {"text": "Instructions"}, "body": [{"text": "Step 1"}], "words_to_mark": ["safe"]}'
    nlp_model_instance.model = DummyModel(valid_text)
    result = nlp_model_instance.NLP_procces("some text")
    assert result["status"] == 1
    assert result["message"] == valid_text
