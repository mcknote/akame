import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLBase:
    def __init__(self, target_url: str):
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url


class ExtractorBase:
    def __init__(self, url_base: URLBase):
        self.url_base = url_base

    def main(self):
        pass


class StaticExtractor(ExtractorBase):
    def __init__(self, url_base: URLBase):
        super().__init__(url_base)


class DynamicExtractor(ExtractorBase):
    def __init__(self, url_base: URLBase):
        super().__init__(url_base)
