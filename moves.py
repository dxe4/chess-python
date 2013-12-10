from itertools import product
from itertools import chain
from functools import wraps


def move(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        x, y = args
        moves = f(x, y)
        if (x, y) in moves: moves.remove((x, y))
        return moves
    return wrapper


def check_range(x):
    return x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8


@move
def knight(x, y):
    moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
    moves = {(x, y) for x, y in moves if check_range((x, y))}
    return moves


@move
def rook(x, y):
    return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})


@move
def bishop(x, y):
    possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
    return {j for i in range(1, 8) for j in possible(i) if check_range(j)}
