from itertools import product
from itertools import chain
from functools import wraps
from math import fabs

"""
The plan is to cache all possible moves ignoring board state,
so on runtime you can get a set and check the state of the board (will save time in case of AI)
"""


def check_range(x:tuple, min=0, max=8) -> bool:
    return min <= x[0] < max and min <= x[1] < max


def _slope(start:tuple, end:tuple):
    return (start[1] - end[1]) / (start[0] - end[0])


def _line(slope:int, end:tuple):
    return lambda x, y: y - end[1] == slope * (x - end[0])


def _safe_divide(a, b):
    if b == 0: return 0
    return a / b


def _diff_points(start:tuple, end:tuple):
    x = start[0] - end[0]
    y = start[1] - end[1]
    return _safe_divide(x, fabs(x)), _safe_divide(y, fabs(y))


def _move(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        return {i for i in moves if check_range(i)} - {args}

    return wrapper


@_move
def _knight(x:int, y:int) -> set:
    moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
    return {(x, y) for x, y in moves}


@_move
def _rook(x:int, y:int) -> set:
    return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})


@_move
def _bishop(x:int, y:int) -> set:
    possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
    return {j for i in range(1, 8) for j in possible(i)}


def _filter_line(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        start, end = args[0], args[1]
        slope = _slope(start, end)
        line = _line(slope, end)
        diff = _diff_points(start, end)
        end_point_check = lambda i,end:i<=end if diff[0] == -1 or diff[1] == -1 else  lambda i,end:i>=end
        return {i for i in moves if line(*i) and _diff_points(start, i) == diff and end_point_check(i,end)}
    return wrapper


def knight(start:tuple, end:tuple, board:dict) -> tuple:
    return _knight(*start)


@_filter_line
def rook(start:tuple, end:tuple, board:dict) -> tuple:
    moves = _rook(*start)
    return moves


@_filter_line
def bishop(start:tuple, end:tuple, board:dict):
    return _bishop(*start)


def pawn(start:tuple, end:tuple, board:dict, player_pos:str, player_down:str) -> set:
    #TODO en passant move
    rule = (1, 1) if player_pos == player_down else (7, -1)
    moves = {(start[0], start[1] + rule[1])}
    if start[1] == rule[0]: moves.add((start[0], start[1] + rule[1] * 2))
    return {i for i in moves if check_range(i)} - {start}


def _king(x:int, y:int) -> set:
    pass


print(bishop((3, 3), (5, 5), {}))
print(rook((0, 0), (7, 0), {}))
print(rook((7, 0), (0, 0), {}))

print(pawn((1, 1), (2, 2), {}, "w", "w"))
print(pawn((1, 7), (1, 6), {}, "w", "b"))
print(pawn((1, 7), (1, 6), {}, "w", "w"))
#0y [0, 1, 2, 3, 4, 5, 6, 7]x
#1y [0, 1, 2, 3, 4, 5, 6, 7]x
#2y [0, 1, 2, 3, 4, 5, 6, 7]x
#3y [0, 1, 2, 3, 4, 5, 6, 7]x
#4y [0, 1, 2, 3, 4, 5, 6, 7]x
#5y [0, 1, 2, 3, 4, 5, 6, 7]x
#6y [0, 1, 2, 3, 4, 5, 6, 7]x
#7y [0, 1, 2, 3, 4, 5, 6, 7]x





