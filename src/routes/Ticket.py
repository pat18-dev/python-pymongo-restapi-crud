from sys import stderr
import json
from flask import (
    Blueprint,
    request,
    render_template,
    session,
    current_app,
    redirect,
    url_for,
)

from routes.utils.decorators import login_required

from models.Ticket import Ticket as TicketModel
from models.Ticket import CATEGORIES, LEVELS, GRADES

from routes.utils.PaymentPDF import PaymentPDF
from routes.utils.PlSql import PlSql

# from mongodb import connect
# TicketRepository = connect("ticket")
Ticket = Blueprint("Ticket", __name__, url_prefix="/ticket")
PATH_DATA = "src/db/data.json"
_ReferencePlSql = PlSql("host=172.27.0.2 dbname=my_db user=postgres password=postgres port=5432")


def get_data(where = None) -> list:
    # data = list()
    # with open(path, mode="r") as json_file:
    #     data = json.load(json_file)
    # return data
    data = list()
    slots = [
        'id',
        'ticketid',
        'personid',
        'levelid',
        'gradeid',
        'categoryid',
        'stateid',
        'write_uid',
        'write_at',
        'name',
        'flag'
    ]
    # query = f"SELECT {slots} FROM ticket;"
    query = "SELECT A.id,A.ticketid,A.personid,A.levelid,A.gradeid,A.categoryid,A.stateid,A.write_uid,A.write_at,B.name,0 FROM ticket A INNER JOIN person B ON B.personid = A.personid"
    if where is not None:
        query += where
    _ReferencePlSql.exec(query)
    data = [dict(zip(slots, row)) for row in _ReferencePlSql.data]
    return data


@Ticket.route("/", defaults={"idx": None})
@Ticket.route("/<idx>")
@login_required
def tickets(idx):
    ladatos = list()
    if idx is None:
        ladatos = get_data(" WHERE stateid = 'P'")
    else:
        ladatos = get_data(f" WHERE id = {int(idx)}")
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
    return get_data(f" WHERE id = {int(idx)}")


@Ticket.route("/filter", methods=["GET"])
def filter_ticket():
    param = request.args.get("param").upper()
    ladatos = get_data(f" WHERE ticketid LIKE '%{param}%' OR name LIKE '%{param}%'")
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
    ladatos = get_data(" WHERE stateid = 'P'")
    if session.get("payment") is None:
        session["payment"] = list()
    if ladatos:
        flag = False
        for item in session["payment"]:
            if item["id"] == int(idx):
                flag = True
        if flag:
            session["payment"].append(ladatos[int(idx)])
    return redirect(url_for("tickets"))


@Ticket.route("/drop_from_car", methods=["GET"])
def drop_from_car():
    id = int(request.args.get("idx"))
    if session.get("payment") is not None:
        idx = None
        for i, item in enumerate(session["payment"]):
            if item["id"] == id:
                idx = i
        if idx is not None:
            del session["payment"][idx]
    return redirect(url_for("Ticket.pays"))


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
    ladata = get_data(f" WHERE id = {int(idx)}")
    if ladata:
        query = f"UPDATE ticket SET stateid = 'X' WHERE id = {idx}"
        _ReferencePlSql.exec(query)
    return {"ok": 1, "message": "ELIMINADO CORRECTAMENTE(TICKET)"}


@Ticket.route("/drop_payment", methods=["POST"])
def drop_payment():
    tmp = request.get_json()
    paymentid = tmp["paymentid"]
    query = f"UPDATE payment SET stateid = 'X' WHERE id = {paymentid}"
    _ReferencePlSql.exec(query)
    return {"ok": 1, "message": "ELIMINADO CORRECTAMENTE(COMPROBANTE)"}


@Ticket.route("/save_ticket", methods=["POST"])
def save_ticket():
    tmp = request.get_json()
    isnew = tmp["isnew"]
    ticket = TicketModel(tmp)
    if str(isnew).upper() == "TRUE":
        query = f"""
        INSERT INTO ticket
        (ticketid,name,levelid,gradeid,categoryid,stateid,write_uid,write_at) VALUES
        SELECT LPAD(((MAX(ticketid)::INT)+1), 4, '0'), {tmp["name"]},{tmp["levelid"]},{tmp["gradeid"]},{tmp["categoryid"]},'P',{session["current_user"]["id"]},NOW() WHERE categoryid = {tmp["categoryid"]} LIMIT 1"""
        _ReferencePlSql.exec(query)
    else:
        query = f"""
        UPDATE ticket SET
        person={tmp["name"]},levelid={tmp["levelid"]},gradeid={tmp["gradeid"]},categoryid={tmp["categoryid"]},write_uid={session["current_user"]["id"]},write_at=NOW()
        WHERE id = {tmp["id"]}"""
        _ReferencePlSql.exec(query)
    return {"ok": 1, "message": "CREADO EXITOSAMENTE(TICKET)"}


@Ticket.route("/payment", methods=["POST"])
def payment():
    name = request.args.get("name")
    if session.get("payment") is not None:
        query = f"INSERT INTO payment(stateid) VALUES('P') RETURNING id"
        _ReferencePlSql.exec(query)
        serial = _ReferencePlSql.data[0]
        nserial = str(serial).zfill(8)
        loPdf = PaymentPDF(current_app.config["PATH_FILE"], nserial)
        loPdf.setData({"name": name, "id": nserial})
        loPdf.setDatos(session["payment"])
        session["payment"] = list()
        return {"ok": 1, "message": nserial}
    return redirect(url_for("tickets"))
