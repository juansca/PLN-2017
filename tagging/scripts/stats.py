"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict
from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    count_sents = len(sents)
    count_words = defaultdict(int)
    count_tags = defaultdict(int)
    tag_to_words = dict()
    # Pre-compute tags and words information to do the statistics
    for sent in sents:
        for tupl in sent:
            word = tupl[0]
            tag = tupl[1]
            # The same word appear
            count_words[word] += 1
            # The same tag appear
            count_tags[tag] += 1
            # Relation between tag and word
            if tag in tag_to_words.keys():
                tag_to_words[tag].add(word)
            else:
                tag_to_words[tag] = {word}
