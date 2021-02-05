import logging
from typing import Any, Type

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManagerBase:
    """Class that derives and manages all URLs for an extractor

    Args:
        target_url (str): Target URL to monitor
    """

    def __init__(self) -> None:
        pass

    def parse_target_url(self):
        pass

    def load_url_referrer(self):

        self.url_referrer = self.target_url

    def load_url_to_request(self):
        self.url_to_request = self.target_url

    def main(self, target_url: str) -> None:
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url

        self.parse_target_url()
        self.load_url_referrer()
        self.load_url_to_request()


class ExtractorBase:
    """Class that defines the base content extractor

    Args:
        url_manager (Type[URLManagerBase]): URL manager
    """

    def __init__(self, url_manager: Type[URLManagerBase]) -> None:
        self.urls = url_manager()

    def update_target_url(self, target_url: str) -> None:
        self.urls.main(target_url=target_url)

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

    def get_parsed_content(self, content: Any) -> Any:
        return content

    # TODO: return MonitoredContent here
    def main(self, target_url: str) -> Any:
        """Function that extracts the content from the target URL

        Args:
            target_url (str): Target URL

        Returns:
            Any: Fetched content
        """
        self.update_target_url(target_url=target_url)
        self.load_request_headers()
        response = self.get_response()
        content = response.text
        parsed_content = self.get_parsed_content(content)

        return parsed_content


class StaticExtractor(ExtractorBase):
    """Class that defines the content extractor for static content

    Args:
        url_extractor (Type[URLManagerBase]): URL extractor
    """

    def __init__(self, url_manager: Type[URLManagerBase]) -> None:
        super().__init__(url_manager)


class DynamicExtractor(ExtractorBase):
    """Class that defines the content extractor for dynamic content

    Args:
        url_extractor (Type[URLManagerBase]): URL extractor
    """

    def __init__(self, url_manager: Type[URLManagerBase]) -> None:
        super().__init__(url_manager)
