from itertools import product
from itertools import chain
from functools import wraps
from math import fabs
from abc import ABCMeta
from abc import abstractmethod

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


def _filter_line(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        start, end = args[0].position, args[1]
        slope = _slope(start, end)
        line = _line(slope, end)
        diff = _diff_points(start, end)
        end_point_check = lambda i, end: i <= end if diff[0] == -1 or diff[1] == -1 else  lambda i, end: i >= end
        return {i for i in moves if line(*i) and _diff_points(start, i) == diff and end_point_check(i, end)}

    return wrapper


class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, color:str, position:tuple):
        self.color = color
        self.position = position

    @abstractmethod
    def find(self, x:int, y:int): pass

    @abstractmethod
    def move(self, end:tuple, board:dict): pass


class Rook(Piece):
    @_move
    def find(self, x:int, y:int) -> set:
        return {(x, i) for i in range(0, 8)}.union({(i, y) for i in range(0, 8)})

    @_filter_line
    def move(self, end:tuple, board:dict) -> tuple:
        moves = self.find(*self.position)
        return moves


class Bishop(Piece):
    @_move
    def find(self, x:int, y:int) -> set:
        possible = lambda k: [(x + k, y + k), (x + k, y - k), (x - k, y + k), (x - k, y - k)]
        return {j for i in range(1, 8) for j in possible(i)}

    @_filter_line
    def move(self, end:tuple, board:dict):
        return self.find(*self.position)


class Knight(Piece):
    @_move
    def find(self, x:int, y:int) -> set:
        moves = chain(product([x - 1, x + 1], [y - 2, y + 2]), product([x - 2, x + 2], [y - 1, y + 1]))
        return {(x, y) for x, y in moves}

    def knight(self, end:tuple, board:dict) -> tuple:
        return self.find(*self.position)


class Pawn(Piece):
    def find(self, x:int, y:int):
        pass

    def move(self, end:tuple, board:dict) -> set:
        player_down = "w"
        #TODO en passant move
        rule = (1, 1) if self.color == player_down else (7, -1)
        moves = {(self.position[0], self.position[1] + rule[1])}
        if self.position[1] == rule[0]: moves.add((self.position[0], self.position[1] + rule[1] * 2))
        return {i for i in moves if check_range(i)} - {self.position}


class King(Piece):
    def find(self, x:int, y:int) -> set:
        return set(product([x - 1, x + 1, x], [y + 1, y - 1, y])) - {(x, y)}

    def move(self, end:tuple, board:dict):
        return self.find(*self.position)


class Queen(Piece):
    def find(self, x:int, y:int):
        print("q")

    def move(self, x:int, y:int):
        pass


bishop = Bishop("w", (3, 3))
_ = bishop.move((5, 5), {})
print(_)

rook = Rook("w", (0, 0))
_ = rook.move((7, 0), {})
print(_)

rook = Rook("w", (7, 0))
_ = rook.move((0, 0), {})
print(_)
#pawn = Pawn("w")
#
#print(pawn((1, 1), (2, 2), {}, "w", "w"))
#print(pawn((1, 7), (1, 6), {}, "w", "b"))
#print(pawn((1, 7), (1, 6), {}, "w", "w"))

#_king(5, 5)
#0y [0, 1, 2, 3, 4, 5, 6, 7]x
#1y [0, 1, 2, 3, 4, 5, 6, 7]x
#2y [0, 1, 2, 3, 4, 5, 6, 7]x
#3y [0, 1, 2, 3, 4, 5, 6, 7]x
#4y [0, 1, 2, 3, 4, 5, 6, 7]x
#5y [0, 1, 2, 3, 4, 5, 6, 7]x
#6y [0, 1, 2, 3, 4, 5, 6, 7]x
#7y [0, 1, 2, 3, 4, 5, 6, 7]x



