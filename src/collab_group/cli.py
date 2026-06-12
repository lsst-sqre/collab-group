"""Command-line to scan, create, and modify directories."""

import asyncio
from pathlib import Path

import yaml

from .config import CollabGroupConfig
from .constants import CONFIG_PATH
from .executor import CollabGroupExecutor

__all__ = ["main"]

import click


@click.version_option(message="%(version)s")
@click.option(
    "--config-file",
    "-c",
    help="Application configuration file",
    type=Path,
    default=CONFIG_PATH,
)
@click.command()
def main(config_file: Path) -> None:
    """Command-line interface to scan, create, and modify directories.

    Uses a configuration file to specify the directory to act upon, the
    location of a YAML file naming groups to exclude, and the path to
    a Gafaelfawr token with ``admin.userinfo`` scope to retrieve a list of
    user groups.

    The program will ensure that any group found that is not named in
    the excluded groups has a directory (of the same name as the group)
    in the top-level directory, and if it must create it, it will create it
    as group-writeable and set-group-id so that further created directories
    are owned by the same group.

    The purpose of this is to provide users of the Rubin Science Platform with
    file space where they can do ad-hoc collaborative work by creating
    groups and adding other users to those groups.
    """
    with config_file.open("r") as f:
        config_obj = yaml.safe_load(f)
    config = CollabGroupConfig.model_validate(config_obj)
    executor = CollabGroupExecutor(config)
    asyncio.run(executor.go())
