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

    words_vocab_len = len(count_words.keys())
    tags_vocab_len = len(count_tags.keys())

    # Extracting the ten most frequent tags
    tags_count_list = count_tags.items()
    tags_count_list = sorted(tags_count_list, key=lambda x: x[1], reverse=True)
    total_tags = sum([tag_tuple[1] for tag_tuple in tags_count_list])

    ten_frequent_tags = tags_count_list[:10]
    # Print the table with the information about the tags
    for i in range(10):
        tag_tuple = ten_frequent_tags[i]
        percent = (tag_tuple[1] / total_tags) * 100
        tag = tag_tuple[0]

        words_with_tag = tag_to_words[tag]
        words_with_tag = sorted(words_with_tag,
                                key=lambda word: count_words[word],
                                reverse=True)
        five_words = words_with_tag[:5]

        print(i, "th -->", tag,
              "\tFrequency:", tag_tuple[1], "Percent:", percent,
              "\tWords most frequent:", five_words)
