import logging
from typing import Any, List, TypeVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DeltaType = TypeVar("DeltaType", bound="DeltaBase")


class DeltaBase:
    """Class that compares two given objects

    Args:
        a (str): Object a to compare
        b (str): Object b to compare
    """

    parts_matched: List[Any]
    parts_changed_a: List[Any]
    parts_changed_b: List[Any]

    def __init__(self, a: str, b: str) -> None:
        self.a = a
        self.b = b

    def main(self):
        pass
