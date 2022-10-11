from bson import json_util
from bson.objectid import ObjectId
from flask import (
    current_app,
    Blueprint,
    json,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    session,
)

from decorators import wrap_response
from mongodb import mongo

Login = Blueprint("Login", __name__)


@Login.route("/login", methods=["POST"])
def login():
    return render_template("login.html", title="login", error="")


@Login.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("Login.login"))


@Login.route("/main", methods=["GET"])
# @user_required
def main():
    return redirect(url_for("Login.login"))
