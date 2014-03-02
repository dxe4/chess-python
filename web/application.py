from flask import jsonify, redirect, request, session
from web import web_app
from flask import send_file
from flask import url_for
from flask_login import flash, login_user, login_required, logout_user
from web.models import User

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


# @web_app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('.home'))
#     return '''
#         <form action="" method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

@web_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # login and validate the user...
        user = User(request.form['username'])
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for(".home"))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@web_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.home'))