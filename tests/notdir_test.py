"""Test collab_group warns when file exists but is not a directory."""

import pytest

import collab_group


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "collab_fs", "collab_config", "mock_discovery", "mock_gafaelfawr"
)
async def test_notdir(
    collab_config: collab_group.CollabGroupConfig,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test warning for existing file that isn't a directory."""
    executor = collab_group.CollabGroupExecutor(config=collab_config)
    cl = collab_config.collab_dir
    assert not (cl / "g_adhoc-1").exists()
    assert not (cl / "g_adhoc-2").exists()
    assert not (cl / "g_adhoc-3").exists()
    (cl / "g_adhoc-3").write_text("I am a file")
    assert (cl / "g_adhoc-3").exists()
    await executor.go()
    assert (cl / "g_adhoc-1").is_dir()
    assert not (cl / "g_adhoc-2").exists()
    assert (cl / "g_adhoc-3").is_file()
    captured = capsys.readouterr().out
    assert "g_adhoc-3 exists but is not a directory" in captured
