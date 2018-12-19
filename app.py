from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
import os

from model import db, Video, VideoQuality, Quality, WaitingQueue
from util import generate_random_string


app = Flask(__name__)
app.config['UPLOAD_DIR'] = "./upload"


@app.before_request
def connect_db():
    if db.is_closed():
        db.connect()


@app.after_request
def close_db(resp):
    if not db.is_closed():
        db.close()

    return resp


def json_error(msg, err_code=400):
    return jsonify({
        "code": err_code,
        "error": msg
    }), err_code


@app.route("/")
def hello():
    return 'hello world~'


@app.route('/video', methods=["POST"])
def upload():
    if 'video' not in request.files:
        return json_error("Video file not found")

    video_file = request.files['video']
    filename = secure_filename(video_file.filename)
    ext = filename.split('.')[-1]
    new_filename = generate_random_string() + '.' + ext
    video_file.save(os.path.join(app.config['UPLOAD_DIR'], new_filename))

    video = Video(filename=new_filename)
    video.save()

    return jsonify(video.to_dict())


@app.route("/queue", methods=["POST"])
def put_video_in_queue():
    if 'video_id' not in request.json:
        return json_error("Video not found")

    if 'qualities' not in request.json:
        return json_error("Target qualities not found")

    qualities = request.json['qualities']
    video_id = request.json['video_id']

    video = Video.get_or_none(id=video_id)
    if video is None:
        return json_error("Video not found")

    video_queue = WaitingQueue.get_or_none(WaitingQueue.video == video)
    if video_queue is not None:
        return json_error("Already in queue")

    video_queue = VideoQuality(video=video)
    video_queue.save()

    success = save_video_qualities(video, qualities)
    if not success:
        video_queue.delete_instance()

    return jsonify(video.to_dict())


def save_video_qualities(video, qualities):
    video_quality = None

    for q in qualities:
        quality = Quality.get_or_none(Quality.slug == q)

        if quality is None:
            continue

        video_quality = VideoQuality(
            video=video,
            quality=quality
        )
        video_quality.save()

    return video_quality is not None


if __name__ == "__main__":
    app.run()
