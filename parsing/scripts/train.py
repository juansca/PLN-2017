"""Train a parser.

Usage:
  train.py [-m <model>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: flat]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.baselines import Flat, RBranch, LBranch


models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('corpus/ancora/', files)

    print('Training model...')
    model = models[opts['-m']](corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    filename = 'Models/parsing/' + filename
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
