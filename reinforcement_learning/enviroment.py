from typing import Optional
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from game.card import Card, Suit
from game.hand import Hand
from game.utils import get_playable_hands
from reinforcement_learning.observation import get_observation, hand_to_observation
from run_game import initialize_hands, return_game_score
from game.deck import Deck
from players import RandomPokerAi, SimplePokerAi, AdvancedPokerAi


class CustomPokerEnv(gym.Env):
    def __init__(self, test=False):
        super(CustomPokerEnv, self).__init__()
        self.player2_ai = SimplePokerAi()
        self.deck = Deck()
        self.player1_hands, self.player2_hands = initialize_hands(self.deck)
        self.current_turn = 0
        self.test = test
        # Define action space: 5 possible actions for choosing which hand to add a card to
        self.action_space = spaces.Discrete(
            len(get_playable_hands(self.player1_hands)))

        # Define observation space: representing player's hands and the current card
        self.observation_space = spaces.Box(
            low=0, high=52, shape=(102,), dtype=np.int32)

    def reset(self, seed: Optional[int] = None):
        super().reset(seed=seed)
        self.deck = Deck()
        self.player1_hands, self.player2_hands = initialize_hands(self.deck)
        self.current_turn = 0
        self.action_space = spaces.Discrete(
            len(get_playable_hands(self.player1_hands)))
        return self._get_observation(), {}

    def step(self, action):
        card = self.deck.pop()

        # Perform the action: add the card to the selected hand
        playable_hands = get_playable_hands(self.player1_hands)
        if action >= len(playable_hands):
            # Illegal move
            reward = -10  # Penalty for illegal move
            done = True   # End the episode
            truncated = False
            info = {"illegal_move": True}
            return self._get_observation(), reward, done, truncated, info

        playable_hands[action].add_card(card)
        observation = self._get_observation()

        # then player 2 performs his action
        card = self.deck.pop()
        played_hand = self.player2_ai.play_move(
            card, self.player2_hands, self.player1_hands, self.deck)
        self.player2_hands[played_hand].add_card(card)

        self.current_turn += 2
        done = self.current_turn >= 40  # End condition for 40 turns

        # Calculate reward (example: difference in scores, could be adjusted)
        reward = self._calculate_reward() if done else 0
        if done and not self.test:
            self.reset()

        self.action_space = spaces.Discrete(
            len(get_playable_hands(self.player1_hands)))

        return observation, reward, done, False, {}

    def render(self, mode='human', close=False):
        print(f"Player 1 hands: {self.player1_hands}")
        print(f"Player 2 hands: {self.player2_hands}")

    def _get_observation(self):
        if self.deck.cards_left_amount > 0:
            current_card = self.deck.cards_left[-1]
        else:
            current_card = Card(Suit.CLUBS, 0)

        return get_observation(self.player1_hands, self.player2_hands, current_card)

    def _calculate_reward(self):
        game_result = return_game_score(
            self.player1_hands, self.player2_hands, verbose=False)
        if game_result.player_scores[0] > game_result.player_scores[1]:
            return 5
        return -5
