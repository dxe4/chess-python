from itertools import product
from itertools import chain
from functools import wraps


def _wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        x, y = args
        moves = f(x, y)
        if (x, y) in moves: moves.remove((x, y))
        return moves
    return wrapper


def check_range(x):
    return x[0] >= 0 and x[1] >= 0 and x[0] < 8 and x[1] < 8


@_wrapper
def knight(x, y):
    moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
    moves = {(x, y) for x, y in moves if check_range((x, y))}
    return moves


@_wrapper
def rook(x, y):
    return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})


@_wrapper
def bishop(x, y):
    possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
    return {j for i in range(1, 8) for j in possible(i) if check_range(j)}


for k in range(0, 8):
    print(k, [i for i in range(0, 8)])

assert knight(5, 4) == {(7, 3), (7, 5), (3, 3), (6, 6), (6, 2), (4, 2), (3, 5), (4, 6)}
assert rook(5, 5) == {(5, 4), (1, 5), (5, 6), (5, 7), (4, 5), (7, 5), (0, 5), (5, 0), (5, 1), (2, 5), (3, 5), (5, 2), (6, 5), (5, 3)}
assert bishop(2, 2) == {(1, 3), (3, 3), (6, 6), (5, 5), (3, 1), (4, 4), (7, 7), (0, 0), (0, 4), (1, 1), (4, 0)}
