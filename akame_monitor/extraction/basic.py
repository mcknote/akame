import logging

import requests

from .core import StaticExtractor, URLBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLExtractor(URLBase):
    def __init__(self, target_url: str):
        super().__init__(target_url)


class ContentExtractor(StaticExtractor):
    def __init__(self, url_extractor: URLExtractor) -> None:
        self.url_extractor = url_extractor

    def load_request_headers(self) -> None:
        self.request_headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/88.0.4324.96 Safari/537.36",
            "accept": "*/*",
        }

    def get_response(self) -> requests.Response:
        return requests.get(self.url_extractor.target_url, headers=self.request_headers)

    def main(self) -> str:
        self.load_request_headers()
        response = self.get_response()
        return response.text
