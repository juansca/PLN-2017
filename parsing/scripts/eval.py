"""Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
"""

from corpus.ancora import SimpleAncoraCorpusReader
from docopt import docopt
import pickle
import sys
from time import time

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    filename = 'Models/parsing/' + filename

    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    start = time()

    print('Loading corpus...')
    m = opts['-m']
    n = opts['-n']
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('corpus/ancora/', files)
    parsed_sents = list(corpus.parsed_sents())
    if m is not None:
        m = int(m)
        parsed_sents = [sent for sent in parsed_sents
                        if len(sent.leaves()) <= m]
    if n is not None:
        n = int(n)
        parsed_sents = parsed_sents[:n]

    print('Parsing...')
    hits, total_gold, total_model = 0, 0, 0
    hits_unlab, total_gold_unlab, total_model_unlab = 0, 0, 0
    n = len(parsed_sents)
    format_str = '{:3.1f}% ({}/{}) (P={:2.2f}%, R={:2.2f}%, F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        gold_spans = spans(gold_parsed_sent, unary=False)
        model_spans = spans(model_parsed_sent, unary=False)
        hits += len(gold_spans & model_spans)
        total_gold += len(gold_spans)
        total_model += len(model_spans)

        # compute labeled partial results
        prec = float(hits) / total_model * 100
        rec = float(hits) / total_gold * 100
        prec_plus_rec = (prec + rec)
        if prec_plus_rec == 0:
            f1 = 0
        else:
            f1 = 2 * prec * rec / prec_plus_rec

        # compute unlabeled scores
        gold_spans_unlab = {span[1:] for span in gold_spans}
        model_spans_unlab = {span[1:] for span in model_spans}

        hits_unlab += len(gold_spans_unlab & model_spans_unlab)
        total_gold_unlab += len(gold_spans_unlab)
        total_model_unlab += len(model_spans_unlab)

        # compute unlabeled partial results
        prec_unlab = float(hits_unlab) / total_model_unlab * 100
        rec_unlab = float(hits_unlab) / total_gold_unlab * 100
        prec_plus_rec = (prec_unlab + rec_unlab)
        if prec_plus_rec == 0:
            f1 = 0
        else:
            f1_unlab = 2 * prec_unlab * rec_unlab / (prec_unlab + rec_unlab)

        progress(format_str.format(float(i+1) * 100 / n, i+1, n,
                                   prec, rec, f1))

    finish = time() - start
    print('')
    print('Parsed {} sentences'.format(n))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(prec))
    print('  Recall: {:2.2f}% '.format(rec))
    print('  F1: {:2.2f}% '.format(f1))

    print('Unlabeled')
    print('  Precision: {:2.2f}% '.format(prec_unlab))
    print('  Recall: {:2.2f}% '.format(rec_unlab))
    print('  F1: {:2.2f}% '.format(f1_unlab))

    print('Time running: {:2.2f}seconds'.format(finish))
