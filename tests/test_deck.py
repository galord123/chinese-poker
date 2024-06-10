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

    def test_pop_cards(self):
        deck = Deck()
        for _ in range(5):
            deck.pop()
        self.assertEqual(deck.cards_left_amount, 52 - 5)


if __name__ == '__main__':
    unittest.main()
