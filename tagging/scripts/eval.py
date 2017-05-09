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

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
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
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        total_acc = float(hits) / total

        # Known and unknown score
        hits_known, hits_uknown = 0, 0
        total_known, total_unknown = 0, 0
        for m, g in zip(model_tag_sent, gold_tag_sent):
            # Unknown word
            if g == 'nc0s000':
                # Hit
                if m == g:
                    hits_uknown += 1
                total_unknown += 1
            # Known word
            else:
                # Hit
                if m == g:
                    hits_known += 1
                total_known += 1

        progress('{:3.1f}% (Total: {:2.2f}%)'.format(float(i) * 100 / n,
                                                     total_acc * 100))
    # Compute accuracy
    total_acc = float(hits) / total
    known_acc = float(hits_known) / total_known
    unknown_acc = float(hits_uknown) / total_unknown

    print('')
    print('Total accuracy: {:2.2f}%'.format(total_acc * 100))
    print('Known accuracy: {:2.2f}%'.format(known_acc * 100))
    print('Unknown accuracy: {:2.2f}%'.format(unknown_acc * 100))
