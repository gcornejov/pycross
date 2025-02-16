import pytest_textual_snapshot 

def test_app_initialization(snap_compare: pytest_textual_snapshot.snap_compare, pycross_app):
    assert snap_compare(pycross_app, terminal_size=(80, 34))
