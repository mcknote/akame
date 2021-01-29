import logging
from typing import Any, Dict

from comparison.basic import BasicComparer
from extraction.core import ExtractorBase, URLBase
from extraction.selector import get_url_extractor
from notification.core import NotifierBase
from notification.pushover import PONotifier
from utility.core import (
    MonitoredContent,
    get_cached_mc,
    get_config,
    get_pushover_creds,
    loop_task,
    cache_mc,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Monitor:
    def __init__(
        self, extractor: ExtractorBase, notifier: NotifierBase, config: Dict[str, Any],
    ):
        self.config = config
        self.extractor = extractor
        self.notifier = notifier

    def get_monitored_content(self) -> MonitoredContent:
        response = self.extractor.main()
        return MonitoredContent(response.text)

    def compare_mirrored_content(self, mc_1: MonitoredContent) -> int:
        mc_0 = get_cached_mc()
        cache_mc(mc_1)
        content_0 = mc_0.content if mc_0 else None
        content_1 = mc_1.content
        comparer = BasicComparer(content_0=content_0, content_1=content_1)
        return comparer.main()

    def main(self):
        def task():
            monitored_content = self.get_monitored_content()
            status_code = self.compare_mirrored_content(monitored_content)
            self.notifier.main(status_code)

        looper = loop_task(
            seconds=self.config["loop_seconds"],
            max_rounds=self.config["loop_max_rounds"],
        )(task)
        looper()


def main():

    config = get_config()
    token, user_key = get_pushover_creds()
    url_base, extractor = get_url_extractor(config["exset_id"])

    # initiate url_base, extractor, and notifier
    url_base: URLBase = url_base(target_url=config["target_url"])
    url_base.main()
    extractor = extractor(url_base=url_base)
    notifier = PONotifier(config["task_name"], token=token, user_key=user_key)

    monitor = Monitor(extractor=extractor, notifier=notifier, config=config,)
    monitor.main()


if __name__ == "__main__":
    main()
