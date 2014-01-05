from itertools import product
from collections import OrderedDict
from copy import deepcopy
from . import Rook, Bishop, Pawn, Queen, King, Knight, Piece

color_change = {"W": "B", "B": "W"}


class Board(OrderedDict):

    """
        Holds the state but has no logic. All logic is done in GameEngine
    """

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

    def __eq__(self, other) -> bool:
        if not other or not isinstance(other, self.__class__):
            return False
        return self.get_pieces("W") == other.get_pieces("W") \
            and self.get_pieces("B") == other.get_pieces("B") \
            and self.killed == other.killed \
            and self.player_down == other.player_down \
            and self.turn == other.turn

    def flip_color(self):
        self.turn = color_change[self.turn]

    def get_pieces(self, color: str):
        # todo cache after moves
        return {piece for position, piece in self.items() if piece and piece.color is color}

    def _color_picker(self, index: int):
        if self.player_down is "W":
            return "W" if index > 3 else "B"
        elif self.player_down is "B":
            return "B" if index > 3 else "W"
        else:
            raise TypeError("player down must be W or B")

    def _get_row(self, y: int) -> tuple:
        """
            Return the whole row as a generator(filter) and a color for the row
        @param y: y position of the row
        @return: (row,color)
        """
        return filter(lambda x: x[1] is y, self.keys()), self._color_picker(y)

    def _add_pawns(self, y: int):
        positions, color = self._get_row(y)
        for i in positions:
            self[i] = Pawn(color, i, self.player_down)

    def _add_other(self, y: int):
        positions, color = self._get_row(y)
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

    def __hash__(self):
        return hash(" ".join(map(str, self.piece, self.start, self.end, self.killed)))

    def __eq__(self, other):
        if not other or not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "%s -> moved from: %s killed: %s" % (self.piece, self.start, self.killed)

    def exec(self, board: Board):
        board[self.piece.position] = None  # remove the piece from the board
        self.piece.update_position(self.end)  # move the piece
        if board[self.end]:  # kill previous piece if existed
            self.killed = board[self.end]
            board.killed.append(self.killed)
        board[self.end] = self.piece  # make the move on the board
        self.piece.increase_moves()

    def undo(self, board: Board):
        board[self.start] = self.piece
        self.piece.update_position(self.start)
        board[self.end] = self.killed
        self.piece.decrease_moves()


class GameEngine:

    """
        Creates and executes move. The only class changing state on pieces and board.
        The main idea is to keep mutation controlled in one place
    """

    def __init__(self, board: Board):
        self.board = board
        self.moves = []
        self.undone_moves = []

    def king_attacked(self):
        # todo refactor cache pieces
        _color = color_change[self.board.turn]
        opposite_team = self.board.get_pieces(_color)
        current_team = self.board.get_pieces(self.board.turn)
        king = [piece for piece in current_team if isinstance(piece, King)][0]
        opposite_attackers = [piece.check_move(king.position, self.board) for piece in opposite_team]
        return len([move for move in opposite_attackers if move]) >= 1

    def _move(self, piece: Piece, end: tuple):
        move = Move(piece, end)
        move.exec(self.board)
        self.moves.append(move)

    def move(self, start: tuple, end: tuple, player: str):
        if player is not self.board.turn:
            raise Exception("Its not your turn. Given %s expected %s" % (player, self.board.turn))
        piece = self.board[start]
        # illegal move
        if not piece or not piece.check_move(end, self.board):
            return False
        # move and check if king is under attack
        self._move(piece, end)
        # move is invalid undo
        if self.king_attacked():
            self.undo()
        else:
            self.board.flip_color()
            return True

    def undo(self, move: Move=None):
        if not move:
            move = self.moves.pop()
        move.undo(self.board)
        self.undone_moves.append(move)
        self.board.flip_color()
