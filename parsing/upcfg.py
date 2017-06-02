from nltk.grammar import Nonterminal, induce_pcfg

from parsing.baselines import Flat
from parsing.cky_parser import CKYParser
from parsing.util import lexicalize, unlexicalize


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        :param parsed_sents: list of training trees.
        """
        self.start = start

        productions = []
        for tree in parsed_sents:
            tree_c = tree.copy(deep=True)
            tree_c = unlexicalize(tree_c)
            tree_c.chomsky_normal_form()
            tree_c.collapse_unary(collapsePOS=True)
            productions += tree_c.productions()

        self.pcfg = induce_pcfg(Nonterminal(start), productions)
        self.parser = CKYParser(self.pcfg)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        pass

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        :param tagged_sent: the tagged sentence (a list of pairs (word, tag)).
        """
        pass
