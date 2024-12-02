from dataclasses import asdict, dataclass
import json
from typing import Literal, Optional

@dataclass
class AssistantTool:
    name: str
    description: str

@dataclass
class Step:
    tool: str
    query: str

    def __json__(self):
        return asdict(self)

@dataclass
class Plan:
    _thinking: str
    plan: list[Step]

    def __json__(self):
        return asdict(self)

@dataclass
class DocMetadata:
    tokens: int
    type: Literal['audio', 'text', 'image', 'document']
    content_type: Literal['chunk', 'complete']
    source: Optional[str] = None
    mimeType: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    source_uuid: Optional[str] = None
    conversation_uuid: Optional[str] = None
    uuid: Optional[str] = None
    duration: Optional[float] = None
    headers: Optional[dict[str, list[str]]] = None
    urls: Optional[list[str]] = None
    images: Optional[list[str]] = None
    screenshots: Optional[list[str]] = None
    chunk_index: Optional[int] = None
    total_chunks: Optional[int] = None


@dataclass
class Document:
    text: str
    metadata: DocMetadata
    
@dataclass
class Domain:
    name: str
    url: str
    scrappable: bool

@dataclass
class Query:
    q: str
    url: str

@dataclass
class Action:
    type: Literal['translate', 'summarize', 'synthesize', 'extract', 'answer']
    url: str
    extraction_type: Optional[str] = None
    description: Optional[str] = None

@dataclass
class PageMetadata:
    url: str
    title: str
    description: str

@dataclass
class CrawlResult:
    markdown: str
    metadata: PageMetadata

