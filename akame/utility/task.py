import logging
import time
from typing import Callable, List

from akame.comparison.core import ComparerType
from akame.extraction.core import ContentExtractorType
from akame.notification.core import NotifierType

from .caching import (
    cache_mc,
    get_cached_mc,
    reset_cached_folder,
    get_task_hash,
)
from .core import MonitoredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loop_task(*ignore, seconds: int, max_rounds: int) -> Callable:
    """Function that decorates the function with looping

    Args:
        seconds (int): interval in seconds
        max_rounds (int): maximum rounds to run

    Returns:
        Callable: decorated function
    """
    logger.info(
        f"Looping the task every {seconds} seconds "
        f"until {max_rounds} rounds"
    )

    def decorator(function) -> Callable:
        def wrapper(*args, **kwargs):
            round = 0
            while round < max_rounds:
                start_time = time.time()
                round += 1
                logger.info(f"Going round {round}")
                function(*args, **kwargs)
                used_interval = (time.time() - start_time) % seconds
                time.sleep(seconds - used_interval)

        return wrapper

    return decorator


class SingleMonitorTask:
    """Class that organizes single monitoring task

    Args:
        task_name (str): Name of the task
        content_extractor (ContentExtractorType): Content extractor
        comparer (ComparerType): Comparer
        notifiers (List[NotifierType]): List of notifiers
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
    """

    def __init__(
        self,
        task_name: str,
        content_extractor: ContentExtractorType,
        comparer: ComparerType,
        notifiers: List[NotifierType],
        loop_seconds: int,
        loop_max_rounds: int,
    ) -> None:

        logger.info(f"Starting the monitoring task: '{task_name}'")

        self.task_name = task_name
        self.task_hash = get_task_hash(task_name)
        self.content_extractor = content_extractor
        self.comparer = comparer
        self.notifiers = notifiers
        self.loop_seconds = loop_seconds
        self.loop_max_rounds = loop_max_rounds

        reset_cached_folder()

    def get_monitored_content(self) -> MonitoredContent:
        content = self.content_extractor.main()
        return MonitoredContent(content)

    def compare_mirrored_content(self, mc_1: MonitoredContent) -> None:
        mc_0 = get_cached_mc()
        cache_mc(mc_1)
        content_0 = mc_0.content if mc_0 else None
        content_1 = mc_1.content
        self.comparer.main(content_0=content_0, content_1=content_1)

    def notify_comparison_results(self) -> None:
        for notifier in self.notifiers:
            notifier.main(self.comparer)

    def main(self) -> None:
        def task():
            monitored_content = self.get_monitored_content()
            self.compare_mirrored_content(monitored_content)
            self.notify_comparison_results()

        looper = loop_task(
            seconds=self.loop_seconds, max_rounds=self.loop_max_rounds
        )(task)
        looper()
