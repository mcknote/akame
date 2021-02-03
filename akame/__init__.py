import logging
from typing import Any, Dict

from .comparison import BasicComparer
from .extraction import BasicExtractor
from .notification import BasicNotifier
from .tasks import SingleMonitorTask
from .utility.caching import TaskCacheManager, reset_cached_folder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Function that initaties akame dependencies"""
    logger.info("Initiating akame dependencies")
    reset_cached_folder(reset_whole_folder=True)


def monitor_in_console(
    task_name: str,
    target_url: str,
    loop_seconds: int,
    loop_max_rounds: int,
) -> None:
    """Function that runs basic monitoring tasks
    and shows results through console logs

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
    """
    logger.info(f"Setting up the monitoring task: '{task_name}'")

    # initiate extractor
    extractor = BasicExtractor(target_url=target_url)

    # initiate comparer
    comparer = BasicComparer()

    # initiate notifiers
    notifiers = [
        BasicNotifier(task_name),
    ]
    cache_manager = TaskCacheManager(task_name=task_name)

    monitor_task = SingleMonitorTask(
        task_name=task_name,
        content_extractor=extractor,
        comparer=comparer,
        notifiers=notifiers,
        cache_manager=cache_manager,
        loop_seconds=loop_seconds,
        loop_max_rounds=loop_max_rounds,
    )
    monitor_task.main()
