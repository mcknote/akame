import json
import logging
import os
import pickle
import sys
from datetime import datetime
from time import sleep
from typing import Any, Callable, Dict, Tuple, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_config(filename: str = "config.json") -> Dict[str, Any]:
    logger.info("Loading monitor configuration")
    path_config = os.path.join(sys.path[0], filename)
    with open(path_config, "r") as f:
        config = json.load(f)

    return config


def get_pushsafer_key() -> str:
    logger.info("Loading Pushsafer key")
    return os.environ["PUSHSAFER_KEY"]


def get_pushover_creds() -> Tuple[str, str]:
    logger.info("Loading PushOver credentials")
    return (os.environ["PUSHOVER_TOKEN"], os.environ["PUSHOVER_USERKEY"])


def loop_task(*ignore, seconds: int, max_rounds: int) -> Callable:
    """Function that decorates function with looping

    Args:
        seconds (int): interval in seconds
        max_rounds (int): maximum rounds to run

    Returns:
        Callable: decorated function
    """
    logger.info(f"Looping the task every {seconds} seconds until {max_rounds} rounds")

    def decorator(function):
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
        return f"MonitoredContent(timestamp={self.timestamp.__repr__()}, \
            content={self.content})"


def get_cached_mc() -> Union[MonitoredContent, None]:
    # only store the latest cache
    path_cache = os.path.join(sys.path[0], "cache", "monitored_content")

    if not os.path.exists(path_cache):
        logger.info("Caching the MC for the first run")
        mc_0: Union[MonitoredContent, None] = None
    else:
        logger.info("Comparing the MCs")
        with open(path_cache, "rb") as f:
            mc_0 = pickle.load(f)

    return mc_0


def cache_mc(mc: MonitoredContent) -> None:
    # only store the latest cache
    path_cache = os.path.join(sys.path[0], "cache", "monitored_content")
    with open(path_cache, "wb") as f:
        pickle.dump(mc, f)
