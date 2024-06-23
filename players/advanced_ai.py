from collections import Counter
from typing import List

import numpy as np

from game import Card, Hand, Deck, get_playable_hands, calculate_hand_base_value
from players.pocker_ai import PokerAi


class AdvancedPokerAi(PokerAi):
    def calculate_hand_improvement(self, hand: Hand, card: Card) -> int:
        """ Calculate the improvement in hand strength if a card is added. """
        current_strength = calculate_hand_base_value(hand.get_cards(self.is_first_player))
        potential_strength = calculate_hand_base_value(hand.get_cards(self.is_first_player) + [card])
        return potential_strength - current_strength

    def calculate_opponent_threat(self, other_hands: List[Hand], hand_index: int) -> int:
        """ Evaluate the threat level of the opponent's hand at a given index. """
        return calculate_hand_base_value(other_hands[hand_index].get_cards(self.is_first_player))

    def calculate_flush_probability(self, hand: Hand, card: Card, deck: Deck) -> float:
        """ Calculate the probability of completing a flush if a card is added. """
        suit_counts = Counter(card.suit for card in (hand.get_cards(self.is_first_player) + [card]))
        if len(suit_counts) > 1:
            return 0
        flash_suit = card.suit
        extra_cards_needed = 5 - len(hand.get_cards(self.is_first_player)) - 1

        suit_cards_left = deck.get_suit_left(flash_suit, self.is_first_player)

        if extra_cards_needed > suit_cards_left:
            return 0
        return extra_cards_needed / deck.cards_left_amount

    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int:
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

        best_hand = best_hand if best_hand else playable_hands[0]
        return hands.index(best_hand)

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int | None:
        return np.random.randint(0, len(hands))
