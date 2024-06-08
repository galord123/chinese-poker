from typing import List
from game.hand import Hand


def get_playable_hands(hands: List[Hand]) -> List[Hand]:
    hand_with_minimum_cards = min(hands, key=lambda hand: len(hand.cards))
    min_number_of_cards = len(hand_with_minimum_cards.cards)
    return [hand for hand in hands if len(hand.cards) == min_number_of_cards]