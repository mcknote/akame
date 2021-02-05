import logging
from typing import TypeVar

from akame.comparison import ComparerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
NotifierType = TypeVar("NotifierType", bound="NotifierBase")


class NotifierBase:
    """Class that defines the base notifier"""

    comparer: ComparerBase

    def __init__(self) -> None:
        """Function that loads notifier configurations (e.g. credentials)"""
        logging.info(f"Initializing notifier: {self.__class__.__name__}")

    def get_formatted_message(self) -> str:
        return ""

    def notify_condition_met(self) -> None:
        message = self.get_formatted_message()

    def notify_condition_notmet(self) -> None:
        pass

    def main(self, comparer: ComparerBase) -> None:
        """Funtion that notifies based on comparer's info

        Args:
            comparer (ComparerBase): Comparer
        """
        self.comparer = comparer
        if self.comparer.status_code == 1:
            self.notify_condition_met()
        else:
            self.notify_condition_notmet()
