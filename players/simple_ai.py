from copy import deepcopy
from typing import List

import numpy as np

from game import Card, Hand, Deck, get_playable_hands, has_better_cards
from players.pocker_ai import PokerAi


class SimplePokerAi(PokerAi):
    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int:
        playable_hands = get_playable_hands(hands)

        for position, hand in enumerate(hands):
            if hand in playable_hands:
                new_hand = deepcopy(hand)
                new_hand._cards.append(card_to_play)
                if has_better_cards(new_hand.get_cards(hand.player), hand.get_cards(hand.player)):
                    return position

        return hands.index(playable_hands[0])

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int | None:
        return np.random.randint(0, len(hands))
