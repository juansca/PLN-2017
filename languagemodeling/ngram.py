# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import uniform


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
            # (preprocessing the sent)
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
        tok = tuple(tokens)
        prev_tok = tuple(prev_tokens)
        return float(self.counts[tok]) / self.counts[prev_tok]

    def sent_prob(self, sent):
        """
        Probability of a sentence. Warning: subject to underflow problems.

        :param sent: the sentence whose Probability is going to be
                     calculated
        :type sent: list of tokens
        """
        n = self.n
        # Adding corresponding start and end tags to the sentence
        # (preprocessing the sent)
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

    def _log2(self, x):
        """
        Simple log2 method. This implementation returns -inf if x <= 0
        :param x: Number to calculate the logaritmic function
        :type x: Real Number
        """
        ret = 0
        if x > 0:
            ret = log(x, 2)
        else:
            ret = float('-inf')
        return ret

    def sent_log_prob(self, sent):
        """
        Log-probability of a sentence.

        :param sent: the sentence to calculate the log probability.
        :type sent: list of tokens
        """
        n = self.n

        # Adding corresponding start and end tags to the sentence
        # (preprocessing the sent)
        sent = self._add_tags(sent)
        prob = self._log2(1)

        # Compute the sentence probability
        if n > 1:
            for i in range(n, len(sent)):
                if prob == float('-inf'):
                    break
                prob = prob + self._log2(self.cond_prob(sent[i - 1],
                                         sent[i - n: i - 1]))
        else:
            for i in range(len(sent)):
                if prob == float('-inf'):
                    break
                prob = prob + self._log2(self.cond_prob(sent[i]))
        return prob

    def log_prob(self, sents):
        """
        Calculate the log probability of a sentence's list.
        Just sum the log probability of each one.
        :param sents: the sentences whose log probability will be calculated.
        :type sents: List of lists of tokens.
        """
        prob = 0
        for sent in sents:
            prob += self.sent_log_prob(sent)

        return prob

    def cross_entropy(self, sents):
        """
        Compute the cross entropy for a list of sentences
        :param sents: sentences whose cross entropy will be calculated
        :type sents: List of lists of tokens
        """
        # Is the total number of words in sents
        totalwords = 0
        for sent in sents:
            totalwords += len(sent)

        entropy = - self.log_prob(sents) / totalwords

        return entropy

    def perplexity(self, sents):
        """
        Compute the perplexity for a list of sentences.
        :param sents: sentences whose perplexity will be calculated
        :type sents: List of lists of tokens
        """
        perplexity = 2 ** self.cross_entropy(sents)

        return perplexity

class NGramGenerator(object):

    def __init__(self, model):
        """
        :param model: n-gram model.
        :type model: Ngram
        """
        self.n = model.n
        n = self.n
        probs = dict()
        self.probs = probs

        # Generate a list of tuples (keys of model.counts) of length n.
        # We obtain these tuples to conservate the relationship between
        # prev_tokens and tokens
        tok_list = [x for x in list(model.counts.keys()) if len(x) == n]

        for token in tok_list:
            probs[token[:n - 1]] = list()

        for token in tok_list:
            tok_prob = tuple()
            # The token that is related to prev_tokens
            tok = token[n - 1:]
            # The prev_tokens related to token
            prev_tok = token[:n - 1]

            cond_tok = model.cond_prob(tok[0], list(prev_tok))
            # First, we save the tuple. Later, we will convert that to a dict.
            # This method facilitates the calculation of self.sorted_probs and
            # the structure of self.probs
            tok_prob = (tok[0], cond_tok)
            probs[prev_tok].append(tok_prob)

        self.sorted_probs = dict(probs)
        for key in probs.keys():
            probs[key] = dict(probs[key])

        # Sorting the lists in self.sorted_probs.
        # The order is defined by: most probably element (second component of
        # the tuple) and, after that, strings (or tokens) in the first element
        # of the tuple orderer (< to >)
        for key in self.sorted_probs.keys():
            self.sorted_probs[key] = sorted(self.sorted_probs[key],
                                            key=lambda x: (-x[1], x[0]))

    def _choice(self, choices):
        """
        This method is a weighted version of random.choice.
        Choice an element from a list of elements asociated with weights; in
        this particular case are probabilities.

        :param choices: Is the list of elements that will be chosen
        :param choices: List of tuples of elements and weights (probabilities)
        """
        total = sum(w for c, w in choices)
        r = uniform(0, total)
        upto = 0
        for c, w in choices:
            if upto + w >= r:
                return c
            upto += w

    def last_n(self, xs, n):
        """
        Returns the last n elements of the list xs.

        :param xs: List whose last n elements will be returned
        :param n: The number of elements that it will return
        :type xs: List
        :type n: int
        """
        assert(n <= len(xs))
        if n == 0:
            return []
        else:
            return xs[-n:]

    def generate_sent(self):
        """Randomly generate a sentence."""

        n = self.n
        # Adding the n - 1 start tags to compute correctly the probabilities
        sentence = ['<s>'] * (n - 1)
        prev_tokens = self.last_n(sentence, n - 1)
        # If '</s>' appears in our sentence, the sentence is finished
        while '</s>' not in sentence:
            generated_tok = self.generate_token(tuple(prev_tokens))
            sentence.append(generated_tok)
            prev_tokens = self.last_n(sentence, n - 1)

        # Rebuiling the sentence. We don't want the tags
        result = []
        for tok in sentence:
            if tok != '</s>' and tok != '<s>':
                result.append(tok)
        return result

    def generate_token(self, prev_tokens=None):
        """
        Randomly generate a token, given prev_tokens.

        :param prev_tokens: the previous n-1 tokens (optional only if n = 1).
        :type prev_tokens: tuple
        """

        return self._choice(self.sorted_probs[prev_tokens])


class AddOneNGram(NGram):
    """Todos los métodos de NGram."""

    def __init__(self, n, sents):
        """
        :param n: order of the model.
        :param sents: list of sentences, each one being a list of tokens.
        """
        super(AddOneNGram, self).__init__(n, sents)

        vocabulary = set()
        self.vocabulary = vocabulary
        wordList = list()
        # We use a set because that structure don't repeate the elements.
        # We want only one repetition for each one
        for sent in sents:
            for word in sent:
                if word != '<s>' and word != '</s>':
                    wordList.append(word)
        vocabulary = set(wordList)
        # We are redundant to avoid repeated calculations
        # Plus 1 because '</s>' is considered
        self.vLen = len(vocabulary) + 1

    def V(self):
        """
        Size of the vocabulary.
        """
        return self.vLen

    def cond_prob(self, token, prev_tokens=None):
        """
        Conditional probability of a token.

        :param token: the token.
        :param prev_tokens: the previous n-1 tokens (optional only if n = 1).
        :type token: token
        :type prev_tokens: list(token)
        """
        n = self.n
        v = self.vLen
        if not prev_tokens:
            prev_tokens = []

        assert(len(prev_tokens) == n - 1)
        tokens = prev_tokens + [token]
        tok = tuple(tokens)
        prev_tok = tuple(prev_tokens)
        return float((self.counts[tok]) + 1.0) / (self.counts[prev_tok] + v)
