import unittest

from game.card import Card, Suit
from game.hand import Hand, HandValue


class TestHands(unittest.TestCase):
    def test_straight_flush(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.DIAMONDS, 2),
            Card(Suit.DIAMONDS, 3),
            Card(Suit.DIAMONDS, 4),
            Card(Suit.DIAMONDS, 5),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.STRAIGHT_FLUSH)

    def test_straight(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 2),
            Card(Suit.HEARTS, 3),
            Card(Suit.DIAMONDS, 5),
            Card(Suit.DIAMONDS, 4),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.STRAIGHT)

    def test_flush(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.DIAMONDS, 3),
            Card(Suit.DIAMONDS, 4),
            Card(Suit.DIAMONDS, 7),
            Card(Suit.DIAMONDS, 9),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.FLUSH)

    def test_pair(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.DIAMONDS, 4),
            Card(Suit.DIAMONDS, 7),
            Card(Suit.DIAMONDS, 9),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.PAIR)

    def test_two_pair(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.DIAMONDS, 2),
            Card(Suit.DIAMONDS, 2),
            Card(Suit.DIAMONDS, 9),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.TWO_PAIR)

    def test_full_house(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.DIAMONDS, 2),
            Card(Suit.DIAMONDS, 2),
            Card(Suit.DIAMONDS, 2),
        ])
        self.assertEqual(hand.calculate_hand_value(), HandValue.FULL_HOUSE)

    def test_better_pair(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.DIAMONDS, 5),
            Card(Suit.DIAMONDS, 4),
            Card(Suit.HEARTS, 6),
        ])

        other_hand = Hand()
        other_hand.add_cards([
            Card(Suit.DIAMONDS, 2),
            Card(Suit.CLUBS, 2),
            Card(Suit.DIAMONDS, 6),
            Card(Suit.HEARTS, 5),
            Card(Suit.DIAMONDS, 4),
        ])
        self.assertTrue(hand > other_hand)

    def test_better_flush(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 10),
            Card(Suit.DIAMONDS, 13),
            Card(Suit.DIAMONDS, 5),
            Card(Suit.DIAMONDS, 4),
            Card(Suit.DIAMONDS, 6),
        ])

        other_hand = Hand()
        other_hand.add_cards([
            Card(Suit.CLUBS, 2),
            Card(Suit.CLUBS, 8),
            Card(Suit.CLUBS, 6),
            Card(Suit.CLUBS, 5),
            Card(Suit.CLUBS, 4),
        ])
        self.assertTrue(hand > other_hand)

    def test_straight_with_royal(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 10),
            Card(Suit.DIAMONDS, 11),
            Card(Suit.DIAMONDS, 12),
            Card(Suit.HEARTS, 13),
        ])

        self.assertEqual(hand.calculate_hand_value(), HandValue.STRAIGHT)

    def test_full_house_comparison(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.CLUBS, 1),
            Card(Suit.DIAMONDS, 3),
            Card(Suit.HEARTS, 3),
        ])
        other_hand = Hand()
        other_hand.add_cards([
            Card(Suit.DIAMONDS, 13),
            Card(Suit.CLUBS, 13),
            Card(Suit.CLUBS, 12),
            Card(Suit.DIAMONDS, 12),
            Card(Suit.HEARTS, 12),
        ])

        self.assertTrue(hand > other_hand)
        self.assertFalse(other_hand > hand)

    def test_pair_comparison(self):
        hand = Hand()
        hand.add_cards([
            Card(Suit.DIAMONDS, 10),
            Card(Suit.CLUBS, 10),
            Card(Suit.CLUBS, 5),
            Card(Suit.DIAMONDS, 6),
            Card(Suit.HEARTS, 1),
        ])
        other_hand = Hand()
        other_hand.add_cards([
            Card(Suit.DIAMONDS, 13),
            Card(Suit.CLUBS, 13),
            Card(Suit.CLUBS, 10),
            Card(Suit.DIAMONDS, 11),
            Card(Suit.HEARTS, 12),
        ])

        self.assertFalse(hand > other_hand)
        self.assertTrue(other_hand > hand)


if __name__ == '__main__':
    unittest.main()
