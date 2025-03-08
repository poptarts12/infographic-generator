import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from models.translation import translator_model

class DummyResponse:
    def __init__(self, text):
        self.text = text

class DummyModel:
    def __init__(self, response_text):
        self.response_text = response_text
    def send(self, text):
        return DummyResponse(self.response_text)

@pytest.fixture
def translator_model_instance():
    return translator_model()

def test_translator_empty_response(translator_model_instance):
    translator_model_instance.model = DummyModel("")
    result = translator_model_instance.translation_procces("some text")
    assert result["status"] == 0
    assert "Empty response" in result["message"]

def test_translator_valid_response(translator_model_instance):
    valid_text = '{"arabic": {"title": {"text": "عنوان"}}, "english": {"title": {"text": "Title"}}, "russian": {"title": {"text": "Заголовок"}}}'
    translator_model_instance.model = DummyModel(valid_text)
    result = translator_model_instance.translation_procces("some text")
    assert result["status"] == 1
    assert result["message"] == valid_text
