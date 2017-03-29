import os
from nltk.corpus import PlaintextCorpusReader

corpusdir = '../corpus/'
if not os.path.isdir(corpusdir):
    os.mkdir(corpusdir)

# Check that our corpus do exist and the files are correct.
assert os.path.isdir(corpusdir)

# Create a new corpus by specifying the parameters
# (1) directory of the new corpus
# (2) the fileids of the corpus
# The fileids are simply the filenames.
my_corpus = PlaintextCorpusReader('../corpus/', 'big.txt')

# Access sentences in the corpus. (list of list of strings)
sent_list = my_corpus.sents()
for i in range(1,200):
    print(sent_list[i])
