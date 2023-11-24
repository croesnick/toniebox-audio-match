import os
from pathlib import Path

import localstorage.client
from flask import g
from models.audio import AudioBook, AudioTrack
from toniecloud.client import TonieCloud

from server.config import Config

tonie_api_client = None

logger = Config.configure_logger(__name__)


def get_tonie_api():
    global tonie_api_client
    if tonie_api_client is None:
        # Initialize the Tonie API client here
        tonie_api_client = TonieCloud(
            os.environ.get("TONIE_AUDIO_MATCH_USER"),
            os.environ.get("TONIE_AUDIO_MATCH_PASS"),
        )
    return tonie_api_client


def audiobooks():
    audiobooks = localstorage.client.audiobooks(Path("../assets/audiobooks"))
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


def get_creative_tonies():
    creative_tonies = g.tonie_api_client.creativetonies()
    print(f"Creative_Tonies:{creative_tonies}")
    return creative_tonies


def get_item_from_request(req_json, item_key, items):
    item_ids = req_json.get(item_key, [])
    if not isinstance(item_ids, list):
        item_ids = [item_ids]

    matched_items = []

    for item_id in item_ids:
        for item in items:
            # Check if the item is a dictionary
            if isinstance(item, dict):
                if item["id"] == item_id:
                    matched_items.append(item)
            # Check if the item is a class object
            else:
                if item.id == item_id:
                    matched_items.append(item)

    return matched_items if matched_items else None
