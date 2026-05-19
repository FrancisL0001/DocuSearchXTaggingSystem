# DocuSearch — Frontend

React + TypeScript + Tailwind CSS interface for the DocuSearch API.

## Requirements

- Node.js 18+
- npm 9+

## Setup

```bash
cd client
npm install
```

## Development

```bash
npm run dev
```

Opens at `http://localhost:5173`. All `/api/*` requests are proxied to `http://localhost:8000`, so the FastAPI backend must be running.

## Run tests

```bash
npm test
```

CI uses `npm ci` for a clean, lockfile-based install before running tests.

## Production build

```bash
npm run build    # outputs to dist/
npm run preview  # preview the built bundle locally
```

## Project structure

```
client/
├── index.html
├── vite.config.ts        API proxy config
├── tailwind.config.js    Design tokens (brand blues + amber accent)
└── src/
    ├── App.tsx            Root component — layout and state
    ├── App.test.tsx       App-level search/tag flow tests
    ├── types/index.ts     Mirrors backend Pydantic schemas
    ├── test/setup.ts      Vitest + Testing Library setup
    ├── api/
    │   ├── search.ts      POST /api/v1/search
    │   ├── search.test.ts
    │   ├── tags.test.ts
    │   └── tags.ts        GET /api/v1/tags
    └── components/
        ├── Header.tsx         Top bar with branding
        ├── SearchBar.tsx      Query input with amber submit button
        ├── TagSidebar.tsx     Topic browser — click to filter
        ├── TagSidebar.test.tsx
        ├── ResultCard.tsx     Document card (title, snippet, score, tag)
        ├── ResultCard.test.tsx
        ├── ResultsSkeleton.tsx  Animated loading placeholders
        └── EmptyState.tsx     No-results feedback
```
