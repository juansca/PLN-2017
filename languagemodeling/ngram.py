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
        for i in range(n - 1):
            sent.insert(0, '<s>')
        sent.append('</s>')
        # Complete the sentence to be in the nth range
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
        :param model: n-gram model.
        :type model: Ngram
        """
        n = model.n
        probs = dict()
        self.probs = probs

        probs_list = list()

        # Genero una lista de tokens de longitud n, cada uno.
        tok_list = [x for x in list(model.counts.keys()) if len(x) == n]
        for token in tok_list:
            probs[token[:n - 1]] = list()

        for token in tok_list:
            tok_prob = tuple()
            tok = token[n - 1:]
            prev_tok = token[:n - 1]

            cond_tok = model.cond_prob(tok[0], list(prev_tok))
            print(prev_tok, tok, cond_tok)
            tok_prob = (tok[0], cond_tok)

            probs[prev_tok].append(tok_prob)


        self.sorted_probs = dict(probs)
        for key in probs.keys():
            probs[key] = dict(probs[key])

        for key in self.sorted_probs.keys():
            sorted(self.sorted_probs[key], key=lambda x: x[1], reverse=True)

    def generate_sent(self):
        """Randomly generate a sentence."""




    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.

        :param: prev_tokens: the previous n-1 tokens (optional only if n = 1).
        """
