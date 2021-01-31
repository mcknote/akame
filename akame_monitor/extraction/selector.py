import logging
from typing import Any, Callable, Dict, Tuple

from .core import ExtractorBase, URLBase

ExtractorSet = Tuple[Any, Any]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_url_extractor_basic() -> ExtractorSet:
    from .basic import ContentExtractor, URLExtractor

    return (URLExtractor, ContentExtractor)


def get_url_extractor_pchome_24h() -> ExtractorSet:
    from .pchome_24h_cart import ContentExtractor, URLExtractor

    return (URLExtractor, ContentExtractor)


def get_url_extractor_books_com_tw() -> ExtractorSet:
    from .books_com_tw_cart import ContentExtractor, URLExtractor

    return (URLExtractor, ContentExtractor)


extractor_catalog: Dict[str, Callable] = {
    "BASIC": get_url_extractor_basic,
    "PCHOME_24H": get_url_extractor_pchome_24h,
    "BOOKS_COM_TW": get_url_extractor_books_com_tw,
}


def get_url_extractor(exset_id: str) -> ExtractorSet:
    logger.info(f"Loading Extractor Set under ID: '{exset_id}'")
    return extractor_catalog[exset_id]()
