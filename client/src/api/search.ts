import type { SearchResponse } from '../types';

// In dev, VITE_API_BASE_URL is empty and Vite's proxy handles /api/* → localhost:8000.
// In prod, set VITE_API_BASE_URL to the full backend URL (e.g. https://api.yourdomain.com).
const BASE = import.meta.env.VITE_API_BASE_URL ?? '';

// POST /api/v1/search — embed query and return ranked documents
export async function searchDocuments(
  query: string,
  topK = 8,
): Promise<SearchResponse> {
  const res = await fetch(`${BASE}/api/v1/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK }),
  });

  if (!res.ok) throw new Error(`Search request failed (HTTP ${res.status})`);
  return res.json();
}
