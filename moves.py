from itertools import product
from itertools import chain
from functools import wraps
from math import atan2

_angle_to_direction = {90: "up", -90: "down", 180: "right", 0: "left", -135: "right_down", 135: "right_up",
                       45: "left_up", -45: "left_down"}


def move(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        x, y = args
        moves = f(x, y)
        if (x, y) in moves: moves.remove((x, y))
        return moves

    return wrapper


def check_range(x:int) -> bool:
    return x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8


@move
def _knight(x:int, y:int) -> set:
    moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
    moves = {(x, y) for x, y in moves if check_range((x, y))}
    return moves


@move
def _rook(x:int, y:int) -> set:
    return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})


@move
def _bishop(x:int, y:int) -> set:
    possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
    return {j for i in range(1, 8) for j in possible(i) if check_range(j)}


def direction(start:tuple, end:tuple) -> str:
    delta_a = start[1] - end[1]
    delta_b = start[0] - end[0]
    return _angle_to_direction[int(atan2(delta_a, delta_b) * 180 / 3.14)]


def _blocks(start:tuple, end:tuple, pattern) -> bool:
    pass


def knight(start:tuple, end:tuple, board:dict) -> tuple:
    possible = _knight(*start)


def rook(start:tuple, end:tuple, board:dict) -> tuple:
    possible = _rook(*start)
    print(possible)


def bishop(start, end, board):
    possible = _bishop(*start)


rook((3, 3), (3, 7), None)




#0y [0, 1, 2, 3, 4, 5, 6, 7]x
#1y [0, 1, 2, 3, 4, 5, 6, 7]x
#2y [0, 1, 2, 3, 4, 5, 6, 7]x
#3y [0, 1, 2, 3, 4, 5, 6, 7]x
#4y [0, 1, 2, 3, 4, 5, 6, 7]x
#5y [0, 1, 2, 3, 4, 5, 6, 7]x
#6y [0, 1, 2, 3, 4, 5, 6, 7]x
#7y [0, 1, 2, 3, 4, 5, 6, 7]x


