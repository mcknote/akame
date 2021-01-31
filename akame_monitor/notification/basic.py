import logging

from akame_monitor.comparison.core import ComparerType

from .core import NotifierBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicNotifier(NotifierBase):
    def __init__(self, task_name: str) -> None:
        super().__init__(task_name)

    def send_notification(self, message: str) -> None:
        logger.info(message)

    def main(self, comparer: ComparerType) -> None:
        self.send_notification(comparer.message)
