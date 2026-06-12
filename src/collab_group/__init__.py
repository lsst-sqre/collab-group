"""Top-level collab-group metadata."""

from importlib.metadata import PackageNotFoundError, version

from .config import CollabGroupConfig
from .executor import CollabGroupExecutor

__all__ = ["CollabGroupConfig", "CollabGroupExecutor", "__version__"]


__version__: str
"""The module version string (PEP 440 / SemVer compatible)."""

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"
