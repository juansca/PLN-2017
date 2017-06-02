from collections import defaultdict
from nltk.tree import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        :param grammar: a binarised NLTK PCFG.
        """
        pass

    def _to_triple(self, prod):
        """Convert the production prod to a triple.

        :param prod: production

        :return 3-uple (left_hand_side, right_hand_side, prob)
        """
        left_hand = str(prod.lhs())
        right_hand = tuple(str(rhs) for rhs in prod.rhs())
        prob = prod.logprob()

        return (left_hand, right_hand, prob)

    def _binary_productions(self, Bs, Cs):
        """Create a list of tuples containing all rules with the form A -> B C
        and its probability. Where B is in Bs and C is in Cs.

        :param Bs: list of nonterminals or terminals
        :param Cs: list of nonterminals or terminals

        :return: 4-uple (A, B, C, prob)
        """
        pass

    def parse(self, sent):
        """Parse a sequence of terminals.

        :param sent: the sequence of terminals.
        """
        pass 
