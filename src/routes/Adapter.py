import sys

from bson import json_util
from bson.objectid import ObjectId
from flask import Blueprint, abort, jsonify, make_response, request

from decorators import wrap_response
from mongodb import mongo

Adapter = Blueprint("adapter", __name__, url_prefix="/adapter")


@Adapter.route("/", methods=["POST"])
@wrap_response
def adapter_repo():
    # get the uploaded file
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
    return redirect(url_for("index"))
