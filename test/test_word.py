import unittest
from losc.word import Word


class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.word = Word()
        self.other_word = Word()

    def test_word_greater(self):
        self.word.value_of_differ_feature = 1.5
        self.other_word.value_of_differ_feature = 0.7

        self.assertTrue(self.word > self.other_word)

    def test_word_less(self):
        self.word.value_of_differ_feature = 15.9
        self.other_word.value_of_differ_feature = 16

        self.assertTrue(self.word < self.other_word)

    def test_word_equal(self):
        self.word.value_of_differ_feature = 0.053
        self.other_word.value_of_differ_feature = 0.053

        self.assertTrue(self.word == self.other_word)


if __name__ == '__main__':
    unittest.main()
