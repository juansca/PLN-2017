"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict
from tabulate import tabulate

from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    count_sents = len(sents)
    words_tags_counter = defaultdict(lambda: defaultdict(int))
    tag_to_words = defaultdict(set)
    words = defaultdict(int)
    count_tags = defaultdict(int)
    # Pre-compute tags and words information to do the statistics
    for sent in sents:
        for tupl in sent:
            word = tupl[0]
            tag = tupl[1]
            # The same word appear
            words[word] += 1
            # The same tag appear
            count_tags[tag] += 1
            # Relation between tag and word
            tag_to_words[tag].add(word)
            words_tags_counter[word][tag] += 1

    count_words = sum(words.values())
    words_vocab_len = len(words)
    tags_vocab_len = len(count_tags)

    print("Cantidad de palabras:", words_vocab_len,
          "\nCantidad de etiquetas:", tags_vocab_len,
          "\nCantidad de oraciones", count_sents,
          "\nCantidad de ocurrencias de palabras", count_words)

    # Extracting the ten most frequent tags
    tags_count_list = count_tags.items()
    tags_count_list = sorted(tags_count_list, key=lambda x: x[1], reverse=True)
    total_tags = sum([tag_tuple[1] for tag_tuple in tags_count_list])

    ten_frequent_tags = tags_count_list[:10]
    # Print the table with the information about the tags
    table = defaultdict(list)
    for i in range(10):
        tag_tuple = ten_frequent_tags[i]
        percent = (tag_tuple[1] / total_tags) * 100
        tag = tag_tuple[0]

        words_with_tag = tag_to_words[tag]
        words_with_tag = sorted(words_with_tag,
                                key=lambda word: words[word],
                                reverse=True)
        five_words = words_with_tag[:5]

        table['Order'].append(i)
        table['Tag'].append(tag)
        table['Freq'].append(tag_tuple[1])
        table['Percent'].append(percent)
        table['WsMFreq'].append(five_words)

    print(tabulate(table, headers="keys"))
