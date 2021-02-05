import logging
from datetime import datetime
from typing import Any, Hashable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitoredContent:
    """Class that structures monitored content

    Args:
        content (Optional[Any], optional):
            Content fetched through extractor. Defaults to None.
        task_name (Optional[str], optional):
            Name of the task. Defaults to None.
        target_url (Optional[str], optional):
            Target URL. Defaults to None.
    """

    def __init__(
        self,
        content: Optional[Any] = None,
        task_name: Optional[str] = None,
        target_url: Optional[str] = None,
    ):
        self.timestamp = datetime.now()
        self.content = content
        self.task_name = task_name if task_name else ""
        self.target_url = target_url if target_url else ""

        str_empty = "" if content else "an empty "
        logger.info(
            f"Initiated {str_empty}{self.__class__.__name__} at {self.timestamp}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            "("
            f"timestamp={self.timestamp.__repr__()}, "
            f"content={self.content.__repr__()}, "
            f"task_name={self.task_name.__repr__()}, "
            f"target_url={self.target_url.__repr__()}"
            ")"
        )

    def __key(self) -> Hashable:
        return tuple(
            v for k, v in sorted(self.__dict__.items()) if k != "timestamp"
        )

    def __hash__(self):
        return hash(self.__key())

    def __eq__(x, y):
        return isinstance(y, x.__class__) and x.__key() == y.__key()
