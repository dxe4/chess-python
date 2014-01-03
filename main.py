from game import chess
import game

board = chess.Board(player_down=game.player_down)
game_engine = chess.GameEngine(board)

game_engine.move((1, 1), (1, 2), "W")
game_engine.move((1, 2), (1, 3), "W")
print(board)
print(game_engine.moves)
print(game_engine.moves[0].piece)
print(game_engine.moves[1].piece)
game_engine.moves[1].undo(board)
print(board)
