import logging
from typing import Optional, Sequence

from akame.comparison import BasicComparer
from akame.comparison.core import ComparerBase
from akame.extraction import BasicExtractor
from akame.extraction.core import ExtractorBase
from akame.notification import BasicNotifier
from akame.notification.core import NotifierBase
from akame.utility.caching import TaskCacheManager, reset_cached_folder
from akame.utility.core import MonitoredContent
from akame.utility.tasking import get_random_task_name, loop_task

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Function that initaties akame dependencies"""
    logger.info("Initiating akame dependencies")
    reset_cached_folder(reset_whole_folder=True)


class Monitor:
    """Class that organizes the monitoring task

    Args:
        target_url (str):
            URL to monitor.
        task_name (Optional[str]):
            Name of the task.
            Defaults to None; task name will be derived from URL.
        loop_seconds (float, optional):
            Interval in seconds between all rounds.
            Defaults to 300.
        loop_max_rounds (int, optional):
            Maximum number of rounds to monitor.
            Defaults to 12.
        extractor (Optional[ExtractorBase], optional):
            Content extractor that extracts the monitored content.
            Defaults to None; BasicExtractor will be initiated.
        comparer (Optional[ComparerBase], optional):
            Comparer that compares the monitored content.
            Defaults to None; BasicComparer will be initiated.
        notifiers (Optional[Sequence[NotifierBase]], optional):
            List of notifiers that push notifications on comparison results.
            Defaults to None; BasicNotifier will be initiated.
        cache_manager (Optional[TaskCacheManager], optional):
            Cache manager that archives and loads all monitored content.
            Defaults to None; TaskCacheManager will be initiated.
    """

    def __init__(
        self,
        target_url: str,
        task_name: Optional[str] = None,
        loop_seconds: float = 300,
        loop_max_rounds: int = 12,
        extractor: Optional[ExtractorBase] = None,
        comparer: Optional[ComparerBase] = None,
        notifiers: Optional[Sequence[NotifierBase]] = None,
        cache_manager: Optional[TaskCacheManager] = None,
    ) -> None:

        self.target_url = target_url
        self.task_name = (
            str(task_name) if task_name else get_random_task_name(target_url)
        )
        logger.info(f"Starting Akame Monitor: '{self.task_name}'")
        self.loop_seconds = loop_seconds
        self.loop_max_rounds = loop_max_rounds

        self.extractor = extractor if extractor else BasicExtractor()
        self.comparer = comparer if comparer else BasicComparer()
        self.notifiers = notifiers if notifiers else [BasicNotifier()]

        self.cache_manager = (
            cache_manager
            if cache_manager
            else TaskCacheManager(task_name=self.task_name)
        )

    def update_extractor(self, extractor: ExtractorBase) -> None:
        self.extractor = extractor

    def update_comparer(self, comparer: ComparerBase) -> None:
        self.comparer = comparer

    def add_notifiers(self, notifiers: Sequence[NotifierBase]) -> None:
        self.notifiers = list(self.notifiers) + list(notifiers)

    def update_notifiers(self, notifiers: Sequence[NotifierBase]) -> None:
        self.notifiers = notifiers

    def _extract_monitored_content(self) -> MonitoredContent:
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

    def _compare_monitored_content(self, mc_1: MonitoredContent) -> None:
        """Function that compares monitored content

        Args:
            mc_1 (MonitoredContent): Monitored content to compare
        """
        mc_0 = self.cache_manager.get_newest_cache()
        self.cache_manager.cache_task_mc(mc_1)
        self.comparer.main(mc_0=mc_0, mc_1=mc_1)

    def _notify_comparison_results(self) -> None:
        """Function that notifies of comparison results. The notification logic
        is defined in each notifier
        """
        for notifier in self.notifiers:
            notifier.main(self.comparer)

    def main(self) -> None:
        """Function that performs the monitoring tasks on a loop"""

        def task():
            monitored_content = self._extract_monitored_content()
            self._compare_monitored_content(monitored_content)
            self._notify_comparison_results()

        looper = loop_task(
            seconds=self.loop_seconds,
            max_rounds=self.loop_max_rounds,
        )(task)
        looper()
