"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram
from languagemodeling.corpus_reader import MyCorpus

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = MyCorpus('../../corpus', '24M.txt')

    # train the model
    n = int(opts['-n'])
    model = NGram(n, sents.sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
