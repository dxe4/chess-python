import moves

assert moves._knight(5, 4) == {(7, 3), (7, 5), (3, 3), (6, 6), (6, 2), (4, 2), (3, 5), (4, 6)}
assert moves._rook(5, 5) == {(5, 4), (1, 5), (5, 6), (5, 7), (4, 5), (7, 5), (0, 5), (5, 0), (5, 1), (2, 5), (3, 5), (5, 2), (6, 5), (5, 3)}
assert moves._bishop(2, 2) == {(1, 3), (3, 3), (6, 6), (5, 5), (3, 1), (4, 4), (7, 7), (0, 0), (0, 4), (1, 1), (4, 0)}

assert moves.direction((3,3),(3,0)) == "up" #90
assert moves.direction((3,3),(3,7)) == "down" #-90
assert moves.direction((0,0),(7,0)) == "right" #180
assert moves.direction((7,0),(0,0)) == "left" #0
assert moves.direction((0,0),(3,3)) == "right_down" #-135
assert moves.direction((3,3),(6,0)) == "right_up" #135
assert moves.direction((3,3),(0,0)) == "left_up" #45
assert moves.direction((3,3),(0,6)) == "left_down" #-45
