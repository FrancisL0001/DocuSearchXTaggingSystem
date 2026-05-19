import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import ResultCard from './ResultCard';
import type { DocumentResult } from '../types';


const doc: DocumentResult = {
  id: 'doc-1',
  title: 'Carbon Targets',
  snippet: 'Policy text about emissions',
  score: 0.876,
  tags: ['climate'],
};

describe('ResultCard', () => {
  it('renders document content, rank, tag, and similarity for search results', () => {
    render(<ResultCard doc={doc} rank={2} />);

    expect(screen.getByText('Carbon Targets')).toBeInTheDocument();
    expect(screen.getByText('Policy text about emissions')).toBeInTheDocument();
    expect(screen.getByText('climate')).toBeInTheDocument();
    expect(screen.getByLabelText('Result 2')).toBeInTheDocument();
    expect(screen.getByLabelText('Similarity: 87.6% match')).toBeInTheDocument();
  });

  it('does not show rank or similarity for tag browsing results', () => {
    render(<ResultCard doc={{ ...doc, score: 0 }} />);

    expect(screen.queryByLabelText(/Result /)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/Similarity:/)).not.toBeInTheDocument();
  });
});
