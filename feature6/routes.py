from flask import Blueprint, Response, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
import queue
import json
from .utils import connect_sse, push_event_all, add_global_announcement
from feature1.models import User

announcement_bp = Blueprint('announcement', __name__, template_folder='templates')


@announcement_bp.route("/")
@jwt_required()
def announce():
    user_id = int(get_jwt_identity())
    return render_template("announce.html", user_id=user_id)


@announcement_bp.route("/stream/")
def stream():
    q = connect_sse()

    def event_stream():
        while True:
            if not q.empty():
                announce = q.get()
                yield f"data: {announce} and\n\n"
            yield f"data:alive \n\n"
            time.sleep(3)

    return Response(event_stream(), mimetype="text/event-stream")


@announcement_bp.route("/add", methods=['GET', 'POST'])
def add_new_feature():
    if request.method == "POST":
        announcement_data = request.form
        title = announcement_data['title']
        body = announcement_data['body']
        data = {
            "title": title,
            "body": body
        }
        add_global_announcement(data)
        push_event_all(data)
    return render_template("add_feature.html")
