from app.extensions import r
from PIL import Image
import os, json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def save_file(file_stream, filepath):
    try:
        chunk_size = 256 * 256
        total_size = 0
        time.sleep(3)
        with open(filepath, "wb") as f:
            while True:
                chunk = file_stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                total_size += len(chunk)
                r.publish("upload_progress", json.dumps({"type": "progress", "progress": total_size}))
    except Exception as e:
        r.publish("upload_progress", json.dumps({"type": "error", "message": str(e)}))


def resize_compress_image(file_path):
    try:
        quality = 70
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist!")

        with Image.open(file_path) as img:
            # cmpress 
            ext = img.format if img.format else "PNG"
            if ext.upper() == "PNG":
                img.save(file_path, "PNG", optimize=True)
            else:
                img = img.convert("RGB")
                img.save(file_path, "JPEG", optimize=True, quality=quality)

            # resize
            resized_img = img.resize((1080, 1350))
            resized_img.save(file_path)
            r.publish("resize_compress_image",
                      json.dumps({"type": "status", "status": "uploaded resize_compress complete"}))
    except Exception as e:
        r.publish("resize_compress_image", json.dumps({"type": "error", "message": str(e)}))


def check_image_quality(file_path):
    """
    {
    format,
    mode,
    dimensions, 
    file_size, 
    
    }
    """
    time.sleep(5)
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} does not exist!")
        with Image.open(file_path) as img:
            info = {
                "format": img.format,
                "mode": img.mode,
                "dimensions": img.size,
                "file_size_kb": round(os.path.getsize(file_path) / 1024, 1)
            }
            r.publish("check_image_quality", json.dumps({"type": "info", "info": info}))
    except Exception as e:
        r.publish("check_image_quality", json.dumps({"type": "error", "message": str(e)}))
