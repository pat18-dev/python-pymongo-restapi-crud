from sys import stderr
import json
from flask import (
    Blueprint,
    request,
    render_template,
    session,
    current_app,
    redirect,
    url_for
)

from routes.utils.decorators import login_required

from models.Ticket import Ticket as TicketModel
from models.Ticket import CATEGORIES, LEVELS, GRADES

from routes.utils.PaymentPDF import PaymentPDF
# from mongodb import connect
# TicketRepository = connect("ticket")
Ticket = Blueprint("Ticket", __name__, url_prefix="/ticket")
PATH_DATA = "src/db/data.json"


def get_data(path: str) -> list:
    data = list()
    with open(path, mode="r") as json_file:
        data = json.load(json_file)
    return data


@Ticket.route("/", defaults={"idx": None})
@Ticket.route("/<idx>")
@login_required
def tickets(idx):
    ladatos = list()
    data = get_data(PATH_DATA)
    if data:
        if idx is None:
            ladatos = [row for row in data if row["state"] == "P"]
        else:
            idx = int(idx)
            ladatos = [row for row in data if row["ticketid"] == idx]
    if session.get("payment") is not None:
        for item in session["payment"]:
            ladatos[item["idx"]]["flag"] = 1
    return render_template(
        "ticket.html",
        title="ticket",
        current_user=session["current_user"],
        datos=ladatos,
        levels=LEVELS,
        grades=GRADES,
        categories=CATEGORIES,
    )
    
    
@Ticket.route("/view_ticket/<int:idx>", methods=["GET"])
def view_ticket(idx):
    data = dict()
    datos = get_data(PATH_DATA)
    if datos:
        data = datos[int(idx)]
    return data


@Ticket.route("/filter", methods=["GET"])
def filter_ticket():
    param = request.args.get("param").upper()
    ladatos = list()
    data = get_data(PATH_DATA)
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
        levels=LEVELS,
        grades=GRADES,
        categories=CATEGORIES,
    )


@Ticket.route("/add_to_car/<idx>", methods=["GET"])
def add_to_car(idx):
    data = get_data(PATH_DATA)
    if session.get("payment") is None:
        session["payment"] = list()
    if data:
        session["payment"].append(data[int(idx)])
    return redirect(url_for('tickets'))


@Ticket.route("/drop_from_car", methods=["GET"])
def drop_from_car():
    id = int(request.args.get("drop_idx"))
    if session.get("payment") is not None:
        idx = None
        for i, item in enumerate(session["payment"]):
            if item["idx"] == id:
                idx = i
        if idx is not None:
            del session["payment"][idx]
    return redirect(url_for('tickets'))


@Ticket.route("/pay", methods=["GET"])
def pays():
    print("---SESSION", file=stderr)
    ladatos = session["payment"] if session.get("payment") is not None else []
    print(ladatos, file=stderr)
    return render_template(
        "payment.html",
        title="payment",
        current_user=session["current_user"],
        datos=ladatos,
        categories=CATEGORIES,
    )


@Ticket.route("/drop_ticket", methods=["GET"])
def drop_ticket():
    idx = int(request.args.get("idx"))
    with open("src/db/data.json", mode="r") as json_file:
        data = json.load(json_file)
    if data:
        data[idx]["state"] = "X"
        with open("db/data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return {"ok": 1, "message": "ELIMINADO CORRECTAMENTE(TICKET)"}


@Ticket.route("/drop_payment", methods=["POST"])
def drop_payment():
    tmp = request.get_json()
    paymentid = tmp["paymentid"]
    with open("src/db/payment.json", mode="r") as json_file:
        data = json.load(json_file)
    if data:
        idx = None
        for i, item in enumerate(data):
            if paymentid == item["paymentid"]:
                idx = i
        if idx is not None:
            del data[idx]
            with open("db/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    return {"ok": 1, "message": "ELIMINADO CORRECTAMENTE(COMPROBANTE)"}


@Ticket.route("/save_ticket", methods=["POST"])
def save_ticket():
    tmp = request.get_json()
    isnew = tmp["isnew"]
    tmp.pop("isnew")
    ticket = TicketModel(tmp)
    if str(isnew).upper() == "TRUE":
        with open("src/db/serial.json", mode="r") as json_file:
            data = json.load(json_file)
        if data:
            ticketid = str(int(data[ticket.category]) + 1).zfill(4)
            data[ticket.category] = ticketid
            with open("db/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        with open("src/db/serial.json", mode="r") as json_file:
            data = json.load(json_file)
        if data:
            data[ticket.idx] = tmp
            with open("db/data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    return {"ok": 1, "message": "CREADO EXITOSAMENTE(TICKET)"}


@Ticket.route("/payment", methods=["POST"])
def payment():
    name = request.args.get("name")
    if session.get("payment") is not None:
        with open("src/db/serial.json", mode="r") as json_file:
            serial = json.load(json_file)
        nserial = serial["F"] + 1
        loPdf = PaymentPDF(current_app.config["PATH_FILE"], nserial)
        lst_ind = [item["idx"] for item in session["payment"]]
        with open("src/db/data.json", mode="r") as json_file:
            data = json.load(json_file)
        if data:
            for idx in lst_ind:
                if data[idx]["state"] != "P":
                    return {
                        "ok": 0,
                        "message": f"ERROR PAGO: {data[idx]['ticketid']}",
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
