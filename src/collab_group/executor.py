"""Executor for class to scan, create, and change ownership and permissions.

This is the main class that does the work to ensure the collaborative volume
is prepared correctly for use.
"""

import os

import safir.logging
import structlog
import yaml
from rubin.gafaelfawr import GafaelfawrClient, GafaelfawrGroup

from .config import CollabGroupConfig

__all__ = ["CollabGroupExecutor"]


class CollabGroupExecutor:
    """Main class for doing directory scanning and creation."""

    def __init__(self, config: CollabGroupConfig) -> None:
        safir.logging.configure_logging(name="collab-group")
        self._logger = structlog.get_logger("collab-group")
        self._token = config.gafaelfawr_token_path.read_text()
        with config.excluded_groups_path.open("r") as f:
            self._exclude_groups = set(yaml.safe_load(f) or [])
        self._collab_dir = config.collab_dir
        self._gafaelfawr_client = GafaelfawrClient(logger=self._logger)
        if not config.collab_dir.is_dir():
            raise RuntimeError(
                f"{config.collab_dir!s} does not exist or is not a directory"
            )
        self._logger.info(
            f"Executor initialized with collab_dir={self._collab_dir}"
        )

    async def go(self) -> None:
        """Check, create, change permissions and ownerships on directories.

        Get the list of groups to check, and then make the directory for
        each one.
        """
        groups = await self._gafaelfawr_client.list_groups(self._token)
        self._logger.info(f"Checking directories in {self._collab_dir}")
        await self._make_dirs(groups.user)
        self._logger.info("Check complete")

    async def _make_dirs(self, groups: list[GafaelfawrGroup]) -> None:
        """Create a directory for each group, if it doesn't already exist.

        We use mkdir(parents=True) rather than checking existence because
        the latter would introduce a race condition.

        Set its permissions to have sgid set (so further dirs created
        have the same ownership) and be group-writeable.  This has the side
        effect of resetting the top-level group permission and sgid if it
        has gotten changed since creation, but it should not have gotten
        changed.

        Change the group ownership so it's owned by the corresponding group.
        """
        for grp in groups:
            gname = grp.name
            if gname in self._exclude_groups:
                self._logger.info(f"Skipping excluded group {gname}")
                continue
            gdir = self._collab_dir / gname
            try:
                gdir.mkdir(exist_ok=True)
                # UID -1 means "don't change it".
                os.chown(gdir, -1, grp.id)
                gdir.chmod(0o2775)
            except FileExistsError:
                # Because we did mkdir(exist_ok=True), we will only ever get
                # this error if the file exists and isn't a directory.
                self._logger.error(f"{gdir!s} exists but is not a directory")
