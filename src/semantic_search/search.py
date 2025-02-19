"""
Semantic Search functionality
"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

import torch
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)

def load_url_data(data_path: Path) -> List[Dict]:
    """Load URL data from JSON file"""
    logger.debug(f"Loading data from {data_path}")
    try:
        with open(data_path) as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} URLs")
        return data
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise

def load_model(model_name: str = 'all-MiniLM-L6-v2') -> SentenceTransformer:
    """Load and return the sentence transformer model"""
    logger.info(f"Loading model: {model_name}")
    return SentenceTransformer(model_name)

def encode_urls(
    model: SentenceTransformer,
    url_data: List[Dict]
) -> torch.Tensor:
    """Encode URL data using the transformer model"""
    logger.debug("Encoding URLs")
    texts = [f"{item['title']} {item['url']}" for item in url_data]
    return model.encode(texts, convert_to_tensor=True)

def search_urls(
    query: str,
    model: SentenceTransformer,
    url_data: List[Dict],
    embeddings: torch.Tensor,
    top_k: int = 5
) -> List[Dict]:
    """Search for most similar URLs given a query"""
    logger.debug(f"Searching for query: {query}")
    
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = torch.topk(cos_scores, k=min(top_k, len(url_data)))
    
    matches = [
        {
            'score': float(score),
            'url': url_data[int(idx)]['url'],
            'title': url_data[int(idx)]['title']
        }
        for score, idx in zip(top_results[0], top_results[1])
    ]
    
    logger.info(f"Found {len(matches)} matches")
    return matches

def main(config: Dict[str, Any], query: str):
    """Main preprocessing function."""
    logger.info("Starting data preprocessing")

    model = load_model()
    url_data = load_url_data(config['data']['output_path'])
    embeddings = encode_urls(model, url_data)
    
    # Perform search
    matches = search_urls(query, model, url_data, embeddings, top_k=5)
    
    # Output results
    for idx, match in enumerate(matches, 1):
        print(f"\n{idx}. Score: {match['score']:.4f}")
        print(f"   Title: {match['title']}")
        print(f"   URL: {match['url']}")

    logger.info("Search was completed")