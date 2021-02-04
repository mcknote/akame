import logging
from typing import List

from akame.comparison.delta.core import DeltaType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FormatterBase:
    """Class that defines base formatter

    Args:
        delta (DeltaType): Delta object
    """

    def __init__(self, delta: DeltaType) -> None:
        self.parts_matched = delta.parts_matched
        self.parts_changed_a = delta.parts_changed_a
        self.parts_changed_b = delta.parts_changed_b
