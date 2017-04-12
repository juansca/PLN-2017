"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.ngram import NGram, AddOneNGram
from languagemodeling.corpus_reader import MyCorpus

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = MyCorpus('../../corpus', 'big.txt')

    # train the model
    n = int(opts['-n'])
    usermodel = str(opts['-m'])
    if usermodel == None or usermodel == 'ngram':
        model = NGram(n, sents.sents)
    elif usermodel == 'addone':
        model = AddOneNGram(n, sents.sents)


    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
