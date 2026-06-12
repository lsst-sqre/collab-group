"""Executor for class to scan, create, and change ownership and permissions.

This is the main class that does the work to ensure the collaborative volume
is prepared correctly for use.
"""

import os

import structlog
import yaml
from rubin.gafaelfawr import GafaelfawrClient, GafaelfawrGroup

from .config import CollabGroupConfig

__all__ = ["CollabGroupExecutor"]


class CollabGroupExecutor:
    """Main class for doing directory scanning and creation."""

    def __init__(self, config: CollabGroupConfig) -> None:
        self._logger = structlog.get_logger("collab_executor")
        with config.gafaelfawr_token_path.open("r") as f:
            self._token = yaml.safe_load(f)
        with config.excluded_groups_path.open("r") as f:
            self._exclude_groups = yaml.safe_load(f)
        self._collab_dir = config.collab_dir
        self._gafaelfawr_client = GafaelfawrClient(logger=self._logger)
        self._logger.info(
            f"Executor initialized with collab_dir={self._collab_dir}"
        )

    async def go(self) -> None:
        """Check, create, change permissions and ownerships on directories.

        Get the list of groups to check, and then pass that to the filesystem
        driver to make and modify directories.
        """
        groups = await self._gafaelfawr_client.list_groups(self._token)
        self._logger.info(f"Checking directories in {self._collab_dir}")
        await self._make_dirs(groups.user)
        self._logger.info("Check complete")

    async def _make_dirs(self, groups: list[GafaelfawrGroup]) -> None:
        """Create a directory for each group, if it doesn't already exist.

        Set its permissions to have sgid set (so further dirs created
        have the same ownership) and be group-writeable.

        Change the group ownership so it's owned by the corresponding group.

        """
        for grp in groups:
            gname = grp.name
            if gname in self._exclude_groups:
                self._logger.info(f"Skipping excluded group {gname}")
                continue
            gdir = self._collab_dir / gname
            if not gdir.exists():
                self._logger.info(f"Creating {gdir!s}")
                gdir.mkdir(mode=0o2775)
                uid = gdir.stat().st_uid
                os.chown(gdir, uid, grp.id)
            elif not gdir.is_dir():
                self._logger.error(f"{gdir!s} exists but is not a directory")
            else:
                self._logger.debug(f"{gdir!s} already exists")
