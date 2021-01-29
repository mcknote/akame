import json
import logging
import os
import re
import sys
from datetime import datetime
from time import sleep
from typing import Any, Dict, Tuple, Union

from joblib import dump, load
from numpy import Inf

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


def loop_task(*ignore, seconds: int, max_rounds: int):
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


def compare_mc_with_cache(monitored_content: MonitoredContent) -> int:
    # only store the latest cache
    path_cache = os.path.join(sys.path[0], "cache", "monitored_content")

    if not os.path.exists(path_cache):
        logger.info("Caching the MC for the first run")
        status_code = -1
    else:
        logger.info("Comparing the MCs")
        monitored_content_0 = load(path_cache)
        is_unchanged = monitored_content_0.content == monitored_content.content
        status_code = 0 if is_unchanged else 1

    dump(monitored_content, path_cache)
    return status_code
