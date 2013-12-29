from itertools import product
from . import Rook,Bishop,Pawn,Queen,King,Knight

def create_board(player_down="w"):
    board = {i: None for i in product(range(0, 8), range(0, 8))}

    def color_picker(index:int):
        if player_down == "w":
            return "w" if index > 3 else "b"
        else:
            return "b" if index > 3 else "w"

    def get_row(row:int):
        return filter(lambda x: x[1] == row, board.keys()), color_picker(row)

    def add_pawns(row):
        keys,color = get_row(row)
        for i in keys:board[i] = Pawn(color, i)

    def add_other(row):
        keys,color = get_row(row)
        keys = sorted(keys, key=lambda x: x[0])
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for count, i in enumerate(keys): board[i] = pieces[count](color,i)

    add_pawns(1)
    add_pawns(6)

    add_other(0)
    add_other(7)

    return board

