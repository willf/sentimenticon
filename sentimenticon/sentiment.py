# -*- coding: utf-8 -*-
"""sentiment

The sentiment module provides methods for returning word-level and
average word sentiment scores, currently for English only.

The sentiment data is from the article Temporal Patterns of Happiness and Information in a Global Social Network: Hedonometrics and Twitter
Peter Sheridan Dodds, Kameron Decker Harris, Isabel M. Kloumann, Catherine A. Bliss, and Christopher M. Danforth

Sentiments range from -1.0 to 1.0, where -1.0 is the most unfavorable, and 1.0 is the most favorable.

In addition, a Sentiment object can be inspected for the original values from the Hedonometrics paper.

Examples::

       >>> from sentimenicon import sentiment
       >>> a = sentiment.Analyzer
       >>> print a.word_sentiment("happy")
       >>> print a.word_sentiment("terrorist")
       >>> print a.average_word_sentiment("I love a happy friend".lower().split(" "))
       >>> s = a.sentiment_object("happy")


"""

import os.path


def safe_float(s):
    """safely return a float -- return None for parse failure"""
    try:
        return float(s)
    except ValueError:
        return None


def safe_int(s):
    """safely return an int -- return None for parse failure"""
    try:
        return int(s)
    except ValueError:
        return None


def normalize(ave):
    """normalize a Likert-scale of 1-9 to -1.0 to 1.0"""
    if (ave > 9.0) or (ave < 1.0):
        raise ValueError("%s not in range (1.0, 9.0)" % ave)
    return (((ave - 1) / 8) * 2) - 1.0


class Sentiment(object):
    """Sentiment object. See paper or data for details. The normed average in the normalized average."""

    def __init__(self, word, rank, normed_average, average, std, twitter, google, nyt, lyrics):
        self.word = word
        self.rank = rank
        self.normed_average = normed_average
        self.average = average
        self.std = std
        self.twitter = twitter
        self.google = google
        self.nyt = nyt
        self.lyrics = lyrics


class Analyzer(object):
    """A sentiment analyzer"""

    def __init__(self, language='en', minimum_frequency=1.0e-08):
        self.language = language
        self.sentiments = dict()
        self.minimum_frequency = minimum_frequency
        cwd = os.path.dirname(os.path.realpath(__file__))
        for line in open(cwd + "/data/" + language + "/journal.pone.0026752.s001.txt"):
            parts = line.strip().split("\t")
            if len(parts) == 8:
                word, rank, average, std, twitter, google, nyt, lyrics = parts
                r = safe_int(rank)
                ave = safe_float(average)
                s = safe_float(std)
                if r and ave and s:
                    norm = normalize(ave)
                    s = Sentiment(word, r, norm, ave, s, safe_int(twitter), safe_int(google), safe_int(nyt),
                                  safe_int(lyrics))
                    self.sentiments[word] = s
                else:
                    pass  # i.e., ignore non data lines in the pone file

    def word_sentiment(self, word, default=0.0):
        """return the normed sentiment of a word, returning default value if not found. word must be lowercased."""
        s = self.sentiments.get(word)
        if s:
            return s.normed_average
        else:
            return default

    def average_word_sentiment(self, words):
        """return the average word sentiment of an iterable of words, using 0.0 for unknown words.
        returns 0.0 for empty lists. """
        if len(words) == 0:
            return 0.0
        total = sum([self.word_sentiment(w) for w in words])
        return total / len(words)

    def sentiment_object(self, word):
        """return the Sentiment object for a word, or None if not found"""
        return self.sentiments.get(word)