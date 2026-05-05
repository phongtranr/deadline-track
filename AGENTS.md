<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

## Cursor Cloud specific instructions

### Project overview

Deadline Track is a Next.js 16 + TypeScript + Tailwind CSS application for tracking deadlines. Uses pnpm as the package manager.

### Commands

| Task | Command |
|------|---------|
| Dev server | `pnpm dev` (runs on port 3000) |
| Lint | `pnpm lint` |
| Test | `pnpm test` (Vitest) |
| Test watch | `pnpm test:watch` |
| Build | `pnpm build` |

### Notes

- Tests use Vitest with jsdom + @testing-library/react. Test setup includes explicit `cleanup()` in `src/test/setup.ts` (required for jsdom environment).
- The app uses the Next.js App Router (`src/app/`).
- Path alias `@/*` maps to `./src/*`.
