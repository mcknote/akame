import logging
import re
from typing import Type

from akame.extraction.core import ExtractorBase, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self, target_url: str):
        super().__init__(target_url)

        self.parse_target_url()
        self.load_url_to_request()

    def parse_target_url(self):
        pattern = (
            r"https://inline.app/booking/"
            r"(?P<company_id>.+)/"
            r"(?P<branch_id>.+)[/\?]*"
        )
        matched = re.match(pattern, self.target_url)
        self.company_id = matched.group("company_id")
        self.branch_id = matched.group("branch_id")

    def load_url_to_request(self):
        self.url_to_request = (
            r"https://inline.app/api/booking-capacities?"
            rf"companyId={self.company_id}"
            rf"&branchId={self.branch_id}"
        )


class Extractor(ExtractorBase):
    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase] = URLManager
    ) -> None:
        super().__init__(target_url, url_manager)