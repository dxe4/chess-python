from itertools import product
from . import Rook, Bishop, Pawn, Queen, King, Knight
from collections import OrderedDict
from operator import itemgetter


def create_board(player_down="W"):
    #TODO probably need a class later on
    board = {i: None for i in product(range(0, 8), range(0, 8))}
    #sort but give priority to x instead of y using ((1 + x[0][1]) * 100))
    board = OrderedDict(sorted(board.items(), key=lambda x: x[0][0] + ((1 + x[0][1]) * 100)))

    def color_picker(index:int):
        if player_down == "W":
            return "W" if index > 3 else "B"
        else:
            return "B" if index > 3 else "W"

    def get_row(row:int):
        return filter(lambda x: x[1] == row, board.keys()), color_picker(row)

    def add_pawns(row):
        keys, color = get_row(row)
        for i in keys:
            board[i] = Pawn(color, i)

    def add_other(row):
        keys, color = get_row(row)
        keys = sorted(keys, key=lambda x: x[0])
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for count, i in enumerate(keys):
            board[i] = pieces[count](color, i)

    add_pawns(1)
    add_pawns(6)

    add_other(0)
    add_other(7)

    return board


def print_board(board:OrderedDict):
    """
       0               1               2               3               4               5               6               7
    0  W Rook          W Knight        W Bishop        W Queen         W King          W Bishop        W Knight        W Rook
    1  W Pawn          W Pawn          W Pawn          W Pawn          W Pawn          W Pawn          W Pawn          W Pawn
    2
    3
    4
    5
    6  B Pawn          B Pawn          B Pawn          B Pawn          B Pawn          B Pawn          B Pawn          B Pawn
    7  B Rook          B Knight        B Bishop        B Queen         B King          B Bishop        B Knight        B Rook
    """
    spaces_count = 15
    spaces = spaces_count * " "
    #top row numbers (x)
    print("  ", spaces.join(map(str, range(0, 8))))
    for position, piece in board.items():
        to_print = repr(piece) if piece else ""
        #start of row print y
        if position[0] == 0: print("%i  " % position[1], end="")
        #magic
        print(to_print + " " * (spaces_count + 1 - len(to_print)), end="")
        #end of row print new line
        if position[0] == 7: print()




