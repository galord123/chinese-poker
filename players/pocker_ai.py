from abc import ABC, abstractmethod
from typing import List

from game import Card, Deck, Hand


class PokerAi(ABC):
    @abstractmethod
    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int:
        pass

    @abstractmethod
    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int | None:
        pass
