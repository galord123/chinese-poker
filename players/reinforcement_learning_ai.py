from typing import List
from stable_baselines3 import PPO
from game import Hand
from game.utils import get_playable_hands
from game.card import Card
from game.deck import Deck
from players.random_ai import RandomPokerAi
from players.simple_ai import SimplePokerAi
from reinforcement_learning.observation import get_observation
from run_game import run_game, PokerAi


class RLPokerAi(PokerAi):
    def __init__(self) -> None:
        super().__init__()
        self.model = PPO.load("./logs/best_model")

    def play_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int:
        observation = get_observation(hands, other_hands, card_to_play)
        action, _states = self.model.predict(observation, deterministic=True)
        playable_hands = get_playable_hands(hands)
        if action >= len(playable_hands):
            return hands.index(playable_hands[0])

        hand = playable_hands[action]
        return hands.index(hand)

    def play_last_move(self, card_to_play: Card, hands: List[Hand], other_hands: List[Hand], deck: Deck) -> int | None:
        return None
