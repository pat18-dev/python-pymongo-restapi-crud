from sys import prefix, stderr
import json
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    session,
)
from models import Ticket

from mongodb import connect

UserRepository = connect("user")
Login = Blueprint("Login", __name__, prefix="ticket")

@Login.route("/", methods=["GET"])
# @user_required
def tickets():
    print(session, file=stderr)
    datos = list()
    with open('db/platos.json', mode='r') as json_file:
        data = json.load(json_file)
        for item in data.items():
            if item["state"] != 'P':
                datos.append(item)
    return render_template("ticket.html", title="ticket", user=session["current_user"], datos=[])

@Login.route("/edit", methods=["POST"])
def edit_ticket(id):
    print(session, file=stderr)
    datos = list()
    new = request.get_json()
    ticket = Ticket(new)
    with open('db/platos.json', mode='r') as json_file:
        data = json.load(json_file)
        for item in data.items():
            if item["ticketid"] == id:
                data
        
    return render_template("ticket.html", title="ticket", user=session["current_user"], datos=[])
