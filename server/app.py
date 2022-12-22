import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

import localstorage.client

# configuration
from models.audio import AudioBook
from models.audio import AudioTrack
from models.tonie import Tonie
from toniecloud.client import TonieCloud
from yt_dlp import YoutubeDL

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


def get_songs():
    songs = localstorage.client.audiofiles(Path("assets/audiobooks"))
    songs = [AudioTrack.from_path(song) for song in songs]
    return songs

def songs_update():
    songs_models = list(get_songs())
    logger.debug(songs_models)
    songs = [
        {
            "file": str(song.file.stem),
            "file_original": str(song.file),
        }
        for song in songs_models
    ]
    return songs

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
creative_tonies = tonie_cloud_api.creativetonies()


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
    return jsonify(
        {
            "status": "success",
            "creativetonies": creative_tonies,
        }
    )


@app.route("/tonie_overview", methods=["POST"])
def tonie_overview():
    body = request.json
    tonie_id = body["tonie_id"]
    tonie = [tonie for tonie in creative_tonies if tonie.id == tonie_id][0]
    tonie_content = tonie_cloud_api.get_tonie_content(tonie)
    return jsonify(
        {
            "status": "success",
            "tracks": tonie_content,
        }
    )


@app.route("/delete_track", methods=["POST"])
def delete_track():
    body = request.json
    tonie_id = body["tonie_id"]
    track_id = body["track_id"]

    tonie = [tonie for tonie in creative_tonies if tonie.id == tonie_id][0]

    current_content = tonie_cloud_api.get_tonie_content(tonie)
    new_content = [
        track for track in current_content["chapters"] if track["id"] not in track_id
    ]

    tonie_cloud_api.update_tonie_content(tonie, new_content)

    return jsonify(
        {
            "status": "success",
            # "tonie": tonie,
            "tonie_id": tonie_id,
            "track_id": track_id,
            # "new_content": new_content,
        }
    )

@app.route("/delete_local_track", methods=["POST"])
def delete_local_track():
    body = request.json
    track_id = body["file"]
    track = [track for track in songs_update() if track["file"] == track_id[0]][0]
    os.remove(Path(track["file_original"]))

    return jsonify(
        {
            "status": "success",
            "track_id": track_id,
        }
    )

@app.route("/download_youtube", methods=["POST"])
def download_youtube():
    body = request.json
    youtube_url = body["youtube_url"]

    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': '/backend/assets/audiobooks/%(title)s.%(ext)s',
            'restrictfilenames': True,
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
            next(filter(lambda t: t.id == tonie, creative_tonies), None),
            next(filter(lambda a: a.id == audiobook, audio_books_models), None),
        )

    @classmethod
    def tracks_from_ids(cls, tonie: Tonie, song: AudioTrack) -> "Upload":
        return cls(
                tonie = tonie,
                audiobook = None,
                track = song,
                )


@app.route("/upload", methods=["POST"])
def upload_album_to_tonie():
    body = request.json
    upload = Upload.from_ids(tonie=body["tonie_id"], audiobook=body["audiobook_id"])
    logger.debug(f"Created upload object: {upload}")

    status = tonie_cloud_api.put_album_on_tonie(upload.audiobook, upload.tonie)
    return (
        jsonify(
            {"status": "success" if status else "failure", "upload_id": str(upload)}
        ),
        201,
    )

@app.route("/upload_track", methods=["POST"])
def upload_track_to_tonie():
    body = request.json;
    tonie_id = body["tonie_id"];
    track_id = body["track_ids"];
    tonie = [to for to in creative_tonies if to.id == tonie_id][0];
    for track in track_id:
        song = [so for so in songs_update() if so['file'] == track];
        upload = Upload.tracks_from_ids(tonie=tonie, song=song)
        status = tonie_cloud_api.put_songs_on_tonie(upload.track, upload.tonie)
    # logger.debug(f"Created upload object: {upload}")
    
    return (
        jsonify(
            {"status": "success",
             "upload_id": "test",
             "songs": songs,
             "track": song,
             "upload": upload,
             "return": status,
             }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
