from game import chess
import game
from web import web_app
from api import api_app
from flask import Flask
from werkzeug.wsgi import DispatcherMiddleware

application = Flask(__name__)
application.wsgi_app = DispatcherMiddleware(web_app, {'/api': api_app})


board = chess.Board(player_down=game.player_down, create=True)
game_engine = chess.GameEngine(board)
print(board)
