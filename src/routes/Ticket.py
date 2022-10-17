from sys import stderr
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

from decorators import login_required
from models import Ticket as TicketModel
from mongodb import connect

UserRepository = connect("user")
Ticket = Blueprint("Ticket", __name__, url_prefix="/ticket")


@Ticket.route("/", defaults={'param': None}, methods=["GET"])
@Ticket.route("/<param>", methods=["GET"])
@login_required
def tickets(param: str = None):
    print("---SESSION", file=stderr)
    print(session, file=stderr)
    ladatos = list()
    with open('src/db/platos.json', mode='r') as json_file:
        data = json.load(json_file)
    with open('src/db/bingos.json', mode='r') as json_file:
        data += json.load(json_file)
    if data:
        if param is None:
            ladatos = [row for row in data if row["state"] == 'P']
        else:
            for row in data:
                if row["ticketid"] == data[param] or row["name"] == data[param]:
                    ladatos.append(row)
    return render_template("ticket.html", title="ticket", current_user=session["current_user"], datos=ladatos, search=param)


@Ticket.route("/view_ticket", methods=["GET"])
def edit_ticket(id):
    print("---SESSION", file=stderr)
    print(session, file=stderr)
    idx = None
    with open('src/db/platos.json', mode='r') as json_file:
        plates = json.load(json_file)
        for i, item in enumerate(plates):
            if item["ticketid"] == id:
                idx = i
    if idx is not None:
        new = TicketModel(plates["id"])
    return {"ok": 1, "data": new.to_json()}
