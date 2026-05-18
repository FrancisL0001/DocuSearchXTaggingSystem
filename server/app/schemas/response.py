from pydantic import BaseModel


class DocumentResult(BaseModel):
    id: str            # Document identifier (e.g. "001")
    title: str         # Full document title
    snippet: str       # First ~220 characters of the body — shown in the UI result card
    score: float       # Cosine similarity to the search query; 0.0 for tag-browse results
    tags: list[str]    # Topic tag(s) assigned by k-means clustering


class SearchResponse(BaseModel):
    results: list[DocumentResult]
    total: int    # Number of results actually returned (may be less than top_k near corpus edges)


class TagGroup(BaseModel):
    # One topic cluster and every document that belongs to it
    tag: str
    documents: list[DocumentResult]


class TagsResponse(BaseModel):
    tags: list[TagGroup]
