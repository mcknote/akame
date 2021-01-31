import logging
from typing import Type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLBase:
    def __init__(self, target_url: str):
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url


class ExtractorBase:
    def __init__(self, url_extractor):
        self.url_extractor = url_extractor

    def main(self):
        pass


class StaticExtractor(ExtractorBase):
    def __init__(self, url_extractor: Type[URLBase]):
        super().__init__(url_extractor)


class DynamicExtractor(ExtractorBase):
    def __init__(self, url_extractor: Type[URLBase]):
        super().__init__(url_extractor)
