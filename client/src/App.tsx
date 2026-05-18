import { useCallback, useEffect, useState } from 'react';

import Header from './components/Header';
import SearchBar from './components/SearchBar';
import TagSidebar from './components/TagSidebar';
import ResultCard from './components/ResultCard';
import ResultsSkeleton from './components/ResultsSkeleton';
import EmptyState from './components/EmptyState';

import { searchDocuments } from './api/search';
import { fetchTags } from './api/tags';
import type { DocumentResult, TagGroup } from './types';

export default function App() {
  // ── Search state ────────────────────────────────────────────────────
  const [query, setQuery] = useState('');
  const [submittedQuery, setSubmittedQuery] = useState('');
  const [searchResults, setSearchResults] = useState<DocumentResult[] | null>(null);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  // ── Tag browser state ────────────────────────────────────────────────
  const [allTags, setAllTags] = useState<TagGroup[]>([]);
  const [activeTag, setActiveTag] = useState<string | null>(null);
  const [loadingTags, setLoadingTags] = useState(true);
  const [tagsError, setTagsError] = useState<string | null>(null);

  // ── Mobile sidebar toggle ────────────────────────────────────────────
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  // Load topic clusters once on mount
  useEffect(() => {
    fetchTags()
      .then(data => setAllTags(data.tags))
      .catch(err => setTagsError((err as Error).message))
      .finally(() => setLoadingTags(false));
  }, []);

  // ── Handlers ─────────────────────────────────────────────────────────

  const handleSearch = useCallback(async (q: string) => {
    if (!q.trim()) return;
    // Switching to search mode — clear any active tag filter
    setActiveTag(null);
    setSubmittedQuery(q);
    setSearching(true);
    setSearchError(null);
    setSearchResults(null);

    try {
      const data = await searchDocuments(q);
      setSearchResults(data.results);
    } catch (err) {
      setSearchError((err as Error).message);
    } finally {
      setSearching(false);
    }
  }, []);

  const handleTagClick = useCallback((tag: string) => {
    // Toggle: clicking the active tag deselects it
    setActiveTag(prev => (prev === tag ? null : tag));
    // Switching to tag mode — clear any search state
    setQuery('');
    setSubmittedQuery('');
    setSearchResults(null);
    setSearchError(null);
    setMobileSidebarOpen(false);
  }, []);

  // ── Derived display values ────────────────────────────────────────────

  // Documents to show depend on whether we're in search or tag-browse mode
  const displayedDocs: DocumentResult[] = activeTag
    ? (allTags.find(g => g.tag === activeTag)?.documents ?? [])
    : (searchResults ?? []);

  const isIdle        = !submittedQuery && !activeTag && !searching;
  const hasResults    = displayedDocs.length > 0;
  const showEmpty     = !searching && !searchError && !isIdle && !hasResults;
  const showResults   = !searching && !searchError && hasResults;

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <Header />

      {/* Layout: sidebar + scrollable main — fills the viewport below the header */}
      <div className="flex h-[calc(100dvh-4rem)]">

        {/* ── Mobile overlay backdrop ───────────────────────────────── */}
        {mobileSidebarOpen && (
          <div
            className="fixed inset-0 z-20 bg-brand-950/40 backdrop-blur-sm lg:hidden"
            onClick={() => setMobileSidebarOpen(false)}
            aria-hidden="true"
          />
        )}

        {/* ── Sidebar ──────────────────────────────────────────────── */}
        {/* Hidden off-screen on mobile; slides in on toggle.
            Always visible as an inline column on ≥lg screens. */}
        <aside
          className={`
            fixed inset-y-16 left-0 z-30 w-72 overflow-y-auto
            bg-white border-r border-slate-200
            transition-transform duration-300 ease-in-out
            ${mobileSidebarOpen ? 'translate-x-0 shadow-xl' : '-translate-x-full'}
            lg:relative lg:inset-auto lg:translate-x-0 lg:shadow-none lg:z-auto
          `}
          aria-label="Topics sidebar"
        >
          <TagSidebar
            tags={allTags}
            activeTag={activeTag}
            loading={loadingTags}
            error={tagsError}
            onTagClick={handleTagClick}
          />
        </aside>

        {/* ── Main content ─────────────────────────────────────────── */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">

            {/* Mobile: button to open the topics sidebar */}
            <button
              className="
                lg:hidden mb-5 flex items-center gap-2
                text-sm font-medium text-brand-700
                bg-brand-50 hover:bg-brand-100
                px-4 py-2.5 rounded-xl border border-brand-200
                transition-colors duration-150 cursor-pointer
                focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand-500
              "
              onClick={() => setMobileSidebarOpen(true)}
              aria-label="Open topics panel"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M7 7h.01M7 12h.01M7 17h.01M11 7h6M11 12h6M11 17h6" />
              </svg>
              Browse Topics
            </button>

            {/* Search bar */}
            <SearchBar
              value={query}
              onChange={setQuery}
              onSubmit={handleSearch}
              loading={searching}
            />

            {/* ── Status line ──────────────────────────────────────── */}
            {!isIdle && (
              <div className="mt-5 mb-3 flex items-center justify-between min-h-[1.25rem]">
                <p className="text-sm text-slate-500">
                  {searching && 'Searching…'}

                  {!searching && activeTag && (
                    <>
                      Topic:{' '}
                      <span className="font-semibold text-accent-700">{activeTag}</span>
                      <span className="text-slate-400 ml-1.5">
                        — {displayedDocs.length} document{displayedDocs.length !== 1 ? 's' : ''}
                      </span>
                    </>
                  )}

                  {!searching && submittedQuery && !activeTag && showResults && (
                    <>
                      <span className="font-semibold text-brand-800">{displayedDocs.length}</span>
                      {' '}result{displayedDocs.length !== 1 ? 's' : ''} for &ldquo;{submittedQuery}&rdquo;
                    </>
                  )}
                </p>

                {/* Clear tag filter button */}
                {activeTag && (
                  <button
                    onClick={() => handleTagClick(activeTag)}
                    className="
                      text-xs text-slate-400 hover:text-red-500
                      transition-colors duration-150 cursor-pointer
                      flex items-center gap-1
                    "
                    aria-label={`Clear filter: ${activeTag}`}
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    Clear filter
                  </button>
                )}
              </div>
            )}

            {/* ── Content area ─────────────────────────────────────── */}
            <div className="mt-4">

              {/* Loading skeleton */}
              {searching && <ResultsSkeleton />}

              {/* Search error */}
              {searchError && (
                <div
                  className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-2xl px-5 py-4 text-red-700 text-sm"
                  role="alert"
                >
                  <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <strong className="font-semibold">Search failed</strong>
                    <p className="mt-0.5 text-red-600">{searchError}</p>
                  </div>
                </div>
              )}

              {/* No results */}
              {showEmpty && <EmptyState query={submittedQuery} />}

              {/* Result cards */}
              {showResults && (
                <ul className="space-y-3" aria-label="Search results">
                  {displayedDocs.map((doc, i) => (
                    <li key={doc.id}>
                      <ResultCard
                        doc={doc}
                        // Only pass rank for search results — tag-browse has no meaningful ranking
                        rank={activeTag ? undefined : i + 1}
                      />
                    </li>
                  ))}
                </ul>
              )}

              {/* Idle state — shown on first load before any interaction */}
              {isIdle && (
                <div className="flex flex-col items-center justify-center py-24 text-center select-none animate-fade-in">
                  <div className="w-20 h-20 bg-gradient-to-br from-brand-100 to-brand-50 rounded-3xl flex items-center justify-center mb-5 shadow-inner">
                    <svg className="w-10 h-10 text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h2 className="text-slate-700 font-semibold text-xl mb-2">
                    Explore 75 Documents
                  </h2>
                  <p className="text-slate-400 text-sm max-w-sm leading-relaxed">
                    Type a question or topic above to run a semantic search, or click a topic
                    in the sidebar to browse documents by cluster.
                  </p>
                </div>
              )}

            </div>
          </div>
        </main>

      </div>
    </div>
  );
}
