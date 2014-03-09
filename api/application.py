from flask import render_template
from flask import jsonify
from flask import request
from api import api_app
from flask import make_response, Response, session
import game
import json


@api_app.route("/initial_board", methods=["GET"])
def initial_board():
#     key = request.form["key"]
#     if not key:
#         raise Exception
    # TODO bugged when black
    game_engine = game.make_game_engine("B")
    json_dict = game_engine.board.json_dict()
    json_dict["moves"] = game_engine.possible_moves(json=True)
    return Response(json.dumps(json_dict),  mimetype='application/json')
