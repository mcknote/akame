import logging
from typing import Any, Dict

from .comparison.basic import BasicComparer
from .extraction.core import ExtractorBase
from .extraction.selector import get_url_and_content_extractors
from .notification.core import NotifierBase
from .notification.pushover import PONotifier
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
    def __init__(
        self,
        content_extractor: ExtractorBase,
        notifier: NotifierBase,
        loop_seconds: int,
        loop_max_rounds: int,
    ):
        self.content_extractor = content_extractor
        self.notifier = notifier
        self.loop_seconds = loop_seconds
        self.loop_max_rounds = loop_max_rounds
        reset_cached_folder()

    def get_monitored_content(self) -> MonitoredContent:
        response = self.content_extractor.main()
        return MonitoredContent(response.text)

    def compare_mirrored_content(self, mc_1: MonitoredContent) -> int:
        mc_0 = get_cached_mc()
        cache_mc(mc_1)
        content_0 = mc_0.content if mc_0 else None
        content_1 = mc_1.content
        comparer = BasicComparer(content_0=content_0, content_1=content_1)
        return comparer.main()

    def main(self) -> None:
        def task():
            monitored_content = self.get_monitored_content()
            status_code = self.compare_mirrored_content(monitored_content)
            self.notifier.main(status_code)

        looper = loop_task(seconds=self.loop_seconds, max_rounds=self.loop_max_rounds)(
            task
        )
        looper()


def run_task(
    task_name: str,
    target_url: str,
    exset_id: str,
    loop_seconds: int,
    loop_max_rounds: int,
    notify_creds: Dict[str, Any],
) -> None:
    """Function that runs the monitoring task

    Args:
        task_name (str): Name of the task
        target_url (str): Target URL to monitor
        exset_id (str): ID of extractor set defined in extraction.selector
        loop_seconds (int): Interval in seconds between all rounds
        loop_max_rounds (int): Maximum number of rounds to monitor
        notify_creds (Dict[str, Any]): Credential for notification programs
    """

    url_extractor, content_extractor = get_url_and_content_extractors(exset_id)

    # initiate url_extractor, extractor, and notifier
    url_extractor = url_extractor(target_url=target_url)
    content_extractor = content_extractor(url_extractor=url_extractor)
    notifier = PONotifier(task_name, notify_creds=notify_creds)

    monitor = Monitor(
        content_extractor=content_extractor,
        notifier=notifier,
        loop_seconds=loop_seconds,
        loop_max_rounds=loop_max_rounds,
    )
    monitor.main()
