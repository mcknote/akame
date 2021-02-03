import logging
import re

import requests
from typing import Type
from akame.extraction.core import StaticExtractor, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self, target_url: str):
        super().__init__(target_url)

        self.parse_target_url()
        self.load_url_referrer()
        self.load_url_to_request()

    def parse_target_url(self):
        pattern = r"https://www.books.com.tw/products/([0-9a-zA-Z]+)"
        self.product_id = re.match(pattern, self.target_url).group(1)
        self.target_url = (
            f"https://www.books.com.tw/products/{self.product_id}"
        )

    def load_url_referrer(self):
        self.url_referrer = self.target_url

    def load_url_to_request(self):
        self.url_to_request = (
            "https://www.books.com.tw/product_show/getProdCartInfoAjax/"
            f"{self.product_id}/M201105_005_view"
        )


class Extractor(StaticExtractor):
    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase] = URLManager
    ) -> None:
        super().__init__(target_url, url_manager)

    def load_request_headers(self) -> None:
        self.request_headers = {
            "Host": "www.books.com.tw",
            "Connection": "keep-alive",
            "Accept": "text/html, */*; q=0.01",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": self.urls.url_referrer,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en,zh-TW;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
        }

    def get_response(self) -> requests.Response:
        return requests.get(
            self.urls.url_to_request, headers=self.request_headers
        )

    def main(self) -> str:
        self.load_request_headers()
        response = self.get_response()
        return response.text
