import type { DocumentResult } from '../types';

interface Props {
  doc: DocumentResult;
  rank?: number; // present for search results, absent for tag-browse results
}

// Convert cosine similarity (0–1) to a "XX.X% match" string
function formatScore(score: number): string {
  return `${(score * 100).toFixed(1)}% match`;
}

export default function ResultCard({ doc, rank }: Props) {
  const showScore = rank !== undefined && doc.score > 0;

  return (
    <article
      className="
        group animate-fade-in bg-white rounded-2xl
        border border-slate-200 hover:border-brand-200 hover:shadow-md
        transition-all duration-200 p-5 cursor-default
      "
    >
      <div className="flex items-start gap-3">
        {/* Rank bubble — shown for search results only */}
        {rank !== undefined && (
          <span
            className="flex-shrink-0 mt-0.5 w-6 h-6 flex items-center justify-center
              bg-brand-100 text-brand-700 font-mono text-xs font-bold rounded-full"
            aria-label={`Result ${rank}`}
          >
            {rank}
          </span>
        )}

        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className="
              font-semibold text-brand-900 text-base leading-snug
              line-clamp-2 group-hover:text-brand-700 transition-colors duration-150
            "
          >
            {doc.title}
          </h3>

          {/* Snippet — truncated to 3 lines */}
          <p className="mt-2 text-sm text-slate-600 leading-relaxed line-clamp-3">
            {doc.snippet}
          </p>

          {/* Footer row: topic tag chip + similarity score */}
          <div className="mt-3 flex items-center flex-wrap gap-2">
            {doc.tags.map(tag => (
              <span
                key={tag}
                className="
                  inline-flex items-center text-xs
                  bg-brand-50 text-brand-700 border border-brand-200
                  rounded-full px-2.5 py-0.5 font-medium
                "
              >
                {tag}
              </span>
            ))}

            {showScore && (
              // Similarity score badge — amber to stand out from blue topic tags
              <span
                className="
                  ml-auto inline-flex items-center gap-1.5 text-xs font-mono font-semibold
                  bg-accent-50 text-accent-700 border border-accent-200
                  rounded-full px-2.5 py-0.5
                "
                aria-label={`Similarity: ${formatScore(doc.score)}`}
              >
                {/* Star icon */}
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {formatScore(doc.score)}
              </span>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}
