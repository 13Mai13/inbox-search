"""
Enforced data model
"""
from pydantic import BaseModel
from typing import Optional

class Entry(BaseModel):
    url: str
    title: str
    content: Optional[str] = ""