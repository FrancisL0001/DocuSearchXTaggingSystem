import { useRef } from 'react';
import type { KeyboardEvent } from 'react';

interface Props {
  value: string;
  onChange: (v: string) => void;
  onSubmit: (q: string) => void;
  loading: boolean;
}

export default function SearchBar({ value, onChange, onSubmit, loading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') onSubmit(value);
  };

  const handleClear = () => {
    onChange('');
    inputRef.current?.focus();
  };

  return (
    <div
      className="
        flex items-center gap-2 bg-white rounded-2xl
        border border-slate-200 shadow-md
        focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-100
        transition-all duration-200
      "
      role="search"
    >
      {/* Search icon — non-interactive, decorative */}
      <div className="pl-4 text-slate-400 pointer-events-none flex-shrink-0" aria-hidden="true">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M21 21l-4.35-4.35m0 0A7 7 0 1110 3a7 7 0 016.65 13.65z" />
        </svg>
      </div>

      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search across 75 policy and research documents…"
        className="flex-1 py-4 pr-2 bg-transparent outline-none text-base text-slate-800 placeholder-slate-400"
        aria-label="Search documents"
        disabled={loading}
        autoComplete="off"
        spellCheck={false}
      />

      {/* Clear button — shown only when there is text */}
      {value && !loading && (
        <button
          onClick={handleClear}
          className="p-1.5 text-slate-400 hover:text-slate-600 transition-colors duration-150 cursor-pointer flex-shrink-0"
          aria-label="Clear search"
          tabIndex={0}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}

      {/* Submit button */}
      <button
        onClick={() => onSubmit(value)}
        disabled={!value.trim() || loading}
        className="
          m-1.5 px-5 py-2.5 rounded-xl text-sm font-semibold flex-shrink-0
          bg-accent-500 hover:bg-accent-600 text-white
          disabled:bg-slate-100 disabled:text-slate-400 disabled:cursor-not-allowed
          transition-colors duration-150 cursor-pointer
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-accent-500
        "
        aria-label="Run search"
      >
        {loading ? (
          // Spinner while searching
          <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24" aria-label="Loading">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : 'Search'}
      </button>
    </div>
  );
}
