import logging
import re

import requests

from .core import StaticExtractor, URLBase, URLExtractorType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLExtractor(URLBase):
    def __init__(self, target_url: str):
        super().__init__(target_url)
        self.url_referrer = None
        self.url_cart_api = None

        self.clean_up_target_url()
        self.clean_up_target_url()
        self.load_url_referrer()
        self.load_url_cart_api()

    def clean_up_target_url(self):
        pattern = "https://24h.pchome.com.tw/prod/([^\\?]+)"
        self.product_id = re.match(pattern, self.target_url).group(1)
        self.target_url = f"https://24h.pchome.com.tw/prod/{self.product_id}"

    def load_url_referrer(self):
        self.url_referrer = self.target_url

    def load_url_cart_api(self):
        self.url_cart_api = (
            "https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/"
            f"button&id={self.product_id}"
            "&fields=Seq,Id,Price,Qty,ButtonType,SaleStatus,isPrimeOnly,SpecialQty"
            "&_callback=jsonp_button&1611904320?_callback=jsonp_button"
        )


class ContentExtractor(StaticExtractor):
    def __init__(self, url_extractor: URLExtractorType):
        super().__init__(url_extractor)

    def load_request_headers(self):
        self.request_headers = {
            "authority": "ecapi.pchome.com.tw",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "accept": "*/*",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "script",
            "referer": self.url_extractor.url_referrer,
            "accept-language": "en,zh-TW;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
        }

    def get_response(self) -> requests.Response:
        return requests.get(
            self.url_extractor.url_cart_api, headers=self.request_headers
        )

    def main(self):
        self.load_request_headers()
        response = self.get_response()
        return response
