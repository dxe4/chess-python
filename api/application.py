import json
from api import api_app
from api import start_queue
from flask import Response, session
import game
from time import sleep


@api_app.route("/initial_board", methods=["GET"])
def initial_board():
    game_engine = game.make_game_engine("B")
    json_dict = game_engine.board.json_dict()
    json_dict["moves"] = game_engine.possible_moves(json=True)
    return Response(json.dumps(json_dict), mimetype='application/json')


def event_stream():
    count = 0
    msg = """
        retry: 10000\ndata:{"count":%s, "message":%s, "game":%s}\n\n
    """
    while True:
        sleep(1)
        #'retry: 10000\n\ndata: %s\n\n' % event['data']
        if start_queue.qsize() > 1:
            yield msg % (count, '"wait"', '"None"')
        else:
            yield msg % (count, '"wait"', '"None"')
        count += 1


@api_app.route("/join_queue", methods=["GET"])
def join_queue():
    start_queue.put_nowait(session["_id"])
    return Response(event_stream(), mimetype='text/event-stream')