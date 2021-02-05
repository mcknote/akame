import logging
from http.client import HTTPSConnection
from urllib.parse import urlencode

from akame.comparison.delta import StringDelta

from .core import NotifierBase
from .formatters import FormatPushoverHTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PushoverNotifier(NotifierBase):
    """Class that handles notification through Pushover

    Args:
        pushover_token (str): Pushover API token
        pushover_user_key (str): Pushover user key
    """

    def __init__(self, pushover_token: str, pushover_user_key: str) -> None:
        super().__init__()
        self.pushover_token = pushover_token
        self.pushover_user_key = pushover_user_key

    def notify_condition_met(self) -> None:
        logger.info("Sending out notification through Pushover")

        message = self.get_formatted_message()

        conn = HTTPSConnection("api.pushover.net:443")
        headers = {
            "token": self.pushover_token,
            "user": self.pushover_user_key,
            "title": self.comparer.task_name,
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

    def get_formatted_message(self) -> str:
        content_0 = self.comparer.content_0
        content_1 = self.comparer.content_1
        target_url = self.comparer.target_url
        comparer_message = self.comparer.message

        delta = StringDelta(a=content_0, b=content_1)
        formatter = FormatPushoverHTML(delta)

        return formatter.main(
            comparer_message=comparer_message, target_url=target_url
        )
