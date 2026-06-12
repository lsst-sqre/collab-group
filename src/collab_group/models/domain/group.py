"""Representation of a group, which has a name and a gid."""

from dataclasses import dataclass

__all__ = ["Group"]


@dataclass
class Group:
    """Representation of a group, which has a name and a gid."""

    name: str
    gid: int
