from itertools import product
from . import Rook, Bishop, Pawn, Queen, King, Knight
from collections import OrderedDict


class Board(OrderedDict):
    def __init__(self, player_down:str="W"):
        super(Board, self).__init__()
        board = {i: None for i in product(range(0, 8), range(0, 8))}
        self.update(sorted(board.items(), key=lambda x: x[0][0] + ((1 + x[0][1]) * 100)))

        self.player_down = player_down
        self._add_pawns(1)
        self._add_pawns(6)
        self._add_other(0)
        self._add_other(7)

        self.turn = "W"

    def move(self, start:tuple, end:tuple):
        print(self[start].check_move(end,self))

    def _color_picker(self, index:int):
        if self.player_down is "W":
            return "W" if index > 3 else "B"
        elif self.player_down is "B":
            return "B" if index > 3 else "W"
        else:
            raise TypeError("player down must be W or B")


    def _get_row(self, row:int):
        return filter(lambda x: x[1] is row, self.keys()), self._color_picker(row)


    def _add_pawns(self, row:int):
        positions, color = self._get_row(row)
        for i in positions:
            self[i] = Pawn(color, i)


    def _add_other(self, row:int):
        positions, color = self._get_row(row)
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for count, i in enumerate(positions):
            self[i] = pieces[count](color, i)


    def __repr__(self):
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
        to_join = []
        #top row numbers (x)
        to_join.extend(["  ", spaces.join(map(str, range(0, 8))), "\n"])
        for position, piece in self.items():
            to_print = repr(piece) if piece else ""
            #start of row print y
            if position[0] == 0: to_join.append("%i  " % position[1])
            #print content with spaces
            to_join.append(to_print)
            to_join.append(" " * (spaces_count + 1 - len(to_print)))
            #end of row print new line
            if position[0] == 7: to_join.append("\n")
        return "".join(to_join)



