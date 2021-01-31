import importlib
import logging
from typing import Any, Dict, Tuple, Type
from .core import ContentExtractorType, URLExtractorType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
ExtractorSet = Tuple[URLExtractorType, ContentExtractorType]

extractor_catalog: Dict[str, str] = {
    "BASIC": "basic",
    "PCHOME_24H_CART": "pchome_24h_cart",
    "BOOKS_COM_TW_CART": "books_com_tw_cart",
}


def get_url_and_content_extractors(exset_id: str) -> ExtractorSet:
    """Function that returns the URL and content extractors

    Args:
        exset_id (str): Extractor ID as defined in `extractor_catalog`

    Returns:
        ExtractorSet: Tuple with URL and content extractors
    """
    logger.info(f"Loading Extractor Set under ID: '{exset_id}'")
    module_name = extractor_catalog[exset_id]
    package_name = "akame_monitor.extraction"
    attrname_url = "URLExtractor"
    attrname_con = "ContentExtractor"

    module = importlib.import_module(name=f".{module_name}", package=package_name)

    return (getattr(module, attrname_url), getattr(module, attrname_con))
