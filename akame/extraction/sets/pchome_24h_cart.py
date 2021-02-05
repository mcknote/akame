import logging
import re
from typing import Type

import requests

from akame.extraction.core import StaticExtractor, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self) -> None:
        super().__init__()

    def parse_target_url(self):
        pattern = r"https://24h.pchome.com.tw/prod/([^\?]+)"
        self.product_id = re.match(pattern, self.target_url).group(1)
        self.target_url = f"https://24h.pchome.com.tw/prod/{self.product_id}"

    def load_url_referrer(self):
        self.url_referrer = self.target_url

    def load_url_to_request(self):
        self.url_to_request = (
            "https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/"
            f"button&id={self.product_id}"
            "&fields=Seq,Id,Price,Qty,ButtonType,SaleStatus,isPrimeOnly,SpecialQty"
            "&_callback=jsonp_button&1611904320?_callback=jsonp_button"
        )


class Extractor(StaticExtractor):
    def __init__(self, url_manager: Type[URLManagerBase] = URLManager) -> None:
        super().__init__(url_manager)

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
            "referer": self.urls.url_referrer,
            "accept-language": "en,zh-TW;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
        }
