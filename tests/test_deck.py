import unittest

from game.card import Suit
from game.deck import Deck


class TestDeck(unittest.TestCase):
    def test_deck_sanity(self):
        deck = Deck()
        self.assertEqual(deck.cards_left_amount, 52)
        self.assertEqual(deck.get_suit_left(Suit.DIAMONDS), 13)
        self.assertEqual(deck.get_suit_left(Suit.DIAMONDS), deck.get_suit_left(Suit.SPADES))

    def test_pop_card(self):
        deck = Deck()
        card = deck.pop()
        self.assertIsNotNone(card)
        self.assertEqual(deck.cards_left_amount, 51)
        self.assertEqual(deck.get_suit_left(card.suit), 12)
        self.assertEqual(deck.get_number_left(card.number), 3)

    def test_pop_two_cards(self):
        deck = Deck()
        first_card = deck.pop()
        self.assertIsNotNone(first_card)
        second_card = deck.pop()
        self.assertIsNotNone(second_card)

        self.assertEqual(deck.cards_left_amount, 50)
        if first_card.suit == second_card.suit:
            self.assertEqual(deck.get_suit_left(first_card.suit), 11)
        else:
            self.assertEqual(deck.get_suit_left(first_card.suit), 12)
            self.assertEqual(deck.get_suit_left(second_card.suit), 12)

        if first_card.number == second_card.number:
            self.assertEqual(deck.get_number_left(first_card.number), 2)
        else:
            self.assertEqual(deck.get_number_left(first_card.number), 3)
            self.assertEqual(deck.get_number_left(second_card.number), 3)

    def test_pop_cards(self):
        deck = Deck()
        for _ in range(5):
            deck.pop()
        self.assertEqual(deck.cards_left_amount, 52 - 5)

    def test_pop_empty_deck(self):
        deck = Deck()
        for _ in range(52):
            deck.pop()
        self.assertIsNone(deck.pop())
        self.assertEqual(deck.cards_left_amount, 0)
        for suit in Suit.__members__.values():
            self.assertEqual(deck.get_suit_left(suit), 0)
        for card_number in range(1, 14):
            self.assertEqual(deck.get_number_left(card_number), 0)


if __name__ == '__main__':
    unittest.main()
