import unittest

from game import calculate_hand_base_value, HandBaseValue, has_better_cards
from game.card import Card, Suit


class TestHandBaseValues(unittest.TestCase):
    def test_high_card(self):
        cards = [Card(Suit.DIAMONDS, i * 2) for i in range(1, 5)] + [Card(Suit.SPADES, 5)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.HIGHEST_CARD)

    def test_pair(self):
        cards = [Card(Suit.DIAMONDS, 2), Card(Suit.CLUBS, 2), Card(Suit.DIAMONDS, 4), Card(Suit.DIAMONDS, 7),
                 Card(Suit.DIAMONDS, 9)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.PAIR)

    def test_two_pair(self):
        cards = [Card(Suit.DIAMONDS, 1), Card(Suit.CLUBS, 1), Card(Suit.DIAMONDS, 2), Card(Suit.DIAMONDS, 2),
                 Card(Suit.DIAMONDS, 9)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.TWO_PAIR)

    def test_triple(self):
        cards = ([Card(suit, 1) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
                 + [Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3)])
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.THREE_OF_A_KIND)

    def test_straight(self):
        cards = [Card(Suit.DIAMONDS, i) for i in range(2, 6)] + [Card(Suit.SPADES, 1)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.STRAIGHT)

    def test_flush(self):
        cards = [Card(Suit.DIAMONDS, i * 2) for i in range(1, 6)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.FLUSH)

    def test_full_house(self):
        cards = [Card(Suit.DIAMONDS, 1), Card(Suit.CLUBS, 1), Card(Suit.DIAMONDS, 2), Card(Suit.DIAMONDS, 2),
                 Card(Suit.DIAMONDS, 2), ]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.FULL_HOUSE)

    def test_four_kind(self):
        cards = [Card(suit, 8) for suit in Suit.__members__] + [Card(Suit.DIAMONDS, 3)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.FOUR_OF_A_KIND)

    def test_straight_flush(self):
        cards = [Card(Suit.DIAMONDS, i) for i in range(1, 6)]
        self.assertEqual(calculate_hand_base_value(cards), HandBaseValue.STRAIGHT_FLUSH)


class TestHandComparison(unittest.TestCase):
    def test_highest_card(self):
        self.assertTrue(has_better_cards([Card(Suit.DIAMONDS, 1)], [Card(Suit.DIAMONDS, 2)]))
        self.assertTrue(has_better_cards([Card(Suit.DIAMONDS, 3)], [Card(Suit.DIAMONDS, 2)]))
        self.assertTrue(has_better_cards([Card(Suit.SPADES, 2)], [Card(Suit.DIAMONDS, 2)]))
        self.assertTrue(has_better_cards([Card(Suit.SPADES, 2), Card(Suit.HEARTS, 4)], [Card(Suit.DIAMONDS, 2)]))

        base_hand = [Card(Suit.SPADES, 10), Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3), Card(Suit.DIAMONDS, 4)]
        self.assertTrue(has_better_cards(base_hand + [Card(Suit.SPADES, 1)], base_hand + [Card(Suit.DIAMONDS, 1)]))
        self.assertTrue(has_better_cards(base_hand + [Card(Suit.SPADES, 1)], base_hand + [Card(Suit.DIAMONDS, 5)]))
        self.assertTrue(has_better_cards(base_hand + [Card(Suit.SPADES, 11)], base_hand + [Card(Suit.DIAMONDS, 5)]))

    def test_pair(self):
        base_pair = [Card(Suit.SPADES, 4), Card(Suit.DIAMONDS, 4)]
        self.assertTrue(has_better_cards(base_pair, [Card(Suit.SPADES, 3), Card(Suit.DIAMONDS, 3)]))
        self.assertTrue(has_better_cards(base_pair + [Card(Suit.SPADES, 3)], base_pair + [Card(Suit.DIAMONDS, 2)]))
        self.assertTrue(has_better_cards(base_pair + [Card(Suit.SPADES, 6)], base_pair + [Card(Suit.DIAMONDS, 5)]))
        self.assertTrue(has_better_cards(base_pair + [Card(Suit.SPADES, 3)], base_pair + [Card(Suit.DIAMONDS, 3)]))

    def test_double_pair(self):
        low_card = [Card(Suit.SPADES, 7)]
        higher_card = [Card(Suit.DIAMONDS, 8)]
        higher_card_higher_suit = [Card(Suit.SPADES, 8)]
        low_pair = [Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 2)]
        medium_pair = [Card(Suit.SPADES, 3), Card(Suit.DIAMONDS, 3)]
        high_pair = [Card(Suit.SPADES, 5), Card(Suit.DIAMONDS, 5)]
        highest_pair = [Card(Suit.SPADES, 1), Card(Suit.DIAMONDS, 1)]

        self.assertTrue(has_better_cards(high_pair + low_pair + higher_card, high_pair + low_pair + low_card))
        self.assertTrue(
            has_better_cards(high_pair + low_pair + higher_card_higher_suit, high_pair + low_pair + higher_card))
        self.assertTrue(has_better_cards(high_pair + low_pair + low_card, medium_pair + low_pair + low_card))
        self.assertTrue(has_better_cards(high_pair + medium_pair + low_card, high_pair + low_pair + low_card))
        self.assertTrue(has_better_cards(highest_pair + medium_pair + low_card, high_pair + low_pair + low_card))

        self.assertTrue(
            has_better_cards(highest_pair + low_pair + higher_card_higher_suit, highest_pair + low_pair + higher_card))

    def test_triple(self):
        triple = ([Card(suit, 8) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
                  + [Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3)])
        better_triple = ([Card(suit, 9) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
                         + [Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3)])
        best_triple = ([Card(suit, 1) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
                       + [Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3)])

        self.assertTrue(has_better_cards(best_triple, better_triple))
        self.assertTrue(has_better_cards(better_triple, triple))

    def test_full_house(self):
        bad_triple = [Card(suit, 2) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
        good_triple = [Card(suit, 8) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
        best_triple = [Card(suit, 1) for suit in [Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]]
        pair = [Card(Suit.SPADES, 5), Card(Suit.DIAMONDS, 5)]

        self.assertTrue(has_better_cards(good_triple + pair, bad_triple + pair))  # only situation can occur
        self.assertTrue(has_better_cards(best_triple + pair, good_triple + pair))

    def test_straight(self):
        bad_straight = [Card(Suit.SPADES, 5)] + [Card(Suit.DIAMONDS, i) for i in range(1, 5)]
        good_straight = [Card(Suit.SPADES, 5)] + [Card(Suit.DIAMONDS, i) for i in range(6, 10)]
        best_straight = [Card(Suit.SPADES, 1)] + [Card(Suit.DIAMONDS, i) for i in range(10, 14)]

        self.assertTrue(has_better_cards(good_straight, bad_straight))
        self.assertTrue(has_better_cards(best_straight, good_straight))

    def test_four_kind(self):
        four_kind = [Card(suit, 8) for suit in Suit.__members__] + [Card(Suit.DIAMONDS, 3)]
        better_four_kind = [Card(suit, 9) for suit in Suit.__members__] + [Card(Suit.DIAMONDS, 3)]
        best_four_kind = [Card(suit, 1) for suit in Suit.__members__] + [Card(Suit.DIAMONDS, 3)]

        self.assertTrue(has_better_cards(best_four_kind, better_four_kind))
        self.assertTrue(has_better_cards(better_four_kind, four_kind))

    def test_flush(self):
        low_hearts_flush = [Card(Suit.HEARTS, i) for i in range(2, 11, 2)]
        higher_clubs_flush = [Card(Suit.CLUBS, i) for i in range(3, 12, 2)]
        higher_diamonds_flush = [Card(Suit.DIAMONDS, i) for i in range(3, 12, 2)]

        self.assertTrue(has_better_cards(higher_diamonds_flush, higher_clubs_flush))
        self.assertTrue(has_better_cards(higher_diamonds_flush, low_hearts_flush))
        self.assertTrue(has_better_cards(higher_clubs_flush, low_hearts_flush))

    def test_straight_flush(self):
        diamonds_straight_flush = [Card(Suit.DIAMONDS, i) for i in range(1, 6)]
        hearts_straight_flush = [Card(Suit.HEARTS, i) for i in range(1, 6)]
        clubs_higher_straight_flush = [Card(Suit.CLUBS, i) for i in range(2, 7)]
        hearts_royal = [Card(Suit.HEARTS, 1)] + [Card(Suit.HEARTS, i) for i in range(10, 14)]
        spades_royal = [Card(Suit.SPADES, 1)] + [Card(Suit.SPADES, i) for i in range(10, 14)]

        self.assertTrue(has_better_cards(hearts_straight_flush, diamonds_straight_flush))
        self.assertTrue(has_better_cards(clubs_higher_straight_flush, hearts_straight_flush))
        self.assertTrue(has_better_cards(hearts_royal, clubs_higher_straight_flush))
        self.assertTrue(has_better_cards(spades_royal, clubs_higher_straight_flush))
        self.assertTrue(has_better_cards(spades_royal, hearts_royal))

    def test_base_rank_comparisons(self):
        illegal_hand = []
        high_card = [Card(Suit.SPADES, 1), Card(Suit.SPADES, 10)] + [Card(Suit.DIAMONDS, i) for i in [4, 5, 6]]
        pair = [Card(Suit.DIAMONDS, 10), Card(Suit.SPADES, 10)] + [Card(Suit.DIAMONDS, i) for i in [4, 5, 6]]
        two_pair = [Card(Suit.DIAMONDS, 2), Card(Suit.SPADES, 2), Card(Suit.DIAMONDS, 3), Card(Suit.DIAMONDS, 3),
                    Card(Suit.DIAMONDS, 4)]
        triple = [Card(Suit.DIAMONDS, 8), Card(Suit.SPADES, 8), Card(Suit.DIAMONDS, 8), Card(Suit.SPADES, 2),
                  Card(Suit.DIAMONDS, 3)]
        straight = [Card(Suit.DIAMONDS, 2)] + [Card(Suit.SPADES, i) for i in range(3, 7)]
        flush = [Card(Suit.CLUBS, i) for i in range(2, 11, 2)]
        full_house = [Card(Suit.DIAMONDS, 8), Card(Suit.SPADES, 8), Card(Suit.SPADES, 7), Card(Suit.HEARTS, 7),
                      Card(Suit.DIAMONDS, 7)]
        four_kind = [Card(suit, 6) for suit in [Suit.CLUBS, Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS]] + [
            Card(Suit.SPADES, 5)]
        straight_flush = [Card(Suit.HEARTS, i) for i in range(1, 6)]
        royal_straight_flush = [Card(Suit.DIAMONDS, i) for i in [1, 10, 11, 12, 13]]

        hands = [high_card, pair, two_pair, triple, straight, flush, full_house, four_kind, straight_flush,
                 royal_straight_flush]

        for i in range(1, len(hands)):
            self.assertTrue(has_better_cards(hands[i], hands[i - 1]))
            self.assertFalse(has_better_cards(hands[i - 1], hands[i]))  # to check < and not just <=

        for hand in hands:
            self.assertTrue(has_better_cards(hand, illegal_hand))


if __name__ == '__main__':
    unittest.main()
