import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComparerBase:
    def __init__(self, content_0: Any, content_1: Any):
        self.content_0 = content_0
        self.content_1 = content_1

    def compare_content(self):
        self.comparison_result = None

    def main(self) -> int:
        self.compare_content()

        if self.comparison_result is None:
            logger.info("No cached content")
            status_code = -1
        elif not self.comparison_result:
            logger.info("Nothing changed")
            status_code = 0
        else:
            logger.info("Changes detected")
            status_code = 1

        return status_code

