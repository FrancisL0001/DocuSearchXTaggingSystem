interface Props {
  query: string; // The query that returned no results
}

export default function EmptyState({ query }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-fade-in">
      {/* Icon container */}
      <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-5">
        <svg
          className="w-8 h-8 text-slate-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M21 21l-4.35-4.35m0 0A7 7 0 1110 3a7 7 0 016.65 13.65z"
          />
        </svg>
      </div>

      <h3 className="text-slate-700 font-semibold text-base mb-1.5">No documents found</h3>

      {query && (
        <p className="text-slate-500 text-sm max-w-xs leading-relaxed">
          Nothing matched{' '}
          <span className="font-medium text-slate-700">"{query}"</span>.
          Try rephrasing, or browse by topic in the sidebar.
        </p>
      )}
    </div>
  );
}
