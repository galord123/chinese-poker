from copy import deepcopy
from typing import List

import numpy as np

from game.card import Card
from game.hand import Hand
from game.utils import get_playable_hands
from players.pocker_ai import PokerAi


class SimplePokerAi(PokerAi):
    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        playable_hands = get_playable_hands(hands)

        for position, hand in enumerate(hands):
            if hand in playable_hands:
                new_hand = deepcopy(hand)
                new_hand.cards.append(card_to_play)
                if new_hand > hand:
                    # print(f"Bot played {card_to_play} to {hand}")
                    return position

        return hands.index(playable_hands[0])
        # print(f"Bot played {card_to_play} to {playable_hands[0]}")

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        return np.random.randint(0, len(hands))