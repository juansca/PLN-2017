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
        from_right_hand = self.from_right_hand

        productions = []

        b_c_right_hands = [right_hand for right_hand in from_right_hand
                           if len(right_hand) == 2]

        for right_hand in b_c_right_hands:
            B, C = right_hand
            if B in Bs and C in Cs:
                productions += [(A, B, C, prob) for A, prob in
                                from_right_hand[right_hand]]
        return productions


    def parse(self, sent):
        """Parse a sequence of terminals.

        :param sent: the sequence of terminals.
        """
        pass
