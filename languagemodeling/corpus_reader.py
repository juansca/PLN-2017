import os
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer


class MyCorpus(object):
    """
    This class represents the corpus tokenizer.
    The corpus tokenized is in ../corpus/
    """

    def __init__(self, corpusDir, fileId):
        """
        :param fileId: file name in ../corpus/ with the text to tokenize
        :type fileId: string
        """
        self.corpusdir = corpusDir
        self.fileId = fileId
        self.sents = list()

        if not os.path.isdir(self.corpusdir):
            os.mkdir(self.corpusdir)

        # Check that our corpus do exist and the files are correct.
        assert os.path.isdir(self.corpusdir)
        self._sents()

    def _sents(self):
        """
        This method tokenize the corpus with the tokenizer pattern defined.
        """
        # Define a tokenizer pattern that is more precise than the default nltk
        # pattern

        pattern = r'''(?ix) # set flag to allow verbose regexps and ignore case
              (?:mr\.|mrs\.)        # abreviation for mister and missus
            | (?:[A-Z]+\'[A-Z]{1,2}) # neg or to be abreviations, e.g can't
            | (?:[A-Z]\.)+          # abbreviations, e.g. U.S.A.
            | \w+(?:-\w+)*          # words with optional internal hyphens
            | \$?\d+(?:\.\d+)?%?    # currency and percentages e.g. $12.40, 82%
            | \.\.\.                # ellipsis
            | [][.,;"'?():-_`]      # these are separate tokens; includes ], [
        '''

        # Instantiate the tokenizer
        tokenizer = RegexpTokenizer(pattern)

        # Create a new corpus by specifying the parameters
        # (1) directory of the new corpus
        # (2) the fileids of the corpus
        # The fileids are simply the filenames.

        my_corpus = PlaintextCorpusReader(self.corpusdir,
                                          self.fileId,
                                          word_tokenizer=tokenizer)

        # Access sentences in the corpus (list of list of strings)
        self.sents = my_corpus.sents()
