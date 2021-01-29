import logging
from typing import Any

from .core import ComparerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicComparer(ComparerBase):
    def __init__(self, content_0: Any, content_1: Any) -> None:
        super().__init__(content_0, content_1)

    def compare_content(self):
        if self.content_0 is None:
            self.comparison_result = None
        else:
            self.comparison_result = self.content_0 != self.content_1
