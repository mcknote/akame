import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional

from akame.comparison import BasicComparer
from akame.comparison.core import ComparerBase
from akame.extraction import BasicExtractor
from akame.extraction.core import ExtractorBase
from akame.notification import BasicNotifier
from akame.notification.core import NotifierBase
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
        task_name (Optional[str]): Name of the task.
            Defaults to None

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
    """Class that organizes the monitoring task

    Args:
        target_url (str):
            URL to monitor.
        task_name (str):
            Name of the task.
        loop_seconds (float, optional):
            Interval in seconds between all rounds.
            Defaults to 300.
        loop_max_rounds (int, optional):
            Maximum number of rounds to monitor.
            Defaults to 288.
        extractor (Optional[ExtractorBase], optional):
            Content extractor that extracts the monitored content.
            Defaults to None.
        comparer (Optional[ComparerBase], optional):
            Comparer that compares the monitored content.
            Defaults to None.
        notifiers (Optional[List[NotifierBase]], optional):
            List of notifiers that push notifications on comparison results.
            Defaults to None.
        cache_manager (Optional[TaskCacheManager], optional):
            Cache manager that archives and loads all monitored content.
            Defaults to None.
    """

    def __init__(
        self,
        target_url: str,
        task_name: str,
        loop_seconds: float = 300,
        loop_max_rounds: int = 288,
        extractor: Optional[ExtractorBase] = None,
        comparer: Optional[ComparerBase] = None,
        notifiers: Optional[List[NotifierBase]] = None,
        cache_manager: Optional[TaskCacheManager] = None,
    ) -> None:

        logger.info(f"Starting the monitoring task: '{task_name}'")
        self.target_url = target_url
        self.task_name = str(task_name)
        self.loop_seconds = loop_seconds
        self.loop_max_rounds = loop_max_rounds

        self.extractor = extractor if extractor else BasicExtractor()
        self.comparer = comparer if comparer else BasicComparer()
        self.notifiers = notifiers if notifiers else [BasicNotifier()]

        self.cache_manager = (
            cache_manager
            if cache_manager
            else TaskCacheManager(task_name=task_name)
        )

    def extract_monitored_content(self) -> MonitoredContent:
        """Function that extracts monitored content

        Returns:
            MonitoredContent: Monitored content
        """
        content = self.extractor.main(target_url=self.target_url)
        return MonitoredContent(
            task_name=self.task_name,
            target_url=self.target_url,
            content=content,
        )

    def compare_monitored_content(self, mc_1: MonitoredContent) -> None:
        """Function that compares monitored content

        Args:
            mc_1 (MonitoredContent): Monitored content to compare
        """
        mc_0 = self.cache_manager.get_newest_cache()
        self.cache_manager.cache_task_mc(mc_1)
        self.comparer.main(mc_0=mc_0, mc_1=mc_1)

    def notify_comparison_results(self) -> None:
        """Function that notifies of comparison results. The notification logic
        is defined in each notifier
        """
        for notifier in self.notifiers:
            notifier.main(self.comparer)

    def main(self) -> None:
        """Function that performs the monitoring tasks on a loop"""

        def task():
            monitored_content = self.extract_monitored_content()
            self.compare_monitored_content(monitored_content)
            self.notify_comparison_results()

        looper = loop_task(
            seconds=self.loop_seconds,
            max_rounds=self.loop_max_rounds,
        )(task)
        looper()
