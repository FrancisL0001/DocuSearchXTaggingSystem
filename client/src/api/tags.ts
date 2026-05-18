import type { TagsResponse } from '../types';

// GET /api/v1/tags — return all topic clusters with their member documents
export async function fetchTags(): Promise<TagsResponse> {
  const res = await fetch('/api/v1/tags');
  if (!res.ok) throw new Error(`Failed to load topics (HTTP ${res.status})`);
  return res.json();
}
