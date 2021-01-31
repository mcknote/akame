import logging
from typing import TypeVar

from akame_monitor.comparison.core import ComparerType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
NotifierType = TypeVar("NotifierType", bound="NotifierBase")


class NotifierBase:
    """Class that defines the base notifier
    """

    def __init__(self, task_name: str) -> None:
        logging.info(f"Initializing notifier: {self.__class__.__name__}")
        self.task_name = task_name

    def main(self, comparer: ComparerType) -> None:
        """Funtion that notifies based on comparer's info

        Args:
            comparer (ComparerType): Comparer
        """
        pass
