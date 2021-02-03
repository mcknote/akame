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
        notifier_creds (Dict[str, Any]): Pushover credentials
            Requires two keys: `token` and `user_key`
    """

    def __init__(self, task_name: str, notifier_creds: Dict[str, Any]) -> None:
        super().__init__(task_name, notifier_creds)
        self.token = notifier_creds["token"]
        self.user_key = notifier_creds["user_key"]

    def send_notification(self, message: str) -> None:
        logger.info("Sending out notification through Pushover")

        conn = HTTPSConnection("api.pushover.net:443")
        headers = {
            "token": self.token,
            "user": self.user_key,
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
