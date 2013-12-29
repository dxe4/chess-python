from .moves import Rook,Bishop,Pawn,Queen,King,Knight
import unittest

class TestThis(unittest.TestCase):

    def setUp(self):pass
    def test_this(self):pass

def test():
    unittest.main()


bishop = Bishop("W", (3, 3))
_ = bishop.move((5, 5), {})
print(_)

rook = Rook("W", (0, 0))
_ = rook.move((7, 0), {})
print(_)

rook = Rook("W", (7, 0))
_ = rook.move((0, 0), {})
print(_)

queen = Queen("W", (0, 0))
_ = queen.move((7, 0), {})
print(_)

_ = queen.move((5, 5), {})
print(_)

knight = Knight("W", (0, 0))
_ = knight.move((2, 1), {})
print(_)