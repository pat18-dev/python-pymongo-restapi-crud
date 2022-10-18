from sys import stderr
import json
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    current_app
)

from decorators import login_required
from models import Ticket as TicketModel
from mongodb import connect
from routes.src.PaymentPDF import PaymentPDF

UserRepository = connect("user")
Ticket = Blueprint("Ticket", __name__, url_prefix="/ticket")


def get_data() -> list:
    data = list()
    with open("src/db/data.json", mode="r") as json_file:
        data = json.load(json_file)
    return data


@Ticket.route("/", defaults={"idx": None})
@Ticket.route("/<idx>")
@login_required
def tickets(idx):
    print("---SESSION", file=stderr)
    print(session, file=stderr)
    ladatos = list()
    data = get_data()
    if data:
        if id is None:
            ladatos = [row for row in data if row["state"] == "P"]
        else:
            ladatos = [row for row in data if row["ticketid"] == idx]
    if session.get("payment") is not None:
        for item in session["payment"]:
            ladatos[item["idx"]]["flag"] = 1
    return render_template(
        "ticket.html",
        title="ticket",
        current_user=session["current_user"],
        datos=ladatos,
    )


@Ticket.route("/filter", methods=["GET"])
def filter_ticket():
    print("---SESSION", file=stderr)
    print(session, file=stderr)
    param = request.args.get("param")
    ladatos = list()
    data = get_data()
    if data:
        for row in data:
            if param in row["ticketid"] or param in row["name"]:
                ladatos.append(row)
    if session.get("payment") is not None:
        for item in session["payment"]:
            ladatos[item["idx"]]["flag"] = 1
    return render_template(
        "ticket.html",
        title="ticket",
        current_user=session["current_user"],
        datos=ladatos,
        search=param,
    )


@Ticket.route("/add_to_car/<idx>", methods=["GET"])
def add_to_car(idx):
    data = get_data()
    if session.get("payment") is None:
        session["payment"] = list()
    if data:
        tmp = data[idx]
        session["payment"].append(tmp)


@Ticket.route("/drop_from_car/<idx>", methods=["GET"])
def drop_from_car(sidx):
    if session.get("payment") is not None:
        idx = None
        for i, item in enumerate(session["payment"]):
            if item["idx"] == idx:
                idx = i
        if idx is not None:
            del session["payment"][idx]


@Ticket.route("/pay", methods=["GET"])
def pay():
    ladatos = session["payment"] if session.get("payment") is not None else []
    return render_template(
        "payment.html",
        title="payment",
        current_user=session["current_user"],
        datos=ladatos,
    )


@Ticket.route("/pay", methods=["POST"])
def make_pay():
    name = request.args.get("name")
    if session.get("payment") is not None:
        with open("src/db/serial.json", mode="r") as json_file:
            serial = json.load(json_file)
        nserial = serial["F"] + 1
        loPdf = PaymentPDF(nserial, current_app.config["PATH_FILE"])
        lst_ind = [item["idx"] for item in session["payment"]]
        with open("src/db/data.json", mode="r") as json_file:
            data = json.load(json_file)
        if data:
            for idx in lst_ind:
                if data[idx]["state"] != "P":
                    return {
                        "ok": 0,
                        "message": f"ERROR EN EL SIGUEINTE PAGO {data[idx]['activityid']}",
                    }
        for idx in lst_ind:
            data[idx]["state"] = "E"
        with open("db/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        with open("db/bill.json", "a", encoding="utf-8") as f:
            json.dump(session["payment"], f, ensure_ascii=False, indent=4)
        loPdf.setData({"name": name, "id": str(nserial).zfill(8)})
        loPdf.setDatos(session["payment"])
        session["payment"] = list()
        return {"ok": 1, "message": nserial}
    return {"ok": 0, "message": "ERROR NO HAY DATOS SELECCIONADOS}"}
