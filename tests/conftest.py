"""pytest fixtures for collab-group tests."""

import json
from pathlib import Path

import httpx
import pytest
import respx
from pyfakefs.fake_filesystem import FakeFilesystem
from rubin.repertoire import Discovery, register_mock_discovery

DATA = Path(__file__).parent / "data"
DISCOVERY = json.loads((DATA / "discovery.json").read_text())
GROUPS = json.loads((DATA / "groups.json").read_text())


@pytest.fixture(autouse=True)
def mock_discovery(
    respx_mock: respx.Router, monkeypatch: pytest.MonkeyPatch
) -> Discovery:
    monkeypatch.setenv("REPERTOIRE_BASE_URL", "https://example.com/repertoire")
    path = Path(__file__).parent / "data" / "discovery.json"
    if not path.exists():
        path = "/etc/nublado/discovery.json"
    return register_mock_discovery(respx_mock, path)


@pytest.fixture(autouse=True)
def mock_groups(respx_mock: respx.Router) -> respx.Router:
    respx_mock.get("https://data.example.com/auth/api/v1/groups").mock(
        return_value=httpx.Response(200, json=GROUPS)
    )
    return respx_mock


@pytest.fixture(autouse=True)
def collab_fs(fs: FakeFilesystem) -> FakeFilesystem:
    fs.add_real_directory(DATA / "root" / "mnt", target_path="/mnt")
    fs.add_real_directory(DATA / "root" / "etc", target_path="/etc")
    return fs
