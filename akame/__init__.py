import logging
from typing import Any, Dict

from akame.extraction.core import ContentExtractorType, URLExtractorType

from .comparison.basic import BasicComparer
from .extraction import select_sets
from .notification.basic import BasicNotifier
from .utility.caching import reset_cached_folder
from .utility.task import SingleMonitorTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Function that initaties akame dependencies"""
    logger.info("Initiating akame dependencies")
    reset_cached_folder(reset_whole_folder=True)


def monitor_in_console(
    task_name: str,
    target_url: str,
    exset_name: str,
    loop_seconds: int,
    loop_max_rounds: int,
) -> None:
    """Function that runs basic monitoring tasks
    and shows results through console logs

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        exset_name (str): Name of the extraction set from `extraction.sets`
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
    """
    logger.info(f"Setting up the monitoring task: '{task_name}'")
    URLExtractor, ContentExtractor = select_sets(exset_name)

    # initiate url_extractor, content_extractor, notifier
    url_extractor = URLExtractor(target_url=target_url)
    content_extractor = ContentExtractor(url_extractor=url_extractor)
    comparer = BasicComparer()
    notifiers = [
        BasicNotifier(task_name),
    ]

    monitor_task = SingleMonitorTask(
        task_name=task_name,
        content_extractor=content_extractor,
        comparer=comparer,
        notifiers=notifiers,
        loop_seconds=loop_seconds,
        loop_max_rounds=loop_max_rounds,
    )
    monitor_task.main()
