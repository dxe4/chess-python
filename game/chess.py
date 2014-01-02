from itertools import product
from . import Rook, Bishop, Pawn, Queen, King, Knight, Piece
from collections import OrderedDict
from copy import deepcopy


class Board(OrderedDict):

    def __init__(self, player_down: str="W"):
        super(Board, self).__init__()
        board = {i: None for i in product(range(0, 8), range(0, 8))}
        self.update(sorted(board.items(), key=lambda x: x[0][0] + ((1 + x[0][1]) * 100)))

        self.player_down = player_down
        self._add_pawns(1)
        self._add_pawns(6)
        self._add_other(0)
        self._add_other(7)

        self.killed = []
        self.turn = "W"

    def _color_picker(self, index: int):
        if self.player_down is "W":
            return "W" if index > 3 else "B"
        elif self.player_down is "B":
            return "B" if index > 3 else "W"
        else:
            raise TypeError("player down must be W or B")

    def _get_row(self, row: int):
        return filter(lambda x: x[1] is row, self.keys()), self._color_picker(row)

    def _add_pawns(self, row: int):
        positions, color = self._get_row(row)
        for i in positions:
            self[i] = Pawn(color, i)

    def _add_other(self, row: int):
        positions, color = self._get_row(row)
        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for count, i in enumerate(positions):
            self[i] = pieces[count](color, i)

    def __repr__(self):
        spaces_count = 15
        spaces = spaces_count * " "
        to_join = []
        # top row numbers (x)
        to_join.extend(["  ", spaces.join(map(str, range(0, 8))), "\n"])
        for position, piece in self.items():
            to_print = repr(piece) if piece else ""
            # start of row print y
            if position[0] == 0:
                to_join.append("%i  " % position[1])
            # print content with spaces
            to_join.append(to_print)
            to_join.append(" " * (spaces_count + 1 - len(to_print)))
            # end of row print new line
            if position[0] == 7:
                to_join.append("\n")
        return "".join(to_join)


class Move:

    def __init__(self, piece: Piece, end: tuple):
        self.piece = deepcopy(piece)
        self.start = piece.position
        self.end = end
        self.killed = None

    def exec(self, board: Board):
        board[self.piece.position] = None  # remove the piece from the board
        self.piece.position = self.end  # move the piece
        if board[self.end]:  # kill previous piece if existed
            self.killed = board[self.end]
            board.killed.append(self.killed)
        board[self.end] = self.piece  # make the move on the board

    def undo(self):
        # TODO implement me
        raise NotImplementedError()

    def __repr__(self):
        return "%s -> moved from: %s killed: %s" % (self.piece, self.start, self.killed)


class GameEngine:

    def __init__(self, board: Board):
        self.board = board
        self.moves = []

    def _move(self, piece: Piece, end: tuple):
        move = Move(piece, end)
        move.exec(self.board)
        self.moves.append(move)

    def move(self, start: tuple, end: tuple, player: str):
        if player is not self.board.turn:
            raise Exception("Its not your turn. Given %s expected %s" % (player, self.board.turn))
        piece = self.board[start]
        if piece.check_move(end, self.board):
            self._move(piece, end)
            return True
