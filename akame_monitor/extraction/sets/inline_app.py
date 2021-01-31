import logging
import re

import requests
from akame_monitor.extraction.core import URLBase, URLExtractorType

from .basic import ContentExtractor as BasicContentExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLExtractor(URLBase):
    def __init__(self, target_url: str):
        super().__init__(target_url)

        self.clean_up_target_url()
        self.load_url_api_endpoint()

    def clean_up_target_url(self):
        pattern = (
            r"https://inline.app/booking/(?P<company_id>.+)/(?P<branch_id>.+)[/\?]*"
        )
        matched = re.match(pattern, self.target_url)
        self.company_id = matched.group("company_id")
        self.branch_id = matched.group("branch_id")

    def load_url_api_endpoint(self):
        self.url_api_endpoint = (
            r"https://inline.app/api/booking-capacities?"
            rf"companyId={self.company_id}"
            rf"&branchId={self.branch_id}"
        )


class ContentExtractor(BasicContentExtractor):
    def __init__(self, url_extractor: URLExtractorType) -> None:
        super().__init__(url_extractor)

    def get_response(self) -> requests.Response:
        return requests.get(
            self.url_extractor.url_api_endpoint, headers=self.request_headers
        )
