import logging
from typing import TypeVar

from akame_monitor.comparison.core import ComparerType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotifierBase:
    def __init__(self, task_name: str) -> None:
        logging.info(f"Initializing notifier: {self.__class__.__name__}")
        self.task_name = task_name

    def main(self, comparer: ComparerType):
        pass


NotifierType = TypeVar("NotifierType", bound="NotifierBase")
