"""Configuration for collab-group."""

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .constants import COLLAB_DIR, GAFAELFAWR_TOKEN_PATH

__all__ = ["CollabGroupConfig"]


class CollabGroupConfig(BaseModel):
    """Configuration for collab-group."""

    model_config = ConfigDict(
        alias_generator=to_camel, extra="forbid", populate_by_name=True
    )

    collab_dir: Annotated[
        Path,
        Field(
            title="Collaboration directory",
            description="Root of collaboration volume",
            examples=[COLLAB_DIR],
        ),
    ] = COLLAB_DIR

    excluded_groups: Annotated[
        list[str] | None,
        Field(
            title="Excluded groups",
            description="List of groups to not create directories for",
            examples=[["g_adhoc-2"]],
        ),
    ] = None

    gafaelfawr_token_path: Annotated[
        Path,
        Field(
            title="File containing Gafaelfawr token",
            description=(
                "File containing Gafaelfawr token with 'admin:userinfo'"
                " scope to query groups"
            ),
            examples=[GAFAELFAWR_TOKEN_PATH],
        ),
    ] = GAFAELFAWR_TOKEN_PATH
