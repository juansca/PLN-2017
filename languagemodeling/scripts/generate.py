"""
Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from languagemodeling.ngram import NGramGenerator

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    filename = opts['-i']
    with open(filename, 'rb') as inFile:
        generator = NGramGenerator(pickle.load(inFile))

    n = int(opts['-n'])
    for _ in range(n):
        print(' '.join(generator.generate_sent()))
