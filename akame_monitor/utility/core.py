from datetime import datetime
from typing import Any, Union


class MonitoredContent:
    """Class that structures monitored content

    Args:
        content (Union[Any, None], optional):
            Any monitored content. Defaults to None.
    """

    def __init__(self, content: Union[Any, None] = None):
        self.content = content
        self.timestamp = datetime.now()

    def __repr__(self) -> str:
        return (
            f"MonitoredContent(timestamp={self.timestamp.__repr__()}, "
            "content={self.content})"
        )
