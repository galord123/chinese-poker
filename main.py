from collections import defaultdict

import matplotlib.pyplot as plt
from tqdm import tqdm

from run_game import run_game
from players import RandomPokerAi, SimplePokerAi


def main():
    win_by_hand_value = defaultdict(int)
    total_player1_score = 0
    total_player2_score = 0
    player1_wins = 0
    player2_wins = 0
    for _ in tqdm(range(1000)):
        game_result = run_game(RandomPokerAi(True), SimplePokerAi(False))
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
    run_game(player1_ai=RandomPokerAi(True), player2_ai=SimplePokerAi(False))
