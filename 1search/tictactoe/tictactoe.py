"""
Tic Tac Toe Player
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


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        i, j = action
    except ValueError:
        raise Exception("None")
    board[i][j] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """ 
    for player in [X, O]:
        # Check rows
        for i in range(3):
            if board[i][0] == player and board[i][1] == player and board[i][2] == player:
                return player
        
        # Check columns
        for j in range(3):
            if board[0][j] == player and board[1][j] == player and board[2][j] == player:
                return player

        # Check diagonals
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return player

        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return player
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
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
    
    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
