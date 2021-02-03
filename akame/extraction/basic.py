import logging

import requests

from .core import StaticExtractor, URLManagerBase
from typing import Type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self, target_url: str) -> None:
        super().__init__(target_url)


class Extractor(StaticExtractor):
    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase] = URLManager
    ) -> None:
        super().__init__(target_url, url_manager)

    def load_request_headers(self) -> None:
        self.request_headers = {
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "accept": "*/*",
        }

    def get_response(self) -> requests.Response:
        return requests.get(
            self.urls.url_to_request, headers=self.request_headers
        )

    def main(self) -> str:
        self.load_request_headers()
        response = self.get_response()
        return response.text
