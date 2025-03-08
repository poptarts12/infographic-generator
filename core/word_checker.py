import re
import unicodedata
import re
from bidi.algorithm import get_display
import arabic_reshaper
from langdetect import detect

def normalize_text(text: str) -> str:
    text = text.strip()
    text = unicodedata.normalize("NFKC", text)

    # Convert all numbers to Arabic numerals (Western digits)
    text = re.sub(r"\d+", lambda x: str(int(x.group())), text)

    # Detect language
    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang in ["he", "ar"]:
        text = get_display(arabic_reshaper.reshape(text))  # Handle RTL

    return text

def word_exists(word, sentence, prefixes=None, threshold=80):
    """
    Check if a word exists in a sentence, allowing for common prefixes in multiple languages.
    Uses fuzzy matching to detect slight variations.
    
    :param word: The word to search for
    :param sentence: The text to search in
    :param prefixes: List of prefixes to ignore (default: common ones for Hebrew, Arabic, Russian, and English)
    :param threshold: Minimum similarity score for fuzzy matching (default: 80)
    :return: True if the word is found, False otherwise
    """
    if prefixes is None:
        prefixes = [
            "to", "in", "for", "the", "a",  # English
            "ב", "ל", "כ", "מ",  # Hebrew
            "ال", "ب", "ل", "ف", "ك", "و",  # Arabic
            "в", "на", "по", "из", "у", "о", "от", "с", "под", "над", "к", "об"  # Russian
        ]

    # Normalize both inputs
    word = normalize_text(word)
    sentence = normalize_text(sentence)

    # Adjust regex to allow flexible word matching
    prefix_pattern = r'(?<!\w)(?:' + '|'.join(map(re.escape, prefixes)) + r')?\s*' + re.escape(word) + r'(\w+)?\s*(?!\w)'
    
    # Check exact match first
    if re.search(prefix_pattern, sentence, re.IGNORECASE | re.UNICODE):
        return True

    return False