from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        :param tagged_sents:training sentences, each one being a list of pairs.
        :type tagged_sents: list of list of tuples (word, tag)
        """
        pass

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
        pass
        
    def unknown(self, w):
        """Check if a word is unknown for the model.

        :param w: the word.
        :type w: str
        """
        return w not in self.word_tags
