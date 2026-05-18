// Animated placeholder cards shown while a search request is in flight

export default function ResultsSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading results">
      {Array.from({ length: 5 }).map((_, i) => (
        <div
          key={i}
          className="bg-white rounded-2xl border border-slate-200 p-5 animate-pulse"
          aria-hidden="true"
        >
          <div className="flex items-start gap-3">
            {/* Rank bubble placeholder */}
            <div className="w-6 h-6 bg-brand-100 rounded-full flex-shrink-0 mt-0.5" />

            <div className="flex-1 space-y-2.5">
              {/* Title line */}
              <div className="h-4 bg-slate-200 rounded-lg w-3/4" />
              {/* Snippet lines */}
              <div className="h-3 bg-slate-100 rounded-lg w-full" />
              <div className="h-3 bg-slate-100 rounded-lg w-5/6" />
              {/* Footer chips */}
              <div className="flex gap-2 pt-1">
                <div className="h-5 bg-brand-100 rounded-full w-28" />
                <div className="h-5 bg-accent-100 rounded-full w-24 ml-auto" />
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
