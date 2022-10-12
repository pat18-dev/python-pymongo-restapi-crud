from flask import Flask, jsonify, make_response, request

# import uuid
from flask_session import Session
from routes.Login import Login

app = Flask(__name__)

app.secret_key = "secretkey"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.register_blueprint(Login)


@app.route("/", methods=["GET"])
def index():
    return make_response(jsonify({"message": "OKEY FROM API"}), 200)


@app.errorhandler(404)
def not_found(error=None):
    return make_response(
        jsonify({"message": "Resource Not Found please, " + request.url}), 200
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
