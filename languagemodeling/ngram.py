# https://docs.python.org/3/library/collections.html
from collections import defaultdict


class NGram(object):

    def __init__(self, n, sents):
        """
        :param n: order of the model.
        :param sents: list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]


    def count(self, tokens):
        """
        Count for an n-gram or (n-1)-gram.

        :param tokens: the n-gram or (n-1)-gram tuple.
        """

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        :param token: the token.
        :param prev_tokens: the previous n-1 tokens (optional only if n = 1).
        """

    def sent_prob(self, sent):
        """
        Probability of a sentence. Warning: subject to underflow problems.

        :param sent: the sentence as a list of tokens.
        """

    def sent_log_prob(self, sent):
        """
        Log-probability of a sentence.

        :param sent: the sentence as a list of tokens.
        """
