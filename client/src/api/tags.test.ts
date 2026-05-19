import { beforeEach, describe, expect, it, vi } from 'vitest';

import { fetchTags } from './tags';


describe('fetchTags', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('loads topic groups from the tags endpoint', async () => {
    const responseBody = {
      tags: [
        {
          tag: 'climate',
          documents: [
            {
              id: 'doc-1',
              title: 'Carbon Targets',
              snippet: 'Policy text',
              score: 0,
              tags: ['climate'],
            },
          ],
        },
      ],
    };
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(responseBody),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(fetchTags()).resolves.toEqual(responseBody);

    expect(fetchMock).toHaveBeenCalledWith(expect.stringMatching(/\/api\/v1\/tags$/));
  });

  it('throws a useful error when topics cannot be loaded', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 503,
    }));

    await expect(fetchTags()).rejects.toThrow('Failed to load topics (HTTP 503)');
  });
});
