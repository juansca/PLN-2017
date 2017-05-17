"""Train a sequence tagger.

Usage:
  train.py [-m <model> [-n <order> -c <clasifier>]] -o <file>
  train.py -h | --help

Options:
  -n <order>    Order of the model trained
  -m <model>    Model to use [default: base]:
                  base: Baseline
                  hmm: Hidden Markov Model
                  mlhmm: Maximum Likelihood Hidden Markov Model
                  memm: Maximum Entropy Markov Models
  -c <clasifier> Clasifier that use in Maximum Entropy Markov Model
                 [default: LogisticRegression]
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from tagging.baseline import BaselineTagger
from tagging.hmm import HMM, MLHMM
from tagging.mem import MEMM

models = {
    'base': BaselineTagger,
    'hmm': HMM,
    'mlhmm': MLHMM,
    'memm': MEMM,
}

clasifiers = {
    'multinomial': MultinomialNB,
    'linear': LinearSVC
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
    c = opts['-c']

    if m == 'mlhmm':
        print("Model", m, "Training with n =", n)
        model = models[m](n, sents)
    elif m == 'memm':
        clasifier = clasifiers[c]
        print("Model", m, "Training with clasifier", c, "and n =", n,)
    else:
        print("Model", m, "Training")
        model = models[m](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
