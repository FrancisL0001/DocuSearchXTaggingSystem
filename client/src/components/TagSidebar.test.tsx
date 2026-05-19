import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';

import TagSidebar from './TagSidebar';
import type { TagGroup } from '../types';


const tags: TagGroup[] = [
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
      {
        id: 'doc-2',
        title: 'Emissions Report',
        snippet: 'Research text',
        score: 0,
        tags: ['climate'],
      },
    ],
  },
  {
    tag: 'housing',
    documents: [
      {
        id: 'doc-3',
        title: 'Housing Study',
        snippet: 'Rent text',
        score: 0,
        tags: ['housing'],
      },
    ],
  },
];

describe('TagSidebar', () => {
  it('shows a loading state while topics load', () => {
    render(
      <TagSidebar
        tags={[]}
        activeTag={null}
        loading={true}
        error={null}
        onTagClick={vi.fn()}
      />,
    );

    expect(screen.getByLabelText('Loading topics')).toHaveAttribute('aria-busy', 'true');
  });

  it('shows an error when topic loading fails', () => {
    render(
      <TagSidebar
        tags={[]}
        activeTag={null}
        loading={false}
        error="Failed to load topics"
        onTagClick={vi.fn()}
      />,
    );

    expect(screen.getByText('Failed to load topics')).toBeInTheDocument();
  });

  it('renders topic buttons with counts and calls the click handler', async () => {
    const user = userEvent.setup();
    const onTagClick = vi.fn();

    render(
      <TagSidebar
        tags={tags}
        activeTag="climate"
        loading={false}
        error={null}
        onTagClick={onTagClick}
      />,
    );

    const climateButton = screen.getByRole('button', {
      name: 'Filter by topic: climate (2 documents)',
    });
    const housingButton = screen.getByRole('button', {
      name: 'Filter by topic: housing (1 documents)',
    });

    expect(climateButton).toHaveAttribute('aria-pressed', 'true');
    expect(housingButton).toHaveAttribute('aria-pressed', 'false');

    await user.click(housingButton);

    expect(onTagClick).toHaveBeenCalledWith('housing');
  });
});
