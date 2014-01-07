from game import chess
import game

board = chess.Board(player_down=game.player_down, create=True)
game_engine = chess.GameEngine(board)
print(board)
