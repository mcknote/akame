import logging
from datetime import datetime
from typing import Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitoredContent:
    """Class that structures monitored content

    Args:
        content (Union[Any, None], optional):
            Any monitored content. Defaults to None.
    """

    def __init__(self, content: Union[Any, None] = None):
        self.content = content
        self.timestamp = datetime.now()
        logger.info(f"Initiated {self.__class__.__name__} at {self.timestamp}")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(timestamp={self.timestamp.__repr__()}, "
            f"content={self.content})"
        )
