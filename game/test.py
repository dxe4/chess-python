import unittest
from game.moves import Rook, Bishop, Pawn, Queen, King, Knight
from game.chess import Board
import game


class TestInitialState(unittest.TestCase):

    def setUp(self):
        self.board = Board(player_down=game.player_down)
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


class TestMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board(player_down=game.player_down)

if __name__ == '__main__':
    unittest.main()
