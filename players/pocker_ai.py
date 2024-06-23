from abc import ABC, abstractmethod
from typing import List

from game import Card, Deck, Hand


class PokerAi(ABC):
    def __init__(self, is_first_player: bool):
        self.is_first_player: bool = is_first_player

    @abstractmethod
    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int:
        pass

    @abstractmethod
    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int | None:
        pass
