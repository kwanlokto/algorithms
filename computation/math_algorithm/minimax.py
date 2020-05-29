import copy
from math import inf

import numpy as np


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)


def check_complete(state):
    is_complete = True
    for row in state:
        for col in row:
            is_complete = is_complete and col != 0
    return is_complete


def get_winning_player(state):
    player1_win = np.ones(len(state))
    player2_win = np.ones(len(state)) + 1

    diagonals = np.array(
        [
            [state[i][i] for i in range(len(state))],
            [state[len(state) - i - 1][i] for i in range(len(state))],
        ]
    )
    win_conditions = np.concatenate((state, state.T, diagonals), axis=0)

    for win_condition in win_conditions:
        if list(win_condition) == list(player1_win):
            return 1
        elif list(win_condition) == list(player2_win):
            return -1

    if check_complete(state):
        return 0
    return None


def build_tree(state, player):
    free_space = 0

    current_node = Node(state)
    game_piece = 1 if player else 2

    if get_winning_player(state) is None:
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    free_space += 1
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = game_piece

                    child_node = build_tree(new_state, not player)
                    if child_node is not None:
                        current_node.add_child(child_node)
    return current_node


def alphabeta(node, depth, alpha, beta, player, heuristic):
    if depth == 0 or node.children == []:
        return node.value, heuristic(node.value)  # value of that state

    best_state = None
    if player:
        value = -inf
        for child in node.children:
            _, opponent_best_move = alphabeta(
                child, depth - 1, alpha, beta, False, heuristic
            )

            if value < opponent_best_move:
                value = opponent_best_move
                best_state = child.value
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # player 2 won't choose node
    else:
        value = inf
        for child in node.children:
            _, opponent_best_move = alphabeta(
                child, depth - 1, alpha, beta, True, heuristic
            )
            if value > opponent_best_move:
                value = opponent_best_move
                best_state = child.value
            beta = min(beta, value)
            if alpha >= beta:
                break  # player 1 won't choose node
    return best_state, value


def print_board(game_state):
    # Format the game state to be human readable
    divider = "-----" * len(game_state)
    for row in range(len(game_state)):
        print(divider)
        gui_board = ""
        for col in game_state[row]:
            if col == 0:
                gui_board += "|   |"
            elif col == 1:
                gui_board += "| X |"
            elif col == 2:
                gui_board += "| O |"
        print(gui_board)
    print(divider + "\n")


def evaluate_winner(winner):
    if winner == 0:
        print("DRAW")
    elif winner == 1:
        print("Player WINS")
    elif winner == 2:
        print("AI WINS")


if __name__ == "__main__":
    """
    A game of tic tac toe to illustrate alpha beta pruning
    """

    game_state = np.zeros((3, 3))

    winner = None
    while winner is None:
        valid = False
        while not valid:
            row = input("Enter a valid row number: ")
            col = input("Enter a valid column number: ")

            valid = game_state[int(row)][int(col)] == 0

        game_state[int(row)][int(col)] = 1
        print_board(game_state)
        tree = build_tree(game_state, False)

        winner = get_winning_player(game_state)
        evaluate_winner(winner)

        game_state, _ = alphabeta(
            tree, 9, -inf, inf, False, get_winning_player
        )
        print_board(game_state)
        winner = get_winning_player(game_state)
        evaluate_winner(winner)
