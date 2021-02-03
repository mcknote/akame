import logging

from . import BasicComparer
from .formatter import StringDelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PushoverComparer(BasicComparer):
    """Class that handles string comparison for Pushover
    with MonitoredContent and difference marked in HTML

    Args:
        target_url (str): Target URL
    """

    def __init__(self, target_url: str) -> None:
        super().__init__()
        self.target_url = target_url

    def get_delta_in_html(self) -> str:
        finder = StringDelta(a=self.content_0, b=self.content_1)
        return finder.get_delta_in_pushover_html()

    def get_target_url_in_html(self) -> str:
        return f'<a href="{self.target_url}">{self.target_url}</a>'

    def express_comparison_results(self) -> None:

        if self.comparison_status is None:
            self.status_code = -1
            self.message = "INITIATED"
        elif not self.comparison_status:
            self.status_code = 0
            self.message = "UNCHANGED"
        else:
            self.status_code = 1
            message_header = "<b>CHANGES DETECTED</b>"
            message_url = self.get_target_url_in_html()
            message_changes = self.get_delta_in_html()
            self.message = (
                f"{message_header}\n{message_url}\n\n{message_changes}"
            )
