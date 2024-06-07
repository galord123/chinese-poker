from dataclasses import dataclass


class Suit:
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


@dataclass
class Card:
    suit: Suit
    number: int

    def __gt__(self, other):
        if self.number == other.number:
            return int(self.suit) > int(other.suit)

        return self.number > other.number

    def __str__(self) -> str:
        suit_arts = {
            Suit.SPADES: "♠",
            Suit.HEARTS: "♥",
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
        }

        return str(self.number) + suit_arts[self.suit]


