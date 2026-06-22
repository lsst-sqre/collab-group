"""pytest fixtures for collab-group tests."""

import json
import os
from collections.abc import AsyncIterator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import pytest_asyncio
import respx
import yaml
from rubin.gafaelfawr import (
    GafaelfawrGroup,
    GafaelfawrGroups,
    MockGafaelfawr,
    register_mock_gafaelfawr,
)
from rubin.repertoire import Discovery, register_mock_discovery

import collab_group

DATA = Path(__file__).parent / "data"
DISCOVERY = json.loads((DATA / "discovery.json").read_text())
GROUPS = GafaelfawrGroups(
    system=[],
    user=[
        GafaelfawrGroup.model_validate(x)
        for x in json.loads((DATA / "groups.json").read_text())
    ],
)
EXCLUDED_GROUPS = ["g_adhoc-2"]


@pytest.fixture
def mock_discovery(
    respx_mock: respx.Router, monkeypatch: pytest.MonkeyPatch
) -> Discovery:
    monkeypatch.setenv("REPERTOIRE_BASE_URL", "https://example.com/repertoire")
    return register_mock_discovery(respx_mock, DISCOVERY)


@pytest_asyncio.fixture
async def mock_gafaelfawr(
    mock_discovery: Discovery, respx_mock: respx.Router
) -> MockGafaelfawr:
    mg = await register_mock_gafaelfawr(respx_mock)
    mg.set_groups(GROUPS)
    return mg


# pyfakefs would have been more elegant, but it got very confused about
# containment.  So we'll do this the old-fashioned way with a temporary
# directory.

# In real life, this will be running with privilege, but we certainly don't
# want to run the test suite that way, so we just make os.chown() a no-op.


def _fake_chown(
    path: str | Path,
    uid: int,
    gid: int,
    *,
    dir_fd: int | None = None,
    follow_symlinks: bool = True,
) -> None:
    pass


@pytest_asyncio.fixture
async def collab_fs(
    mock_gafaelfawr: MockGafaelfawr, monkeypatch: pytest.MonkeyPatch
) -> AsyncIterator[str]:
    with TemporaryDirectory() as td:
        tpath = Path(td)
        collab_dir = tpath / "collab"
        cfg_file = tpath / "config.yaml"
        tok_file = tpath / "gafaelfawr-token"
        collab_dir.mkdir()
        config = {
            "collabDir": str(collab_dir),
            "excludedGroups": EXCLUDED_GROUPS,
            "gafaelfawrTokenPath": str(tok_file),
        }
        cfg_file.write_text(yaml.dump(config))
        token = mock_gafaelfawr.create_token(
            "bot-collab-group", scopes=("admin:userinfo",)
        )
        tok_file.write_text(token)
        monkeypatch.setattr(os, "chown", _fake_chown)
        yield td


@pytest_asyncio.fixture
async def collab_config(
    collab_fs: str,
) -> AsyncIterator[collab_group.CollabGroupConfig]:
    cfg_path = Path(collab_fs) / "config.yaml"
    config = yaml.safe_load(cfg_path.read_text())
    yield collab_group.CollabGroupConfig.model_validate(config)
