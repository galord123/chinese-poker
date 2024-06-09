from random import shuffle
from typing import List, Dict

from game.card import Card, Suit

SUITS = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]


class Deck:
    def __init__(self):
        self.cards_left: List[Card] = [Card(suit, number) for suit in SUITS for number in range(1, 14)]
        self.shuffle()

        self.cards_left_amount = len(self.cards_left)
        self.suits_left: Dict[Suit, int] = {suit: 13 for suit in SUITS}
        self.number_left: Dict[int, int] = {number: 4 for number in range(1, 14)}

    def pop(self) -> Card:
        returned_card = self.cards_left.pop()

        self.cards_left_amount -= 1
        self.suits_left[returned_card.suit] -= 1
        self.number_left[returned_card.number] -= 1

        return returned_card

    def shuffle(self) -> None:
        shuffle(self.cards_left)

    def get_suit_left(self, suit: Suit) -> int:
        return self.suits_left[suit]

    def get_number_left(self, number: int) -> int:
        return self.number_left[number]
