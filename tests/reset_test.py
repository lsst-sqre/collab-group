"""Test that broken (top-level) permissions get fixed."""

import pytest

import collab_group


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "collab_fs", "collab_config", "mock_discovery", "mock_gafaelfawr"
)
async def test_reset_perms(
    collab_config: collab_group.CollabGroupConfig,
) -> None:
    """Test that broken perms (at the top level) get fixed."""
    executor = collab_group.CollabGroupExecutor(config=collab_config)
    cl = collab_config.collab_dir
    assert not (cl / "g_adhoc-1").exists()
    assert not (cl / "g_adhoc-2").exists()
    assert not (cl / "g_adhoc-3").exists()
    (cl / "g_adhoc-3").mkdir()
    (cl / "g_adhoc-3").chmod(0o700)
    assert (cl / "g_adhoc-3").is_dir()
    assert (cl / "g_adhoc-3").stat().st_mode & 0o7777 == 0o0700
    await executor.go()
    assert (cl / "g_adhoc-1").is_dir()
    assert (cl / "g_adhoc-1").stat().st_mode & 0o7777 == 0o2775
    assert not (cl / "g_adhoc-2").exists()
    assert (cl / "g_adhoc-3").is_dir()
    assert (cl / "g_adhoc-3").stat().st_mode & 0o7777 == 0o2775
