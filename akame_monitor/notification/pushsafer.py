import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PSNotifier(NotifierBase):
    def __init__(self, task_name: str, pushsafer_key: str) -> None:
        super().__init__(task_name)
        self.pushsafer_key = pushsafer_key
        self.endpoint = "https://www.pushsafer.com/api"
        self.device_id = 35088

    def send_notification(self):
        logger.info("Sending out notification through PushSafer")
        post_fields = {
            "t": self.task_name,
            "m": "monitored content has changed",
            "s": None,
            "v": None,
            "i": 1,
            "c": None,
            "d": self.device_id,
            "u": None,
            "ut": None,
            "k": self.pushsafer_key,
        }

        request = Request(self.endpoint, urlencode(post_fields).encode())
        json = urlopen(request).read().decode()
        print(json)

    def main(self, status_code: int):
        if status_code == 0:
            pass
        elif status_code == 1:
            self.send_notification()
