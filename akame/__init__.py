import logging
from typing import Any, Dict

from .comparison.pushover import PushoverComparer
from .extraction.selector import get_extraction_set
from .notification.basic import BasicNotifier
from .notification.pushover import PushoverNotifier
from .utility.task import SingleMonitorTask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_task(
    task_name: str,
    target_url: str,
    exset_name: str,
    loop_seconds: int,
    loop_max_rounds: int,
    notify_creds: Dict[str, Any],
) -> None:
    """Function that runs the monitoring task

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        exset_name (str): Name of the extraction set from `extraction.sets`
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
        notify_creds (Dict[str, Any]): Credential for notification programs
    """
    logger.info(f"Setting up the monitoring task: '{task_name}'")

    url_extractor, content_extractor = get_extraction_set(exset_name)

    # initiate url_extractor, content_extractor, notifier
    url_extractor = url_extractor(target_url=target_url)
    content_extractor = content_extractor(url_extractor=url_extractor)
    comparer = PushoverComparer(target_url=target_url)
    notifiers = [
        BasicNotifier(task_name),
        PushoverNotifier(task_name, notify_creds=notify_creds),
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
