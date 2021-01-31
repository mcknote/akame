import logging

from http.client import HTTPSConnection
from urllib.parse import urlencode

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PONotifier(NotifierBase):
    def __init__(self, task_name: str, token: str, user_key: str) -> None:
        super().__init__(task_name)
        self.token = token
        self.user_key = user_key

    def send_notification(self):
        logger.info("Sending out notification through PushOver")

        conn = HTTPSConnection("api.pushover.net:443")
        headers = {
            "token": self.token,
            "user": self.user_key,
            "title": self.task_name,
            "message": "monitored content has changed",
        }
        conn.request(
            "POST",
            "/1/messages.json",
            urlencode(headers),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()

    def main(self, status_code: int):
        if status_code == 0:
            pass
        elif status_code == 1:
            self.send_notification()
