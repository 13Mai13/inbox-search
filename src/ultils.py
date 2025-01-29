"""
All auxiliary functions that don't belong to any folder
"""
import yaml
import logging
from pathlib import Path
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Setup logging configuration"""
    logging_config = config["logging"]

    # Check for required keys first
    required_keys = ["level", "format", "file"]
    missing_keys = [key for key in required_keys if key not in logging_config]
    if missing_keys:
        raise KeyError(f"Missing required logging config keys: {', '.join(missing_keys)}")

    # Validate log level
    try:
        log_level = getattr(logging, logging_config["level"].upper())
    except AttributeError:
        raise ValueError(f"Invalid logging level: {logging_config['level']}")

    try:
        # Create log directory if it doesn't exist
        log_path = Path(logging_config["file"])
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Reset any existing logging configuration
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Configure logging
        logging.basicConfig(
            level=log_level,
            format=logging_config["format"],
            handlers=[
                logging.FileHandler(logging_config["file"]),
                logging.StreamHandler()
            ],
            force=True
        )

        return logging.getLogger("src.ultils")

    except (OSError, PermissionError) as e:
        raise ValueError(f"Failed to setup logging directory: {str(e)}")


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config