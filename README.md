# inbox-search

A search engine on top of my open browser tabs. 

## Setup

### Worktree

```
.
├── LICENSE
├── README.md
├── configs
│   └── dev-config.yaml
├── data
│   ├── data.txt
│   └── processed.json
├── logs
│   └── inbox_search.log
├── main.py
├── pyproject.toml
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   ├── preprocessing
│   ├── semantic_search
│   └── ultils.py
├── test
│   ├── __init__.py
│   ├── __pycache__
│   ├── test_preprocessing.py
│   ├── test_semantic_search.py
│   └── test_utils.py
├── uv.lock
```

Example of `data.txt`

```
https://github.com/microsoft/graphrag | microsoft/graphrag: A modular graph-based Retrieval-Augmented Generation (RAG) system
https://poloclub.github.io/transformer-explainer/ | Transformer Explainer: LLM Transformer Model Visually Explained
```

### Install dependencies

```
uv venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
uv pip install -r requirements.txt
```

```
pre-commit install
pre-commit run --all-files
```

### Commands

```
python main.py --stage search --env dev --query "python tips"
```

## Project 

### Why? 

If you are anything like me, you'll probably have + 100 tabs open in every single device you own that has access to the internet. This isn't great for **multiple** reasons: resource consumption, visual clutter, ... but specially because you can **never** find that one article you read and want to recommend to someone, or that resource you've found and you are "saving for latter". 

### What? 

The idea is to try if having search on top of all this link repository would be useful for me. There are two main things I want to achive: 

* Monitor: What am I intersted in lately? -> Most likely because I'd want to devote proper time to read / explore that

* Build a searcher that given a sentece can retrive the link I'm looking for

### How? 

We'll start with the basic stuff. I use [one tab](https://chromewebstore.google.com/detail/onetab/chphlpgkkbolifaimnlloiipkdnihall?hl=en) that has an hability to export links. This is the initial database. 

I'll build a small cli on top of my personal information. 
