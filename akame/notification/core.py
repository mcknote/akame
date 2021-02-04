import logging
from typing import TypeVar

from akame.comparison.core import ComparerType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
NotifierType = TypeVar("NotifierType", bound="NotifierBase")


class NotifierBase:
    """Class that defines the base notifier"""

    task_name: str
    target_url: str

    def __init__(self) -> None:
        """Function that loads notifier configurations (e.g. credentials)"""
        logging.info(f"Initializing notifier: {self.__class__.__name__}")

    def load_task_info(self, task_name: str, target_url: str) -> None:
        """Function that loads task configurations (e.g. task name)

        Args:
            task_name (str): Name of the task
            target_url (str): Target URL
        """
        self.task_name = task_name
        self.target_url = target_url

    def get_formatted_message(self, comparer: ComparerType) -> str:
        pass

    def main(self, comparer: ComparerType) -> None:
        """Funtion that notifies based on comparer's info

        Args:
            comparer (ComparerType): Comparer
        """
        pass
