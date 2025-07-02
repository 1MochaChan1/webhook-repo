from flask import Blueprint, json, request

webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")


@webhook.route("/receiver", methods=["POST"])
def receiver():
    data = request.json["payload"]
    event = request.json["event"]
    return_data = {}

    if event == "push":
        return_data = {
            "request_id": data["after"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data["ref"].split("/")[-1],
            "author": data["pusher"]["name"],
            "timestamp": data["head_commit"]["timestamp"],
        }

    if event == "pull_request":
        d = data["pull_request"]
        return_data = {
            "request_id": d["id"],
            "action": "MERGE" if d["merged"] else "PUSH",
            "from_branch": d["head"]["ref"],
            "to_branch": d["base"]["ref"],
            "author": d["merged_by"]["login"] if d["merged"] else d["user"]["login"],
            "timestamp": d["merged_at"] if d["merged"] else d["updated_at"],
        }

    return return_data, 200
