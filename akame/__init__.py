import logging
from typing import Any, Dict

from .comparison import BasicComparer
from .extraction import BasicExtractor
from .notification import BasicNotifier
from .notification.email_sendgrid import SendGridNotifier
from .notification.pushover import PushoverNotifier
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
    notifiers = [BasicNotifier(task_name)]
    # initiate notifiers
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


def monitor_with_pushover(
    task_name: str,
    target_url: str,
    loop_seconds: int,
    loop_max_rounds: int,
    pushover_token: str,
    pushover_user_key: str,
) -> None:
    """Function that runs basic monitoring tasks
    and shows results through Pushover notifications

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
        pushover_token (str): Pushover API token
        pushover_user_key (str): Pushover API token
    """
    logger.info(f"Setting up the monitoring task: '{task_name}'")

    # initiate extractor
    extractor = BasicExtractor(target_url=target_url)
    # initiate comparer
    comparer = BasicComparer()
    # initiate notifiers
    notifiers = [
        BasicNotifier(task_name=task_name),
        PushoverNotifier(
            task_name=task_name,
            pushover_token=pushover_token,
            pushover_user_key=pushover_user_key,
        ),
    ]
    # initiate notifiers
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


def monitor_with_sendgrid(
    task_name: str,
    target_url: str,
    loop_seconds: int,
    loop_max_rounds: int,
    sendgrid_api_key: str,
    from_email: str,
    to_email: str,
) -> None:
    """Function that runs basic monitoring tasks
    and shows results through console logs

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
        sendgrid_api_key (str): SendGrid API key
        from_email (str): Emails to be sent from
        to_email (str): Emails to be sent to
    """
    logger.info(f"Setting up the monitoring task: '{task_name}'")

    # initiate extractor
    extractor = BasicExtractor(target_url=target_url)
    # initiate comparer
    comparer = BasicComparer()
    # initiate notifiers
    notifiers = [
        BasicNotifier(task_name=task_name),
        SendGridNotifier(
            task_name=task_name,
            sendgrid_api_key=sendgrid_api_key,
            from_email=from_email,
            to_email=to_email,
        ),
    ]
    # initiate notifiers
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
