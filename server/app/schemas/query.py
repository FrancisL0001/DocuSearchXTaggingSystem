from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    # The natural-language question or phrase the user wants to search for
    query: str = Field(..., min_length=1, max_length=500, description="Natural-language search query")

    # How many ranked results to return (capped at 20 to keep responses manageable)
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")
