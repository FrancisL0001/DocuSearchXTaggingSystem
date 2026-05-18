// Mirrors the Pydantic response schemas from the FastAPI backend

export interface DocumentResult {
  id: string;
  title: string;
  snippet: string;   // First ~220 chars of the document body
  score: number;     // Cosine similarity in [0, 1]; 0.0 for tag-browse results
  tags: string[];    // Topic tags assigned by k-means clustering
}

export interface SearchResponse {
  results: DocumentResult[];
  total: number;
}

export interface TagGroup {
  tag: string;
  documents: DocumentResult[];
}

export interface TagsResponse {
  tags: TagGroup[];
}
