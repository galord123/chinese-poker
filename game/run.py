import random
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Optional, Tuple

from game.card import Card, Suit
from game.hand import Hand, HandValue
from players.pocker_ai import PokerAi
from players.random_ai import RandomPokerAi


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

    player1_hands, player2_hands = initialize_hands(deck)

    for i in range(40):
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

        played_hand = player.play_move(card, current_hands, other_hands, deck)
        current_hands[played_hand].add_card(card)

    first_player_card = deck.pop()
    player1_replaced_index = player1_ai.play_last_move(first_player_card, other_hands, current_hands, deck)
    other_hands[player1_replaced_index].replace_cards(first_player_card)

    second_player_card = deck.pop()
    player2_replaced_index = player2_ai.play_last_move(second_player_card, current_hands, other_hands, deck)
    current_hands[player2_replaced_index].replace_cards(second_player_card)

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


def initialize_hands(deck: List[Card]):
    player1_hands = [Hand() for _ in range(5)]
    player2_hands = [Hand() for _ in range(5)]
    for i in range(5):
        first_card = deck.pop()
        second_card = deck.pop()
        player1_hands[i].add_card(first_card)
        player2_hands[i].add_card(second_card)

    return player1_hands, player2_hands
