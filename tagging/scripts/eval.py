"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
from collections import Counter
from time import time

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    start = time()
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total = 0, 0
    hits_known, hits_unknown = 0, 0
    total_known, total_unknown = 0, 0

    n = len(sents)

    are_known = []

    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        total_acc = float(hits) / total

        # known words score
        for j in range(len(hits_sent)):
            # using the Counter method, descripted later, we have to asign
            # some values if are known or unknown and if are hit or not.
            if not model.unknown(word_sent[j]):
                are_known += [hits_sent[j] + 1]
            else:
                are_known += [hits_sent[j] - 2]

        progress('{:3.1f}% (Total: {:2.2f}%)'.format(float(i) * 100 / n,
                                                     total_acc * 100))

    # For eficiency we will use the Counter object from collections
    # library.
    # We redefine some things to look for them later
    known = 2
    fail_known = 1
    unknown = -1
    fail_unknown = -2

    # Counter creates a dictionary whose keys are known, fail_known, unknown
    # and fail_unknown.
    counter = Counter(are_known)
    # Now get the values that represent how many times does apears each one
    hits_known += counter[known]
    total_known += counter[known] + counter[fail_known]

    hits_unknown += counter[unknown]
    total_unknown += counter[unknown] + counter[fail_unknown]

    # Compute accuracy
    total_acc = float(hits) / total
    known_acc = float(hits_known) / total_known
    unknown_acc = float(hits_unknown) / total_unknown
    finish = time() - start
    print('')
    print('Total accuracy: {:2.2f}%'.format(total_acc * 100))
    print('Known accuracy: {:2.2f}%'.format(known_acc * 100))
    print('Unknown accuracy: {:2.2f}%'.format(unknown_acc * 100))
    print('Time running: {:2.2f}seconds'.format(finish))
