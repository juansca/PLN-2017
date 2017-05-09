from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        :param tagged_sents:training sentences, each one being a list of pairs.
        :type tagged_sents: list of list of tuples (word, tag)
        """
        word_tags = dict()
        self.word_tags = word_tags

        for sent in tagged_sents:
            for word_tagged in sent:
                word = word_tagged[0]
                tag = word_tagged[1]

                if word in word_tags:
                    word_tags[word][tag] += 1
                else:
                    word_tags[word] = defaultdict(int)
                    word_tags[word][tag] += 1

        for word in word_tags:
            word_tags[word] = word_tags[word].items()
            word_tags[word] = sorted(word_tags[word], key=lambda x: x[1],
                                     reverse=True)

    def tag(self, sent):
        """Tag a sentence.

        :param sent: the sentence.
        :type sent: list of words
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        :param w: the word.
        :type w: str
        """
        if not self.unknown(w):
            tag = self.word_tags[w][0][0]
        else:
            tag = 'nc0s000'

        return tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        :param w: the word.
        :type w: str
        """
        return w not in self.word_tags
