from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Optional, Tuple, List

from game import Hand, HandBaseValue, Deck, calculate_hand_base_value, has_better_cards
from players import PokerAi, RandomPokerAi


@dataclass
class GameResult:
    player_scores: Tuple[int, int]
    win_by_hand_value: DefaultDict[HandBaseValue, int]


def initialize_hands(deck: Deck) -> Tuple[List[Hand], List[Hand]]:
    player1_hands = [Hand(True) for _ in range(5)]
    player2_hands = [Hand(False) for _ in range(5)]
    for i in range(5):
        first_card = deck.pop()
        second_card = deck.pop()
        player1_hands[i].add_card(first_card)
        player2_hands[i].add_card(second_card)

    return player1_hands, player2_hands


def return_game_score(player1_hands: List[Hand], player2_hands: List[Hand], verbose: bool) -> GameResult:
    win_by_hand_value = defaultdict(int)
    player1_score = 0
    player2_score = 0
    for hand1, hand2 in zip(player1_hands, player2_hands):
        if verbose:
            print(hand1, calculate_hand_base_value(hand1.get_cards(True)))
            print(hand2, calculate_hand_base_value(hand2.get_cards(False)))
        result = has_better_cards(hand1.get_cards(True), hand2.get_cards(False))
        if verbose:
            print(result)
        if result:
            player1_score += 1
            win_by_hand_value[calculate_hand_base_value(hand1.get_cards(True))] += 1
        else:
            player2_score += 1
            win_by_hand_value[calculate_hand_base_value(hand1.get_cards(False))] += 1
    return GameResult((player1_score, player2_score), win_by_hand_value)


def run_game(player1_ai: Optional[PokerAi] = None, player2_ai: Optional[PokerAi] = None,
             verbose: bool = False) -> GameResult:
    deck = Deck()
    player1_ai = player1_ai if player1_ai is not None else RandomPokerAi(True)
    player2_ai = player2_ai if player2_ai is not None else RandomPokerAi(False)
    player1_hands, player2_hands = initialize_hands(deck)

    for i in range(40):
        card = deck.pop()
        turn: bool = i % 2 == 0  # TODO: e2e test about that player turn and deck
        player = player1_ai if turn else player2_ai
        current_hands = player1_hands if turn else player2_hands
        other_hands = player2_hands if turn else player1_hands

        if verbose:
            print(f"#{i}: {'player 1' if turn else 'player 2'}")
            print("to play", card)
            print(current_hands)

        played_hand = player.play_move(card, current_hands, other_hands, deck)
        current_hands[played_hand].add_card(card)

    first_player_card = deck.pop()
    player1_replaced_index = player1_ai.play_last_move(first_player_card, other_hands, current_hands, deck)
    if player1_replaced_index is not None:
        other_hands[player1_replaced_index].replace_last_card(first_player_card)

    second_player_card = deck.pop()
    player2_replaced_index = player2_ai.play_last_move(second_player_card, current_hands, other_hands, deck)
    if player2_replaced_index is not None:
        current_hands[player2_replaced_index].replace_last_card(second_player_card)

    return return_game_score(player1_hands, player2_hands, verbose)
