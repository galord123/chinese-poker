import numpy as np
from game.card import Card, Suit
from game.deck import Deck
from game.hand import Hand


def hand_to_observation(hand: Hand):
    current_cards = [(card.number, card.suit.value+1) for card in hand.cards]
    missing_cards = 5 - len(hand.cards)
    padding = [(0, 0) for _ in range(missing_cards)]
    return current_cards + padding


def normalize_1d(data: np.ndarray) -> np.ndarray:
    return (data - data.min()) / (data.max() - data.min())


def get_observation(player1_hands, player2_hands, card_to_play: Card):
    player1_observation = [
        item for hand in player1_hands for item in hand_to_observation(hand)]
    player2_observation = [
        item for hand in player2_hands for item in hand_to_observation(hand)]

    # Combine all parts of the observation
    combined_observation = player1_observation + player2_observation
    combined_observation.append((card_to_play.number, card_to_play.suit.value))

    # Flatten the observation to a single list of integers
    flat_observation = [item for tup in combined_observation for item in tup]

    return normalize_1d(np.array(flat_observation, dtype=np.int32))
