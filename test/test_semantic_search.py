import pytest
from sentence_transformers import SentenceTransformer
import torch

from src.semantic_search.search import load_model, encode_urls, search_urls

@pytest.fixture
def model():
    return load_model()

@pytest.fixture
def sample_data():
    return [
        {
            "url": "https://example.com/python",
            "title": "Python Programming",
            "content": ""
        },
        {
            "url": "https://example.com/javascript",
            "title": "JavaScript Basics",
            "content": ""
        }
    ]

def test_load_model():
    model = load_model()
    assert isinstance(model, SentenceTransformer)

def test_encode_urls(model, sample_data):
    embeddings = encode_urls(model, sample_data)
    assert isinstance(embeddings, torch.Tensor)
    assert len(embeddings) == len(sample_data)

def test_search_urls(model, sample_data):
    embeddings = encode_urls(model, sample_data)
    results = search_urls("python programming", model, sample_data, embeddings, top_k=1)
    assert len(results) == 1
    assert all(k in results[0] for k in ['score', 'url', 'title'])