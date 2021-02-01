import logging
from typing import Any, TypeVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
URLExtractorType = TypeVar("URLExtractorType", bound="URLBase")
ContentExtractorType = TypeVar("ContentExtractorType", bound="ExtractorBase")


class URLBase:
    """Class that defines the base URL extractor

    Args:
        target_url (str): Target URL to be monitored
    """

    # for mypy checks
    url_referrer: str
    url_cart_api: str
    url_api_endpoint: str

    def __init__(self, target_url: str) -> None:
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url


class ExtractorBase:
    """Class that defines the base content extractor

    Args:
        url_extractor (URLExtractorType): URL extractor
    """

    def __init__(self, url_extractor: URLExtractorType) -> None:
        self.url_extractor = url_extractor

    def main(self) -> Any:
        """Function that extracts the target content"""
        pass


class StaticExtractor(ExtractorBase):
    """Class that defines the content extractor for static content

    Args:
        url_extractor (URLExtractorType): URL extractor
    """

    def __init__(self, url_extractor) -> None:
        super().__init__(url_extractor)


class DynamicExtractor(ExtractorBase):
    """Class that defines the content extractor for dynamic content

    Args:
        url_extractor (URLExtractorType): URL extractor
    """

    def __init__(self, url_extractor) -> None:
        super().__init__(url_extractor)
