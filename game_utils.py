from typing import List
from game_hand import Hand


def get_available_hands(hands: List[Hand]) -> List[Hand]:
    min_deck = min(hands, key=lambda hand: len(hand.cards))
    min_number = len(min_deck.cards)
    return [hand for hand in hands if len(hand.cards) == min_number]