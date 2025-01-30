"""
Semantic Search functionality
"""

import logging
from typing import List, Dict

import torch
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)

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
