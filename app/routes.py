from flask import Blueprint, render_template
from app.extensions import mongo
from datetime import datetime, timezone
from dateutil import parser

ui = Blueprint("ui", __name__, url_prefix="/ui")


@ui.route("/", methods=["GET"])
def home():

    collection = mongo.cx["techstax"]["github_actions"]
    doc_cursor = collection.find().sort("_id", -1).limit(1)

    docs = list(doc_cursor)

    if len(docs) < 1:
        return render_template("ui.html", message="Sorry no data available")

    doc = docs[0]
    doc["_id"] = str(doc["_id"])
    doc["timestamp"] = str(format_date(doc["timestamp"]))
    msg = "null"

    match doc["action"]:
        case "PUSH":
            msg = (
                f"'{doc['author']}' pushed to {doc['to_branch']} on {doc['timestamp']}"
            )
        case "PULL_REQUEST":
            msg = f"'{doc['author']}' submitted a pull request from {doc['from_branch']} to {doc['to_branch']} on {doc['timestamp']}"
        case "MERGE":
            msg = f"'{doc['author']}' merged branch {doc['from_branch']} to {doc['to_branch']} on {doc['timestamp']}"

    return render_template("ui.html", message=msg)


def format_date(iso_str):
    dt = parser.isoparse(iso_str).astimezone(timezone.utc)

    day = dt.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        sfx = "th"
    else:
        last_digit = day % 10
        sfx = ["st", "nd", "rd"][last_digit - 1]

    _day = f"{day}{sfx}"
    _month = dt.strftime("%B")
    _year = dt.strftime("%Y")
    _hour = dt.hour % 12 or 12
    _min = dt.strftime("%M")
    _ampm = dt.strftime("%p")

    return f"{_day} {_month} {_year} - {_hour}:{_min} {_ampm} UTC"
