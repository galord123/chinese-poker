from typing import List

from game.card import Card


class Hand:
    def __init__(self, player: bool, cards: List[Card] = None):
        self.player: bool = player
        self._cards: List[Card] = []
        self._values: List[int] = []

        if cards is not None:
            self.add_cards(cards)

    def add_card(self, card: Card) -> None:
        self._cards.append(card)
        self._values.append(card.number)
        self._values.sort(reverse=True)

    def add_cards(self, cards: List[Card]) -> None:
        for card in cards:
            self.add_card(card)

    def replace_last_card(self, new_card: Card):
        replaced_card = self._cards[-1]
        self._cards[-1] = new_card

        self._values.remove(replaced_card.number)
        self._values.append(new_card.number)
        self._values.sort(reverse=True)

    def get_cards(self, player: bool) -> List[Card]:
        if self.player == player:
            return self._cards
        return self._cards[:4]

    def get_values(self, player: bool) -> List[int]:
        if self.player == player:
            return self._values
        return sorted([card.number for card in self.get_cards(player)], reverse=True)

    # Note: repr full state of the hand for both players
    def __repr__(self) -> str:
        return " ".join([str(card) for card in self._cards])
