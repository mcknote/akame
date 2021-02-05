import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_random_task_name(target_url: str) -> str:
    domain = urlparse(target_url).netloc
    return f"Monitor @ {domain}"


def check_loop_seconds(seconds: float) -> None:
    """Function that checks loop seconds

    Args:
        seconds (float): Loop interval in seconds
    """
    min_seconds = 60
    if seconds < min_seconds:
        logger.warning(
            "Consider increasing the interval "
            f"to {min_seconds} seconds: "
            f"interval < {min_seconds} seconds might "
            "not cover the execution time "
            "and abuse the target website"
        )


def loop_task(*ignore, seconds: float, max_rounds: int) -> Callable:
    """Function that decorates the function with looping

    Args:
        seconds (float): Interval in seconds
        max_rounds (int): Maximum rounds to run
        task_name (Optional[str]): Name of the task.
            Defaults to None

    Returns:
        Callable: Decorated function to be executed
    """
    check_loop_seconds(seconds)

    logger.info(
        f"Looping the task every {seconds} seconds "
        f"until {max_rounds} rounds"
    )

    def decorator(function) -> Callable:
        def wrapper(*args, **kwargs):
            round = 0
            while round < max_rounds:
                start_time = time.time()
                round += 1
                logger.info(f"Going round {round}")
                function(*args, **kwargs)
                used_interval = (time.time() - start_time) % seconds
                time.sleep(seconds - used_interval)

        return wrapper

    return decorator


# slightly modified from
# https://stackoverflow.com/questions/7207309/how-to-run-functions-in-parallel
def run_tasks_in_parallel(tasks: List[Callable]):
    """Function that runs multiple monitoring tasks in parallel

    Args:
        tasks (List[Callable]): List of monitoring tasks
    """
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()
