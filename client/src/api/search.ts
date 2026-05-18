import type { SearchResponse } from '../types';

// POST /api/v1/search — embed query and return ranked documents
export async function searchDocuments(
  query: string,
  topK = 8,
): Promise<SearchResponse> {
  const res = await fetch('/api/v1/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK }),
  });

  if (!res.ok) throw new Error(`Search request failed (HTTP ${res.status})`);
  return res.json();
}
