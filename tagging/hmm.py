class HMM:

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
            prob = trans.get(tag, 0)

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
        complete_y = ['<s>'] * (n-1) + y + ['<\s>']
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

        x -- sentence.
        y -- tagging.
        """

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
