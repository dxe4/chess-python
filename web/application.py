from flask import jsonify, redirect, request, session
from web import web_app
from flask import send_file
from flask import url_for, Response, jsonify, make_response
from flask_login import flash, login_user, login_required, logout_user
from web.models import User
from time import sleep


@web_app.route('/')
def home():
    return send_file("templates/interface.html")

@web_app.route("/bar", methods=["GET"])
def search():
    website = request.args.get('website')
    return jsonify(results=list(filter(lambda x: website in x["name"], {})))


def event_stream():
    count = 0
    while True:
        sleep(1)
        #'retry: 10000\n\ndata: %s\n\n' % event['data']
        yield """
            retry: 10000\ndata:{"count":%s, "message":%s}\n\n
        """ % (count, '"it works!"')
        count += 1


@web_app.route("/stream")
def stream():
    return Response(
        event_stream(),
        mimetype='text/event-stream')


@web_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # login and validate the user...
        user = User(request.args.get['username'])
        login_user(user)
        flash("Logged in successfully.")
        return make_response("OK", 200)
    else:
        return make_response("", 404)
        #redirect(request.args.get("next") or url_for(".home"))


@web_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))