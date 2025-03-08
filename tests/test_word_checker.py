import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.word_checker import normalize_text, word_exists

def test_normalize_text():
    text = "Hello, world! 123"
    normalized = normalize_text(text)
    # Check that numbers are normalized
    assert "123" in normalized
    # For English, the text should remain mostly unchanged
    assert "Hello, world!" in normalized or "Hello, world!" in normalized.strip()

def test_word_exists_positive():
    assert word_exists("keyword", "This sentence contains keyword")

def test_word_exists_negative():
    assert not word_exists("nonexistent", "This sentence contains keyword")
