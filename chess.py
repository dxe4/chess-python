from itertools import product
from collections import OrderedDict

#r rook, k knight, b bishop, q queen, k king

def create_board(player_down="w"):
    board = {i: None for i in product(range(0, 8), range(0, 8))}

    def color_picker(index:int):
        if player_down == "w":
            return "w" if index > 3 else "b"
        else:
            return "w" if index < 3 else "b"

    def get_row(row:int):
        return filter(lambda x: x[1] == row, board.keys()),color_picker(row)

    def add_pawns(keys, color:str):
        for i in keys: board[i] = (color, "p")

    def add_other(keys, color:str):
        keys = sorted(keys, key=lambda x: x[0])
        pieces = ["r", "k", "b", "q", "k", "b", "k", "r"]
        for count, i in enumerate(keys): board[i] = (color,pieces[count])

    add_pawns(*get_row(1))
    add_pawns(*get_row(6))

    add_other(*get_row(0))
    add_other(*get_row(7))

    return board


print(create_board(player_down="w"))

