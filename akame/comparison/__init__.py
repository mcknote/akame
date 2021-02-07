import logging
from typing import Optional

from akame.comparison.core import ComparerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicComparer(ComparerBase):
    """Class that defines the basic comparer"""

    def __init__(self, matches_expression: Optional[str] = None) -> None:
        super().__init__()
        self.matches_expression = matches_expression

    def load_comparison_status(self) -> None:
        if self.mc_0.content is None:
            self.comparison_status = None
        else:
            self.comparison_status = self.mc_0.content != self.mc_1.content

    def compose_comparison_results(self) -> None:
        if self.comparison_status is None:
            self.status_code = -1
            self.message = "INITIATED"
        elif not self.comparison_status:
            self.status_code = 0
            self.message = "UNCHANGED"
        else:
            self.status_code = 1
            self.message = "CHANGES DETECTED"
