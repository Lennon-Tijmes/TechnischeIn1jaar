"""
Tic Tac Toe Player
"""

import math
# copy.deepcopy(obj[, memo])
# Return a deep copy of obj. We need to use that so I am forced to use a library great
# https://docs.python.org/3/library/copy.html#copy.deepcopy
import copy


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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_player = sum(row.count(X) for row in board)
    o_player = sum(row.count(O) for row in board)

    return X if x_player == o_player else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # is it possible? Is it edible?
    if board[i][j] is not EMPTY:
        raise ValueError("Not possible, already something there mate")

    # Copy the board
    new_board = copy.deepcopy(board)

    # makes sure itll work
    current_player = player(board)

    new_board[i][j] = current_player

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = [
                #Rows
                [board[0][0], board[0][1], board[0][2]],
                [board[1][0], board[1][1], board[1][2]],
                [board[2][0], board[2][1], board[2][2]],

                # Columns
                [board[0][0], board[1][0], board[2][0]],
                [board[0][1], board[1][1], board[2][1]],
                [board[0][2], board[1][2], board[2][2]],

                # Diagonal valley (Harry Pottah)
                [board[0][0], board[1][1], board[2][2]],
                [board[0][2], board[1][1], board[2][0]]
            ]

    for line in lines:
        if line[0] == line[1] == line[2] and line[0] is not EMPTY:
            return line[0]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    elif any(EMPTY in row for row in board):
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)

    # Maxi for X (Gotta train my woodcutting in OSRS)
    if current == X:
        best_score = -math.inf
        best_move = None
        for action in actions(board):
            score = min_play(result(board, action))
            if score > best_score:
                best_score  = score
                best_move = action
        return best_move

    # Minimizing for O (Like me not fixing :
    # :( result raises exception on negative out-of-bounds move expected exception, none caught )
    else:
        best_score = math.inf
        best_move = None
        for action in actions(board):
            score = max_play(result(board, action))
            if score < best_score:
                best_score = score
                best_move = action
        return best_move

def max_play(board):
    """
    It's X's turn and tries his very best, what a good AI
    """

    if terminal(board):
        return utility(board)

    score = -math.inf
    for action in actions(board):
        score = max(score, min_play(result(board, action)))
    return score

def min_play(board):
    """
    It's O's turn and tries to return the worst possible score for X.
    """
    if terminal(board):
        return utility(board)

    score = math.inf
    for action in actions(board):
        score = min(score, max_play(result(board, action)))
    return score
