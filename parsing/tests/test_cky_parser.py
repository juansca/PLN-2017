# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log2

from nltk.tree import Tree
from nltk.grammar import PCFG

from parsing.cky_parser import CKYParser


class TestCKYParser(TestCase):

    def test_parse(self):
        grammar = PCFG.fromstring(
            """
                S -> NP VP              [1.0]
                NP -> Det Noun          [0.6]
                NP -> Noun Adj          [0.4]
                VP -> Verb NP           [1.0]
                Det -> 'el'             [1.0]
                Noun -> 'gato'          [0.9]
                Noun -> 'pescado'       [0.1]
                Verb -> 'come'          [1.0]
                Adj -> 'crudo'          [1.0]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('el gato come pescado crudo'.split())

        # check chart
        pi = {
            (1, 1): {'Det': log2(1.0)},
            (2, 2): {'Noun': log2(0.9)},
            (3, 3): {'Verb': log2(1.0)},
            (4, 4): {'Noun': log2(0.1)},
            (5, 5): {'Adj': log2(1.0)},

            (1, 2): {'NP': log2(0.6 * 1.0 * 0.9)},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': log2(0.4 * 0.1 * 1.0)},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S':
                     log2(1.0) +  # rule S -> NP VP
                     log2(0.6 * 1.0 * 0.9) +  # left part
                     log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},  # right part
        }
        self.assertEqualPi(parser._pi, pi)

        # check partial results
        bp = {
            (1, 1): {'Det': Tree.fromstring("(Det el)")},
            (2, 2): {'Noun': Tree.fromstring("(Noun gato)")},
            (3, 3): {'Verb': Tree.fromstring("(Verb come)")},
            (4, 4): {'Noun': Tree.fromstring("(Noun pescado)")},
            (5, 5): {'Adj': Tree.fromstring("(Adj crudo)")},

            (1, 2): {'NP': Tree.fromstring("(NP (Det el) (Noun gato))")},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': Tree.fromstring("(NP (Noun pescado) (Adj crudo))")},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': Tree.fromstring(
                "(VP (Verb come) (NP (Noun pescado) (Adj crudo)))")},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S': Tree.fromstring(
                """(S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                   )
                """)},
        }
        self.assertEqual(parser._bp, bp)

        # check tree
        t2 = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)
        self.assertEqual(t, t2)

        # check log probability
        lp2 = log2(1.0 * 0.6 * 1.0 * 0.9 * 1.0 * 1.0 * 0.4 * 0.1 * 1.0)
        self.assertAlmostEqual(lp, lp2)

    def test_ambiguous(self):
        grammar = PCFG.fromstring(
            """
                S -> NP VP               [1.0]
                NP -> Det Noun           [0.7]
                NP -> NP PP              [0.3]
                VP -> VP PP              [0.65]
                VP -> Verb NP            [0.35]
                PP -> Prep NP            [1.0]
                Prep -> 'with'           [1.0]
                Det -> 'The'             [0.33]
                Noun -> 'tourist'        [0.33]
                Verb -> 'saw'            [1.0]
                Det -> 'the'             [0.67]
                Noun -> 'astronomer'     [0.33]
                Noun -> 'telescope'      [0.34]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('The tourist saw the astronomer with the telescope'.split())

        pi = {
            (1, 1): {'Det': log2(0.33)},
            (2, 2): {'Noun': log2(0.33)},
            (3, 3): {'Verb': log2(1.0)},
            (4, 4): {'Det': log2(0.67)},
            (5, 5): {'Noun': log2(0.33)},
            (6, 6): {'Prep': log2(1.0)},
            (7, 7): {'Det': log2(0.67)},
            (8, 8): {'Noun': log2(0.34)},


            (1, 2): {'NP': log2(0.7 * 0.33 * 0.33)},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': log2(0.7 * 0.67 * 0.33)},
            (5, 6): {},
            (6, 7): {},
            (7, 8): {'NP': log2(0.7 * 0.67 * 0.34)},


            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': log2(0.35 * 0.7 * 0.67 * 0.33)},
            (4, 6): {},
            (5, 7): {},
            (6, 8): {'PP': log2(1.0 * 1.0 * 0.7 * 0.67 * 0.34)},


            (1, 4): {},
            (2, 5): {},
            (3, 6): {},
            (4, 7): {},
            (5, 8): {},

            (1, 5): {'S':
                     log2(1.0) +
                     log2(0.7 * 0.67 * 0.33) +
                     log2(0.35) + log2(1.0 * 0.7 * 0.33 * 0.33)},
            (2, 6): {},
            (3, 7): {},
            (4, 8): {'NP':
                     log2(0.3) +
                     log2(0.7 * 0.67 * 0.33) +
                     log2(1.0 * 1.0 * 0.7 * 0.67 * 0.34)},

            (1, 6): {},
            (2, 7): {},
            (3, 8): {'VP':
                     log2(0.65) +
                     log2(0.35 * 0.7 * 0.67 * 0.33) +
                     log2(1.0 * 1.0 * 0.7 * 0.67 * 0.34)},

            (1, 7): {},
            (2, 8): {},

            (1, 8): {'S':
                     log2(1.0) +  # rule S -> NP VP
                     log2(0.7 * 0.33 * 0.33) +  # left part
                     log2(0.65) + log2(0.35 * 0.7 * 0.67 * 0.33) +  # rightpart
                     log2(1.0 * 1.0 * 0.7 * 0.67 * 0.34)},
        }

        self.assertEqualPi(parser._pi, pi)

        bp = {
            (1, 1): {'Det': Tree('Det', ['The'])},
            (2, 2): {'Noun': Tree('Noun', ['tourist'])},
            (3, 3): {'Verb': Tree('Verb', ['saw'])},
            (4, 4): {'Det': Tree('Det', ['the'])},
            (5, 5): {'Noun': Tree('Noun', ['astronomer'])},
            (6, 6): {'Prep': Tree('Prep', ['with'])},
            (7, 7): {'Det': Tree('Det', ['the'])},
            (8, 8): {'Noun': Tree('Noun', ['telescope'])},


            (1, 2): {'NP': Tree('NP', [
                     Tree('Det', ['The']),
                     Tree('Noun', ['tourist'])
                     ])},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': Tree('NP', [
                     Tree('Det', ['the']),
                     Tree('Noun', ['astronomer'])
                     ])},
            (5, 6): {},
            (6, 7): {},
            (7, 8): {'NP': Tree('NP', [
                     Tree('Det', ['the']),
                     Tree('Noun', ['telescope'])
                     ])},


            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': Tree('VP', [
                      Tree('Verb', ['saw']),
                      Tree('NP', [
                          Tree('Det', ['the']), Tree('Noun', ['astronomer'])])
                      ])},
            (4, 6): {},
            (5, 7): {},
            (6, 8): {'PP': Tree('PP', [
                     Tree('Prep', ['with']),
                     Tree('NP', [
                          Tree('Det', ['the']),
                          Tree('Noun', ['telescope'])
                          ])
                     ])},


            (1, 4): {},
            (2, 5): {},
            (3, 6): {},
            (4, 7): {},
            (5, 8): {},


            (1, 5): {'S': Tree('S', [
                     Tree('NP', [
                          Tree('Det', ['The']),
                          Tree('Noun', ['tourist'])
                          ]),
                     Tree('VP', [
                          Tree('Verb', ['saw']),
                          Tree('NP', [
                               Tree('Det', ['the']),
                               Tree('Noun', ['astronomer'])
                               ])
                          ])
                     ])},
            (2, 6): {},
            (3, 7): {},
            (4, 8): {'NP': Tree('NP', [
                      Tree('NP', [
                           Tree('Det', ['the']),
                           Tree('Noun', ['astronomer'])
                           ]),
                      Tree('PP', [
                           Tree('Prep', ['with']),
                           Tree('NP', [
                                Tree('Det', ['the']),
                                Tree('Noun', ['telescope'])
                                ])
                           ])
                      ])},



            (1, 6): {},
            (2, 7): {},
            (3, 8): {'VP': Tree('VP', [
                      Tree('VP', [
                           Tree('Verb', ['saw']),
                           Tree('NP', [
                                Tree('Det', ['the']),
                                Tree('Noun', ['astronomer'])
                                ])
                           ]),
                      Tree('PP', [
                           Tree('Prep', ['with']),
                           Tree('NP', [
                                Tree('Det', ['the']),
                                Tree('Noun', ['telescope'])
                                ])
                           ])
                      ])},



            (1, 7): {},
            (2, 8): {},


            (1, 8): {'S': Tree('S', [
                     Tree('NP', [
                          Tree('Det', ['The']),
                          Tree('Noun', ['tourist'])
                          ]),
                     Tree('VP', [
                           Tree('VP', [
                                Tree('Verb', ['saw']),
                                Tree('NP', [
                                      Tree('Det', ['the']),
                                      Tree('Noun', ['astronomer'])
                                      ])
                                ]),
                           Tree('PP', [
                                 Tree('Prep', ['with']),
                                 Tree('NP', [
                                      Tree('Det', ['the']),
                                      Tree('Noun', ['telescope'])
                                      ])
                                 ])
                            ])
                     ])},

        }
        self.assertEqual(parser._bp, bp)

    def assertEqualPi(self, pi1, pi2):
        self.assertEqual(set(pi1.keys()), set(pi2.keys()))

        for k in pi1.keys():
            d1, d2 = pi1[k], pi2[k]
            self.assertEqual(d1.keys(), d2.keys(), k)
            for k2 in d1.keys():
                prob1 = d1[k2]
                prob2 = d2[k2]
                self.assertAlmostEqual(prob1, prob2)
