import pytest
import src.preprocessing.main as preprocess

@pytest.fixture
def sample_data():
    return "https://www.wheresyoured.at/pop-culture/ | Pop Culture \n https://medium.com/recommender using Qdrant, LlamaIndex, and Google Gemini | by Benito Martin | Medium"

def test_preprocess(sample_data):
    result = preprocess(sample_data)
    transformed = {

    }
    assert result == transformed
