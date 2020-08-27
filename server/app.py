import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from redis import Redis
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job, JobStatus

import localstorage.client
from models.audio import AudioBook
from models.tonie import Tonie
from toniecloud.client import TonieCloud
from worker.upload import upload_facade

redis = Redis.from_url(os.getenv("TONIE_AUDIO_MATCH_REDIS_URI"))
queue = Queue(connection=redis)

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
logger = logging.getLogger(__name__)

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

tonie_cloud_api = TonieCloud(os.environ.get("TONIE_AUDIO_MATCH_USER"), os.environ.get("TONIE_AUDIO_MATCH_PASS"))


def audiobooks():
    audiobooks = localstorage.client.audiobooks(Path("assets/audiobooks"))
    logger.debug("Discovered audiobook paths: %s", audiobooks)
    for album in audiobooks:
        audiobook = AudioBook.from_path(album)
        if audiobook:
            yield audiobook


audio_books_models = list(audiobooks())
audio_books = [
    {
        "id": album.id,
        "artist": album.artist,
        "title": album.album,
        "disc": album.album_no,
        "cover_uri": str(album.cover_relative) if album.cover else None,
    }
    for album in audio_books_models
]

creative_tonies = tonie_cloud_api.creativetonies()


@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/audiobooks", methods=["GET"])
def all_audiobooks():
    return jsonify({"status": "success", "audiobooks": audio_books, })


@app.route("/creativetonies", methods=["GET"])
def all_creativetonies():
    return jsonify({"status": "success", "creativetonies": creative_tonies, })


@dataclass
class Upload:
    tonie: Tonie
    audiobook: AudioBook

    @classmethod
    def from_ids(cls, tonie: str, audiobook: str) -> "Upload":
        return cls(
            next(filter(lambda t: t.id == tonie, creative_tonies), None),
            next(filter(lambda a: a.id == audiobook, audio_books_models), None),
        )


@app.route("/uploads", methods=["POST"])
def upload_album_to_tonie():
    body = request.json
    upload = Upload.from_ids(tonie=body["tonie_id"], audiobook=body["audiobook_id"])
    logger.debug(f"Created upload object: {upload}")

    job = queue.enqueue(upload_facade, upload.audiobook, upload.tonie)
    return jsonify({"id": job.id}), 202


@app.route("/uploads/<upload_id>", methods=["GET"])
def upload_status(upload_id: str):
    def response(status_: Optional[str] = None) -> str:
        return jsonify({"id": upload_id, "status": status_})

    try:
        job = Job.fetch(upload_id, connection=redis)
        status = job.get_status()
    except NoSuchJobError:
        return response(), 404
    else:
        pending = status is None or status in (JobStatus.QUEUED, JobStatus.STARTED, JobStatus.DEFERRED)
        if pending:
            return response("pending"), 200

        result: Optional[bool] = job.result
        failed = not status or status == JobStatus.FAILED or not result

        if failed:
            return response("failed"), 200

        success = status == JobStatus.FINISHED and result is True
        if success:
            return response("success"), 200

        return response("unknown"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
