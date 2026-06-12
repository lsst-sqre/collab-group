"""Test collab_group's basic functionality."""

import pytest

import collab_group

# Because we're not using pyfakefs, we exercise all of the configuration
# settings (by writing a config relative to the tempdir in conftest).

# The only thing that doesn't get exercised is the CLI itself, and
# that's because if it runs in a subprocess, the network mocks don't work,
# because they're not mocked in the subprocess.


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "collab_fs", "collab_config", "mock_discovery", "mock_gafaelfawr"
)
async def test_basic(
    collab_config: collab_group.CollabGroupConfig,
) -> None:
    """Test happy path."""
    executor = collab_group.CollabGroupExecutor(config=collab_config)
    cl = collab_config.collab_dir
    assert not (cl / "g_adhoc-1").exists()
    assert not (cl / "g_adhoc-2").exists()
    assert not (cl / "g_adhoc-3").exists()
    await executor.go()
    assert (cl / "g_adhoc-1").is_dir()
    assert not (cl / "g_adhoc-2").exists()
    assert (cl / "g_adhoc-3").is_dir()
