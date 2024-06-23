import unittest

from game.card import Suit
from game.deck import Deck


class TestDeckSanity(unittest.TestCase):
    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(deck.cards_left_amount, 52)
        for suit in Suit.__members__.values():
            self.assertEqual(deck.get_suit_left(suit, True), 13)
        for number in range(1, 14):
            self.assertEqual(deck.get_number_left(number, True), 4)

    def test_pop_card(self):
        deck = Deck()
        card = deck.pop()
        self.assertIsNotNone(card)
        self.assertEqual(deck.cards_left_amount, 51)
        self.assertEqual(deck.get_suit_left(card.suit, True), 12)
        self.assertEqual(deck.get_number_left(card.number, True), 3)

    def test_pop_two_cards(self):
        deck = Deck()
        first_card = deck.pop()
        self.assertIsNotNone(first_card)
        second_card = deck.pop()
        self.assertIsNotNone(second_card)

        self.assertEqual(deck.cards_left_amount, 50)
        if first_card.suit == second_card.suit:
            self.assertEqual(deck.get_suit_left(first_card.suit, True), 11)
        else:
            self.assertEqual(deck.get_suit_left(first_card.suit, True), 12)
            self.assertEqual(deck.get_suit_left(second_card.suit, True), 12)

        if first_card.number == second_card.number:
            self.assertEqual(deck.get_number_left(first_card.number, True), 2)
        else:
            self.assertEqual(deck.get_number_left(first_card.number, True), 3)
            self.assertEqual(deck.get_number_left(second_card.number, True), 3)

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
            self.assertEqual(deck._suits_left[suit], 0)
        for card_number in range(1, 14):
            self.assertEqual(deck._number_left[card_number], 0)


class TestDeckHiddenCards(unittest.TestCase):
    def test_deck_first_hidden_pop_card(self):
        deck = Deck()
        for _ in range(40):
            deck.pop()
        first_player_card = deck.pop()

        self.assertEqual(deck.cards_left_amount, 11)

        self.assertFalse(first_player_card in deck.get_cards_left(True))
        self.assertTrue(first_player_card in deck.get_cards_left(False))

        self.assertEqual(deck.get_suit_left(first_player_card.suit, True) + 1,
                         deck.get_suit_left(first_player_card.suit, False))

        self.assertEqual(deck.get_number_left(first_player_card.number, True) + 1,
                         deck.get_number_left(first_player_card.number, False))

    def test_pop_multiple_hidden_cards(self):
        players_cards = [[], []]

        deck = Deck()
        for _ in range(40):
            deck.pop()

        for i in range(12):
            players_cards[i % 2].append(deck.pop())

        self.assertEqual(deck.cards_left_amount, 0)
        self.assertNotEqual(players_cards[0], players_cards[1])
        self.assertListEqual(sorted(players_cards[0]), sorted(deck.get_cards_left(False)))
        self.assertListEqual(sorted(players_cards[1]), sorted(deck.get_cards_left(True)))

        first_suits = [card.suit for card in players_cards[0]]
        second_suits = [card.suit for card in players_cards[1]]
        first_numbers = [card.number for card in players_cards[0]]
        second_numbers = [card.number for card in players_cards[1]]

        for suit in Suit.__members__.values():
            self.assertEqual(deck.get_suit_left(suit, True), second_suits.count(suit))
            self.assertEqual(deck.get_suit_left(suit, False), first_suits.count(suit))

        for number in range(1, 14):
            self.assertEqual(deck.get_number_left(number, True), second_numbers.count(number))
            self.assertEqual(deck.get_number_left(number, False), first_numbers.count(number))


if __name__ == '__main__':
    unittest.main()
