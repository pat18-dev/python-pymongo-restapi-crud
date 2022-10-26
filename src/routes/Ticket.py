import csv
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
    send_from_directory,
)

from routes.utils.decorators import login_required

from models.Ticket import Ticket as TicketModel
from models.Ticket import CATEGORIES, LEVELS, GRADES, PRICES, DATE_FORMAT

from routes.utils.PaymentPDF import PaymentPDF
from routes.utils.PlSql import PlSql


Ticket = Blueprint("Ticket", __name__, url_prefix="/ticket")
PATH_DATA = "src/db/data.json"
_ReferencePlSql = PlSql(
    "host=172.27.0.3 dbname=my_db user=postgres password=postgres port=5432"
)


def get_data(where=None) -> list:
    data = list()
    slots = [
        "id",
        "ticketid",
        "personid",
        "levelid",
        "gradeid",
        "categoryid",
        "stateid",
        "write_uid",
        "write_at",
        "name",
        "flag",
    ]
    query = "SELECT id,ticketid,personid,levelid,gradeid,categoryid,stateid,write_uid,write_at,name,0 FROM ticket"
    if where is not None:
        query += where
    _ReferencePlSql.exec(query)
    data = [dict(zip(slots, row)) for row in _ReferencePlSql.data]
    return data


@Ticket.route("/", defaults={"idx": None})
@Ticket.route("/<idx>")
@login_required
def tickets(idx):
    if idx is None:
        ladatos = get_data(" WHERE stateid = 'P'")
    else:
        ladatos = get_data(f" WHERE id = {int(idx)}")
    print("---SESSION", file=stderr)
    print(session["payment"], file=stderr)
    if session.get("payment") is not None:
        for item in session["payment"]:
            ladatos[item["id"]]["flag"] = 1
    return render_template(
        "ticket.html",
        title="ticket",
        current_user=session["current_user"],
        datos=ladatos,
        levels=LEVELS,
        grades=GRADES,
        categories=CATEGORIES,
    )


@Ticket.route("/reset_pay")
@login_required
def reset_payment():
    session["payment"] = list()
    return {"ok": 1, "message": "SESSION LIMPIA"}


@Ticket.route("/view_ticket/<int:idx>", methods=["GET"])
def view_ticket(idx):
    return get_data(f" WHERE id = {int(idx)}")[0]


@Ticket.route("/filter", methods=["GET"])
def filter_ticket():
    param = request.args.get("param").upper()
    ladatos = get_data(f" WHERE ticketid LIKE '%{param}%' OR name LIKE '%{param}%'")
    if session.get("payment") is not None:
        for item in session["payment"]:
            ladatos[item["id"]]["flag"] = 1
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


@Ticket.route("/add_to_car", methods=["GET"])
def add_to_car():
    try:
        id = int(request.args.get("idx")) - 1
        ladatos = get_data(f" WHERE id = {id}")[0]
        if session.get("payment") is None:
            session["payment"] = list()
        if ladatos:
            flag = False
            for item in session["payment"]:
                if item["id"] == id:
                    flag = True
            if not flag:
                session["payment"].append(ladatos)
    except Exception as err:
        print("---ERROR", file=stderr)
        print(err, file=stderr)
    return redirect(url_for("Ticket.tickets"))


@Ticket.route("/drop_from_car", methods=["GET"])
def drop_from_car():
    id = int(request.args.get("idx")) - 1
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
    idx = int(request.args.get("idx")) - 1
    ladata = get_data(f" WHERE id = {int(idx)}")
    if ladata:
        query = f"UPDATE ticket SET stateid = 'X' WHERE id = {idx}"
        _ReferencePlSql.exec(query)
    return redirect(url_for("Ticket.tickets"))


@Ticket.route("/drop_payment", methods=["POST"])
def drop_payment():
    paymentid = int(request.args.get("id"))
    query = f"UPDATE payment SET stateid = 'X' WHERE id = {paymentid}"
    _ReferencePlSql.exec(query)
    query1 = f"UPDATE ticket SET stateid = 'P', paymentid = NULL WHERE paymentid = {paymentid}"
    _ReferencePlSql.exec(query1)
    return {"ok": 1, "message": "ELIMINADO CORRECTAMENTE(COMPROBANTE)"}


@Ticket.route("/save_ticket", methods=["POST"])
def save_ticket():
    tmp = request.get_json()
    print("---JSON", file=stderr)
    print(tmp, file=stderr)
    isnew = tmp["isnew"]
    if str(isnew).upper() == "TRUE":
        query = f"""
        INSERT INTO ticket
        (ticketid,name,levelid,gradeid,categoryid,stateid,write_uid,write_at) VALUES
        SELECT LPAD(((MAX(ticketid)::INT)+1), 4, '0'), {tmp["name"]},{tmp["levelid"]},{tmp["gradeid"]},{tmp["categoryid"]},'P',{session["current_user"]["id"]},NOW() WHERE categoryid = {tmp["categoryid"]} LIMIT 1"""
        # _ReferencePlSql.exec(query)
    else:
        query = f"""
        UPDATE ticket SET
        name='{tmp["name"]}',levelid={tmp["levelid"]},gradeid={tmp["gradeid"]},categoryid='{tmp["categoryid"]}',write_uid={session["current_user"]["id"]},write_at=NOW()
        WHERE id = {tmp["id"]}"""
        # _ReferencePlSql.exec(query)
    print(query, file=stderr)
    return {"ok": 1, "message": "CREADO EXITOSAMENTE(TICKET)"}


@Ticket.route("/payment", methods=["POST"])
def payment():
    name = request.args.get("name")
    response = {"ok": 0, "message": "ERROR AL GENERAR PAGART"}
    if session.get("payment"):
        ids = ",".join([item for item in session["payment"]])
        query = f"INSERT INTO payment(stateid) VALUES('A') RETURNING id"
        _ReferencePlSql.exec(query)
        serial = _ReferencePlSql.data[0]
        nserial = str(serial).zfill(8)
        query1 = f"UPDATE ticket SET stateid = 'E', paymentid = {nserial} WHERE id IN ({ids})"
        _ReferencePlSql.exec(query1)
        loPdf = PaymentPDF(current_app.config["PATH_FILE"], nserial)
        loPdf.setData({"name": name, "id": nserial})
        filter = ",".join(session["payment"])
        loPdf.setDatos(get_data(f" WHERE id IN ({filter})"))
        loPdf.mxprint(CATEGORIES, PRICES, DATE_FORMAT)
        session["payment"] = list()
        response = {"ok": 1, "message": nserial}
    return response


@Ticket.route("/report/pdf/name")
def send_pdf(filename):
    return send_from_directory(current_app.config["PATH_FILE"], filename + ".pdf")


@Ticket.route("/report/xls")
def send_xls():
    ladatos = get_data(f" WHERE stateid = 'E' AND paymentid IS NOT NULL")
    data = [v for row in ladatos for _, v in row.items()]
    with open("example.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(data)
    return send_from_directory(current_app.config["PATH_FILE"], "report.csv")
