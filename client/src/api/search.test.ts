import { beforeEach, describe, expect, it, vi } from 'vitest';

import { searchDocuments } from './search';


describe('searchDocuments', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('posts the query and top_k to the search endpoint', async () => {
    const responseBody = {
      results: [
        {
          id: 'doc-1',
          title: 'Carbon Targets',
          snippet: 'Policy text',
          score: 0.9,
          tags: ['climate'],
        },
      ],
      total: 1,
    };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(responseBody),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(searchDocuments('carbon policy', 3)).resolves.toEqual(responseBody);

    expect(fetchMock).toHaveBeenCalledWith(expect.stringMatching(/\/api\/v1\/search$/), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'carbon policy', top_k: 3 }),
    });
  });

  it('throws a useful error for non-2xx responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
    }));

    await expect(searchDocuments('carbon policy')).rejects.toThrow(
      'Search request failed (HTTP 500)',
    );
  });
});
