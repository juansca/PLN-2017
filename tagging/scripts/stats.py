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
    corpus = SimpleAncoraCorpusReader('corpus/ancora/')
    sents = list(corpus.tagged_sents())

    # compute the statistics
    count_sents = len(sents)
    words_tags_counter = defaultdict(set)
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
            # Used for ambiguity
            # Relation between tag and word
            tag_to_words[tag].add(word)
            words_tags_counter[word].add(tag)

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

    # Ambiguety
    words_ambiguety = words_tags_counter.items()
    # Generate list of tuples (word, level)
    words_ambiguety = [(word, len(tags)) for word, tags in words_ambiguety]
    words_ambiguety.sort(key=lambda word: word[1])

    ambiguety = defaultdict(set)
    level = 1
    for word in words_ambiguety:
        if level == 9:
            break
        word_level = word[1]
        if level == word_level:
            ambiguety[level].add(word[0])
        else:
            level += 1

    # Print the table with ambiguety information
    table = defaultdict(list)
    for i in range(1, 10):
        table['Level'].append(i)
        table['Words count'].append(len(ambiguety[i]))
        table['Total percent'].append(len(ambiguety[i]) / words_vocab_len)
        freq_words = list(ambiguety[i])
        freq_words = [(word, words[word]) for word in freq_words]
        freq_words.sort(key=lambda word: word[1], reverse=True)
        five_freq_words = [word[0] for word in freq_words]
        table['WsMFreq'].append(five_freq_words[:5])
    print("\n")
    print("\n")
    print(tabulate(table, headers="keys"))
