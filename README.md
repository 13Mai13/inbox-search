# inbox-search

## Setup

### Worktree

```
.
├── LICENSE
├── README.md
└── data
    └── data.txt # File with all the links
```

Example of `data.txt`

```
https://github.com/microsoft/graphrag | microsoft/graphrag: A modular graph-based Retrieval-Augmented Generation (RAG) system
https://poloclub.github.io/transformer-explainer/ | Transformer Explainer: LLM Transformer Model Visually Explained
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
