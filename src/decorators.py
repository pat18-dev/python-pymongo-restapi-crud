import functools
import sys
import traceback
from flask import(
    current_app,
    session,
    url_for,
    redirect,
    request,
)


def wrap_response(func):
    @functools.wraps(func)
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            print(type(err), file=sys.stderr)
            print(str(err), file=sys.stderr)
            print(err.__class__.__name__, file=sys.stderr)
            traceback.print_exc()
            print("-" * 60)

    return inner_function


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if current_app.config["SECURE"]:
            if "current_user" not in session:
                return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function
