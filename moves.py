from itertools import product
from itertools import chain
from functools import wraps


def check_range(x:tuple, min=0, max=8) -> bool:
    return min <= x[0] < max and min <= x[1] < max


def move(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        return {i for i in moves if check_range(i)} - {args}

    return wrapper


@move
def _knight(x:int, y:int) -> set:
    moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
    return {(x, y) for x, y in moves}


@move
def _rook(x:int, y:int) -> set:
    return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})


@move
def _bishop(x:int, y:int) -> set:
    possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
    return {j for i in range(1, 8) for j in possible(i)}


def knight(start:tuple, end:tuple, board:dict) -> tuple:
    return _knight(*start)


def rook(start:tuple, end:tuple, board:dict) -> tuple:
    return _rook(*start)


def bishop(start:tuple, end:tuple, board:dict):
    return _bishop(*start)


def pawn(start:tuple, end:tuple, board:dict, player_pos:str, player_down:str) -> set:
    #TODO en passant move
    rule = (1, 1) if player_pos == player_down else (7, -1)
    moves = {(start[0], start[1] + rule[1])}
    if start[1] == rule[0]: moves.add((start[0], start[1] + rule[1]*2))
    return {i for i in moves if check_range(i)} - {start}


def _king(x:int, y:int) -> set:
    pass


print(bishop((3, 3), (5, 5), {}))
print(rook((0, 0), (7, 0), {}))

print(pawn((1,1),(2,2),{},"w","w"))
print(pawn((1,7),(1,6),{},"w","b"))
print(pawn((1,7),(1,6),{},"w","w"))
#0y [0, 1, 2, 3, 4, 5, 6, 7]x
#1y [0, 1, 2, 3, 4, 5, 6, 7]x
#2y [0, 1, 2, 3, 4, 5, 6, 7]x
#3y [0, 1, 2, 3, 4, 5, 6, 7]x
#4y [0, 1, 2, 3, 4, 5, 6, 7]x
#5y [0, 1, 2, 3, 4, 5, 6, 7]x
#6y [0, 1, 2, 3, 4, 5, 6, 7]x
#7y [0, 1, 2, 3, 4, 5, 6, 7]x





