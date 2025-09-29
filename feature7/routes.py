from flask import Blueprint, request, render_template, Response
import os, uuid
from io import BytesIO
from app.extensions import r
from .services import save_file, resize_compress_image, check_image_quality
from threading import Thread

image_pros_bp = Blueprint('image_prosess', __name__, template_folder='templates')
upload_progress = {}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def process_file(file_stream, file_path):
    save_file(file_stream, file_path)
    resize_compress_image(file_path)
    check_image_quality(file_path)


@image_pros_bp.route("/")
def upload():
    return render_template("index.html")


@image_pros_bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    data = file.read()
    file_stream = BytesIO(data)

    Thread(target=process_file, args=(file_stream, file_path)).start()
    return {"status": "processing", "filename": filename}


@image_pros_bp.route("/progress")
def progress_stream():
    def event_stream():
        pubsub = r.pubsub()
        pubsub.subscribe("upload_progress", "check_image_quality", "resize_compress_image")

        for message in pubsub.listen():
            if message["type"] == "message":
                data = message['data'].decode()
                yield f"data: {data}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")
