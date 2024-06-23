from collections import defaultdict
from copy import deepcopy
from random import shuffle
from typing import List, Dict, Counter

from game.card import Card, Suit

SUITS = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]


class Deck:
    def __init__(self, initial_cards: List[Card] = None):
        if initial_cards is None:
            self._cards_left: List[Card] = [Card(suit, number) for suit in SUITS for number in range(1, 14)]
            self.shuffle()

            self.cards_left_amount = len(self._cards_left)
            self._suits_left: Dict[Suit, int] = {suit: 13 for suit in SUITS}
            self._number_left: Dict[int, int] = {number: 4 for number in range(1, 14)}
            self._decks: List["Deck"] = []

        else:
            self._cards_left: List[Card] = initial_cards
            self.cards_left_amount = len(self._cards_left)
            self._suits_left: Dict[Suit, int] = defaultdict(int)
            self._number_left: Dict[int, int] = defaultdict(int)

            for card in self._cards_left:
                self._suits_left[card.suit] += 1
                self._number_left[card.number] += 1

    def pop(self) -> Card | None:
        if self.cards_left_amount == 0:
            return None

        returned_card = self._cards_left.pop()
        self.cards_left_amount -= 1
        self._suits_left[returned_card.suit] -= 1
        self._number_left[returned_card.number] -= 1

        if self.cards_left_amount == 12:
            self._decks = [Deck(deepcopy(self._cards_left)), Deck(deepcopy(self._cards_left))]

        if self.cards_left_amount < 12:
            deck_index_to_remove = (self.cards_left_amount + 1) % 2
            self._decks[deck_index_to_remove].remove_card(returned_card)

        return returned_card

    def remove_card(self, card: Card) -> None:
        if card in self._cards_left:
            self._cards_left.remove(card)
            self._number_left[card.number] -= 1
            self._suits_left[card.suit] -= 1
            self.cards_left_amount -= 1

    def shuffle(self) -> None:
        shuffle(self._cards_left)

    def get_suit_left(self, suit: Suit, player: bool) -> int:
        if self.cards_left_amount > 12:
            return self._suits_left[suit]
        else:
            player_deck_index = 0 if player else 1
            return self._decks[player_deck_index]._suits_left[suit]

    def get_number_left(self, number: int, player: bool) -> int:
        if number == 14:
            number = 1

        if self.cards_left_amount > 12:
            return self._number_left[number]
        else:
            player_deck_index = 0 if player else 1
            return self._decks[player_deck_index]._number_left[number]

    def get_cards_left(self, player: bool) -> List[Card]:
        if self.cards_left_amount < 12:
            player_deck_index = 0 if player else 1
            return self._decks[player_deck_index]._cards_left
        return self._cards_left
