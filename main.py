from game import chess
import game

board = chess.Board(player_down=game.player_down)
print(board)
board.move((1,1),(1,2))


