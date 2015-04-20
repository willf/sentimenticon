import unittest

from sentimenticon.sentiment import Analyzer


class TestSentimenticon(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(True)

    def test_read(self):
        a = Analyzer()

    def test_word(self):
        a = Analyzer()
        self.assertTrue(a.word_sentiment("happy") > 0)
        self.assertTrue(a.word_sentiment("terrorist") < 0)

    def test_sentence(self):
        a = Analyzer()
        self.assertTrue(a.average_word_sentiment("i like happy friendly people".split(" ")) > 0)
        self.assertTrue(a.average_word_sentiment("i hate every ugly terrorist".split()) < 0)


if __name__ == '__main__':
    unittest.main()