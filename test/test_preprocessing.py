"""
Test preprocessing module
"""

import pytest
from pathlib import Path
import json
from src.preprocessing.main import (
    load_data,
    clean_text,
    transform_txt_to_json,
    save_data,
    main
)

# Test data fixtures
@pytest.fixture
def sample_lines():
    return [
        "https://example.com | Example Title\n",
        "https://test.com | Test Title\n",
        "invalid line without delimiter\n",
        "\n",  # Empty line
        "https://another.com | Another Title\n"
    ]

@pytest.fixture
def expected_processed_data():
    return [
        {
            "url": "https://example.com",
            "title": "example title",
            "content": ""
        },
        {
            "url": "https://test.com",
            "title": "test title",
            "content": ""
        },
        {
            "url": "https://another.com",
            "title": "another title",
            "content": ""
        }
    ]

@pytest.fixture
def test_input_file(tmp_path, sample_lines):
    """Create a temporary input file with sample data"""
    input_file = tmp_path / "test_input.txt"
    with open(input_file, "w") as f:
        f.writelines(sample_lines)
    return input_file

@pytest.fixture
def test_output_file(tmp_path):
    """Create a temporary output file path"""
    return tmp_path / "output" / "processed.json"

@pytest.fixture
def test_config(test_input_file, test_output_file):
    """Create a test configuration"""
    return {
        "data": {
            "input_path": str(test_input_file),
            "output_path": str(test_output_file)
        }
    }

# Test individual functions
def test_load_data(test_input_file, sample_lines):
    """Test loading data from a file"""
    loaded_lines = load_data(test_input_file)
    assert loaded_lines == sample_lines
    assert isinstance(loaded_lines, list)
    assert all(isinstance(line, str) for line in loaded_lines)

def test_load_data_file_not_found():
    """Test loading data from a non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_data(Path("nonexistent_file.txt"))

def test_clean_text():
    """Test text cleaning functionality"""
    test_cases = [
        ("Hello World  ", "hello world"),
        ("  UPPER case  ", "upper case"),
        ("Multiple    Spaces", "multiple    spaces"),
        ("", ""),
        ("   ", "")
    ]
    
    for input_text, expected in test_cases:
        assert clean_text(input_text) == expected

def test_transform_txt_to_json(sample_lines, expected_processed_data):
    """Test transformation of text lines to JSON format"""
    result = transform_txt_to_json(sample_lines)
    assert result == expected_processed_data
    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)

def test_save_data(tmp_path, expected_processed_data):
    """Test saving data to JSON file"""
    output_file = tmp_path / "test_output.json"
    save_data(expected_processed_data, output_file)
    
    # Verify file exists and content is correct
    assert output_file.exists()
    with open(output_file, "r") as f:
        saved_data = json.load(f)
    assert saved_data == expected_processed_data

def test_save_data_permission_error(tmp_path, expected_processed_data, monkeypatch):
    """Test saving data with permission error"""
    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")
    
    monkeypatch.setattr("builtins.open", mock_open)
    with pytest.raises(PermissionError):
        save_data(expected_processed_data, tmp_path / "test.json")

# Test main integration function
def test_main_success(test_config, expected_processed_data):
    """Test successful execution of main function"""
    main(test_config)
    
    # Verify output file exists and contains correct data
    output_path = Path(test_config["data"]["output_path"])
    assert output_path.exists()
    with open(output_path, "r") as f:
        processed_data = json.load(f)
    assert processed_data == expected_processed_data

def test_main_input_file_not_found(test_config):
    """Test main function with non-existent input file"""
    test_config["data"]["input_path"] = "nonexistent_file.txt"
    with pytest.raises(FileNotFoundError):
        main(test_config)

def test_main_creates_output_directory(test_config):
    """Test that main function creates output directory if it doesn't exist"""
    output_path = Path(test_config["data"]["output_path"])
    if output_path.parent.exists():
        output_path.parent.rmdir()
    
    main(test_config)
    assert output_path.parent.exists()
    assert output_path.exists()