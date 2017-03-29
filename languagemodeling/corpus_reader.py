import os
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

corpusdir = '../corpus/'
if not os.path.isdir(corpusdir):
    os.mkdir(corpusdir)

# Check that our corpus do exist and the files are correct.
assert os.path.isdir(corpusdir)

# Define a tokenizer pattern that is more precise than the default nltk pattern

pattern = r'''(?ix)          # set flag to allow verbose regexps and ignore case
      (?:mr\.|mrs\.)         # abreviation for mister and missus
    | (?:[A-Z]+\'[A-Z]{1,2}) # neg or tobe abreviations, e.g I'm, can't
    | (?:[A-Z]\.)+           # abbreviations, e.g. U.S.A.
    | \w+(?:-\w+)*           # words with optional internal hyphens
    | \$?\d+(?:\.\d+)?%?     # currency and percentages, e.g. $12.40, 82%
    | \.\.\.                 # ellipsis
    | [][.,;"'?():-_`]       # these are separate tokens; includes ], [
'''



# Instanciamos el tokenizer con este pattern

tokenizer = RegexpTokenizer(pattern)

# Create a new corpus by specifying the parameters
# (1) directory of the new corpus
# (2) the fileids of the corpus
# The fileids are simply the filenames.

my_corpus = PlaintextCorpusReader('../corpus/',
                                  'big.txt',
                                  word_tokenizer=tokenizer)

# Access sentences in the corpus. (list of list of strings)
sent_list = my_corpus.sents()
for i in range(1, 600):
    print(sent_list[i])



pattern = r'''(?ix)       # set flag to allow verbose regexps and ignore case
      (?:mr\.|mrs\.)      # abreviation for mister and missus
    | (?:[A-Z]+\'[A-Z]{1,2})
    | (?:[A-Z]\.)+        # abbreviations, e.g. U.S.A.
    | \w+(?:-\w+)*        # words with optional internal hyphens
    | \$?\d+(?:\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
    | \.\.\.              # ellipsis
    | [][.,;"'?():-_`]    # these are separate tokens; includes ], [
'''
