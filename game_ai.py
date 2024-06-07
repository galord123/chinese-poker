from copy import deepcopy
from abc import abstractmethod, ABC
from game_card import Card
from game_hand import Hand
from game_utils import get_available_hands
from collections import Counter
from typing import List


class PokerAi(ABC):
    @abstractmethod
    def play_move(self, card_to_play, hands, other_hands, deck):
        pass


class SimplePokerAi(PokerAi):
    def play_move(self, card_to_play, hands, other_hands, deck):
        playable_hands = get_available_hands(hands)

        for hand in playable_hands:
            new_hand = deepcopy(hand)
            new_hand.cards.append(card_to_play)
            if new_hand > hand:
                hand.cards.append(card_to_play)
                # print(f"Bot played {card_to_play} to {hand}")
                return

        playable_hands[0].cards.append(card_to_play)
        # print(f"Bot played {card_to_play} to {playable_hands[0]}")


class RandomPokerAi(PokerAi):
    def play_move(self, card_to_play, hands, other_hands, deck):
        playable_hands = get_available_hands(hands)
        playable_hands[0].cards.append(card_to_play)
        # print(f"Bot played {card_to_play} to {playable_hands[0]}")


class AdvancedPokerAi(PokerAi):
    def calculate_hand_improvement(self, hand: Hand, card: Card) -> float:
        """ Calculate the improvement in hand strength if a card is added. """
        current_strength = hand.calculate_hand_value()
        potential_strength = hand.potential_strength(card)
        return potential_strength - current_strength

    def calculate_opponent_threat(self, other_hands: List[Card], hand_index: int) -> float:
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

    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: List[Card]):
        available_hands = get_available_hands(hands)

        best_hand = None
        best_score = -float('inf')

        for hand in available_hands:
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
            best_hand.cards.append(card_to_play)
            # print(f"Bot played {card_to_play} to {best_hand}")
        else:
            available_hands[0].cards.append(card_to_play)
