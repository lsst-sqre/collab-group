"""Filesystem storage for collab-group."""

import os
from pathlib import Path

from structlog.stdlib import BoundLogger

from ..models.domain.group import Group

__all__ = ["FilesystemStorage"]


class FilesystemStorage:
    """Filesystem storage for collab-group."""

    def __init__(self, collab_dir: Path, logger: BoundLogger) -> None:
        self._collab_dir = collab_dir
        self._logger = logger

    async def make_dirs(self, groups: list[Group]) -> None:
        """Create a directory for each group, if it doesn't already exist.

        Set its permissions to have group sticky set (so further dirs created
        have the same ownership) and group-writeable.

        Change the group ownership so it's owned by the corresponding group.
        """
        for grp in groups:
            gname = grp.name
            gdir = self._collab_dir / gname
            if not gdir.exists():
                gdir.mkdir(mode=0o1775)
                uid = gdir.stat().st_uid
                os.chown(gdir, uid, grp.gid)
            elif not gdir.is_dir():
                self._logger.error(f"{gdir!s} exists but is not directory")
