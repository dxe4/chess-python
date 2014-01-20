from flask import render_template
from flask import jsonify
from flask import request
from web import web_app
from flask import send_file
from flask import url_for

@web_app.route('/')
def home():
    # make_response(open('templates/index.html').read())
    return send_file("templates/interface.html")


@web_app.route('/foo')
def results():
    return jsonify(results={})


@web_app.route("/bar", methods=["GET"])
def search():
    website = request.args.get('website')
    return jsonify(results=list(filter(lambda x: website in x["name"], {})))


@web_app.route("/baz", methods=["GET"])
def about():
    return "about"


@web_app.route("/eggs", methods=["GET"])
def results_today():
    return jsonify(results={})
