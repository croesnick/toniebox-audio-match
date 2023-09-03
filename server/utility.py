import logging
import os
import sys
from pathlib import Path

import localstorage.client
from models.audio import AudioBook, AudioTrack
from toniecloud.client import TonieCloud

tonie_api_client = None

def logger():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    logger = logging.getLogger(__name__)
    return logger

def get_tonie_api():
    global tonie_api_client
    if tonie_api_client is None:
        tonie_api_client = TonieCloud(os.environ.get("TONIE_AUDIO_MATCH_USER"), 
                                      os.environ.get("TONIE_AUDIO_MATCH_PASS"))
    return tonie_api_client

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

def get_creative_tonies():
    tonie_api_client = get_tonie_api()
    creative_tonies = tonie_api_client.creativetonies()
    return creative_tonies