from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    :param h: a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()


def word_istitle(h):
    """
    Feature: current word starts with an uppercase letter.

    :param h: a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()


def word_isupper(h):
    """
    Feature: current word is uppercased.

    :param h: a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()


def word_isdigit(h):
    """
    Feature: current word is a number.

    :param h: a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isnumeric()


class NPrevTags(Feature):

    def __init__(self, n):
        """
        Feature: n previous tags tuple.

        :param n: number of previous tags to consider.
        """
        self.n = n

    def _evaluate(self, h):
        """
        n previous tags tuple.

        :param h: a history.
        """
        n = self.n
        prevs = prev_tags(h)
        return prevs[-n:]


class PrevWord(Feature):

    def __init__(self, f):
        """
        Feature: the feature f applied to the previous word.

        :param f: the feature.
        """
        pass

    def _evaluate(self, h):
        """
        Apply the feature to the previous word in the history.

        :param h: the history.
        """
        pass
