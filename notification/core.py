import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotifierBase:
    def __init__(self, task_name: str) -> None:
        logging.info("Initializing notifier")
        self.task_name = task_name