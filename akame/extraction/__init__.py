import importlib
import logging

from .core import ExtractionSet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def select_sets(exset_name: str) -> ExtractionSet:
    """Function that returns the URL and content extractors

    Args:
        exset_name (str): Name of the extraction set

    Returns:
        ExtractionSet: Tuple with URL and content extractors
    """
    logger.info(f"Loading extraction set: '{exset_name}'")
    package_name = "akame.extraction.sets"
    attrname_url = "URLExtractor"
    attrname_con = "ContentExtractor"

    module = importlib.import_module(
        name=f".{exset_name}", package=package_name
    )

    return (getattr(module, attrname_url), getattr(module, attrname_con))
