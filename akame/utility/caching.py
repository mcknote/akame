import logging
import pickle
import sys
from hashlib import sha1
from pathlib import Path
from shutil import rmtree
from typing import Union

from .core import MonitoredContent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

path_cache_folder = Path(sys.path[0]) / "akame" / ".akame_cache"


def get_task_hash(task_name: str) -> str:
    """Function that gets the hashed task name

    Args:
        task_name (str): Name of the task

    Returns:
        str: Hashed task name
    """
    # using SHA-1 for noncryptographic purpose
    return sha1(task_name.encode("utf-8")).hexdigest()


def check_is_folder_emtpy(path_to_folder: Path) -> bool:
    """Function that checks whether the folder is empty

    Args:
        path_to_folder (Path): Folder to check

    Returns:
        bool: Whether the folder is totally empty
    """
    return not next(path_to_folder.iterdir(), None)


def reset_folder(path_to_folder: Path) -> None:
    """Function that removes and recreates the target folder

    Args:
        path_to_folder (Path): Folder to reset
    """
    if path_to_folder.exists():
        if check_is_folder_emtpy(path_to_folder):
            logger.info(
                f"Skipping '{path_to_folder}': the folder is already empty"
            )
            return
        else:
            logger.info(f"Removing '{path_to_folder}' and all its files")
            rmtree(path_to_folder)
    else:
        logger.warning(f"Folder '{path_to_folder}' does not exist")

    logger.info(f"Creating '{path_to_folder}'")
    path_to_folder.mkdir(parents=True, exist_ok=True)


def reset_cached_folder(
    task_hash: Union[str, None] = None,
    reset_whole_folder: bool = False,
    path_cache_folder: Path = path_cache_folder,
) -> None:
    """Function that resets the cached folder

    Args:
        task_hash (Union[str, None], optional):
            Hashed task name. Defaults to None.
        reset_whole_folder (bool, optional): USE WITH CAUTION.
            Whether to reset the whole cache folder.
            If `task_hash` is provided, this arg will be ignored
        path_cache_folder (str, optional): Path to the cache folder.
            Defaults to path_cache_folder.
    """

    if not isinstance(reset_whole_folder, bool):
        logger.warning(
            "Skipping the operation: "
            "for security reason "
            "`reset_whole_folder` only accepts bool"
        )
        return

    if not task_hash and not reset_whole_folder:
        logger.warning(
            "Skipping the operation: "
            "no `task_hash` was provided "
            "and `reset_whole_folder` set to False"
        )
        return

    elif task_hash:
        logger.info("Resetting task-specific caches")
        if reset_whole_folder:
            logger.warning(
                "Ignoring `reset_whole_folder`: `task_hash` was provided"
            )
        path_cache_folder_th = path_cache_folder / task_hash
        reset_folder(path_cache_folder_th)

    elif not task_hash and reset_whole_folder:
        reset_folder(path_cache_folder)


def get_cached_mc(path_cache) -> Union[MonitoredContent, None]:
    """Function that returns the cached Monitored Content

    Args:
        path_cache (Path, optional): Path to the cache file.

    Returns:
        Union[MonitoredContent, None]: Fetched MonitoredContent or nothing
    """
    if not path_cache.exists():
        logger.info("Caching Monitored Content for the first run")
        mc_0: Union[MonitoredContent, None] = None
    else:
        logger.info("Comparing the old and new Monitored Content")
        with open(path_cache, "rb") as f:
            mc_0 = pickle.load(f)

    return mc_0


def cache_mc(mc: MonitoredContent, path_cache: Path) -> None:
    """Function that caches the given MonitoredContent

    Args:
        mc (MonitoredContent): MonitoredContent to cache
        path_cache (Path, optional): Path to the cache file.
    """
    with open(path_cache, "wb") as f:
        pickle.dump(mc, f)


class TaskCacheManager:
    """Class that handles caching for a monitoring task

    Args:
        task_hash (str): Hashed task name
        n_versions (int, optional):
            Number of cache versions to retain. Defaults to 3.
        path_cache_folder (Path, optional):
            Path to the cache folder. Defaults to path_cache_folder.
    """

    def __init__(
        self,
        task_hash: str,
        n_versions: int = 3,
        path_cache_folder: Path = path_cache_folder,
    ) -> None:
        self.task_hash = task_hash
        self.n_versions = int(n_versions)
        self.check_n_versions()
        self.path_cache_folder = path_cache_folder

        self.setup_cache_folder()

    def check_n_versions(self):
        """Function that checks whether `n_version` is valid"""
        if self.n_versions < 1:
            logger.warning("Coercing `n_version` to 1: value < 1 was provided")
            self.n_versions = 1

    def setup_cache_folder(self) -> None:
        """Function that sets up the task cache folder and configurations"""
        self.path_cache_folder_th = path_cache_folder / self.task_hash
        self.cache_extention = "akamecache"
        self.cache_oldest_version: int = 0
        self.cache_newest_version: int = (
            self.cache_oldest_version + self.n_versions - 1
        )

        reset_folder(self.path_cache_folder_th)

    def get_path_cache(self, version: int) -> Path:
        filename = str(version) + "." + self.cache_extention
        return self.path_cache_folder_th / filename

    def replace_older_caches(self) -> None:
        """Function that replaces older caches with their new versions"""
        paths_cache = self.path_cache_folder_th.iterdir()
        existing_versions = sorted([int(path.stem) for path in paths_cache])
        version_migration = [
            (version, version - 1) for version in existing_versions
        ]

        for v_old, v_new in version_migration:
            if v_new < self.cache_oldest_version:
                pass
            else:
                path_old = self.get_path_cache(v_old)
                path_new = self.get_path_cache(v_new)
                path_old.rename(path_new)

    def cache_task_mc(self, mc: MonitoredContent) -> None:
        """Function that rotates and caches monitored content

        Args:
            mc (MonitoredContent): MonitoredContent to cache
        """
        if self.n_versions > 1:
            if check_is_folder_emtpy(self.path_cache_folder_th):
                pass
            else:
                self.replace_older_caches()

        cache_mc(mc, self.get_path_cache(self.cache_newest_version))

    def get_newest_cache(self) -> Union[MonitoredContent, None]:
        """Function that gets the newest cache"""
        path_cache = self.get_path_cache(self.cache_newest_version)
        return get_cached_mc(path_cache)
