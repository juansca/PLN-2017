"""Train a parser.

Usage:
  train.py [-m <model> [-n <order>]] -o <file>
  train.py -h | --help

Options:
  -n <order>   Use Horizontal Markovization (Only for upcfg model)
  -m <model>    Model to use [default: flat]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
                  upcfg: Unlexicalized PCFG model
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.baselines import Flat, RBranch, LBranch
from parsing.upcfg import UPCFG

models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
    'upcfg': UPCFG,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('corpus/ancora/', files)

    print('Training model...')
    model = models[opts['-m']]
    if opts['-m'] == 'upcfg':
        horizMarkov = opts['-n']
        if horizMarkov is not None:
            horizMarkov = int(horizMarkov)
        print(opts['-m'], "with Horizontal Markov order = ", horizMarkov)
        model = model(corpus.parsed_sents(), horzMarkov=horizMarkov)
    else:
        model = model(corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    filename = 'Models/parsing/' + filename
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
