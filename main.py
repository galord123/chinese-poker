import random
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Optional, Tuple

import matplotlib.pyplot as plt
from tqdm import tqdm

from game_ai import PokerAi, RandomPokerAi, SimplePokerAi
from game_card import Card, Suit
from game_hand import Hand, HandValue


def initialize_deck() -> List[Card]:
    suites = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]

    deck = []
    for suit in suites:
        for i in range(1, 14):
            deck.append(Card(suit, i))

    random.shuffle(deck)
    return deck


@dataclass
class GameResult:
    player_scores: Tuple[int, int]
    win_by_hand_value: DefaultDict[HandValue, int]


def run_game(player1_ai: Optional[PokerAi] = None, player2_ai: Optional[PokerAi] = None,
             verbose: bool = False) -> GameResult:
    win_by_hand_value = defaultdict(int)
    deck = initialize_deck()

    player1_ai = player1_ai if player1_ai is not None else RandomPokerAi()
    player2_ai = player2_ai if player2_ai is not None else RandomPokerAi()

    player1_hands = [
        Hand(),
        Hand(),
        Hand(),
        Hand(),
        Hand(),
    ]
    player2_hands = [
        Hand(),
        Hand(),
        Hand(),
        Hand(),
        Hand(),
    ]
    for i in range(50):
        card = deck.pop()
        turn = i % 2 == 0
        if turn:
            player = player1_ai
            current_hands = player1_hands
            other_hands = player2_hands
        else:
            player = player2_ai
            current_hands = player2_hands
            other_hands = player1_hands

        if verbose:
            print(f"#{i}: {'player 1' if turn else 'player 2'}")
            print("to play", card)
            print(current_hands)

        player.play_move(card, current_hands, other_hands, deck)

    player1_score = 0
    player2_score = 0
    for hand1, hand2 in zip(player1_hands, player2_hands):
        if verbose:
            print(hand1, hand1.calculate_hand_value())
            print(hand2, hand2.calculate_hand_value())
        result = hand1 > hand2
        if verbose:
            print(result)
        if result:
            player1_score += 1
            win_by_hand_value[hand1.calculate_hand_value()] += 1
        else:
            player2_score += 1
            win_by_hand_value[hand2.calculate_hand_value()] += 1

    return GameResult((player1_score, player2_score), win_by_hand_value)


def main():
    win_by_hand_value = defaultdict(int)
    total_player1_score = 0
    total_player2_score = 0
    player1_wins = 0
    player2_wins = 0
    for _ in tqdm(range(1000)):
        game_result = run_game(RandomPokerAi(), SimplePokerAi(), )
        player1_score, player2_score = game_result.player_scores
        total_player1_score += player1_score
        total_player2_score += player2_score

        if player1_score > player2_score:
            player1_wins += 1
        else:
            player2_wins += 1

        for key, value in game_result.win_by_hand_value.items():
            win_by_hand_value[key] += value

    labels = 'player 1', 'player 2',
    sizes = [total_player1_score, total_player2_score]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax1.set_title("total player scores")
    ax2.pie([player1_wins, player2_wins], labels=labels, autopct='%1.1f%%')
    ax2.set_title("total player wins")
    plt.show()

    ax = plt.subplot()
    ax.bar([key.name for key in win_by_hand_value.keys()], [value for value in win_by_hand_value.values()])
    plt.show()


if __name__ == "__main__":
    main()
    run_game(player1_ai=RandomPokerAi(),
             player2_ai=SimplePokerAi(), verbose=True)
