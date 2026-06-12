"""Command-line to scan, create, and modify directories."""

import asyncio
from pathlib import Path

import yaml

from .config import CollabGroupConfig
from .constants import CONFIG_PATH
from .factory import CollabFactory

__all__ = ["main"]

import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
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
    """Command-line interface to scan, create, and modify directories."""
    with config_file.open("r") as f:
        config_obj = yaml.safe_load(f)
    config = CollabGroupConfig.model_validate(config_obj)
    factory = CollabFactory(config)
    asyncio.run(factory.go())
