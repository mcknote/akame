import logging
import os
import pickle
import sys
from datetime import datetime
from shutil import rmtree
from time import sleep
from typing import Any, Callable, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def loop_task(*ignore, seconds: int, max_rounds: int) -> Callable:
    """Function that decorates function with looping

    Args:
        seconds (int): interval in seconds
        max_rounds (int): maximum rounds to run

    Returns:
        Callable: decorated function
    """
    logger.info(f"Looping the task every {seconds} seconds until {max_rounds} rounds")

    def decorator(function) -> Callable:
        def wrapper(*args, **kwargs):
            round = 0
            while round < max_rounds:
                round += 1
                logger.info(f"Going round {round}")
                function(*args, **kwargs)
                sleep(seconds)

        return wrapper

    return decorator


class MonitoredContent:
    """Class that structures monitored content

    Args:
        content (Union[Any, None], optional):
            Any monitored content. Defaults to None.
    """

    def __init__(self, content: Union[Any, None] = None):
        self.content = content
        self.timestamp = datetime.now()

    def __repr__(self) -> str:
        return (
            f"MonitoredContent(timestamp={self.timestamp.__repr__()}, "
            "content={self.content})"
        )


path_cache_folder = os.path.join(sys.path[0], "akame_monitor", ".akame_cache")
path_cache = os.path.join(path_cache_folder, "monitored_content")


def reset_cached_folder(path_cache_folder: str = path_cache_folder) -> None:
    if os.path.exists(path_cache_folder):
        rmtree(path_cache_folder)
    os.mkdir(path_cache_folder)


def get_cached_mc(path_cache: str = path_cache) -> Union[MonitoredContent, None]:
    if not os.path.exists(path_cache):
        logger.info("Caching the MC for the first run")
        mc_0: Union[MonitoredContent, None] = None
    else:
        logger.info("Comparing the MCs")
        with open(path_cache, "rb") as f:
            mc_0 = pickle.load(f)

    return mc_0


def cache_mc(mc: MonitoredContent, path_cache: str = path_cache) -> None:
    with open(path_cache, "wb") as f:
        pickle.dump(mc, f)
