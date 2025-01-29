"""
Enforced data model
"""
from pydantic import BaseModel
from typing import Optional

class Resource(BaseModel):
    url: str
    title: str
    document: Optional[str]