from .moves import Rook,Bishop,Pawn,Queen,King,Knight

bishop = Bishop("w", (3, 3))
_ = bishop.move((5, 5), {})
print(_)

rook = Rook("w", (0, 0))
_ = rook.move((7, 0), {})
print(_)

rook = Rook("w", (7, 0))
_ = rook.move((0, 0), {})
print(_)

queen = Queen("w", (0, 0))
_ = queen.move((7, 0), {})
print(_)

_ = queen.move((5, 5), {})
print(_)

knight = Knight("w", (0, 0))
_ = knight.move((2, 1), {})
print(_)