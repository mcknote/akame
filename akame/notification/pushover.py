import logging
from http.client import HTTPSConnection
from typing import Any, Dict
from urllib.parse import urlencode

from akame.comparison.core import ComparerType

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PushoverNotifier(NotifierBase):
    """Class that handles notification through Pushover

    Args:
        task_name (str): Task name
        pushover_token (str): Pushover API token
        pushover_user_key (str): Pushover user key
    """

    def __init__(
        self, task_name: str, pushover_token: str, pushover_user_key: str
    ) -> None:
        super().__init__(task_name)
        self.pushover_token = pushover_token
        self.pushover_user_key = pushover_user_key

    def send_notification(self, message: str) -> None:
        logger.info("Sending out notification through Pushover")

        conn = HTTPSConnection("api.pushover.net:443")
        headers = {
            "token": self.pushover_token,
            "user": self.pushover_user_key,
            "title": self.task_name,
            "message": message,
            "html": 1,
        }
        conn.request(
            "POST",
            "/1/messages.json",
            urlencode(headers),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        try:
            conn.getresponse()
        except Exception as e:
            logger.error(f"Failed to send the message: {e}")

    def main(self, comparer: ComparerType) -> None:
        if comparer.status_code == 1:
            self.send_notification(comparer.message)
