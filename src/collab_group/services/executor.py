"""Service to query Gafaelfawr for user groups and then create corresponding
directories on collab_dir.
"""

from structlog.stdlib import BoundLogger

from ..storage.filesystem import FilesystemStorage
from ..storage.gafaelfawr import GafaelfawrStorage


class Executor:
    """Carry out the duties of the service."""

    def __init__(
        self,
        filesystem_storage: FilesystemStorage,
        gafaelfawr_storage: GafaelfawrStorage,
        logger: BoundLogger,
    ) -> None:
        self._filesystem_storage = filesystem_storage
        self._gafaelfawr_storage = gafaelfawr_storage
        self._logger = logger
        self._logger.info("Executor initialized.")

    async def go(self) -> None:
        """Check, create, change permissions and ownerships on directories.

        Get the list of groups to check, and then pass that to the filesystem
        driver to make and modify directories.
        """
        self._logger.info("Beginning directory checking.")
        groups = await self._gafaelfawr_storage.get_groups()
        await self._filesystem_storage.make_dirs(groups)
        self._logger.info("Directory checking done.")
