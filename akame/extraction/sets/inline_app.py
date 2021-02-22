import json
import logging
import re
from json.decoder import JSONDecodeError
from typing import Type

from akame.extraction.core import StaticExtractor, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self) -> None:
        super().__init__()

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


class Extractor(StaticExtractor):
    """Class that extracts restaurant availability from inline.app

    Args:
        url_manager (Type[URLManagerBase], optional):
            URL Manager to parse the URL. Defaults to URLManager.
    """

    def __init__(self, url_manager: Type[URLManagerBase] = URLManager) -> None:
        super().__init__(url_manager)

    def get_parsed_content(self, response) -> str:
        response_text = response.text
        report = ""

        try:
            response_dict = json.loads(response_text)
            dates_open = response_dict["default"]
            seats_open = {
                date: seats for date, seats in dates_open.items() if seats
            }
            report = (
                f"Dates with open seats: '{seats_open}';\n"
                f"Dates open: '{dates_open}';"
            )

        except JSONDecodeError as e:
            logger.error(e)

        except Exception as e:
            logger.error(e)

        return report
