import os

from models.audio import AudioBook
from models.tonie import Tonie
from toniecloud.client import TonieCloud


def upload_facade(audiobook: AudioBook, tonie: Tonie) -> bool:
    api = TonieCloud(os.environ.get("TONIE_AUDIO_MATCH_USER"), os.environ.get("TONIE_AUDIO_MATCH_PASS"))
    return api.put_album_on_tonie(audiobook, tonie)
