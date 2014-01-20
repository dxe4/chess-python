from flask import render_template
from flask import jsonify
from flask import request
from api import api_app
from flask import make_response


@api_app.route("/foo", methods=["PUT"])
def vote_website():
    try:
        return make_response("OK", 200)
    except Exception as e:
        return make_response('NOT OK', 200)
