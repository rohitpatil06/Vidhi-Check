# VidhiCheck

VidhiCheck is an AI-assisted packaged commodity compliance checker for Legal Metrology officers.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm --filter @workspace/vidhicheck run dev` — run the VidhiCheck web app
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5 with demo analysis, verification, dashboard, history, and report routes
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `artifacts/vidhicheck/src/` — frontend routes, shell, demo data, and report download flow
- `artifacts/api-server/src/routes/inspections.ts` — inspection API and resilient demo analysis data
- `lib/api-spec/openapi.yaml` — source of truth for generated API hooks and schemas
- `artifacts/vidhicheck/src/index.css` — VidhiCheck visual tokens and shared UI styling

## Architecture decisions

- The prototype uses a demo-friendly analysis mode with seeded product outcomes, so the main presentation flow works without OCR dependencies.
- The browser keeps a local inspection copy as a fallback when the API is unavailable; server routes remain the primary source when reachable.
- Officer verification stays explicit and separate from AI analysis; the final status is only set by the officer action.
- Reports are generated through the API contract and downloaded as a lightweight PDF from the browser for a dependency-light demo.

## Product

- Demo officer login
- Dashboard with compliance totals and recent inspections
- Image upload and sample-product analysis flow
- Extracted declarations with confidence, rule checks, violations, and score
- Officer verification with remarks
- Searchable inspection history
- Report preview and PDF download

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

_Populate as you build — sharp edges, "always run X before Y" rules._

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
