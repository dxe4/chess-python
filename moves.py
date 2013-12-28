from itertools import product
from itertools import chain
from functools import wraps
from math import fabs
from abc import ABCMeta
from abc import abstractmethod
from chess import player_down

"""
The plan is to cache all possible moves ignoring board state,
so on runtime you can get a set and check the state of the board (will save time in case of AI)
"""


def check_range(move:tuple, min=0, max=8) -> bool:
    """
        Check if a point is within a range. The default range is 0,8.
    @param move: The move to check
    @param min: Minimum allowed value of the point (included)
    @param max: Maximum allowed value of the point (excluded)
    @return: True if in range else False
    """
    return min <= move[0] < max and min <= move[1] < max


def _slope(start:tuple, end:tuple) -> int:
    """
        For the math formula of the line.
    @return: slope int
    """
    return (start[1] - end[1]) / (start[0] - end[0])


def _line(slope:int, end:tuple) -> callable:
    """
        Line math formula
    @param slope: Slope for line as generated by _slope
    @return: lambda expression representing the line
    """
    return lambda x, y: y - end[1] == slope * (x - end[0])


def _safe_divide(a:int, b: int) -> int:
    """
        Return 0 if dividing by 0
    """
    if b == 0: return 0
    return a / b


def _diff_points(start:tuple, end:tuple) -> tuple:
    """
        Calculate a tuple to identify how we move.
        For (3,3),(5,5) will return (-1,-1) identifying that both x and y increase
        (3, 3) (0, 0) will return  (1, 1) identifying that both x and y decrease
    """
    x = start[0] - end[0]
    y = start[1] - end[1]
    return _safe_divide(x, fabs(x)), _safe_divide(y, fabs(y))


def _move(f):
    #TODO may not be needed
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        return {move for move in moves if check_range(move)} - {args}

    return wrapper


def _filter_line(f):
    #TODO documentat since this is a confusing part
    @wraps(f)
    def wrapper(*args, **kwargs):
        moves = f(*args, **kwargs)
        start, end = args[0].position, args[1]
        slope = _slope(start, end)
        line = _line(slope, end)
        diff = _diff_points(start, end)
        end_point_check = \
            lambda move, end: move <= end if diff[0] == -1 or diff[1] == -1 else  lambda move, end: move >= end
        return \
            {move for move in moves if line(*move) and _diff_points(start, move) == diff and end_point_check(move, end)}

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

    def __repr__(self):
        return "%s %s " % (type(self).__name__, self.color)

    def __str__(self):
        return "%s %s" % (repr(self), str(self.position))


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
        y_initial,y_add= (1, 1) if self.color == player_down else (6, -1)
        moves = {(x, y + y_add)}
        if y == y_initial:#first position can move two
            moves.add((x, y + y_add * 2))
        return {move for move in moves if check_range(move)} - {(x,y)}

    def move(self, end:tuple, board:dict) -> set:
        #TODO en passant move
        return self.find(*self.position[0])



class King(Piece):
    def find(self, x:int, y:int) -> set:
        return set(product([x - 1, x + 1, x], [y + 1, y - 1, y])) - {(x, y)}

    def move(self, end:tuple, board:dict):
        return self.find(*self.position)


class Queen(Piece):
    def find(self, x:int, y:int):
        pass

    def move(self, end:tuple, board:dict):
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



