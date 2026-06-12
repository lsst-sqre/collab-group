"""Test basic importing."""

import collab_group


def test_load_module() -> None:
    """The import should have worked."""
    _ = collab_group.__version__
