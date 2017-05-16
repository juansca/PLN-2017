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
        :param n: order of the model.
        :param tagged_sents: training sentences, each one being a list of pairs
        :param addone: whether to use addone smoothing (default: True).
        """
        tcounts = defaultdict(int)
        trans = defaultdict(lambda: defaultdict(int))
        out = defaultdict(lambda: defaultdict(int))
        word_vocabulary = set()
        tagset = set()

        self.tcounts = tcounts
        self.trans = trans
        self.n = n
        self.addone = addone
        self.out = out

        init_tag = ['<s>'] * (n-1)

        for sent in tagged_sents:
            # Build word_vocabulary and tagset
            # On each sent process the (word, tag) element
            sent_words = [word_tagged[0] for word_tagged in sent]
            sent_tags = [word_tagged[1] for word_tagged in sent]
            word_vocabulary.union(sent_words)
            tagset.union(sent_tags)
            words = init_tag + sent_words + ['</s>']
            tags = init_tag + sent_tags + ['</s>']
            for i in range(len(tags) - n + 1):
                act_word_tag = i + (n-1)
                out[tags[act_word_tag]][words[act_word_tag]] += 1
                ngram = tuple(tags[i:(i+n)])
                tcounts[ngram] += 1
                tcounts[ngram[:-1]] += 1

        self.word_vocabulary = set(word_vocabulary)
        self.tagset = set(tagset)
        if '</s>' in out:
            del out['</s>']

        # Compute probabilities
        for tag, words in out.items():
            total = sum(words.values())
            for word, ocurrences in words.items():
                # Probability that occurs word given tag
                words[word] = words[word] / total

        ngram_list = [ngram for ngram in tcounts if len(ngram) == n]
        for ngram in ngram_list:
            # Probability that occurs (x_1, ..., x_n) given that occurs
            # (x_1, ..., x_(n-1))
            trans[ngram[:-1]][ngram[:-1]] = tcounts[ngram] / \
                                            tcounts[ngram[:-1]]
        self.trans = dict(trans)
        self.out = dict(out)

    def tcount(self, tokens):
        """Count for an n-gram or (n-1)-gram of tags.

        :param tokens: the n-gram or (n-1)-gram tuple of tags.
        """
        tokens = tuple(tokens)
        n = self.n
        toklen = len(tokens)
        print(tokens, toklen, n)
        if toklen == 0:
            toklen = 1

        print(tokens)
        print(self.tcounts)
        assert (toklen == n) | (toklen == (n-1))

        count = self.tcounts[tokens]
        return count

    def unknown(self, w):
        """Check if a word is unknown for the model.

        :param w: the word.
        """
        return w not in self.word_vocabulary

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        :param tag: the tag.
        :param prev_tags: tuple with the previous n-1 tags (optional only
                          if n = 1).
        """
        addone = self.addone
        trans = self.trans
        if addone:
            tag_count = self.tcount(prev_tags + (tag,)) + 1
            denom = self.tcount(prev_tags) + len(self.tagset) + 1
            prob = tag_count / denom
        else:
            if prev_tags in trans:
                tag_trans = trans[prev_tags]
                prob = tag_trans.get(tag, 0)
            else:
                prob = 0
        return prob

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        :param word: the word.
        :param tag: the tag.
        """
        addone = self.addone
        out = self.out
        if tag in out:
            tag_trans = out[tag]
            prob = tag_trans.get(tag, 0)
        else:
            prob = 0
        if addone and self.unknown(word):
            prob = 1 / len(self.word_vocabulary)
        return prob


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
