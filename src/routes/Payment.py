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
from models import Payment as PaymentModel

from mongodb import connect

UserRepository = connect("user")
Payment = Blueprint("Payment", __name__, url_prefix="/payment")


@Payment.route("/", methods=["GET"])
# @user_required
def tickets():
    print(session, file=stderr)
    datos = list()
    with open("db/platos.json", mode="r") as json_file:
        data = json.load(json_file)
        for item in data.items():
            if item["state"] != "P":
                datos.append(item)
    return render_template(
        "payment.html", title="Payment", user=session["current_user"], datos=[]
    )


@Payment.route("/drop", methods=["POST"])
def edit_ticket(id):
    print(session, file=stderr)
    datos = list()
    new = request.get_json()
    Payment = TicketModel(new)
    idx = None
    with open("db/platos.json", mode="r") as json_file:
        plates = json.load(json_file)
        for i, item in enumerate(plates):
            if item["ticketid"] == id:
                idx = i
    if idx is not None:
        plates[idx] = Payment.to_json()
        with open("db/platos.json", "w", encoding="utf-8") as f:
            json.dump(plates, f, ensure_ascii=False, indent=4)


@Payment.route("/add", methods=["POST"])
def add_ticket(id):
    print(session, file=stderr)
    datos = list()
    new = request.get_json()
    Payment = TicketModel(new)
    idx = None
    with open("db/platos.json", mode="r") as json_file:
        plates = json.load(json_file)
        for i, item in enumerate(plates):
            if item["ticketid"] == id:
                return {"OK": 0, "Msg": "Payment is used"}
    if idx is not None:
        plates[idx] = Payment.to_json()
        with open("db/platos.json", "w", encoding="utf-8") as f:
            json.dump(plates, f, ensure_ascii=False, indent=4)
    return {"OK": 1, "Msg": "Success"}
