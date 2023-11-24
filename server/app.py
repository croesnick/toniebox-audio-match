import os
from dataclasses import dataclass
from pathlib import Path

from config import Config
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from models.audio import AudioBook, AudioTrack
from models.tonie import Tonie
from utility import (
    audiobooks,
    get_creative_tonies,
    get_item_from_request,
    get_tonie_api,
    songs_update,
)
from yt_dlp import YoutubeDL

# instantiate the app
app = Flask(__name__)
app.config.from_object(Config)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})



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

songs = songs_update()
logger = Config.configure_logger(__name__)


@app.before_request
def before_request_func():
    if "tonie_api_client" not in g:
        g.tonie_api_client = get_tonie_api()


@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@app.route("/audiobooks", methods=["GET"])
def all_audiobooks():
    return jsonify(
        {
            "status": "success",
            "audiobooks": audio_books,
        }
    )


@app.route("/songs", methods=["GET"])
def all_songs():
    songs_local = songs_update()
    return jsonify(
        {
            "songs": songs_local,
        }
    )


@app.route("/creativetonies", methods=["GET"])
def all_creativetonies():
    creative_tonies = get_creative_tonies()
    return jsonify(
        {
            "status": "success",
            "creativetonies": creative_tonies,
        }
    )


@app.route("/tonie_overview", methods=["POST"])
def tonie_overview():
    tonies = get_item_from_request(request.json, "tonie_id", get_creative_tonies())
    
    if tonies is None:
        return jsonify({"status": "failure", "message": "No matching tonie found"}), 400

    if len(tonies) > 1:
        return (
            jsonify(
                {
                    "status": "failure",
                    "message": "Multiple tonies provided, can only handle one",
                }
            ),
            400,
        )

    if len(tonies) == 1:
        tonie = tonies[0]

    tonie_content = g.tonie_api_client.get_tonie_content(tonie)

    return jsonify(
        {
            "status": "success",
            "tracks": tonie_content,
        }
    )


@app.route("/delete_track", methods=["POST"])
def delete_track():
    tonie = get_item_from_request(request.json, "tonie_id", get_creative_tonies())

    if tonie is None:
        return jsonify({"status": "failure", "message": "No matching tonie found"}), 400

    if len(tonie) > 1:
        return (
            jsonify(
                {
                    "status": "failure",
                    "message": "Multiple tonies provided, can only handle one",
                }
            ),
            400,
        )

    if len(tonie) == 1:
        tonie = tonie[0]

    current_content = g.tonie_api_client.get_tonie_content(tonie)

    tracks = get_item_from_request(
        request.json, "track_id", current_content["chapters"]
    )
    track_ids = [track["id"] for track in tracks]

    new_content = [
        remaining_track
        for remaining_track in current_content["chapters"]
        if remaining_track["id"] not in track_ids
    ]

    g.tonie_api_client.update_tonie_content(tonie, new_content)

    return jsonify(
        {
            "status": "success",
            "tonie_id": tonie.id,
            "track_id": track_ids,
        }
    )


@app.route("/delete_local_track", methods=["POST"])
def delete_local_track():
    body = request.json
    track_id = body["file"]

    track = [track for track in songs_update() if track["file"] in track_id]
    for t in track:
        os.remove(Path(t["file_original"]))

    return jsonify(
        {
            "status": "success",
        }
    )


@app.route("/download_youtube", methods=["POST"])
def download_youtube():
    body = request.json
    youtube_url = body["youtube_url"]

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "outtmpl": "/backend/assets/audiobooks/%(title)s.%(ext)s",
        "restrictfilenames": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return jsonify(
        {
            "status": "success",
        }
    )


@dataclass
class Upload:
    tonie: Tonie
    audiobook: AudioBook
    track: AudioTrack

    @classmethod
    def from_ids(cls, tonie: str, audiobook: str) -> "Upload":
        return cls(
            next(filter(lambda t: t.id == tonie, get_creative_tonies()), None),
            next(filter(lambda a: a.id == audiobook, audio_books_models), None),
        )

    @classmethod
    def tracks_from_ids(cls, tonie: Tonie, song: AudioTrack) -> "Upload":
        return cls(
            tonie=tonie,
            audiobook=None,
            track=song,
        )


@app.route("/upload", methods=["POST"])
def upload_album_to_tonie():
    tonie_id = get_item_from_request(request.json, "tonie_id", get_creative_tonies())
    audiobook_id = get_item_from_request(
        request.json, "audiobook_id", get_creative_tonies()
    )
    upload = Upload.from_ids(tonie=tonie_id, audiobook=audiobook_id)
    logger.debug(f"Created upload object: {upload}")

    status = g.tonie_api_client.put_album_on_tonie(upload.audiobook, upload.tonie)
    return (
        jsonify(
            {"status": "success" if status else "failure", "upload_id": str(upload)}
        ),
        201,
    )


@app.route("/upload_track", methods=["POST"])
def upload_track_to_tonie():
    tonie_id = get_item_from_request(request.json, "tonie_id", get_creative_tonies())
    track_id = get_item_from_request(request.json, "track_id", get_creative_tonies())
    tonie = [to for to in get_creative_tonies() if to.id == tonie_id][0]
    for track in track_id:
        song = [so for so in songs_update() if so["file"] == track]
        upload = Upload.tracks_from_ids(tonie=tonie, song=song)
        status = g.tonie_api_client.put_songs_on_tonie(upload.track, upload.tonie)
    # logger.debug(f"Created upload object: {upload}")

    return (
        jsonify(
            {
                "status": "success",
                "upload_id": "test",
                "songs": songs,
                "track": song,
                "upload": upload,
                "return": status,
            }
        ),
        201,
    )
