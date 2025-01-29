"""
Test utils.py
"""

import pytest
import logging
import yaml
from pathlib import Path
from src.ultils import setup_logging, load_config


@pytest.fixture
def valid_config():
    return {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/test.log"
        }
    }

@pytest.fixture
def invalid_level_config():
    return {
        "logging": {
            "level": "INVALID_LEVEL",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "logs/test.log"
        }
    }

@pytest.fixture
def missing_keys_config():
    return {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            # missing 'file' key
        }
    }

@pytest.fixture
def temp_config_file(tmp_path):
    config_data = {
        "test_key": "test_value",
        "nested": {
            "key": "value"
        }
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)
    return str(config_file)

def test_setup_logging_success(valid_config):
    """Test successful logging setup"""
    logger = setup_logging(valid_config)
    assert isinstance(logger, logging.Logger)
    assert logger.name == "src.ultils"
    assert logger.getEffectiveLevel() == logging.INFO
    
    # Clean up log file if created
    log_path = Path(valid_config["logging"]["file"])
    if log_path.exists():
        log_path.unlink()
        log_path.parent.rmdir()

def test_setup_logging_invalid_level(invalid_level_config):
    """Test logging setup with invalid log level"""
    with pytest.raises(ValueError, match="Invalid logging level:"):
        setup_logging(invalid_level_config)

def test_setup_logging_missing_keys(missing_keys_config):
    """Test logging setup with missing required keys"""
    with pytest.raises(KeyError, match="Missing required logging config keys:"):
        setup_logging(missing_keys_config)

def test_setup_logging_permission_error(valid_config, monkeypatch):
    """Test logging setup with permission error"""
    def mock_mkdir(*args, **kwargs):
        raise PermissionError("Permission denied")
    
    monkeypatch.setattr(Path, "mkdir", mock_mkdir)
    with pytest.raises(ValueError, match="Failed to setup logging directory:"):
        setup_logging(valid_config)

def test_load_config_success(temp_config_file):
    """Test successful config loading"""
    config = load_config(temp_config_file)
    assert isinstance(config, dict)
    assert config["test_key"] == "test_value"
    assert config["nested"]["key"] == "value"

def test_load_config_file_not_found():
    """Test config loading with non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_config.yaml")

def test_load_config_invalid_yaml(tmp_path):
    """Test config loading with invalid YAML"""
    invalid_yaml_file = tmp_path / "invalid.yaml"
    with open(invalid_yaml_file, "w") as f:
        f.write("invalid: yaml: content: :")
    
    with pytest.raises(yaml.YAMLError):
        load_config(str(invalid_yaml_file))