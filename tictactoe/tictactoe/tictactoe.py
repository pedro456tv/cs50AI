"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

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
    if(board == initial_state()):
        return X
    x_sum = sum([i.count(X) for i in board])
    o_sum = sum([i.count(O) for i in board])
    if(x_sum > o_sum):
        return O
    return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    akcie = set()
    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                akcie.add((i,j))
    return akcie

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newb = copy.deepcopy(board)
    if(action not in actions(board)):
        raise AttributeError
    myplayer = player(board)
    if(myplayer == X):
        newb[action[0]][action[1]] = X
        return newb
    newb[action[0]][action[1]] = O
    return newb

    raise NotImplementedError

def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None
    
def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) != None or (not any(EMPTY in x for x in board) and winner(board) == None)):
        return True
    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if(win == X):
        return 1
    elif(win == O):
        return -1
    return 0

    raise NotImplementedError

def MAX_val(board):
    v = -100000
    if(terminal(board)):
        return utility(board)
    for actioni in actions(board):
        v = max(v,MIN_val(result(board,actioni)))
    return v

def MIN_val(board):
    v = 100000
    if(terminal(board)):
        return utility(board)
    for actioni in actions(board):
        v = min(v,MAX_val(result(board,actioni)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    myplayer = player(board)
    if(myplayer == X):
        if(board == initial_state()):
            return (1,1)
        move = None
        bstscore = -10000
        for i in actions(board):
            score = MIN_val(result(board,i))
            if(score > bstscore):
                bstscore = score
                move = i
        return move
    else:
        move = None
        bstscore = 10000
        for i in actions(board):
            score = MAX_val(result(board,i))
            if(score < bstscore):
                bstscore = score
                move = i
        return move

    raise NotImplementedError
