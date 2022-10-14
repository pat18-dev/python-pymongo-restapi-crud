from sys import stderr
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from mongodb import Mongo

UserRepository = Mongo("user")
Login = Blueprint("Login", __name__)


@Login.route("/login", methods=["GET", "POST"])
def login():
    error = None
    user = {"id": "00000000", "name": "INVITADO", "is_authenticated": False}
    if request.method == 'POST':
        print("---DATA", file=stderr)
        data = request.form.to_dict()
        print(data, file=stderr)
        if UserRepository.collection.find_one("user", {"document": data.document}):
            flash('Error document not defined')
        user = {"id": data.document, "name": "user1", "is_authenticated": True}
        session["current_user"] = user
        return redirect(url_for('Login.main'))
    return render_template("login.html", title="login", current_user=user, error=error)


@Login.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("Login.login"))


@Login.route("/main", methods=["GET"])
# @user_required
def main():
    print(session, file=stderr)
    return render_template("main.html", title="main", user=session["current_user"], datos="")    # return redirect(url_for("Login.login"))
