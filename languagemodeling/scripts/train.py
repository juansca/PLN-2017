"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model> [-g <gamma>]] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: An interpolation model. Without addone smoothing.
                  interpolatedaddone: An interpolation model with addone smoothing.

  -g <value>    Value of gamma (Only if interpolated is chosen)
  -a <bool>     Use Addone model for the n = 1 (Only if interpolated is chosen)
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram
from languagemodeling.corpus_reader import MyCorpus

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = MyCorpus('../../corpus', 'toTrain.txt')

    # train the model
    n = int(opts['-n'])
    usermodel = str(opts['-m'])

    if usermodel is None or usermodel == 'ngram':
        print("OK! NGram Model is training.")
        model = NGram(n, sents.sents)
    elif usermodel == 'addone':
        print("OK! AddOne Model is training.")
        model = AddOneNGram(n, sents.sents)
    elif usermodel == 'interpolated':
        gamma = opts['-g']
        if gamma is None:
            print("OK! Interpolation Model")
            print("With a Gamma estimation and addone = False is training.")
            model = InterpolatedNGram(n, sents.sents, addone=False)
        else:
            gamma = float(gamma)
            print("OK! Interpolation Model")
            print("With Gamma = ", gamma, " and addone = False is training.")
            model = InterpolatedNGram(n, sents.sents, gamma=gamma, addone=False)
    elif usermodel == 'interpolatedaddone':
        gamma = opts['-g']
        if gamma is None:
            print("OK! Interpolation Model with a ")
            print("Gamma estimation and addone = True is training.")
            model = InterpolatedNGram(n, sents.sents)
        else:
            gamma = float(gamma)
            print("OK! Interpolation Model with")
            print("Gamma =", gamma, "and addone = True is training.")
            model = InterpolatedNGram(1, sents.sents, gamma=gamma)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
