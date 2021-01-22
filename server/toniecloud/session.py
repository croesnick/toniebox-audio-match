from base64 import b64encode
from typing import ClassVar

import requests


class TonieCloudSession(requests.Session):
    URI: ClassVar[str] = "https://api.tonie.cloud/v2"
    OPENID_CONNECT: ClassVar[str] = "https://login.tonies.com/auth/realms/tonies/protocol/openid-connect/token"

    def __init__(self):
        super().__init__()
        self.token: str = None  # type: ignore

    def acquire_token(self, username: str, password: str) -> None:
        self.token = self._acquire_token(username, password)

    def _acquire_token(self, username: str, password: str) -> str:
        data = {
            "grant_type": 'password',
            "client_id": "my-tonies",
            "scope": "openid",
            "username": username,
            "password": password,
        }
        response = requests.post(self.OPENID_CONNECT, data=data)
        return response.json()["access_token"]
