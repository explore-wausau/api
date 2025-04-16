# Auth Levels:
# 1 - Organizer
# 2 - Admin
# 3 - Superuser

# Endpoints:
# /events/all - List of all events.
# /events/lookup - Event lookup.
# /events/create - Create event. (Auth level 1+)
# /events/modify - Modify event. (Auth level 1+)
# /events/delete - Delete event. (Auth level 1+)
# /organizer/all - List all organizers. (Auth level 2+)
# /organizer/lookup - Organizer lookup. (Auth level 2+)
# /organizer/create - Create organizer. (Auth level 2+)
# /organizer/modify - Modify organizer. (Auth level 2+)
# /organizer/delete - Delete organizer. (Auth level 2+)
# /admin/all - List all admins. (Auth level 3+)
# /admin/lookup - Admin lookup. (Auth level 3+)
# /admin/create - Create admin. (Auth level 3+)
# /admin/modify - Modify admin. (Auth level 3+)
# /admin/delete - Delete admin. (Auth level 3+)
# /data/clear - Clear ALL data. (Auth level 3+)

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from events import *
from utils import create_error_msg
import os

load_dotenv()

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

@app.route("/events/all")
def allevents():
    return jsonify(list_events())

@app.route("/events/lookup")
def eventsearch():
    return jsonify(search_events())

@app.route("/events/create")
def eventcreate():
    return jsonify(create_event())

@app.route("/events/modify")
def eventmodify():
    return create_error_msg("Not Implemented"), 501

@app.route("/events/delete")
def eventdelete():
    return create_error_msg("Not Implemented"), 501

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT"))
