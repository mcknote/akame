import logging
import re
from ast import literal_eval
from typing import Dict, List, Optional, Union

import requests

from akame.extraction.sets.inline_app import URLManager
from akame.notification.core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InlineReservationHelper(NotifierBase):
    """Class that handles reservation through Inline

    Args:
        desired_group_size (int): Desired group size
        desired_dates (List[str]): Desired dates
        desired_times (Optional[List[str]]): Desired times
        contact_name (str): Contact name
        contact_phone (str): Contact phone
    """

    def __init__(
        self,
        desired_group_size: int,
        desired_dates: List[str],
        desired_times: Optional[List[str]],
        contact_name: str,
        contact_phone: str,
    ) -> None:
        super().__init__()
        self.desired_group_size = desired_group_size
        self.desired_dates = desired_dates
        self.desired_times = desired_times
        self.contact_name = contact_name
        self.contact_phone = contact_phone

        self.url_manager = URLManager()
        self.url_to_request = "https://inline.app/api/reservations"

    def notify_condition_met(self) -> None:
        self.parse_target_url()
        self.load_request_headers()
        self.load_available_dates()

        reserve_success = False

        for available_date in self.available_dates:
            logger.info(
                f"Making reservation at {available_date['date']} "
                f"{available_date['time']} "
                f"for party size of {available_date['size']} "
            )
            request_data = self.get_request_data(available_date)

            request = requests.post(
                url=self.url_to_request,
                headers=self.request_headers,
                data=request_data,
            )

            if request.status_code == 200:
                reserve_success = True
                break

        if reserve_success:
            logger.info(
                "Successfully made a reservation "
                f"using the following info: \n{request_data}"
            )
        else:
            logger.info("Failed to make any reservation")

    def parse_target_url(self):
        self.url_manager.main(self.comparer.target_url)
        self.company_id = self.url_manager.company_id
        self.branch_id = self.url_manager.branch_id

    def load_request_headers(self):
        self.request_headers = {
            "authority": "inline.app",
            "accept": "application/json",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "content-type": "application/json",
            "origin": "https://inline.app",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": (
                r"https://inline.app/booking/"
                rf"{self.company_id}/{self.branch_id}/form"
            ),
            "accept-language": "en,zh-TW;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
        }

    def load_available_dates(self, reserve_all_or_none: bool = True):

        pattern = r"Dates with open seats: '(?P<open_seats>\{.*?\})';"
        message = self.comparer.mc_1.content
        message = str(message) if message else "{}"
        avail_found = re.search(pattern, message)
        avail_raw = avail_found.group("open_seats") if avail_found else "{}"
        avail_parsed: Dict[str, Dict[str, List[int]]] = literal_eval(avail_raw)

        # TODO: use dataclass to improve type checking here
        avail_list: List[Dict] = [
            {
                "date": dt,
                "time": tm,
                "size": min(max(seats), self.desired_group_size),
            }
            for dt, info in avail_parsed.items()
            for tm, seats in info.items()
        ]

        # sort by group size
        avail_list = sorted(avail_list, key=lambda x: x["size"], reverse=True)

        # filter group size
        if reserve_all_or_none:
            avail_list = [
                x for x in avail_list if x["size"] >= self.desired_group_size
            ]

        # filter desired dates
        avail_list = [x for x in avail_list if x["date"] in self.desired_dates]

        # filter desired times
        if self.desired_times:
            avail_list = [
                x for x in avail_list if x["time"] in self.desired_times
            ]

        self.available_dates = avail_list

    def get_request_data(self, available_date: Dict[str, Union[str, int]]):
        request_data = {
            "language": "en",
            "company": self.company_id,
            "branch": self.branch_id,
            "groupSize": available_date["size"],
            "kids": 0,
            "gender": 2,
            "purposes": [],
            "email": "",
            "name": self.contact_name,
            "phone": self.contact_phone,
            "note": "",
            "date": available_date["date"],
            "time": available_date["time"],
            "numberOfKidChairs": 0,
            "numberOfKidSets": 0,
            "skipPhoneValidation": False,
        }
        return request_data
