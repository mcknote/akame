import logging
from typing import Any, Dict, List

from .comparison.pushover import PushoverComparer
from .comparison.core import ComparerType
from .extraction.core import ContentExtractorType
from .extraction.selector import get_extraction_set
from .notification.basic import BasicNotifier
from .notification.core import NotifierType
from .notification.pushover import PushoverNotifier
from .utility.core import (
    MonitoredContent,
    cache_mc,
    get_cached_mc,
    loop_task,
    reset_cached_folder,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Monitor:
    """Class that organizes the monitoring task

    Args:
        content_extractor (ContentExtractorType): Content extractor
        comparer (ComparerType): Comparer
        notifiers (List[NotifierType]): List of notifiers
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
    """

    def __init__(
        self,
        content_extractor: ContentExtractorType,
        comparer: ComparerType,
        notifiers: List[NotifierType],
        loop_seconds: int,
        loop_max_rounds: int,
    ) -> None:

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
    logger.info(f"Initializing the monitoring task: '{task_name}'")

    url_extractor, content_extractor = get_extraction_set(exset_name)

    # initiate url_extractor, content_extractor, notifier
    url_extractor = url_extractor(target_url=target_url)
    content_extractor = content_extractor(url_extractor=url_extractor)
    comparer = PushoverComparer(target_url=target_url)
    notifiers = [
        BasicNotifier(task_name),
        PushoverNotifier(task_name, notify_creds=notify_creds),
    ]

    monitor = Monitor(
        content_extractor=content_extractor,
        comparer=comparer,
        notifiers=notifiers,
        loop_seconds=loop_seconds,
        loop_max_rounds=loop_max_rounds,
    )
    monitor.main()
