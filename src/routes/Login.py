from bson import json_util
from bson.objectid import ObjectId
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from flask_session import Session

from decorators import wrap_response
from database import DB

UserRepository = DB()
Login = Blueprint("Login", __name__)


@Login.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        data = request.get_json()
        if UserRepository.find_one("user", {"document": data.document}):
            flash('Error document not defined')
        session¨["current_user"] = {"id": data.document, "name": "user1", "is_authenticated": True}
        return redirect(url_for('main'))
    return render_template("templates/login.html", title="login", error=error)


@Login.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("Login.login"))


@Login.route("/main", methods=["GET"])
# @user_required
def main():
    return render_template("templates/main.html", title="main", user = current_user, datos="")    # return redirect(url_for("Login.login"))
