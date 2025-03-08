import unittest
from core.word_checker import word_exists, normalize_text_for_matching

def split_sentence(sentence: str):
    """
    Normalizes the sentence for matching and then splits it into words.
    This external splitting is done before passing the list to word_exists.
    """
    normalized = normalize_text_for_matching(sentence)
    return normalized.split()

class TestWordCheckerExternalSplit(unittest.TestCase):
    def test_word_exists_exact(self):
        # Arabic: "هذا كتاب مفيد" should contain "كتاب"
        sentence = "هذا كتاب مفيد"
        word = "كتاب"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_word_not_exists(self):
        # Arabic: "المدينة كبيرة" should not contain "مدرسة"
        sentence = "المدينة كبيرة"
        word = "مدرسة"
        words = split_sentence(sentence)
        self.assertFalse(word_exists(word, words))
    
    def test_mark_non_number(self):
        # Arabic subtitle: "عند سماع صفارة إنذار" should detect "إنذار"
        sentence = "عند سماع صفارة إنذار"
        word = "إنذار"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_word_exists_with_common_prefix(self):
        # Arabic: "البيت جميل" should match "بيت" (after removing the definite article)
        sentence = "البيت جميل"
        word = "بيت"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_fuzzy_matching_threshold(self):
        # Arabic: "الكتاب مفيد" should be fuzzy-matched with "كتا" (a slightly off version)
        sentence = "الكتاب مفيد"
        slightly_off_word = "كتا"  # missing the final character of "كتاب"
        words = split_sentence(sentence)
        # At default threshold, the match should fail:
        self.assertFalse(word_exists(slightly_off_word, words))
        # Lowering the threshold to 70 should allow a match:
        self.assertTrue(word_exists(slightly_off_word, words, threshold=70))
    
    def test_word_exists_exact_hebrew(self):
        # Hebrew: "אני קורא ספר" should contain "ספר"
        sentence = "אני קורא ספר"
        word = "ספר"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_word_not_exists_hebrew(self):
        # Hebrew: "השמש זורחת" should not contain "ירח"
        sentence = "השמש זורחת"
        word = "ירח"
        words = split_sentence(sentence)
        self.assertFalse(word_exists(word, words))
    
    def test_word_exists_exact_russian(self):
        # Russian: "Я люблю книгу" should contain "книгу"
        sentence = "Я люблю книгу"
        word = "книгу"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_word_not_exists_russian(self):
        # Russian: "Сегодня прекрасная погода" should not contain "книга"
        sentence = "Сегодня прекрасная погода"
        word = "книга"
        words = split_sentence(sentence)
        self.assertFalse(word_exists(word, words))
    
    def test_word_exists_exact_english(self):
        # English: "This book is amazing" should contain "book"
        sentence = "This book is amazing"
        word = "book"
        words = split_sentence(sentence)
        self.assertTrue(word_exists(word, words))
    
    def test_word_not_exists_english(self):
        # English: "This movie is great" should not contain "book"
        sentence = "This movie is great"
        word = "book"
        words = split_sentence(sentence)
        self.assertFalse(word_exists(word, words))


if __name__ == "__main__":
    unittest.main()
