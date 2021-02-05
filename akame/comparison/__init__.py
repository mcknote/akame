import logging
from typing import Any, Optional, TypeVar, Union

from akame.utility.core import MonitoredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComparerBase:
    """Class that defines the base comparer"""

    mc_0: MonitoredContent
    mc_1: MonitoredContent
    content_0: Any
    content_1: Any
    task_name: str
    target_url: str

    def __init__(self) -> None:
        logging.info(f"Initializing comparer: {self.__class__.__name__}")
        self.comparison_status: Union[bool, None] = None
        self.status_code: int = -1
        self.message: str = ""

    def load_comparison_status(self) -> None:
        self.comparison_status = None

    def compose_comparison_results(self) -> None:
        self.status_code = -1
        self.message = ""

    def main(
        self, mc_1: MonitoredContent, mc_0: Optional[MonitoredContent] = None
    ):
        """Function that loads the content to compare

        Args:
            mc_1 (MonitoredContent): Current mnoitored content
            mc_0 (Optional[MonitoredContent]): Archived monitored content
                to be compared against. Defaults to None.
        """
        self.mc_1 = mc_1
        self.task_name = mc_1.task_name
        self.target_url = mc_1.target_url
        self.mc_0 = mc_0 if mc_0 else MonitoredContent()

        self.content_0 = self.mc_0.content
        self.content_1 = self.mc_1.content

        self.load_comparison_status()
        self.compose_comparison_results()


class BasicComparer(ComparerBase):
    """Class that defines the basic comparer"""

    def __init__(self) -> None:
        super().__init__()

    def load_comparison_status(self) -> None:
        if self.mc_0.content is None:
            self.comparison_status = None
        else:
            self.comparison_status = self.mc_0.content != self.mc_1.content

    def compose_comparison_results(self) -> None:
        if self.comparison_status is None:
            self.status_code = -1
            self.message = "INITIATED"
        elif not self.comparison_status:
            self.status_code = 0
            self.message = "UNCHANGED"
        else:
            self.status_code = 1
            self.message = "CHANGES DETECTED"
