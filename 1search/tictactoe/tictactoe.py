"""
Tic Tac Toe Player
https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def count(player, board):
    """
    Return the count of player in a grid
    """
    return sum(row.count(player) for row in board)


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if count(X, board) > count(O, board):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(len(board)):         # or simply len(3)
        for j in range(len(board[i])):  # agian simply range(3)
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible

from copy import deepcopy
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError
    i, j = action
    board_cpy = deepcopy(board)
    board_cpy[i][j] = player(board)
    
    return board_cpy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for i in range(3):
        if all(player == board[i][0] for player in board[i]):
            return board[i][0]
    
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return count(EMPTY, board) == 0 or winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    is_won = winner(board)
    if is_won == X:
        return 1
    elif is_won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #   • Given a state s:
    #       • MAX picks action a in ACTIONS(s) that produces highest value of MIN-VALUE(RESULT(s, a))
    #       • MIN picks action a in ACTIONS(s) that produces smallest value of MAX-VALUE(RESULT(s, a))
    if terminal(board):
        return None
    if player(board) == X:      # MAXIMIZE
        ans = []
        for action in actions(board):
            ans.append((action, min_value(result(board, action), -math.inf, math.inf)))
        return max(ans, key=lambda item:item[1])[0]
    else:                       # MINIMIZE
        ans = []
        for action in actions(board):
            ans.append((action, max_value(result(board, action), -math.inf, math.inf)))
        return min(ans, key=lambda item:item[1])[0]

# alpha: max & beta: min
def max_value(board, alpha, beta):
    #   function MAX-VALUE(state):
    #       if TERMINAL(state):
    #           return UTILITY(state)
    #       v = -∞
    #       for action in ACTIONS(state):
    #           v = MAX(v, MIN-VALUE(RESULT(state, action)))
    #       return v
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        # alpha-beta pruning
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v

def min_value(board, alpha, beta):
    #   function MAX-VALUE(state):
    #       if TERMINAL(state):
    #           return UTILITY(state)
    #       v = +∞
    #       for action in ACTIONS(state):
    #           v = MIN(v, MAX-VALUE(RESULT(state, action)))
    #       return v
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        # alpha-beta pruning
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v
