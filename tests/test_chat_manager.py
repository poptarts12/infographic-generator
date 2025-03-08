import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import subprocess
import pytest
from PIL import Image
from chat_manager import ChatManager

def test_chat_manager_status_and_result():
    cm = ChatManager()
    job_id = "test_job"
    assert cm.get_status(job_id) == "Job not found"
    cm.jobs[job_id] = "completed"
    cm.job_results[job_id] = {
        "hebrew": "dummy",
        "arabic": "dummy",
        "english": "dummy",
        "russian": "dummy"
    }
    status = cm.get_status(job_id)
    result = cm.get_result(job_id)
    assert status == "completed"
    assert result is not None
    assert all(lang in result for lang in ["hebrew", "arabic", "english", "russian"])

def test_convert_to_svg_failure(monkeypatch, tmp_path):
    cm = ChatManager()
    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0], "simulated error")
    monkeypatch.setattr(subprocess, "run", fake_run)
    input_file = str(tmp_path / "dummy_input.png")
    output_file = str(tmp_path / "dummy_output.svg")
    Image.new("RGB", (100, 100), color="white").save(input_file)
    with pytest.raises(subprocess.CalledProcessError):
        cm.convert_to_svg(input_file, output_file)

def test_chat_manager_process_job_integration(tmp_path, monkeypatch):
    from chat_manager import ChatManager, clean_json
    from core.infographic_maker import InfographicGenerator

    cm = ChatManager()
    job_id = "integration_test"
    
    # Dummy response classes
    class DummyResponse:
        def __init__(self, text):
            self.text = text

    class DummyModel:
        def __init__(self, response_text):
            self.response_text = response_text
        def send(self, text):
            return DummyResponse(self.response_text)
    
    # Set dummy responses for NLP and translator models
    valid_nlp_response = '{"title": {"text": "Safe"}, "subtitle": {"text": "Instructions"}, "body": [{"text": "Step 1"}], "words_to_mark": ["safe"]}'
    cm.nlp_model.model = DummyModel(valid_nlp_response)
    valid_trans_response = '{"arabic": {"title": {"text": "عنوان"}}, "english": {"title": {"text": "Title"}}, "russian": {"title": {"text": "Заголовок"}}}'
    cm.translator.model = DummyModel(valid_trans_response)
    
    # Bypass file-based operations:
    monkeypatch.setattr(cm, "convert_to_svg", lambda inp, out: None)
    monkeypatch.setattr(InfographicGenerator, "create_infographic", lambda self, output_path, text_data: None)
    
    result = cm.process_job(job_id, "dummy text")
    assert result is True
    assert cm.get_status(job_id) == "completed"
    job_result = cm.get_result(job_id)
    assert job_result is not None
    assert all(lang in job_result for lang in ["hebrew", "arabic", "english", "russian"])
