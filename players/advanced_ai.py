from collections import Counter
from typing import List

import numpy as np

from game.card import Card
from game.hand import Hand
from game.utils import get_playable_hands
from players.pocker_ai import PokerAi


class AdvancedPokerAi(PokerAi):
    def calculate_hand_improvement(self, hand: Hand, card: Card) -> int:
        """ Calculate the improvement in hand strength if a card is added. """
        current_strength = hand.calculate_hand_value()
        potential_strength = hand.potential_strength(card)
        return potential_strength - current_strength

    def calculate_opponent_threat(self, other_hands: List[Hand], hand_index: int) -> int:
        """ Evaluate the threat level of the opponent's hand at a given index. """
        return other_hands[hand_index].calculate_hand_value()

    def calculate_flush_probability(self, hand: Hand, card: Card, deck: List[Card]) -> float:
        """ Calculate the probability of completing a flush if a card is added. """
        suit_counts = Counter(card.suit for card in hand.cards + [card])
        max_suit_count = max(suit_counts.values())
        needed_cards = 5 - max_suit_count
        remaining_suit_cards = sum(
            1 for c in deck if c.suit in suit_counts and suit_counts[c.suit] == max_suit_count)

        if needed_cards > len(deck):
            return 0.0
        return remaining_suit_cards / len(deck)

    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        playable_hands = get_playable_hands(hands)

        best_hand = None
        best_score = -float('inf')

        for hand in playable_hands:
            improvement = self.calculate_hand_improvement(hand, card_to_play)
            hand_index = hands.index(hand)
            opponent_threat = self.calculate_opponent_threat(
                other_hands, hand_index)
            flush_probability = self.calculate_flush_probability(
                hand, card_to_play, deck)
            score = improvement - opponent_threat + flush_probability

            if score > best_score:
                best_score = score
                best_hand = hand

        # Add the card to the chosen hand
        if best_hand:
            return hands.index(best_hand)
            # print(f"Bot played {card_to_play} to {best_hand}")
        else:
            playable_hand = playable_hands[0]
            return hands.index(playable_hand)

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]) -> int:
        return np.random.randint(0, len(hands))
