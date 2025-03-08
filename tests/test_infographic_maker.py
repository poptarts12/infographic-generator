import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PIL import Image, ImageDraw, ImageFont
from core.infographic_maker import InfographicGenerator

def test_remove_punctuation():
    generator = InfographicGenerator(lang="english")
    result = generator.remove_punctuation("Hello, world!")
    assert result == "Hello world"

def test_letter_reversal_non_rtl():
    generator = InfographicGenerator(lang="english")
    text = "Hello world"
    result = generator.letter_reversal(text)
    assert result == text

def test_wrap_text():
    generator = InfographicGenerator(lang="english")
    # Create a dummy image and drawing context
    img = Image.new("RGB", (300, 200))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text = "This is a test sentence to check text wrapping functionality."
    lines = generator.wrap_text(draw, text, font, max_width=100)
    assert isinstance(lines, list)
    assert len(lines) > 0

def test_create_infographic(tmp_path):
    # Create a dummy template image
    dummy_template = tmp_path / "dummy_template.png"
    img = Image.new("RGB", (400, 400), color="white")
    img.save(dummy_template)
    generator = InfographicGenerator(lang="english")
    generator.template_path = str(dummy_template)
    text_data = {
        "title": {"text": "Test Title"},
        "subtitle": {"text": "Test Subtitle"},
        "body": [{"text": "Test body sentence."}],
        "words_to_mark": ["Test"]
    }
    output_file = tmp_path / "test_output.png"
    generator.create_infographic(str(output_file), text_data)
    assert output_file.exists()
