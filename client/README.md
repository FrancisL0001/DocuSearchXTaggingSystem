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
    ├── types/index.ts     Mirrors backend Pydantic schemas
    ├── api/
    │   ├── search.ts      POST /api/v1/search
    │   └── tags.ts        GET /api/v1/tags
    └── components/
        ├── Header.tsx         Top bar with branding
        ├── SearchBar.tsx      Query input with amber submit button
        ├── TagSidebar.tsx     Topic browser — click to filter
        ├── ResultCard.tsx     Document card (title, snippet, score, tag)
        ├── ResultsSkeleton.tsx  Animated loading placeholders
        └── EmptyState.tsx     No-results feedback
```
