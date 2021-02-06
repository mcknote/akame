import logging
from typing import Type

import requests

from akame.extraction.core import StaticExtractor, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self) -> None:
        super().__init__()

    def parse_target_url(self):
        pass

    def load_url_referrer(self):
        self.url_referrer = f"https://www.clearadmit.com/"

    def load_url_to_request(self):
        self.url_to_request = self.target_url


class Extractor(StaticExtractor):
    """Class that extracts application reports from Clear Admit

    Args:
        action (str): Data pull action on CA (e.g. livewire_load_posts)
        school (str): School code (e.g. harvard)
        round (str): Application round (e.g. round-1)
        status (str): Application status (e.g. interview-invite)
        orderby (str, optional): Order of the results. Defaults to "default".
        paged (int, optional): Page to fetch. Defaults to 1.
        url_manager (Type[URLManagerBase], optional):
            URL Manager to parse the URL. Defaults to URLManager.
    """

    def __init__(
        self,
        action: str,
        school: str,
        round: str,
        status: str,
        orderby: str = "default",
        paged: int = 1,
        url_manager: Type[URLManagerBase] = URLManager,
    ) -> None:
        super().__init__(url_manager)

        self.action = action
        self.school = school
        self.round = round
        self.status = status
        self.orderby = orderby
        self.paged = paged

    def load_request_data(self) -> None:
        self.request_data = {
            "action": self.action,
            "school": self.school,
            "round": self.round,
            "status": self.status,
            "orderby": self.orderby,
            "paged": self.paged,
        }

    def get_response(self) -> requests.Response:
        return requests.post(
            self.urls.url_to_request,
            headers=self.request_headers,
            data=self.request_data,
        )