from collections import defaultdict
from math import log2


def _log2(x):
    """Math base 2 log extended to compute log2(0)"""
    if x == 0:
        return float('-inf')
    else:
        return log2(x)


class HMM(object):

    def __init__(self, n, tagset, trans, out):
        """
        :param n: n-gram size.
        :param tagset: set of tags.
        :param trans: transition probabilities dictionary.
        :param out: output probabilities dictionary.
        """
        self.n = n
        self.tagset = tagset
        self.trans = trans
        self.out = out
        self.tagger = ViterbiTagger(self)

    def tagset(self):
        """Returns the set of tags."""
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        :param tag: the tag.
        :param prev_tags: tuple with the previous n-1 tags (optional only
                          if n = 1).
        """
        prob = 0.0
        trans = self.trans

        if prev_tags in trans:
            prob = trans[prev_tags].get(tag, 0)
        return prob

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        :param word: the word.
        :param tag: the tag.
        """
        prob = 0.0
        out = self.out
        if tag in out:
            prob = out[tag].get(word, 0)

        return prob

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        param y: tagging.
        """
        n = self.n
        complete_y = ['<s>'] * (n-1) + y + ['</s>']
        prob = 1

        for i in range(len(complete_y) - (n - 1)):
            prev_tags = tuple(complete_y[i: i + (n-1)])
            tag = complete_y[i + (n-1)]
            prob *= self.trans_prob(tag, prev_tags)

            if prob == 0:
                break

        return prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        :param x: sentence.
        :param y: tagging.
        """
        prob = self.tag_prob(y)

        for word, tag in zip(x, y):
            prob *= self.out_prob(word, tag)
            if prob == 0:
                break

        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        :param y: tagging.
        """

        n = self.n
        complete_y = ['<s>'] * (n-1) + y + ['</s>']
        prob = 0

        for i in range(len(complete_y) - (n - 1)):

            prev_tags = tuple(complete_y[i: i + (n-1)])
            tag = complete_y[i + (n-1)]
            prob += _log2(self.trans_prob(tag, prev_tags))
            if prob == float('-inf'):
                break

        return prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        :param x: sentence.
        :param y: tagging.
        """
        prob = self.tag_log_prob(y)

        for word, tag in zip(x, y):
            prob += _log2(self.out_prob(word, tag))
            if prob == float('-inf'):
                break

        return prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        :param sent: the sentence.
        """
        # Just tag with ViterbiTagger
        tagger = self.tagger

        return tagger.tag(sent)


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """

    def tcount(self, tokens):
        """Count for an n-gram or (n-1)-gram of tags.

        tokens -- the n-gram or (n-1)-gram tuple of tags.
        """

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """


class ViterbiTagger(object):

    def __init__(self, hmm):
        """
        :param hmm: the HMM.
        """
        self.model = hmm
        self.n = self.model.n
        self.tagset = self.model.tagset

        pi = defaultdict(lambda: defaultdict(tuple))
        self._pi = pi
        pi[0][('<s>',) * (self.n-1)] = (0, [])

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        :param sent: the sentence.
        """
        pi = self._pi
        tagset = self.tagset
        model = self.model

        for k in range(len(sent)):
            word = sent[k]
            pi_k = pi[k]
            pi_k1 = pi[k + 1]
            for prev_tags in pi_k:
                for tag in tagset:
                    # Compute the max
                    prob = _log2(model.out_prob(word, tag) *
                                 model.trans_prob(tag, prev_tags))
                    if prob == float('-inf'):
                        continue
                    # Prev tag probability accumulated
                    prob += pi_k[prev_tags][0]
                    # Relation between tag and prev_tags
                    tags = pi_k[prev_tags][1] + [tag]

                    prev_prob = pi_k1.get((prev_tags + (tag,))[1:],
                                          (float('-inf'),))[0]
                    # Maximising
                    if prev_prob < prob:
                        pi_k1[(prev_tags + (tag,))[1:]] = (prob, tags)

        state = list(pi[max(pi)].values())
        probs = [key[0] for key in state]
        self._pi = pi
        max_prob_index = probs.index(max(probs))
        return state[max_prob_index][1]
