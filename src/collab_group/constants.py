"""Global constants."""

from pathlib import Path

__all__ = [
    "COLLAB_DIR",
    "CONFIG_PATH",
    "GAFAELFAWR_TOKEN_PATH",
]

COLLAB_DIR = Path("/mnt/collab")
"""Path to root of collaboration volume.

The service must run with root-equivalent privilege on the collaboration
filesystem."""

CONFIG_PATH = Path("/etc/collab-group/config.yaml")
"""Path to configuration YAML file."""

GAFAELFAWR_TOKEN_PATH = Path("/etc/gafaelfawr/token")
"""Path to Gafaelfawr token.

This token must have 'admin:userinfo' scope in order to list groups.
"""
