"""
Preprocess the data for the LLM to be able to retrive the link
"""

import json
from pathlib import Path
from typing import Dict, List, Any
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

def load_data(path: Path) -> List[str]:
    """Load data from a text file."""
    logger.info(f"Loading data from {path}")
    with open(path, "r") as f:
        lines = f.readlines()
    return lines

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    return text.lower().strip()

def transform_txt_to_json(lines: List[str]) -> List[Dict[str, Any]]:
    """Transform lines of text into a structured JSON format."""
    logger.info("Transforming text data to JSON format")
    data = []
    for line in tqdm(lines, desc="Processing lines"):
        line = line.strip()
        if line:
            # Split the line into URL and title using the delimiter " | "
            parts = line.split(" | ", 1)
            if len(parts) == 2:
                url, title = parts
                data.append({
                    "url": clean_text(url),
                    "title": clean_text(title),
                    "content": ""  # Placeholder for content (if available)
                })
    return data

def save_data(data: List[Dict[str, Any]], output_path: Path):
    """Save processed data to a JSON file."""
    logger.info(f"Saving processed data to {output_path}")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def main(config: Dict[str, Any]):
    """Main preprocessing function."""
    logger.info("Starting data preprocessing")

    input_path = Path(config["data"]["input_path"])
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        raise FileNotFoundError(f"Input file not found: {input_path}")

    lines = load_data(input_path)

    processed_data = transform_txt_to_json(lines)

    output_path = Path(config["data"]["output_path"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_data(processed_data, output_path)

    logger.info("Data preprocessing completed")