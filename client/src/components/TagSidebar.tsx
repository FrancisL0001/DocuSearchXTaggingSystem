import type { TagGroup } from '../types';

interface Props {
  tags: TagGroup[];
  activeTag: string | null;
  loading: boolean;
  error: string | null;
  onTagClick: (tag: string) => void;
}

export default function TagSidebar({ tags, activeTag, loading, error, onTagClick }: Props) {
  return (
    <nav className="p-4 h-full" aria-label="Browse by topic">
      {/* Section heading */}
      <div className="flex items-center gap-2 mb-4 px-1">
        <svg className="w-4 h-4 text-brand-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M7 7h.01M7 12h.01M7 17h.01M11 7h6M11 12h6M11 17h6" />
        </svg>
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">
          Browse Topics
        </span>
      </div>

      {/* Loading skeletons */}
      {loading && (
        <div className="space-y-2" aria-busy="true" aria-label="Loading topics">
          {Array.from({ length: 7 }).map((_, i) => (
            <div key={i} className="h-11 bg-slate-100 rounded-xl animate-pulse" />
          ))}
        </div>
      )}

      {/* Error state */}
      {error && !loading && (
        <p className="text-xs text-red-600 bg-red-50 border border-red-200 rounded-xl p-3 leading-relaxed">
          {error}
        </p>
      )}

      {/* Tag list */}
      {!loading && !error && (
        <ul className="space-y-1">
          {tags.map(group => {
            const isActive = activeTag === group.tag;
            return (
              <li key={group.tag}>
                <button
                  onClick={() => onTagClick(group.tag)}
                  className={`
                    w-full text-left px-3 py-2.5 rounded-xl text-sm
                    transition-all duration-150 cursor-pointer
                    focus-visible:outline focus-visible:outline-2 focus-visible:outline-brand-500
                    ${isActive
                      ? 'bg-accent-50 border border-accent-300 text-accent-800 font-semibold shadow-sm'
                      : 'border border-transparent text-slate-700 hover:bg-brand-50 hover:text-brand-800'
                    }
                  `}
                  aria-pressed={isActive}
                  aria-label={`Filter by topic: ${group.tag} (${group.documents.length} documents)`}
                >
                  <div className="flex items-center justify-between gap-2">
                    {/* Active indicator dot */}
                    <span className="flex items-center gap-2 min-w-0">
                      {isActive && (
                        <span className="w-1.5 h-1.5 bg-accent-500 rounded-full flex-shrink-0" aria-hidden="true" />
                      )}
                      <span className="truncate leading-snug">{group.tag}</span>
                    </span>

                    {/* Document count badge */}
                    <span
                      className={`
                        flex-shrink-0 text-xs font-mono px-1.5 py-0.5 rounded-md tabular-nums
                        ${isActive
                          ? 'bg-accent-200 text-accent-900'
                          : 'bg-slate-100 text-slate-500'
                        }
                      `}
                    >
                      {group.documents.length}
                    </span>
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </nav>
  );
}
