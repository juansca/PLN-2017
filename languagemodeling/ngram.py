# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log

class NGram(object):

    def __init__(self, n, sents):
        """
        :param n: order of the model.
        :param sents: list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        counts = defaultdict(int)
        self.counts = counts

        for sent in sents:
            # In the unigram, don't consider the open tag
            if n > 1:
                sent.insert(0, '<s>')
            sent.append('</s>')
            # Complete the sentence to be in the nth range
            for i in range(len(sent), n):
                sent.insert(0, '<s>')
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def count(self, tokens):
        """
        Count for an n-gram or (n-1)-gram.

        :param tokens: the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        :param token: the token.
        :param prev_tokens: the previous n-1 tokens (optional only if n = 1).
        :type token: token
        :type prev_tokens: list(token)
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []

        assert(len(prev_tokens) == n - 1)
        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

    def sent_prob(self, sent):
        """
        Probability of a sentence. Warning: subject to underflow problems.

        :param sent: the sentence whose Probability is going to be calculated
        :type sent: list(tokens)
        """
        prob = self.cond_prob(sent[0])

        if self.n > 1:
            for i in range(len(sent) - 1):
                if prob == 0:
                    break
                prob = prob * self.cond_prob(sent[i + 1], sent[:i + 1])
        else:
            for i in range(len(sent) - 1):
                if prob == 0:
                    break
                prob = prob * self.cond_prob(sent[i + 1])

        return prob

    def sent_log_prob(self, sent):
        """
        Log-probability of a sentence.

        :param sent: the sentence as a list of tokens.
        """
