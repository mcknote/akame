import logging
from datetime import datetime
from typing import Any, Hashable, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitoredContent:
    """Class that structures monitored content

    Args:
        content (Union[Any, None], optional):
            Any monitored content. Defaults to None.
    """

    def __init__(self, content: Optional[Any] = None):
        self.content = content
        self.timestamp = datetime.now()

        str_empty = "" if content else "an empty "
        logger.info(
            f"Initiated {str_empty}{self.__class__.__name__} at {self.timestamp}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(timestamp={self.timestamp.__repr__()}, "
            f"content={self.content.__repr__()})"
        )

    # TODO: improve key design
    def __key(self) -> Hashable:
        """Function that defines the key of a monitored content

        Returns:
            Hashable: Hashable object
        """
        if isinstance(self.content, Hashable):
            content_key = self.content
        else:
            content_type = type(self.content)
            try:
                logger.warning(
                    f"Content type {content_type} is not hashable. "
                    "Trying to convert it to tuple"
                )
                content_key = tuple(self.content)
            except TypeError:
                logger.warning(
                    f"Content type {content_type} cannot be converted "
                    "to tuple. Trying to use the content's __repr__. "
                    "Consider changing the monitored content as "
                    "this may result in falsy comparison"
                )
                content_key = repr(self.content)

        return content_key

    def __hash__(self):
        return hash(self.__key())

    def __eq__(x, y):
        return isinstance(y, x.__class__) and x.__key() == y.__key()