import type { TagsResponse } from '../types';

const BASE = import.meta.env.VITE_API_BASE_URL ?? '';

// GET /api/v1/tags — return all topic clusters with their member documents
export async function fetchTags(): Promise<TagsResponse> {
  const res = await fetch(`${BASE}/api/v1/tags`);
  if (!res.ok) throw new Error(`Failed to load topics (HTTP ${res.status})`);
  return res.json();
}
