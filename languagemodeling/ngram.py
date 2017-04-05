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
            # Adding corresponding start and end tags to the sentence
            #(preprocessing the sent)
            sent = self._add_tags(sent)

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

    def _add_tags(self, sent):
        """
        This method adds the start and anding tags correspondly
        :param sent: sentence to be processed
        :type sent: list of tokens
        """
        n = self.n
        if n > 1:
            # In the unigram, don't consider the open tag
            sent.insert(0, '<s>')
        sent.append('</s>')
        # Complete the sentence to be in the nth range
        for i in range(len(sent), n):
            sent.insert(0, '<s>')

        return sent

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

        :param sent: the sentence whose Probability is going to be
                     calculated
        :type sent: list of tokens
        """
        n = self.n
        # Adding corresponding start and end tags to the sentence
        #(preprocessing the sent)
        sent = self._add_tags(sent)
        prob = 1
        # Compute the sentence probability
        if n > 1:
            for i in range(n, len(sent)):
                if prob == 0:
                    break
                prob = prob * self.cond_prob(sent[i - 1], sent[i - n: i - 1])
        else:
            for i in range(len(sent)):
                if prob == 0:
                    break
                prob = prob * self.cond_prob(sent[i])

        return prob

    def sent_log_prob(self, sent):
        """
        Log-probability of a sentence.

        :param sent: the sentence to calculate the log probability.
        :type sent: list of tokens
        """
        n = self.n
        log1 = lambda x: log(x, 2) if x > 0  else float('-inf')

        # Adding corresponding start and end tags to the sentence
        #(preprocessing the sent)
        sent = self._add_tags(sent)
        prob = log1(1)

        # Compute the sentence probability
        if n > 1:
            for i in range(n, len(sent)):
                if prob == float('-inf'):
                    break
                prob = prob + log1(self.cond_prob(sent[i - 1], sent[i - n: i - 1]))
        else:
            for i in range(len(sent)):
                if prob == float('-inf'):
                    break
                prob = prob + log1(self.cond_prob(sent[i]))
        return prob
        
class NGramGenerator:

    def __init__(self, model):
        """
        model -- n-gram model.
        """

    def generate_sent(self):
        """Randomly generate a sentence."""

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.

        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
