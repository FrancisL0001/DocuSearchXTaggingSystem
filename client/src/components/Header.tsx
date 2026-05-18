// Sticky top bar — branding, corpus stats, and a subtle status indicator

export default function Header() {
  return (
    <header className="sticky top-0 z-10 h-16 bg-brand-950 flex items-center px-5 shadow-lg">
      {/* Logo mark: amber square with search icon */}
      <div className="flex items-center gap-3 flex-shrink-0">
        <div className="w-9 h-9 bg-accent-500 rounded-xl flex items-center justify-center shadow-md flex-shrink-0">
          <svg
            className="w-5 h-5 text-brand-950"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2.5}
              d="M21 21l-4.35-4.35m0 0A7 7 0 1110 3a7 7 0 016.65 13.65z"
            />
          </svg>
        </div>

        <div>
          <h1 className="font-mono font-bold text-white text-lg leading-none tracking-tight">
            DocuSearch
          </h1>
          <p className="text-blue-400 text-xs mt-0.5 font-light">
            Policy &amp; Research Intelligence
          </p>
        </div>
      </div>

      {/* Right side: corpus size + live indicator */}
      <div className="ml-auto hidden sm:flex items-center gap-4">
        <span className="text-blue-300 text-xs font-mono">
          75 documents · 8 topics
        </span>
        <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium">
          <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" aria-hidden="true" />
          Semantic index live
        </div>
      </div>
    </header>
  );
}
