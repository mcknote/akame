import requests

from .core import URLBase, StaticExtractor


class BasicExtractor(StaticExtractor):
    def __init__(self, url_base: URLBase):
        self.url_base = url_base

    def load_request_headers(self):
        self.request_headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/88.0.4324.96 Safari/537.36",
            "accept": "*/*",
        }

    def get_response(self) -> requests.Response:
        return requests.get(self.url_base.target_url, headers=self.request_headers)

    def main(self):
        self.load_request_headers()
        response = self.get_response()
        return response
