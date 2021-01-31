import importlib
import logging
from typing import Dict, Tuple
from .core import ContentExtractorType, URLExtractorType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# define types
ExtractorSet = Tuple[URLExtractorType, ContentExtractorType]


def get_url_and_content_extractors(exset_name: str) -> ExtractorSet:
    """Function that returns the URL and content extractors

    Args:
        exset_name (str): Name of the extraction set

    Returns:
        ExtractorSet: Tuple with URL and content extractors
    """
    logger.info(f"Loading extraction set: '{exset_name}'")
    package_name = "akame_monitor.extraction.sets"
    attrname_url = "URLExtractor"
    attrname_con = "ContentExtractor"

    module = importlib.import_module(name=f".{exset_name}", package=package_name)

    return (getattr(module, attrname_url), getattr(module, attrname_con))
