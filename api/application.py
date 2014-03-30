import json
from time import sleep
from flask import Response, session
from asyncio_redis import Pool
from api import api_app
from api import start_queue, games, pending
import game


@api_app.route("/initial_board", methods=["GET"])
def initial_board():
    game_engine = game.make_game_engine("B")
    json_dict = game_engine.board.json_dict()
    json_dict["moves"] = game_engine.possible_moves(json=True)
    return Response(json.dumps(json_dict), mimetype='application/json')

def make_game():
    game_engine = game.make_game_engine("W")
    games[game_engine.uuid] = game_engine
    return game_engine.uuid

def event_stream(id):
    count = 0
    msg = """
        retry: 10000\ndata:{"count":%s, "message":%s, "game":%s}\n\n
    """
    while True:
        sleep(1)
        #'retry: 10000\n\ndata: %s\n\n' % event['data']
        if id in pending:
            game_id = pending[id]
            del pending[id]
            yield msg % (count, '"done"', '"%s"' % game_id)
        elif len(start_queue) > 1:
           # TODO that won't do for big queue but for now its fine
            first_ids = start_queue[0], start_queue[1]
            if id in first_ids:
                game_id = make_game()
                pending_id = next((i for i in first_ids if i != id))
                pending[pending_id] = game_id
                yield msg % (count, '"done"', '"%s"' % game_id)
        else:
            yield msg % (count, '"wait"', '""')
        count += 1


@api_app.route("/join_queue", methods=["GET"])
def join_queue():
    id = session["_id"]
    start_queue.append(id)
    return Response(event_stream(id), mimetype='text/event-stream')