"""Factory for class to scan, create, and change ownership and permissions.

This is the main class that does the work to ensure the collaborative volume
is prepared correctly for use.
"""

import structlog
import yaml

from .config import CollabGroupConfig
from .services.executor import Executor
from .storage.filesystem import FilesystemStorage
from .storage.gafaelfawr import GafaelfawrStorage

__all__ = ["CollabFactory"]


class CollabFactory:
    """Main class for doing directory scanning and creation."""

    def __init__(self, config: CollabGroupConfig) -> None:
        self._logger = structlog.get_logger("collab_factory")
        with config.gafaelfawr_token_path.open("r") as f:
            token = yaml.safe_load(f)
        with config.excluded_groups_path.open("r") as f:
            exclude_groups = yaml.safe_load(f)
        self._gafaelfawr_storage = GafaelfawrStorage(
            token=token, exclude_groups=exclude_groups, logger=self._logger
        )
        self._file_storage = FilesystemStorage(
            collab_dir=config.collab_dir, logger=self._logger
        )
        self._executor = Executor(
            gafaelfawr_storage=self._gafaelfawr_storage,
            filesystem_storage=self._file_storage,
            logger=self._logger,
        )

    async def go(self) -> None:
        """Carry out directory scanning and creation."""
        await self._executor.go()
