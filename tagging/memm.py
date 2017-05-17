import numpy as np
from itertools import chain
from tagging.features import History


class MEMM:

    def __init__(self, n, tagged_sents):
        """
        :param n: order of the model.
        :param tagged_sents: list of sentences, each one being a list of pairs.
        """
        pass

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        :param tagged_sents: the corpus (a list of sentences)
        """
        pass

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        :param tagged_sent: the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        initial_tags = self.init_tags
        # All words tagged in the tagged sent
        words = [tagged_word[0] for tagged_word in tagged_sent]
        tags = tuple([tagged_word[1] for tagged_word in tagged_sent])
        # Add initial tags to tags sent
        tags = initial_tags + tags

        histories = [History(words, tags[i:i + n - 1], i)
                     for i in np.arange(len(words))]
        return iter(histories)

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        :param tagged_sents: the corpus (a list of sentences)
        """
        # Take tags from all the tagged sents
        tags = [self.sent_tags(tagged_sent) for tagged_sent in tagged_sents]

        return chain(*tags)

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        :param tagged_sent: the tagged sentence (a list of pairs (word, tag)).
        """
        # We use np array for efficiency
        tags = np.array([word_tagged[1] for word_tagged in tagged_sent])

        return np.nditer(tags)

    def tag(self, sent):
        """Tag a sentence.

        :param sent: the sentence.
        """
        n = self.n
        tagging = []
        tags = ('<s>',)*(n-1)
        for i in np.arange(len(sent)):
            # Create the correspondly history
            act_history = History(sent, tags, i)
            # Tag the history
            act_tag = self.tag_history(act_history)
            # New tag added
            tagging.append(act_tag)
            tags = (tags + (act_tag,))[1:]
        return tagging

    def tag_history(self, h):
        """Tag a history.

        :param h: the history.
        """
        # Just predict with scikit-learn pipeline model
        predicted_tagging = self.pipeline.predict([h])
        return predicted_tagging[0]

    def unknown(self, w):
        """Check if a word is unknown for the model.

        :param w: the word.
        """
        return w not in self.word_vocabulary
