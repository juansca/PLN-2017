from collections import defaultdict
from nltk.tree import Tree
from itertools import product


class CKYParser:

    def __init__(self, grammar):
        """
        :param grammar: a binarised NLTK PCFG.
        """
        self.grammar = grammar
        productions = grammar.productions()

        from_right_hand = defaultdict(list)
        self.from_right_hand = from_right_hand

        self.b_c_right_hands = []
        for p in productions:
            left_hand, right_hand, prob = self._to_triple(p)
            from_right_hand[right_hand].append((left_hand, prob))

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

        :return: list 4-uple (A, B, C, prob)
        """
        from_right_hand = self.from_right_hand

        productions = []

        for B, C in product(Bs, Cs):
            if (B, C) in from_right_hand:
                productions += [(A, B, C, prob) for A, prob in
                                from_right_hand[(B, C)]]
        return productions

    def _init_CKY_triangle(self, sent):
        """Initilize CKY triangle

        :param sent: the sequence of terminals
        """
        len_sent = len(sent)
        score = {}
        back = {}
        from_right_hand = self.from_right_hand

        for i in range(1, len_sent + 1):
            for j in range(i, len_sent + 1):
                score[(i, j)] = dict()
                back[(i, j)] = dict()

        # Creating the base of the CKY triangle
        for i, word in enumerate(sent):
            for A, prob in from_right_hand[(word,)]:
                j = i + 1
                score[(j, j)][A] = prob
                back[(j, j)][A] = Tree(A, [word])
        return score, back

    def parse(self, sent):
        """Parse a sequence of terminals.

        :param sent: the sequence of terminals.
        """
        len_sent = len(sent)
        score, back = self._init_CKY_triangle(sent)
        self._pi, self._bp = score, back

        for span in range(1, len_sent):
            for begin in range(1, len_sent - span + 1):
                end = begin + span
                for split in range(begin, end):
                    left, right = (begin, split), (split + 1, end)

                    binary_prods = self._binary_productions(score[left],
                                                            score[right])

                    for A, B, C, rule_prob in binary_prods:
                        # Sum probability because is logprob
                        prob = score[left][B] + score[right][C]
                        if A not in score[(begin, end)] \
                           or score[(begin, end)][A] < prob + rule_prob:
                            score[(begin, end)][A] = prob + rule_prob
                            right_back = back[right][C]
                            left_back = back[left][B]
                            back[(begin, end)][A] = Tree(A, [left_back,
                                                             right_back])
        start = str(self.grammar.start())
        if (1, len_sent) in score and start in score[(1, len_sent)]:
            return (score[(1, len_sent)][start], back[(1, len_sent)][start])
        return (float('-inf'), None)
