import logging
from typing import Any, Type

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLManagerBase:
    """Class that derives and manages all URLs for an extractor"""

    def __init__(self) -> None:
        pass

    def parse_target_url(self):
        """Function that parses target URL"""
        pass

    def load_url_referrer(self):
        """Function that parses and loads referrer URL"""
        self.url_referrer = self.target_url

    def load_url_to_request(self):
        """Function that parses and loads actual URL to request"""
        self.url_to_request = self.target_url

    def main(self, target_url: str) -> None:
        """Function that parses and loads all core URLs

        Args:
            target_url (str): Target URL to monitor
        """
        logger.info(f"Loading target url: '{target_url}'")
        self.target_url = target_url

        self.parse_target_url()
        self.load_url_referrer()
        self.load_url_to_request()


class ExtractorBase:
    """Class that defines the base content extractor

    Args:
        url_manager (Type[URLManagerBase], optional):
            URL Manager to parse the URL. Defaults to URLManagerBase.
    """

    def __init__(
        self, url_manager: Type[URLManagerBase] = URLManagerBase
    ) -> None:
        self.urls = url_manager()

    def update_target_url(self, target_url: str) -> None:
        """Function that parses and loads all core URLs in URL Manager

        Args:
            target_url (str): Target URL to monitor
        """
        self.urls.main(target_url=target_url)

    def get_response(self) -> Any:
        """Function that returns the results from the data request"""
        return None

    def get_parsed_content(self, response: Any) -> Any:
        return response

    def main(self, target_url: str) -> Any:
        """Function that extracts the content from the target URL

        Args:
            target_url (str): Target URL

        Returns:
            Any: Fetched content
        """
        self.update_target_url(target_url=target_url)
        response = self.get_response()
        content = self.get_parsed_content(response)

        return content


class StaticExtractor(ExtractorBase):
    """Class that defines the content extractor for static content

    Args:
        url_manager (Type[URLManagerBase], optional):
            URL Manager to parse the URL. Defaults to URLManagerBase.
    """

    def __init__(
        self, url_manager: Type[URLManagerBase] = URLManagerBase
    ) -> None:
        super().__init__(url_manager)

    def load_request(self):
        self.load_request_headers()
        self.load_request_data()

    def load_request_headers(self) -> None:
        """Function that loads headers to use in the HTTPS request"""
        self.request_headers = {
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/88.0.4324.96 Safari/537.36"
            ),
            "referer": self.urls.url_referrer,
        }

    def load_request_data(self) -> None:
        """Function that loads data to use in the HTTPS request"""
        pass

    def get_response(self) -> requests.Response:
        return requests.get(
            self.urls.url_to_request, headers=self.request_headers
        )

    def get_parsed_content(self, response: Any) -> Any:
        return response.text

    def main(self, target_url: str) -> Any:
        """Function that extracts the content from the target URL

        Args:
            target_url (str): Target URL

        Returns:
            Any: Fetched content
        """
        self.update_target_url(target_url=target_url)
        self.load_request()
        response = self.get_response()
        content = self.get_parsed_content(response)

        return content


class DynamicExtractor(ExtractorBase):
    """Class that defines the content extractor for dynamic content

    Args:
        url_manager (Type[URLManagerBase], optional):
            URL Manager to parse the URL. Defaults to URLManagerBase.
    """

    def __init__(
        self, url_manager: Type[URLManagerBase] = URLManagerBase
    ) -> None:
        super().__init__(url_manager)
