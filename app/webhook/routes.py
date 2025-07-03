from flask import Blueprint, request
from app.extensions import mongo
from dateutil import parser
from datetime import timezone

webhook = Blueprint("Webhook", __name__, url_prefix="/webhook")


@webhook.route("/receiver", methods=["POST"])
def receiver():
    collection = mongo.cx["techstax"]["github_actions"]

    data = request.json
    event = request.headers.get("X-GitHub-Event")
    return_data = {}

    if event == "push":
        branch = data["ref"].split("/")[-1]
        timestamp = data["head_commit"]["timestamp"]

        recent_merge = mongo.cx["techstax"]["github_actions"].find_one(
            {
                "action": "MERGE",
                "to_branch": branch
            },
            sort=[("_id", -1)]
        )

        # CHECK IF PUSH IS AUTO-PUSH (happesn after merge.)
        if recent_merge:
            ts_now = parser.isoparse(timestamp).astimezone(timezone.utc)
            merge_time = parser.isoparse(recent_merge["timestamp"]).astimezone(timezone.utc)
            time_diff = (ts_now - merge_time).total_seconds()

            if 0 <= time_diff < 5:
                print("Skipping PUSH — recent MERGE detected.")
                return {'message':'Ignoring auto push'}, 200

       
        return_data = {
            "request_id": data["after"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": branch,
            "author": data["pusher"]["name"],
            "timestamp": timestamp,
        }

    if event == "pull_request":
        d = data["pull_request"]
        return_data = {
            "request_id": d["id"],
            "action": "MERGE" if d["merged"] else "PULL_REQUEST",
            "from_branch": d["head"]["ref"],
            "to_branch": d["base"]["ref"],
            "author": d["merged_by"]["login"] if d["merged"] else d["user"]["login"],
            "timestamp": d["merged_at"] if d["merged"] else d["updated_at"],
        }
    collection.insert_one(return_data)

    return {'message':'Action data successfully added.'}, 200
