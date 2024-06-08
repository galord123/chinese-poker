from typing import List

import numpy as np

from game.card import Card
from game.hand import Hand
from game.utils import get_playable_hands
from players.pocker_ai import PokerAi


class RandomPokerAi(PokerAi):
    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        playable_hands = get_playable_hands(hands)
        return hands.index(playable_hands[0])
        # print(f"Bot played {card_to_play} to {playable_hands[0]}")

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        return np.random.randint(0, len(hands))
