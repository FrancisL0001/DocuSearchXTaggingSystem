import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import App from './App';
import { searchDocuments } from './api/search';
import { fetchTags } from './api/tags';
import type { SearchResponse, TagsResponse } from './types';


vi.mock('./api/search', () => ({
  searchDocuments: vi.fn(),
}));

vi.mock('./api/tags', () => ({
  fetchTags: vi.fn(),
}));

const tagResponse: TagsResponse = {
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
    {
      tag: 'housing',
      documents: [
        {
          id: 'doc-2',
          title: 'Housing Study',
          snippet: 'Rent text',
          score: 0,
          tags: ['housing'],
        },
      ],
    },
  ],
};

const searchResponse: SearchResponse = {
  results: [
    {
      id: 'doc-3',
      title: 'Emissions Report',
      snippet: 'Research text',
      score: 0.91,
      tags: ['climate'],
    },
  ],
  total: 1,
};

describe('App', () => {
  beforeEach(() => {
    vi.mocked(fetchTags).mockReset();
    vi.mocked(searchDocuments).mockReset();
    vi.mocked(fetchTags).mockResolvedValue(tagResponse);
  });

  it('loads topics and displays documents for a selected tag', async () => {
    const user = userEvent.setup();
    render(<App />);

    const climateButton = await screen.findByRole('button', {
      name: 'Filter by topic: climate (1 documents)',
    });

    await user.click(climateButton);

    expect(screen.getByText('Topic:')).toBeInTheDocument();
    expect(screen.getByText('Carbon Targets')).toBeInTheDocument();
    expect(screen.getByText('Policy text')).toBeInTheDocument();
    expect(screen.queryByLabelText(/Similarity:/)).not.toBeInTheDocument();
  });

  it('submits a search, clears tag mode, and renders ranked results', async () => {
    const user = userEvent.setup();
    vi.mocked(searchDocuments).mockResolvedValue(searchResponse);
    render(<App />);

    await screen.findByRole('button', {
      name: 'Filter by topic: climate (1 documents)',
    });

    await user.type(screen.getByLabelText('Search documents'), 'carbon policy');
    await user.click(screen.getByRole('button', { name: 'Run search' }));

    expect(searchDocuments).toHaveBeenCalledWith('carbon policy');

    const results = await screen.findByRole('list', { name: 'Search results' });
    expect(within(results).getByText('Emissions Report')).toBeInTheDocument();
    expect(within(results).getByLabelText('Result 1')).toBeInTheDocument();
    expect(within(results).getByLabelText('Similarity: 91.0% match')).toBeInTheDocument();
    expect(screen.getByText(/result for/)).toBeInTheDocument();
  });

  it('shows an error state when search fails', async () => {
    const user = userEvent.setup();
    vi.mocked(searchDocuments).mockRejectedValue(new Error('Search request failed'));
    render(<App />);

    await screen.findByRole('button', {
      name: 'Filter by topic: climate (1 documents)',
    });

    await user.type(screen.getByLabelText('Search documents'), 'carbon policy');
    await user.click(screen.getByRole('button', { name: 'Run search' }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Search failed');
    expect(screen.getByText('Search request failed')).toBeInTheDocument();
  });

  it('keeps the page usable when tags fail to load', async () => {
    vi.mocked(fetchTags).mockRejectedValue(new Error('Failed to load topics'));
    render(<App />);

    expect(await screen.findByText('Failed to load topics')).toBeInTheDocument();
    expect(screen.getByLabelText('Search documents')).toBeEnabled();
  });
});
