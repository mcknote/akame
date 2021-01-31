import logging
import os
import pickle
import sys
from shutil import rmtree
from typing import Union

from .core import MonitoredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

path_cache_folder = os.path.join(sys.path[0], "akame_monitor", ".akame_cache")
path_cache = os.path.join(path_cache_folder, "monitored_content")


def reset_cached_folder(path_cache_folder: str = path_cache_folder) -> None:
    """Function that resets the cached folder

    Args:
        path_cache_folder (str, optional): Path to the cache folder.
            Defaults to path_cache_folder.
    """
    if os.path.exists(path_cache_folder):
        rmtree(path_cache_folder)
    os.mkdir(path_cache_folder)


def get_cached_mc(
    path_cache: str = path_cache,
) -> Union[MonitoredContent, None]:
    """Function that returns the cached Monitored Content

    Args:
        path_cache (str, optional): Path to the cache file.
            Defaults to path_cache.

    Returns:
        Union[MonitoredContent, None]: Fetched MonitoredContent or nothing
    """
    if not os.path.exists(path_cache):
        logger.info("Caching Monitored Content for the first run")
        mc_0: Union[MonitoredContent, None] = None
    else:
        logger.info("Comparing the old and new Monitored Content")
        with open(path_cache, "rb") as f:
            mc_0 = pickle.load(f)

    return mc_0


def cache_mc(mc: MonitoredContent, path_cache: str = path_cache) -> None:
    """Function that caches the given MonitoredContent

    Args:
        mc (MonitoredContent): MonitoredContent to cache
        path_cache (str, optional): Path to the cache file.
            Defaults to path_cache.
    """
    with open(path_cache, "wb") as f:
        pickle.dump(mc, f)
