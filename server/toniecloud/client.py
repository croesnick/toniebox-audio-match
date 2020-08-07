import enum
import logging
import mimetypes
from pathlib import Path
from typing import List

from models.audio import AudioBook, AudioTrack
from models.tonie import Tonie, Household
from toniecloud.session import TonieCloudSession

logger = logging.getLogger(__name__)

MIME_TO_CONTENT_TYPE = {
    "audio/mp4a-latm": "audio/x-m4a",
}


class Verb(enum.Enum):
    GET = "GET"
    POST = "POST"


class TonieCloud:
    def __init__(self, username: str, password: str) -> None:
        self.session = TonieCloudSession()

        self._username = username
        self._password = password

        self.session.acquire_token(username, password)

    @property
    def url(self):
        return self.session.URI

    @property
    def auth_header(self):
        return {"Authorization": f"Bearer {self.session.token}"}

    def households(self) -> List[Household]:
        return [Household(household["id"]) for household in self._get("households")]

    def creativetonies(self) -> List[Tonie]:
        tonies: List[Tonie] = []
        for household in self.households():
            url = f"households/{household.id}/creativetonies"
            data = self._get(url)
            for tonie in data:
                tonies.append(Tonie(id=tonie["id"], household=household, name=tonie["name"], image=tonie["imageUrl"]))

        return tonies

    def put_album_on_tonie(self, audiobook: AudioBook, tonie: Tonie) -> bool:
        data = {
            "chapters": [
                {"title": track.title, "file": self._upload_track(track)}
                for track in sorted(audiobook.tracks, key=lambda t: t.track)
            ]
        }

        logger.debug("Sending chapter data from audio book %r to tonie %r: %r", audiobook.album, tonie.name, data)
        response = self.session.patch(
            f"{self.url}/households/{tonie.household.id}/creativetonies/{tonie.id}", headers=self.auth_header, json=data
        )

        if not response.ok:
            logger.error("Something went wrong :'( -> %s", response)
            return False

        body = response.json()

        logger.info("Yay! Uploaded album %r to tonie %r! Response: %s", audiobook.album, tonie.name, response)

        logger.debug("Transcoding errors: %r", body["transcodingErrors"])
        logger.debug("Chapters on tonie %r: %r", tonie.name, body["chapters"])
        logger.debug("Seconds remaining on tonie %r: %r", tonie.name, body["secondsRemaining"])

        return True

    def _upload_track(self, track: AudioTrack) -> str:
        return self._upload_file(track.file)

    def _upload_file(self, file: Path) -> str:
        data = self.session.post(f"{self.url}/file", headers=self.auth_header).json()
        logger.debug("Response of POST /file: %r", data)

        payload = data["request"]["fields"]

        audio_mime_type = mimetypes.guess_type(file)
        logger.debug("Guessed MIME type %r for file %r", audio_mime_type, str(file))
        if audio_mime_type in MIME_TO_CONTENT_TYPE:
            files = {"file": (data["request"]["fields"]["key"], file.open("rb"), MIME_TO_CONTENT_TYPE[audio_mime_type])}
        else:
            files = {"file": (data["request"]["fields"]["key"], file.open("rb"))}

        response = self.session.post(data["request"]["url"], data=payload, files=files)
        if not response.ok:
            raise ValueError("Well, something went wrong. :'(")

        logger.debug("File location: %r, id: %r", response.headers["Location"], data["fileId"])
        return data["fileId"]

    def _get(self, path: str) -> dict:
        headers = {"Authorization": f"Bearer {self.session.token}"}

        resp = self.session.request("GET", f"{self.url}/{path}", headers=headers, data={})

        if not resp.ok:
            # TODO Properly handle errors, especially outdated tokens
            logger.error("HTTP request failed: %s", resp)
            return {}

        return resp.json()
