import pytest
from src.config import load_config

def test_load_config():
    config = load_config()
    assert isinstance(config, dict)
    assert "data_dir" in config