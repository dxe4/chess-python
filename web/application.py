from flask import jsonify, redirect, request, session
from web import web_app
from flask import send_file, session
from flask import url_for, Response, jsonify, make_response
from flask_login import flash, login_user, login_required, logout_user
from web.models import User
from time import sleep


@web_app.route('/')
def home():
    return send_file("templates/index.html")


@web_app.route('/templates/<path:path>')
def static_proxy(path):
    return send_file("templates/%s" % path)


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


@web_app.route("/login", methods=["POST"])
def login():
    if not request.method == 'POST':
        return make_response("", 404)

    if session and "user_id" in session:
        user_id = session["user_id"]
        if user_id:
            return make_response(user_id, 200)

    _json = request.get_json(force=True)
    user = User(_json['username'])
    login_user(user)
    flash("Logged in successfully.")
    return make_response(_json['username'], 200)


@web_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))