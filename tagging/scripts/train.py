"""Train a sequence tagger.

Usage:
  train.py [-m <model> [-n <order>]] -o <file>
  train.py -h | --help

Options:
  -n <order>    Order of the model trained
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  hmm: Hidden Markov Model
                  mlhmm: Maximum Likelihood Hidden Markov Model
                  memm: Maximum Entropy Markov Models
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import HMM, MLHMM
from tagging.mem import MEMM

models = {
    'base': BaselineTagger,
    'hmm': HMM,
    'mlhmm': MLHMM,
    'memm': MEMM,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/', files)
    sents = list(corpus.tagged_sents())

    # train the model
    n = int(opts['-n'])
    m = opts['-m']
    if m == 'mlhmm' or m == 'memm':
        print("Model", m, "Training with n =", n)
        model = models[m](n, sents)
    else:
        print("Model", m, "Training")
        model = models[m](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
