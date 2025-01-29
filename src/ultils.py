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

    Path(logging_config["file"]).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging_config["level"],
        format=logging_config["format"],
        handlers=[logging.FileHandler(logging_config["file"]), logging.StreamHandler()],
    )

    return logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config