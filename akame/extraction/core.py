import logging
from typing import Any, Type, TypeVar

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
URLManagerType = TypeVar("URLManagerType", bound="URLManagerBase")
ExtractorType = TypeVar("ExtractorType", bound="ExtractorBase")


class URLManagerBase:
    """Class that derives and manages all URLs for an extractor

    Args:
        target_url (str): Target URL to monitor
    """

    def __init__(self, target_url: str) -> None:
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url
        self.url_to_request = target_url
        self.url_referrer = target_url

    def parse_target_url(self):
        pass

    def load_url_referrer(self):
        pass

    def load_url_to_request(self):
        pass


class ExtractorBase:
    """Class that defines the base content extractor

    Args:
        target_url (str): Target URL to monitor
        url_manager (Type[URLManagerBase]): URL manager
    """

    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase]
    ) -> None:
        self.urls = url_manager(target_url)

    def load_request_headers(self):
        self.request_headers = {
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "referer": self.urls.url_referrer,
        }

    def get_response(self) -> requests.Response:
        return requests.get(
            self.urls.url_to_request, headers=self.request_headers
        )

    # TODO: return MonitoredContent here
    def main(self) -> Any:
        """Function that extracts the target content"""
        response = self.load_request_headers()
        content = response.text
        return content


class StaticExtractor(ExtractorBase):
    """Class that defines the content extractor for static content

    Args:
        url_extractor (URLExtractorType): URL extractor
    """

    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase]
    ) -> None:
        super().__init__(target_url, url_manager)


class DynamicExtractor(ExtractorBase):
    """Class that defines the content extractor for dynamic content

    Args:
        url_extractor (URLExtractorType): URL extractor
    """

    def __init__(
        self, target_url: str, url_manager: Type[URLManagerBase]
    ) -> None:
        super().__init__(target_url, url_manager)
