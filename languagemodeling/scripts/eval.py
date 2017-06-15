"""
Evaluate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""

from languagemodeling.corpus_reader import MyCorpus

from docopt import docopt
import pickle

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    filename = opts['-i']
    filename = "../Models/" + filename
    with open(filename, 'rb') as modelFile:
        model = pickle.load(modelFile)
        modelFile.close()

    datatest = MyCorpus('../../corpus', 'toTest.txt')

    perplexity = model.perplexity(datatest.sents)
    print("La perplexity es: ", perplexity)
