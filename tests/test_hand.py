import unittest

from game import Hand, Card
from game.card import Suit


class TestHand(unittest.TestCase):
    def __init__(self, method_name: str = "runTest"):
        super().__init__(method_name)
        self.player = None

    def setUp(self):
        self.current_player = self.player

    def test_hand_add_card(self):
        hand = Hand(self.current_player)
        hand.add_card(Card(Suit.DIAMONDS, 2))
        self.assertEqual(len(hand.get_cards(self.current_player)), 1)
        self.assertTrue(Card(Suit.DIAMONDS, 2) in hand.get_cards(self.current_player))
        self.assertEqual(len(hand.get_cards(not self.current_player)), 1)
        self.assertTrue(Card(Suit.DIAMONDS, 2) in hand.get_cards(not self.current_player))

    def test_hand_add_cards(self):
        hand = Hand(self.current_player)
        cards = [Card(Suit.DIAMONDS, 3), Card(Suit.DIAMONDS, 2)]
        hand.add_cards(cards)
        self.assertEqual(len(hand.get_cards(self.current_player)), 2)
        self.assertEqual(len(hand.get_cards(not self.current_player)), 2)

        for card in cards:
            self.assertTrue(card in hand.get_cards(self.current_player))
            self.assertTrue(card in hand.get_cards(not self.current_player))
            self.assertTrue(card.number in hand.get_values(self.current_player))
            self.assertTrue(card.number in hand.get_values(not self.current_player))

        self.assertEqual(3, hand.get_values(self.current_player)[0])
        self.assertEqual(3, hand.get_values(not self.current_player)[0])

    def test_hand_show_cards(self):
        hand = Hand(self.current_player)
        hand.add_cards([Card(Suit.DIAMONDS, i * 2) for i in range(1, 6)])

        self.assertEqual(len(hand.get_cards(self.current_player)), 5)
        self.assertEqual(len(hand.get_cards(not self.current_player)), 4)

        for i in range(1, 5):
            self.assertTrue(Card(Suit.DIAMONDS, i * 2) in hand.get_cards(self.current_player))
            self.assertTrue(i * 2 in hand.get_values(self.current_player))
            self.assertTrue(Card(Suit.DIAMONDS, i * 2) in hand.get_cards(not self.current_player))
            self.assertTrue(i * 2 in hand.get_values(not self.current_player))

        self.assertTrue(Card(Suit.DIAMONDS, 10) in hand.get_cards(self.current_player))
        self.assertTrue(10 in hand.get_values(self.current_player))
        self.assertFalse(Card(Suit.DIAMONDS, 10) in hand.get_cards(not self.current_player))
        self.assertFalse(10 in hand.get_values(not self.current_player))

    def test_hand_show_cards_reversed(self):
        hand = Hand(self.current_player)
        hand.add_cards([Card(Suit.DIAMONDS, i * 2) for i in range(5, 0, -1)])

        self.assertEqual(len(hand.get_cards(self.current_player)), 5)
        self.assertEqual(len(hand.get_cards(not self.current_player)), 4)

        for i in range(5, 1, -1):
            self.assertTrue(Card(Suit.DIAMONDS, i * 2) in hand.get_cards(self.current_player))
            self.assertTrue(i * 2 in hand.get_values(self.current_player))
            self.assertTrue(Card(Suit.DIAMONDS, i * 2) in hand.get_cards(not self.current_player))
            self.assertTrue(i * 2 in hand.get_values(not self.current_player))

        self.assertTrue(Card(Suit.DIAMONDS, 2) in hand.get_cards(self.current_player))
        self.assertTrue(2 in hand.get_values(self.current_player))
        self.assertFalse(Card(Suit.DIAMONDS, 2) in hand.get_cards(not self.current_player))
        self.assertFalse(2 in hand.get_values(not self.current_player))

    def test_hand_replace_last_card(self):
        hand = Hand(self.current_player)
        hand.add_cards([Card(Suit.DIAMONDS, i * 2) for i in range(1, 6)])
        hand.replace_last_card(Card(Suit.DIAMONDS, 13))

        self.assertTrue(Card(Suit.DIAMONDS, 13) in hand.get_cards(self.current_player))
        self.assertTrue(13 in hand.get_values(self.current_player))
        self.assertFalse(Card(Suit.DIAMONDS, 13) in hand.get_cards(not self.current_player))
        self.assertFalse(13 in hand.get_values(not self.current_player))

        self.assertFalse(Card(Suit.DIAMONDS, 10) in hand.get_cards(self.current_player))
        self.assertFalse(Card(Suit.DIAMONDS, 10) in hand.get_cards(not self.current_player))
        self.assertFalse(10 in hand.get_values(self.current_player))
        self.assertFalse(10 in hand.get_values(not self.current_player))


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    players_to_test = [True, False]
    for player in players_to_test:
        test_functions = loader.loadTestsFromTestCase(TestHand)
        for test_function in test_functions:
            test_function.player = player
        suite.addTest(test_functions)
    return suite


if __name__ == '__main__':
    unittest.main()
