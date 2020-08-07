from base64 import b64encode
from typing import ClassVar

import requests


class TonieCloudSession(requests.Session):
    URI: ClassVar[str] = "https://api.tonie.cloud/v2"

    def __init__(self):
        super().__init__()
        self.token: str = None  # type: ignore

    def acquire_token(self, username: str, password: str) -> None:
        self.token = self._acquire_token(username, password)

    def _acquire_token(self, username: str, password: str) -> str:
        req = requests.post(f"{self.URI}/sessions", json={"email": username, "password": password,})

        return req.json()["jwt"]
