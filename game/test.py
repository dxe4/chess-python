import unittest
from game.chess import Rook, Bishop, Pawn, Queen, King, Knight
from game.chess import Board, GameEngine
import game


class TestInitialState(unittest.TestCase):

    def setUp(self):
        self.board = Board(player_down=game.player_down, create=True)
        self.black_knight = self.board[1, 7]
        self.black_knight_2 = self.board[6, 7]

        self.white_knight = self.board[1, 0]
        self.white_knight_2 = self.board[6, 0]

        self.white_rook = self.board[0, 0]
        self.white_rook_2 = self.board[7, 0]

    def test_board_init(self):
        assert isinstance(self.white_rook, Rook)
        assert isinstance(self.white_rook_2, Rook)
        assert isinstance(self.black_knight, Knight)
        assert isinstance(self.black_knight_2, Knight)

        assert self.white_rook.color is "W"
        assert self.white_rook_2.color is "W"
        assert self.black_knight.color is "B"
        assert self.black_knight_2.color is "B"

    def test_possible_moves_knights(self):
        # black knight
        assert self.black_knight.check_move((0, 5), self.board)
        assert self.black_knight.check_move((2, 5), self.board)

        assert self.black_knight_2.check_move((7, 5), self.board)
        assert self.black_knight_2.check_move((5, 5), self.board)

        # white knight
        assert self.white_knight.check_move((0, 2), self.board)
        assert self.white_knight_2.check_move((7, 2), self.board)

        assert self.white_knight.check_move((2, 2), self.board)
        assert self.white_knight_2.check_move((5, 2), self.board)

    def test_impossible_moves(self):
        assert not self.white_rook.check_move((5, 5), self.board)
        assert not self.white_rook.check_move((7, 0), self.board)
        assert not self.white_rook.check_move((0, 7), self.board)

        assert not self.white_knight_2.check_move((0, 0), self.board)
        assert not self.white_knight.check_move((3, 1), self.board)


class TestModernDefence(unittest.TestCase):

    """
        http://www.chess.com/opening/eco/B06_Modern_Defense_Standard_Defense
    """

    def setUp(self):
        self.board = Board(player_down="W", create=True)
        self.game_engine = GameEngine(self.board)

    def test_moves(self):
        assert self.board.player_down is "W"

        assert self.game_engine.move((4, 6), (4, 4), "W")
        assert self.game_engine.move((6, 1), (6, 2), "B")

        assert self.game_engine.move((3, 6), (3, 4), "W")
        assert self.game_engine.move((5, 0), (6, 1), "B")

        assert self.game_engine.move((1, 7), (2, 5), "W")
        assert self.game_engine.move((3, 1), (3, 2), "B")

        self.assertRaises(Exception, self.wrong_player_moved)

        assert len(self.board.moves) is 6
        assert self.board.turn is "W"

        # undo all moves
        for i in range(0, len(self.board.moves)):
            self.game_engine.undo()
        # assert undo was fine
        assert self.board == Board(player_down="W", create=True)
        assert not self.board == Board(player_down="B", create=True)
        assert self.board.turn is "W"
        assert not self.board.moves

    def wrong_player_moved(self):
        # TODO move in separate class and make it generic, for now its fine
        assert self.game_engine.move((0, 1), (0, 2), "B")


class TestCastling(unittest.TestCase):

    def setUp(self):
        self.board = Board(player_down="W", create=False)
        self.game_engine = GameEngine(self.board)
        self._add_piece((4, 7), "W", King)
        self._add_piece((0, 7), "W", Rook)
        self._add_piece((7, 7), "W", Rook)

        self._add_piece((4, 0), "B", King)
        self._add_piece((0, 0), "B", Rook)
        self._add_piece((7, 0), "B", Rook)

    def _add_piece(self, start: tuple, color: str, clazz):
        self.board[start] = clazz(color, start)

    def test_white(self):
        # white
        assert self.game_engine.move((4, 7), (6, 7), "W")
        self.game_engine.undo()
        assert self.game_engine.move((4, 7), (2, 7), "W")
        # black
        assert self.game_engine.move((4, 0), (2, 0), "B")
        self.game_engine.undo()
        assert self.game_engine.move((4, 0), (6, 0), "B")

        assert isinstance(self.board[2, 7], King)
        assert isinstance(self.board[3, 7], Rook)
        assert isinstance(self.board[7, 7], Rook)

        assert isinstance(self.board[6, 0], King)
        assert isinstance(self.board[5, 0], Rook)
        assert isinstance(self.board[0, 0], Rook)


if __name__ == '__main__':
    unittest.main()
