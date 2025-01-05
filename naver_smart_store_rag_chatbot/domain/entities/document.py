from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    id: str
    title: str
    content: str
    related_titles: List[str]
