import logging
from typing import Type

from akame.extraction.core import StaticExtractor, URLManagerBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManager(URLManagerBase):
    def __init__(self) -> None:
        super().__init__()


class BasicExtractor(StaticExtractor):
    def __init__(self, url_manager: Type[URLManagerBase] = URLManager) -> None:
        super().__init__(url_manager)
