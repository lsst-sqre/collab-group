"""Global constants."""

from pathlib import Path

__all__ = [
    "COLLAB_DIR",
    "CONFIG_PATH",
    "EXCLUDED_GROUPS_PATH",
    "GAFAELFAWR_TOKEN_PATH",
]

COLLAB_DIR = Path("/mnt/collab")
"""Path to root of collaboration volume.

The service must run with root-equivalent privilege on the collaboration
filesystem."""

CONFIG_PATH = Path("/etc/collab-group/config.yaml")
"""Path to configuration YAML file."""

EXCLUDED_GROUPS_PATH = Path("/etc/collab-group/exclude-groups.yaml")
"""Path to YAML file listing groups to exclude from consideration.

Any "user" group that is not listed in "exclude-groups.yaml" will have
a directory created and ownership and permissions set for it when this
service runs.
"""

GAFAELFAWR_TOKEN_PATH = Path("/etc/gafaelfawr/token")
"""Path to Gafaelfawr token.

This token must have 'admin:userinfo' scope in order to list groups.
"""
