import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional

from akame.comparison.core import ComparerType
from akame.extraction.core import ExtractorType
from akame.notification.core import NotifierType
from akame.utility.caching import TaskCacheManager
from akame.utility.core import MonitoredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_loop_seconds(seconds: float) -> None:
    """Function that checks loop seconds

    Args:
        seconds (float): Loop interval in seconds
    """
    min_seconds = 60
    if seconds < min_seconds:
        logger.warning(
            "Consider increasing the interval "
            f"to {min_seconds} seconds: "
            f"interval < {min_seconds} seconds might "
            "not cover the execution time "
            "and abuse the target website"
        )


def loop_task(*ignore, seconds: float, max_rounds: int) -> Callable:
    """Function that decorates the function with looping

    Args:
        seconds (float): Interval in seconds
        max_rounds (int): Maximum rounds to run

    Returns:
        Callable: Decorated function to be executed
    """
    check_loop_seconds(seconds)

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


# slightly modified from
# https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel
def run_tasks_in_parallel(tasks: List[Callable]):
    """Function that runs multiple monitoring tasks in parallel

    Args:
        tasks (List[Callable]): List of monitoring tasks
    """
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


class SingleMonitorTask:
    """Class that organizes single monitoring task

    Args:
        task_name (str): Name of the task
        extractor (ExtractorType): Content extractor
            that extracts the monitored content
        comparer (ComparerType): Comparer
            that compares the monitored content
        notifiers (List[NotifierType]): List of notifiers
            that push notifications on comparison results
        loop_seconds (float): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
        cache_manager (CacheManagerType): Cache manager
            that archives and loads all monitored content.
            Defaults to None; predefined manager will be initiated
    """

    def __init__(
        self,
        task_name: str,
        extractor: ExtractorType,
        comparer: ComparerType,
        notifiers: List[NotifierType],
        loop_seconds: float,
        loop_max_rounds: int,
        cache_manager: Optional[TaskCacheManager] = None,
    ) -> None:

        logger.info(f"Starting the monitoring task: '{task_name}'")

        self.task_name = str(task_name)
        self.extractor = extractor
        self.comparer = comparer
        self.notifiers = notifiers
        self.initiate_notifiers()
        self.loop_seconds = loop_seconds
        self.loop_max_rounds = loop_max_rounds

        if cache_manager:
            self.cache_manager = cache_manager
        else:
            self.cache_manager = TaskCacheManager(task_name=task_name)

    def initiate_notifiers(self) -> None:
        _ = [
            notifier.load_task_info(
                task_name=self.task_name,
                target_url=self.extractor.urls.target_url,
            )
            for notifier in self.notifiers
        ]

    def extract_monitored_content(self) -> MonitoredContent:
        content = self.extractor.main()
        return MonitoredContent(content)

    def compare_monitored_content(self, mc_1: MonitoredContent) -> None:
        mc_0 = self.cache_manager.get_newest_cache()
        self.cache_manager.cache_task_mc(mc_1)
        content_0 = mc_0.content if mc_0 else None
        content_1 = mc_1.content
        self.comparer.main(content_0=content_0, content_1=content_1)

    def notify_comparison_results(self) -> None:
        for notifier in self.notifiers:
            notifier.main(self.comparer)

    def main(self) -> None:
        def task():
            monitored_content = self.extract_monitored_content()
            self.compare_monitored_content(monitored_content)
            self.notify_comparison_results()

        looper = loop_task(
            seconds=self.loop_seconds, max_rounds=self.loop_max_rounds
        )(task)
        looper()
